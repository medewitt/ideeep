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
"""
from __future__ import annotations
import argparse
import contextlib
import io
import os
import sys

os.environ.setdefault("MPLBACKEND", "Agg")          # headless matplotlib

START = "<!-- python-output:auto -->"
END = "<!-- /python-output:auto -->"
MAX_LINES = 15                                        # cap long output
FENCE = "```"


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

    changed, injected = [], 0
    for path in iter_md(args.paths):
        original = open(path, encoding="utf-8").read()
        trailing = "\n" if original.endswith("\n") else ""
        new = process(original.rstrip("\n")) + trailing
        injected += new.count(START)
        if new != original:
            changed.append(path)
            if args.write:
                open(path, "w", encoding="utf-8").write(new)

    if args.write:
        print(f"python-output: updated {len(changed)} file(s); {injected} output block(s) total")
        for p in changed:
            print("  ", p)
        return 0
    if changed:
        print(f"python-output: {len(changed)} file(s) out of date (run `just python-output`)")
        for p in changed:
            print("  ", p)
        return 1
    print(f"python-output: all outputs up to date ({injected} block(s))")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
