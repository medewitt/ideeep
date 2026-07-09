# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy", "scipy", "sympy", "pandas", "polars", "statsmodels",
#     "networkx", "matplotlib", "scikit-learn", "numpyro", "jax",
# ]
# ///
"""Execute the embedded ```python code blocks in the content pages and inject
their captured stdout beneath each block, so the outputs shown on the site are
real and reproducible.

How it works
------------
* For each Markdown file, the ```python fenced blocks are run in order in a
  single shared namespace (so a block may use names defined earlier on the
  page), exactly as a reader working top-to-bottom would.
* Whatever a block prints to stdout is injected immediately after it, wrapped
  in HTML-comment markers so the injection is idempotent: re-running strips the
  previous output and regenerates it.
* Output is injected ONLY when a block actually prints something and runs
  without raising — so plot-only blocks, pseudo-code, and deliberate "bad"
  examples that error are left untouched.

Because the rendered SVGs / generated outputs are committed, the site build
(cargo run) never needs Python; this is a dev-time tool, like `just figures`.

Usage:
  inject_python_output.py --write PATH ...   # run blocks and inject outputs
  inject_python_output.py --check PATH ...    # exit 1 if any file would change
Paths may be files or directories (searched for *.md).

Content-hash cache
------------------
Executing the blocks is the only expensive part (some math pages run MCMC /
jax sampling that takes minutes). A page's injected output is a pure function
of its ordered ```python block sources, so we fingerprint those sources and
record the fingerprint in `scripts/.python-output-cache.json` after a
successful `--write`. On a later run, a page whose fingerprint still matches
the cache has unchanged blocks, so its committed output is already current and
we skip execution entirely. Prose-only edits change nothing here (the
fingerprint ignores prose and the injected output), so they no longer trigger
re-sampling. The cache is committed alongside the injected outputs, so CI's
`--check` only executes pages whose code actually changed.
"""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import io
import json
import os
import sys

os.environ.setdefault("MPLBACKEND", "Agg")          # headless matplotlib

START = "<!-- python-output:auto -->"
END = "<!-- /python-output:auto -->"
MAX_LINES = 15                                        # cap long output
FENCE = "```"

CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          ".python-output-cache.json")
CACHE_VERSION = 1
# Bump this tag whenever the injection *format* changes (marker text, line cap,
# skip rules) so stale fingerprints are invalidated and pages re-run.
FORMAT_TAG = f"v1;maxlines={MAX_LINES};markers={START}|{END}"


def strip_injected(lines: list[str]) -> list[str]:
    out, i = [], 0
    while i < len(lines):
        if lines[i].strip() == START:
            # drop a preceding blank line we added, if present
            if out and out[-1].strip() == "":
                out.pop()
            while i < len(lines) and lines[i].strip() != END:
                i += 1
            i += 1                                     # skip the END marker
            continue
        out.append(lines[i])
        i += 1
    return out


def run_block(code: str, ns: dict) -> str | None:
    """Return captured stdout, or None if the block raised."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            exec(compile(code, "<page-block>", "exec"), ns)
    except BaseException:
        return None
    return buf.getvalue()


def process(text: str) -> str:
    lines = strip_injected(text.split("\n"))
    ns: dict = {}
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if line.strip() == FENCE + "python":
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
            if "# no-run" in code:
                continue
            captured = run_block(code, ns)
            if captured and captured.strip():
                shown = captured.rstrip("\n").split("\n")
                truncated = len(shown) > MAX_LINES
                shown = shown[:MAX_LINES]
                if truncated:
                    shown.append("... (output truncated)")
                out += ["", START, FENCE + "text", *shown, FENCE, END]
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def extract_block_sources(text: str) -> list[str]:
    """Return the raw code of each ```python block, in order, without running
    anything. Injected output is stripped first so the result depends only on
    the author's code (a fingerprint over this is stable across re-injection)."""
    lines = strip_injected(text.split("\n"))
    blocks: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        if lines[i].strip() == FENCE + "python":
            i += 1
            code_lines = []
            while i < n and lines[i].strip() != FENCE:
                code_lines.append(lines[i])
                i += 1
            if i < n:                                  # skip closing fence
                i += 1
            blocks.append("\n".join(code_lines))
            continue
        i += 1
    return blocks


def page_fingerprint(text: str) -> str:
    """Content hash of a page's ordered python blocks (plus the format tag).
    Two files with the same fingerprint produce byte-identical injected output,
    so a match against the cache means execution can be skipped."""
    h = hashlib.sha256()
    h.update(FORMAT_TAG.encode("utf-8"))
    for block in extract_block_sources(text):
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


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args()
    if not (args.check or args.write):
        args.check = True

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
            injected += original.count(START)
            skipped += 1
            continue

        trailing = "\n" if original.endswith("\n") else ""
        new = process(original.rstrip("\n")) + trailing
        injected += new.count(START)
        if new != original:
            changed.append(path)
            if args.write:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
        if args.write:
            # After writing, the file's output matches its blocks; record the
            # fingerprint (unaffected by injection) so later runs can skip it.
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
