#!/usr/bin/env python3
"""Consistency check for the glossary against the built site.

The glossary listing (`content/_glossary.yaml`) drives two things in the build:
the first mention of each term is auto-linked on every page, and a
`glossary.html` page is generated with a reverse "Discussed on" index. A term
that is defined but never actually appears in prose is dead weight — it clutters
the listing and the glossary page without ever linking anything — and a `see:`
target that does not resolve is a broken promise.

This checker reads the emitted HTML in `dist/` (like `check_links.py`) so it
reflects exactly what the build produced, and reports:

  - unused terms   — defined in the listing but never auto-linked on any page
                     (i.e. neither the term nor an alias appears in real prose)
  - missing see:   — a `see:` target that is not a built page
  - duplicate slug — two terms that would collide on the same glossary anchor

Because auto-linking skips code, math, links, and headings, an "unused" term is
one that truly never occurs in body prose anywhere on the site.

Usage:
    python3 scripts/check_glossary.py [--check] [DIST]

    DIST      built site to scan (default: dist)
    --check   exit non-zero if any problem is found (for CI); without it the
              same report prints but the exit code stays 0

Stdlib only; the tiny slice of YAML used here (a list of `term:`/`see:` fields)
is parsed directly so the checker needs no third-party dependency.
"""
import argparse
import re
import sys
from pathlib import Path

GLOSSARY_FILE = Path("content/_glossary.yaml")


def slugify(text: str) -> str:
    """Mirror the generator's `slugify`: ASCII alphanumerics lower-cased, every
    other run collapsed to a single hyphen, trimmed."""
    out = []
    prev_dash = False
    for c in text:
        if c.isascii() and c.isalnum():
            out.append(c.lower())
            prev_dash = False
        elif out and not prev_dash:
            out.append("-")
            prev_dash = True
    return "".join(out).strip("-")


def _clean(value: str) -> str:
    value = value.strip()
    # Drop a trailing inline comment that is clearly not part of a quoted value.
    if value and value[0] not in "\"'" and "#" in value:
        value = value.split("#", 1)[0].strip()
    if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
        value = value[1:-1]
    return value


def parse_glossary(path: Path):
    """Parse the term list into [{term, see}], tolerant of the simple shape this
    file uses (a YAML sequence of mappings with `term:` and optional `see:`)."""
    terms = []
    current = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^\s*-\s*term:\s*(.+)$", raw)
        if m:
            current = {"term": _clean(m.group(1)), "see": None}
            terms.append(current)
            continue
        m = re.match(r"^\s*term:\s*(.+)$", raw)
        if m and current is not None and not current["term"]:
            current["term"] = _clean(m.group(1))
            continue
        m = re.match(r"^\s*see:\s*(.+)$", raw)
        if m and current is not None:
            current["see"] = _clean(m.group(1))
    return [t for t in terms if t["term"]]


def used_slugs(dist: Path):
    """Every glossary anchor slug that some page links to (a term auto-linked at
    least once), read from the emitted HTML."""
    used = set()
    ref = re.compile(r"glossary\.html#([a-z0-9-]+)")
    for html in dist.rglob("*.html"):
        if html.name == "glossary.html":
            continue
        used.update(ref.findall(html.read_text(encoding="utf-8", errors="ignore")))
    return used


def main() -> int:
    ap = argparse.ArgumentParser(description="Check the glossary against dist/.")
    ap.add_argument("dist", nargs="?", default="dist")
    ap.add_argument("--check", action="store_true", help="exit non-zero on any problem")
    args = ap.parse_args()

    if not GLOSSARY_FILE.exists():
        print(f"No {GLOSSARY_FILE}; nothing to check.")
        return 0
    dist = Path(args.dist)
    if not dist.exists():
        print(f"error: {dist} does not exist -- build the site first", file=sys.stderr)
        return 2

    terms = parse_glossary(GLOSSARY_FILE)
    used = used_slugs(dist)

    unused, missing_see, dup = [], [], []
    seen_slugs = {}
    for t in terms:
        slug = slugify(t["term"])
        if slug in seen_slugs:
            dup.append((t["term"], seen_slugs[slug], slug))
        else:
            seen_slugs[slug] = t["term"]
        if slug not in used:
            unused.append((t["term"], slug))
        see = t["see"]
        if see:
            key = see[:-3] if see.endswith(".md") else see
            if not (dist / f"{key}.html").exists():
                missing_see.append((t["term"], see))

    problems = 0
    for term, slug in unused:
        print(f"unused term: '{term}' (#{slug}) is never auto-linked on any page")
        problems += 1
    for term, see in missing_see:
        print(f"missing see: '{term}' points to '{see}', which is not a built page")
        problems += 1
    for term, first, slug in dup:
        print(f"duplicate slug: '{term}' and '{first}' both resolve to #{slug}")
        problems += 1

    if problems:
        print(f"\n{problems} glossary problem(s) across {len(terms)} term(s).")
        return 1 if args.check else 0
    print(f"OK: {len(terms)} glossary term(s), all used and resolvable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
