#!/usr/bin/env python3
"""Reformat Markdown prose to one sentence per line (semantic line breaks).

Only ordinary prose paragraphs and list-item text are reflowed. The following
are left byte-for-byte untouched:

  * YAML front matter (the leading `---` ... `---` block)
  * fenced code blocks (``` or ~~~, any fence length)
  * display math blocks (`\\[ ... \\]` and `$$ ... $$`)
  * headings, blockquotes, tables, horizontal rules, and raw HTML lines

Splitting is boundary-aware: inline code, inline math, and links are masked
before sentence detection, and a list of common abbreviations prevents false
breaks (e.g. "e.g.", "i.e.", "et al."). Because Markdown collapses a soft line
break inside a paragraph into a single space, this transformation never changes
the rendered HTML -- only the source layout.

Usage:
  sentence_lint.py --check PATH ...   # exit 1 if any file would change
  sentence_lint.py --write PATH ...   # rewrite files in place
Paths may be files or directories (directories are searched for *.md).
"""
from __future__ import annotations
import argparse
import os
import re
import sys

# Abbreviations after which a period does NOT end a sentence.
ABBREV = {
    "e.g", "i.e", "cf", "vs", "etc", "al", "fig", "eq", "eqs", "no", "nos",
    "vol", "pp", "sec", "ch", "approx", "resp", "dr", "prof", "mr", "mrs",
    "ms", "st", "inc", "ltd", "co", "jr", "sr", "ca", "viz", "esp",
}

# Mask inline spans that must never be split across a line boundary.
_MASK_PATTERNS = [
    re.compile(r"`[^`]*`"),                 # inline code
    re.compile(r"!\[[^\]]*\]\([^)]*\)"),    # image
    re.compile(r"\[[^\]]*\]\([^)]*\)"),     # link
    re.compile(r"\$[^$\n]*\$"),             # inline math
]

_LIST_RE = re.compile(r"^(\s*(?:[-*+]|\d+[.)])\s+)(.*)$")
_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")
_HR_RE = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
_FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")


def _mask(text: str):
    store: list[str] = []

    def repl(m: re.Match) -> str:
        store.append(m.group(0))
        return f"\x00{len(store) - 1}\x00"

    for pat in _MASK_PATTERNS:
        text = pat.sub(repl, text)
    return text, store


def _unmask(text: str, store: list[str]) -> str:
    # Placeholders can nest (e.g. inline code inside a link's text), so resolve
    # repeatedly until none remain.
    pat = re.compile(r"\x00(\d+)\x00")
    while pat.search(text):
        text = pat.sub(lambda m: store[int(m.group(1))], text)
    return text


def split_sentences(text: str) -> list[str]:
    """Split one paragraph (already whitespace-collapsed) into sentences."""
    masked, store = _mask(text)
    out, start, i, n = [], 0, 0, len(masked)
    while i < n:
        c = masked[i]
        if c in ".!?":
            j = i + 1
            while j < n and masked[j] in '.!?"\'”’)]}':
                j += 1
            # boundary requires whitespace then a plausible sentence start
            if j < n and masked[j] == " ":
                k = j + 1
                nxt = masked[k] if k < n else ""
                word = masked[start:i]
                last = re.split(r"[\s(\[]", word)[-1].lower().rstrip('."\'')
                is_abbrev = last in ABBREV
                is_initial = len(last) == 1 and last.isalpha()
                is_decimal = c == "." and i > 0 and masked[i - 1].isdigit() and nxt.isdigit()
                starts_ok = bool(re.match(r'[A-Z0-9$\x00("\'“*_\[]', nxt))
                if not (is_abbrev or is_initial or is_decimal) and starts_ok:
                    out.append(masked[start:j])
                    start = j + 1
                    i = j + 1
                    continue
        i += 1
    out.append(masked[start:])
    return [_unmask(s.strip(), store) for s in out if s.strip()]


def _is_para_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if _HEADING_RE.match(line) or _HR_RE.match(line):
        return False
    if s[0] in "#>|<":
        return False
    # Fenced directive lines (`:::spoiler`/`:::details` openers, the bare `:::`
    # closer, and `:::{include}:::` shortcodes) must sit on their own line, so
    # never reflow or merge them into an adjacent paragraph — doing so would
    # glue the summary onto the first body sentence or detach the closing `:::`,
    # corrupting the block for the site's `expand_spoilers` parser.
    if s.startswith(":::"):
        return False
    if _LIST_RE.match(line):
        return False
    if "|" in s:  # table row
        return False
    return True


def reflow(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i, n = 0, len(lines)
    in_front = False
    if lines and lines[0].strip() == "---":
        # YAML front matter
        out.append(lines[0])
        i = 1
        while i < n and lines[i].strip() != "---":
            out.append(lines[i]); i += 1
        if i < n:
            out.append(lines[i]); i += 1
    math_close = None
    while i < n:
        line = lines[i]
        # fenced code
        fence = _FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            out.append(line); i += 1
            while i < n:
                out.append(lines[i])
                if lines[i].strip().startswith(marker[0] * len(marker)) and lines[i].strip().rstrip(marker[0]) == "":
                    i += 1; break
                i += 1
            continue
        # display math block \[ ... \]  or  $$ ... $$
        stripped = line.strip()
        if stripped in ("\\[", "$$") or (stripped.startswith("\\[") and "\\]" not in stripped) or (stripped.startswith("$$") and len(stripped) > 2 and not stripped.endswith("$$")):
            close = "\\]" if "\\[" in stripped else "$$"
            out.append(line); i += 1
            while i < n and close not in lines[i]:
                out.append(lines[i]); i += 1
            if i < n:
                out.append(lines[i]); i += 1
            continue
        # list item: reflow the text after the marker, indent continuations
        m = _LIST_RE.match(line)
        if m:
            prefix, content = m.group(1), m.group(2)
            # gather lazy continuation lines (indented, non-blank, not new block)
            block = [content]
            i += 1
            cont_indent = " " * len(prefix)
            while i < n and lines[i].strip() and not _LIST_RE.match(lines[i]) \
                    and not _HEADING_RE.match(lines[i]) and not _FENCE_RE.match(lines[i]) \
                    and lines[i].strip()[0] not in "#>|<" and "|" not in lines[i] \
                    and not lines[i].strip().startswith(":::") \
                    and lines[i].startswith((" ", "\t")):
                block.append(lines[i].strip()); i += 1
            joined = re.sub(r"\s+", " ", " ".join(block)).strip()
            sents = split_sentences(joined)
            out.append(prefix + sents[0])
            for s in sents[1:]:
                out.append(cont_indent + s)
            continue
        # blank / heading / hr / blockquote / html / table -> passthrough
        if not _is_para_line(line):
            out.append(line); i += 1
            continue
        # plain paragraph: gather run of paragraph lines
        block = [line.strip()]
        i += 1
        while i < n and _is_para_line(lines[i]) and not _FENCE_RE.match(lines[i]):
            block.append(lines[i].strip()); i += 1
        joined = re.sub(r"\s+", " ", " ".join(block)).strip()
        out.extend(split_sentences(joined))
    result = "\n".join(out)
    return result


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
    g.add_argument("--check", action="store_true", help="report files that need changes (exit 1)")
    g.add_argument("--write", action="store_true", help="rewrite files in place")
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args()
    if not (args.check or args.write):
        args.check = True

    changed = []
    for path in iter_md(args.paths):
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
        trailing = "\n" if original.endswith("\n") else ""
        formatted = reflow(original.rstrip("\n")) + trailing
        if formatted != original:
            changed.append(path)
            if args.write:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(formatted)

    if args.write:
        print(f"sentence-lint: rewrote {len(changed)} file(s)")
        for p in changed:
            print("  fixed", p)
        return 0
    if changed:
        print(f"sentence-lint: {len(changed)} file(s) need reformatting (run `just fmt-prose`):")
        for p in changed:
            print("  ", p)
        return 1
    print("sentence-lint: all files conform to one-sentence-per-line")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # tolerate `... | head` and similar
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
