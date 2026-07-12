# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy", "scipy", "sympy", "pandas", "polars", "statsmodels",
#     "networkx", "matplotlib", "scikit-learn", "numpyro", "jax", "torch",
#     "mapie", "xgboost", "shap", "umap-learn", "hdbscan", "torchdiffeq",
#     "flax", "optax", "torch-geometric",
#     # numba floor: shap/umap pull numba->llvmlite; without this uv can
#     # backtrack to an ancient llvmlite that fails to build on Python 3.12.
#     "numba>=0.60",
# ]
# ///
"""Execute the embedded code blocks in the content pages and inject their
captured stdout beneath each block, so the outputs shown on the site are real
and reproducible.

How it works
------------
* ```python blocks run by default; add `# no-run` to skip one.
* ```r and ```julia blocks are illustrative by default; add `# run` to opt one
  in. They only execute when the interpreter (`Rscript` / `julia`) is on PATH —
  otherwise they are skipped with a warning and any committed output is left
  untouched.
* For each Markdown file, the runnable blocks of a language run in order with
  shared state (Python: one namespace; R/Julia: one interpreter process per
  page, so a block may use names defined earlier on the page), exactly as a
  reader working top-to-bottom would. R auto-prints visible top-level values
  (REPL-like, via `print.eval`); Python and Julia print only what the code
  explicitly prints.
* Whatever a block prints to stdout is injected immediately after it, wrapped
  in HTML-comment markers so the injection is idempotent: re-running strips the
  previous output and regenerates it.
* Output is injected ONLY when a block actually prints something and runs
  without raising — so plot-only blocks, pseudo-code, and deliberate "bad"
  examples that error are left untouched. (An erroring R/Julia block may still
  leave partial state behind for later blocks, since the process continues.)

Because the rendered SVGs / generated outputs are committed, the site build
(cargo run) never needs Python/R/Julia; this is a dev-time tool, like
`just figures`.

Usage:
  inject_python_output.py --write PATH ...   # run blocks and inject outputs
  inject_python_output.py --check PATH ...    # exit 1 if any file would change
Paths may be files or directories (searched for *.md).

Content-hash cache
------------------
Executing the blocks is the only expensive part (some math pages run MCMC /
jax sampling that takes minutes). A page's injected output is a pure function
of its runnable block sources (every ```python block, plus each ```r/```julia
block carrying `# run`), so we fingerprint those sources and record the
fingerprint in `scripts/.python-output-cache.json` after a successful
`--write`. On a later run, a page whose fingerprint still matches the cache
has unchanged blocks, so its committed output is already current and we skip
execution entirely. Prose-only edits change nothing here (the fingerprint
ignores prose, illustrative R/Julia blocks, and the injected output), so they
do not trigger re-sampling. The cache is committed alongside the injected
outputs, so CI's `--check` only executes pages whose code actually changed.
A page whose runnable R/Julia blocks could not run (missing toolchain, or a
failed interpreter process) is never recorded as fresh, so a machine that does
have the toolchain will pick it up.
"""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

os.environ.setdefault("MPLBACKEND", "Agg")          # headless matplotlib

START = "<!-- python-output:auto -->"
END = "<!-- /python-output:auto -->"
R_START = "<!-- r-output:auto -->"
R_END = "<!-- /r-output:auto -->"
JULIA_START = "<!-- julia-output:auto -->"
JULIA_END = "<!-- /julia-output:auto -->"
ALL_MARKERS = {START: END, R_START: R_END, JULIA_START: JULIA_END}
MAX_LINES = 15                                        # cap long output
FENCE = "```"

NO_RUN_DIRECTIVE = "# no-run"                         # opt-out (python)
RUN_DIRECTIVE = "# run"                               # opt-in (r / julia)

# Per-language execution config, keyed by the fence info-string. `opt_in`
# gives the directive polarity: python runs unless `# no-run` is present;
# r/julia run only when `# run` is present. Only a language's own directive is
# consulted (`# run` in python is a no-op; `# no-run` in r/julia is ignored).
LANGS = {
    "python": {"opt_in": False, "markers": (START, END), "interpreter": None},
    "r": {"opt_in": True, "markers": (R_START, R_END),
          "interpreter": "Rscript", "ext": ".R"},
    "julia": {"opt_in": True, "markers": (JULIA_START, JULIA_END),
              "interpreter": "julia", "ext": ".jl"},
}

# Fixed sentinels the r/julia driver prints to stdout so per-block output can
# be attributed (and erroring blocks detected) from a single shared process.
BLOCK_SENTINEL = "@@IDEEEP-BLOCK-b7f3c1@@"
ERROR_SENTINEL = "@@IDEEEP-ERROR-b7f3c1@@"
SUBPROCESS_TIMEOUT = 120                              # seconds, per language

CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          ".python-output-cache.json")
CACHE_VERSION = 1
# Bump this tag whenever the injection *format* changes (marker text, line cap,
# skip rules) so stale fingerprints are invalidated and pages re-run.
FORMAT_TAG = f"v1;maxlines={MAX_LINES};markers={START}|{END}"


class ProcessedPage(str):
    """The processed page text. `incomplete` is True when some runnable block
    could not be executed this run (missing toolchain or a failed interpreter
    process) — such a page must not be recorded as fresh in the cache."""
    incomplete = False


def fence_lang(line: str) -> str | None:
    """The LANGS key when `line` opens a runnable-language fence, else None."""
    s = line.strip()
    if s.startswith(FENCE) and s[len(FENCE):] in LANGS:
        return s[len(FENCE):]
    return None


def has_directive(code: str, directive: str) -> bool:
    """True when `directive` appears as its own comment line (ignoring
    indentation). Matching the whole line, not a substring, keeps an
    incidental comment like `# runs n times` from being read as `# run`."""
    return any(line.strip() == directive for line in code.split("\n"))


def wants_run(lang: str, code: str) -> bool:
    if LANGS[lang]["opt_in"]:
        return has_directive(code, RUN_DIRECTIVE)
    return not has_directive(code, NO_RUN_DIRECTIVE)


def toolchain_available(lang: str) -> bool:
    interp = LANGS[lang]["interpreter"]
    return interp is None or shutil.which(interp) is not None


_warned_missing: set[str] = set()


def warn_missing(lang: str) -> None:
    interp = LANGS[lang]["interpreter"]
    if interp in _warned_missing:
        return
    _warned_missing.add(interp)
    print(f"inject_python_output: {interp} not found on PATH; skipping "
          f"runnable {lang} block(s) (committed output left unchanged)",
          file=sys.stderr)


def strip_injected(lines: list[str], markers: dict[str, str] | None = None) -> list[str]:
    """Remove injected-output regions whose START marker is in `markers`
    (all marker pairs by default). Regions of an *inactive* language are kept,
    so output that cannot be regenerated this run is never stripped-then-lost."""
    markers = ALL_MARKERS if markers is None else markers
    out, i = [], 0
    while i < len(lines):
        s = lines[i].strip()
        if s in markers:
            end = markers[s]
            # drop a preceding blank line we added, if present
            if out and out[-1].strip() == "":
                out.pop()
            while i < len(lines) and lines[i].strip() != end:
                i += 1
            i += 1                                     # skip the END marker
            continue
        out.append(lines[i])
        i += 1
    return out


def iter_blocks(lines: list[str]):
    """Yield (lang, code) for every LANGS fenced block, in order."""
    i, n = 0, len(lines)
    while i < n:
        lang = fence_lang(lines[i])
        if lang is not None:
            i += 1
            code_lines = []
            while i < n and lines[i].strip() != FENCE:
                code_lines.append(lines[i])
                i += 1
            if i < n:                                  # skip closing fence
                i += 1
            yield lang, "\n".join(code_lines)
            continue
        i += 1


def run_block(code: str, ns: dict) -> str | None:
    """Return captured stdout, or None if the block raised."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            exec(compile(code, "<page-block>", "exec"), ns)
    except BaseException:
        return None
    return buf.getvalue()


def run_language_blocks(lang: str, codes: list[str]) -> list[str | None] | None:
    """Run all runnable blocks of one language in a single interpreter process
    (so they share state), and return each block's captured stdout, with None
    for a block that errored. Returns None wholesale if the interpreter process
    itself fails or times out — the caller then leaves the page untouched."""
    spec = LANGS[lang]
    with tempfile.TemporaryDirectory() as tmp:
        names = []
        for idx, code in enumerate(codes):
            name = f"blk{idx:02d}{spec['ext']}"
            with open(os.path.join(tmp, name), "w", encoding="utf-8") as f:
                f.write(code + "\n")
            names.append(name)
        driver_lines = []
        if lang == "r":
            for name in names:
                driver_lines.append(f'cat("{BLOCK_SENTINEL}\\n")')
                driver_lines.append(
                    f'tryCatch(source("{name}", local = globalenv(), '
                    f'print.eval = TRUE), '
                    f'error = function(e) cat("{ERROR_SENTINEL}\\n"))')
            driver = "driver.R"
        else:
            for name in names:
                driver_lines.append(f'println("{BLOCK_SENTINEL}")')
                driver_lines.append("try")
                driver_lines.append(f'    include("{name}")')
                driver_lines.append("catch")
                driver_lines.append(f'    println("{ERROR_SENTINEL}")')
                driver_lines.append("end")
            driver = "driver.jl"
        with open(os.path.join(tmp, driver), "w", encoding="utf-8") as f:
            f.write("\n".join(driver_lines) + "\n")
        try:
            proc = subprocess.run(
                [spec["interpreter"], driver], capture_output=True, text=True,
                timeout=SUBPROCESS_TIMEOUT, cwd=tmp)
        except (subprocess.TimeoutExpired, OSError):
            return None
    if proc.returncode != 0:
        return None
    segments = proc.stdout.split(BLOCK_SENTINEL)
    # segments[0] is any pre-first-block prelude; one segment per block after.
    if len(segments) - 1 != len(codes):
        return None
    outputs: list[str | None] = []
    for seg in segments[1:]:
        # drop the newline printed right after the sentinel itself
        seg = seg.removeprefix("\n")
        outputs.append(None if ERROR_SENTINEL in seg else seg)
    return outputs


def emit_output(start: str, end: str, captured: str | None) -> list[str]:
    """The lines to inject after a block, or [] when there is nothing to show
    (block errored, or printed nothing)."""
    if not captured or not captured.strip():
        return []
    shown = captured.rstrip("\n").split("\n")
    truncated = len(shown) > MAX_LINES
    shown = shown[:MAX_LINES]
    if truncated:
        shown.append("... (output truncated)")
    return ["", start, FENCE + "text", *shown, FENCE, end]


def process(text: str) -> ProcessedPage:
    all_lines = text.split("\n")

    # Collect each opt-in language's runnable block sources (from a fully
    # stripped view, so previously injected output is invisible to the code),
    # and run them up front — one shared process per language per page.
    runnable: dict[str, list[str]] = {}
    for lang, code in iter_blocks(strip_injected(all_lines)):
        if LANGS[lang]["opt_in"] and wants_run(lang, code):
            runnable.setdefault(lang, []).append(code)

    incomplete = False
    outputs: dict[str, list[str | None]] = {}
    active = dict(ALL_MARKERS)
    for lang, codes in runnable.items():
        if not toolchain_available(lang):
            warn_missing(lang)
            result = None
        else:
            result = run_language_blocks(lang, codes)
            if result is None:
                print(f"inject_python_output: {LANGS[lang]['interpreter']} "
                      f"failed or timed out; leaving {lang} output unchanged",
                      file=sys.stderr)
        if result is None:
            # Can't regenerate this language's output: keep its committed
            # regions (don't strip its markers) and don't cache the page.
            incomplete = True
            del active[LANGS[lang]["markers"][0]]
        else:
            outputs[lang] = result

    lines = strip_injected(all_lines, active)
    ns: dict = {}
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        lang = fence_lang(line)
        if lang is not None:
            block = [line]
            i += 1
            code_lines = []
            while i < n and lines[i].strip() != FENCE:
                code_lines.append(lines[i])
                block.append(lines[i])
                i += 1
            if i < n:                                  # closing fence
                block.append(lines[i]); i += 1
            out.extend(block)
            code = "\n".join(code_lines)
            if not wants_run(lang, code):
                continue
            if lang == "python":
                captured = run_block(code, ns)
            elif lang in outputs:
                captured = outputs[lang].pop(0)
            else:
                continue                               # toolchain unavailable
            start, end = LANGS[lang]["markers"]
            out.extend(emit_output(start, end, captured))
            continue
        out.append(line)
        i += 1
    page = ProcessedPage("\n".join(out))
    page.incomplete = incomplete
    return page


def extract_block_sources(text: str) -> list[str]:
    """Return the raw code of each ```python block, in order, without running
    anything. Injected output is stripped first so the result depends only on
    the author's code (a fingerprint over this is stable across re-injection)."""
    lines = strip_injected(text.split("\n"))
    return [code for lang, code in iter_blocks(lines) if lang == "python"]


def extract_fingerprint_units(text: str) -> list[tuple[str, str]]:
    """The (lang, code) units the fingerprint covers, in document order: every
    ```python block, plus each ```r/```julia block that opts in with `# run`.
    Illustrative r/julia blocks are excluded, so editing them (or adding new
    ones) never invalidates a page's cache entry."""
    lines = strip_injected(text.split("\n"))
    return [(lang, code) for lang, code in iter_blocks(lines)
            if lang == "python" or wants_run(lang, code)]


def page_fingerprint(text: str) -> str:
    """Content hash of a page's runnable blocks (plus the format tag). Two
    files with the same fingerprint produce byte-identical injected output, so
    a match against the cache means execution can be skipped. Python-only
    pages hash exactly as before r/julia support, keeping the committed cache
    warm. The hash is toolchain-independent: a machine without R/Julia computes
    the same value (freshness is handled separately via the incomplete flag)."""
    h = hashlib.sha256()
    h.update(FORMAT_TAG.encode("utf-8"))
    for lang, block in extract_fingerprint_units(text):
        if lang != "python":
            h.update(b"\x01")
            h.update(lang.encode("utf-8"))
        h.update(b"\x00")
        h.update(block.encode("utf-8"))
    return h.hexdigest()


def load_cache() -> dict:
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and data.get("version") == CACHE_VERSION:
            files = data.get("files")
            if isinstance(files, dict):
                return files
    except (OSError, ValueError):
        pass
    return {}


def save_cache(files: dict) -> None:
    tmp = CACHE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"version": CACHE_VERSION, "files": files},
                  f, indent=1, sort_keys=True)
        f.write("\n")
    os.replace(tmp, CACHE_PATH)


def iter_md(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in sorted(files):
                    if f.endswith(".md"):
                        yield os.path.join(root, f)
        else:
            yield p


def count_injected(text: str) -> int:
    return sum(text.count(start) for start in ALL_MARKERS)


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args()
    if not (args.check or args.write):
        args.check = True

    _warned_missing.clear()                          # one warning per language per run

    cache = load_cache()
    # Start from the existing cache so writing a subset of pages (e.g. a single
    # file) preserves fingerprints for pages we did not touch.
    new_cache = dict(cache)

    changed, injected, skipped = [], 0, 0
    for path in iter_md(args.paths):
        with open(path, encoding="utf-8") as f:
            original = f.read()
        key = os.path.normpath(path)
        fp = page_fingerprint(original)

        if cache.get(key) == fp:
            # Blocks are unchanged since the last successful injection, so the
            # committed output is already current — skip executing the page.
            injected += count_injected(original)
            skipped += 1
            continue

        trailing = "\n" if original.endswith("\n") else ""
        page = process(original.rstrip("\n"))
        new = page + trailing
        injected += count_injected(new)
        if new != original:
            changed.append(path)
            if args.write:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
        if args.write:
            if page.incomplete:
                # Some runnable block could not execute here (e.g. Rscript not
                # installed): leave the page uncached so a toolchain-equipped
                # machine re-runs it instead of trusting this partial pass.
                new_cache.pop(key, None)
            else:
                # After writing, the file's output matches its blocks; record
                # the fingerprint (unaffected by injection) so later runs can
                # skip it.
                new_cache[key] = fp

    if args.write:
        save_cache(new_cache)
        print(f"python-output: updated {len(changed)} file(s); "
              f"{injected} output block(s) total; {skipped} page(s) cached")
        for p in changed:
            print("  ", p)
        return 0
    if changed:
        print(f"python-output: {len(changed)} file(s) out of date (run `just python-output`)")
        for p in changed:
            print("  ", p)
        return 1
    print(f"python-output: all outputs up to date "
          f"({injected} block(s); {skipped} page(s) cached)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
