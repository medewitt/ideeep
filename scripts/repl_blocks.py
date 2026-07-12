# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy", "scipy", "sympy", "pandas", "polars", "statsmodels",
#     "networkx", "matplotlib", "scikit-learn", "numpyro", "jax", "torch",
#     "mapie", "xgboost", "shap", "umap-learn", "hdbscan", "torchdiffeq",
#     "flax", "optax", "torch-geometric",
#     "numba>=0.60",
# ]
# ///
"""Interactively run a content page's code blocks in the injector's environment
— a dev-time authoring convenience, like a "send block to REPL" editor command.

This is the *opposite end* of `inject_python_output.py`: that script runs blocks
in batch and commits their stdout for the published site; this one hands the
blocks to a live REPL so you can poke at a page's code while writing it. It is a
local tool only — it lives in `scripts/`, is never copied into the built site
(`dist/`), and does nothing unless *you* run it against your own clone. Readers
of the published (static HTML) site have no way to invoke it.

The dependency header above mirrors the injector's, so `uv run --script` gives
the same scientific-Python environment a ` ```python ` block would execute in.

Usage (via `just repl`, or directly through uv):
  just repl content/math/foo.md                 # run every python block, then a REPL
  just repl content/math/foo.md --list          # number the runnable blocks and exit
  just repl content/math/foo.md --block 3       # run only block 3, then a REPL
  just repl content/math/foo.md --through 3      # run blocks 1..3, then a REPL
  just repl content/math/foo.md --lang r         # same, for the page's R blocks
  just repl content/math/foo.md --no-repl        # run blocks and print output, no prompt

By default it runs **every** block of the chosen language in document order (that
is the authoring intent — try the code you are writing), which differs from the
injector's opt-in rule for R/Julia (`# run`) and opt-out for Python (`# no-run`).
Pass `--respect-directives` to restrict to exactly the blocks the injector would
execute, so you can preview precisely what will be committed.

Python blocks run in-process and open a `code.interact` prompt with the page's
namespace preloaded. R/Julia blocks are written to a temp file and handed to an
interactive `R` / `julia` session (state preloaded), when that interpreter is on
PATH; otherwise the tool says so and exits.
"""
from __future__ import annotations
import argparse
import os
import subprocess
import sys
import tempfile
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inject_python_output as inj


def collect_blocks(text: str, lang: str, respect_directives: bool) -> list[str]:
    """The page's blocks for `lang`, in document order. By default every block;
    with `respect_directives`, only those the injector would run."""
    lines = inj.strip_injected(text.split("\n"))
    blocks = [code for l, code in inj.iter_blocks(lines) if l == lang]
    if respect_directives:
        blocks = [b for b in blocks if inj.wants_run(lang, b)]
    return blocks


def preview(code: str) -> str:
    for line in code.split("\n"):
        s = line.strip()
        if s and s not in (inj.RUN_DIRECTIVE, inj.NO_RUN_DIRECTIVE):
            return s[:70]
    return "(empty)"


def select(blocks: list[str], only: int | None, through: int | None) -> list[tuple[int, str]]:
    """1-indexed selection of (number, code) pairs to run."""
    numbered = list(enumerate(blocks, start=1))
    if only is not None:
        return [p for p in numbered if p[0] == only]
    if through is not None:
        return [p for p in numbered if p[0] <= through]
    return numbered


def banner(n: int, total: int, code: str) -> str:
    return f"\n# ── block {n}/{total}  {preview(code)}"


def run_python(selected: list[tuple[int, str]], total: int, open_repl: bool) -> int:
    ns: dict = {}
    for n, code in selected:
        print(banner(n, total, code), file=sys.stderr)
        try:
            exec(compile(code, f"<block {n}>", "exec"), ns)
        except BaseException:                            # keep going; state accumulates
            traceback.print_exc()
    if open_repl:
        import code as codemod
        names = sorted(k for k in ns if not k.startswith("__"))
        codemod.interact(
            banner=f"[repl] {total} block(s) loaded. In scope: "
                   f"{', '.join(names) or '(nothing)'}\nPython "
                   f"{sys.version.split()[0]} — Ctrl-D to exit.",
            local=ns, exitmsg="")
    return 0


def run_external(lang: str, selected: list[tuple[int, str]], total: int,
                 open_repl: bool) -> int:
    spec = inj.LANGS[lang]
    interp = spec["interpreter"]
    if not inj.toolchain_available(lang):
        print(f"repl: {interp} is not on PATH — install it to run {lang} blocks.",
              file=sys.stderr)
        return 1
    # Assemble the preloaded script: a comment banner then each block, in order.
    parts = []
    for n, code in selected:
        parts.append(f"# ── block {n}/{total}")
        parts.append(code)
    script = "\n\n".join(parts) + "\n"
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "preload" + spec["ext"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(script)
        if not open_repl:
            runner = "Rscript" if lang == "r" else interp
            cmd = [runner, path]
            return subprocess.run(cmd).returncode
        if lang == "r":
            # R runs R_PROFILE_USER at startup, then drops to the prompt with
            # state loaded.
            env = dict(os.environ, R_PROFILE_USER=path)
            print(f"[repl] {total} R block(s) preloaded — Ctrl-D to exit.",
                  file=sys.stderr)
            return subprocess.run([interp, "--no-save", "--quiet"], env=env).returncode
        # julia -i runs the file then stays interactive with Main populated.
        print(f"[repl] {total} Julia block(s) preloaded — Ctrl-D to exit.",
              file=sys.stderr)
        return subprocess.run([interp, "-i", path]).returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("page")
    ap.add_argument("--lang", choices=list(inj.LANGS), default="python")
    ap.add_argument("--list", action="store_true", help="number the blocks and exit")
    ap.add_argument("--block", type=int, metavar="N", help="run only block N")
    ap.add_argument("--through", type=int, metavar="N", help="run blocks 1..N")
    ap.add_argument("--no-repl", action="store_true",
                    help="run the blocks and print output without opening a prompt")
    ap.add_argument("--respect-directives", action="store_true",
                    help="only run blocks the injector would (# run / # no-run)")
    args = ap.parse_args()

    if args.block is not None and args.through is not None:
        ap.error("--block and --through are mutually exclusive")

    try:
        with open(args.page, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"repl: cannot read {args.page}: {e}", file=sys.stderr)
        return 2

    blocks = collect_blocks(text, args.lang, args.respect_directives)
    if not blocks:
        which = "runnable " if args.respect_directives else ""
        print(f"repl: no {which}{args.lang} blocks in {args.page}", file=sys.stderr)
        return 1

    if args.list:
        for n, code in enumerate(blocks, start=1):
            print(f"{n:3}. {preview(code)}")
        return 0

    for bound in (args.block, args.through):
        if bound is not None and not (1 <= bound <= len(blocks)):
            ap.error(f"block number {bound} out of range (page has {len(blocks)} "
                     f"{args.lang} block(s))")

    selected = select(blocks, args.block, args.through)
    open_repl = not args.no_repl
    if args.lang == "python":
        return run_python(selected, len(blocks), open_repl)
    return run_external(args.lang, selected, len(blocks), open_repl)


if __name__ == "__main__":
    sys.exit(main())
