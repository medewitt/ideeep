#!/usr/bin/env python3
"""Internal link checker for the built site.

Scans every `*.html` under `dist/` and verifies that internal references
resolve against the actual output the compiler just wrote:

  - <a href> to another page or asset exists as a file in dist/
  - a `#fragment` (alone or after a path) matches an `id`/`name` in the target
  - <img src>, <link href>, <script src>, and <source src>/srcset assets exist

External links (http/https, protocol-relative `//`, mailto:, tel:, data:,
javascript:) are not fetched or validated -- this checker only proves the
site is internally consistent, which is the class of breakage the build can
introduce on its own (a renamed page, a stale hub link, a mistyped anchor).

Because it reads the emitted HTML rather than the Markdown sources, it also
catches link-rewriting bugs (`.md` -> `.html`) and missing generated pages.

Usage:
    python3 scripts/check_links.py [--check] [DIST]

    DIST      directory to scan (default: dist)
    --check   exit non-zero if any broken link is found (for CI); without it
              the same report prints but the exit code stays 0

Stdlib only; no build dependencies.
"""
import argparse
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

# Schemes / forms we deliberately do not resolve locally.
EXTERNAL_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:")

# Attributes that carry a single URL, keyed by tag.
URL_ATTRS = {
    "a": "href",
    "link": "href",
    "area": "href",
    "img": "src",
    "script": "src",
    "source": "src",
    "iframe": "src",
    "audio": "src",
    "video": "src",
    "track": "src",
    "embed": "src",
}


class RefCollector(HTMLParser):
    """Collect anchor ids and outgoing local references from one HTML file."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()          # every id="" / name="" on the page
        self.refs = []            # (raw_url,) outgoing references worth checking

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d and d["id"]:
            self.ids.add(d["id"])
        if "name" in d and d["name"] and tag in ("a", "map"):
            self.ids.add(d["name"])

        attr = URL_ATTRS.get(tag)
        if attr and d.get(attr):
            self.refs.append(d[attr].strip())
        # <source srcset="a.jpg 1x, b.jpg 2x"> and <img srcset=...>
        if "srcset" in d and d["srcset"]:
            for part in d["srcset"].split(","):
                url = part.strip().split(" ")[0].strip()
                if url:
                    self.refs.append(url)


def is_external(url: str) -> bool:
    return url.startswith(EXTERNAL_PREFIXES)


def split_fragment(url: str):
    """Return (path, fragment_or_None), stripping any ?query from the path."""
    frag = None
    if "#" in url:
        url, frag = url.split("#", 1)
    if "?" in url:
        url = url.split("?", 1)[0]
    return url, frag


def resolve(dist: Path, page: Path, path: str) -> Path:
    """Resolve a link target to a filesystem path within dist."""
    path = unquote(path)
    if path.startswith("/"):
        target = dist / path.lstrip("/")
    else:
        target = page.parent / path
    # A directory reference (".../" or "") means its index.html.
    if path.endswith("/") or path == "":
        target = target / "index.html"
    return target


def parse_files(dist: Path):
    """Parse every html file once; return {page_path: RefCollector}."""
    parsed = {}
    for page in sorted(dist.rglob("*.html")):
        parser = RefCollector()
        try:
            parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:  # a parse failure is itself worth surfacing
            print(f"warning: could not parse {page}: {e}", file=sys.stderr)
        parsed[page.resolve()] = parser
    return parsed


def check(dist: Path):
    parsed = parse_files(dist)
    # Fast membership test for asset/page existence without a stat() per ref.
    existing = {p.resolve() for p in dist.rglob("*") if p.is_file()}
    ids_by_file = {path: pr.ids for path, pr in parsed.items()}

    broken = []  # (page_rel, raw_url, reason)
    for page, pr in parsed.items():
        page_rel = page.relative_to(dist.resolve())
        for raw in pr.refs:
            url = html.unescape(raw)
            if is_external(url) or url.startswith("#") and url == "#":
                # pure "#" is a common no-op link target; skip it
                if url == "#":
                    continue
            if is_external(url):
                continue

            path, frag = split_fragment(url)

            if path == "":
                # same-page fragment
                if frag and frag not in pr.ids:
                    broken.append((page_rel, raw, f"no #{frag} on this page"))
                continue

            target = resolve(dist, page, path).resolve()
            if target not in existing:
                broken.append((page_rel, raw, "target file does not exist"))
                continue

            if frag:
                target_ids = ids_by_file.get(target)
                if target_ids is None:
                    # linked to a non-HTML asset with a fragment; skip anchor check
                    continue
                if frag not in target_ids:
                    rel_t = target.relative_to(dist.resolve())
                    broken.append((page_rel, raw, f"no #{frag} in {rel_t}"))

    return broken, len(parsed)


def main():
    ap = argparse.ArgumentParser(description="Check internal links in the built site.")
    ap.add_argument("dist", nargs="?", default="dist", help="built site directory (default: dist)")
    ap.add_argument("--check", action="store_true", help="exit non-zero if any link is broken")
    args = ap.parse_args()

    dist = Path(args.dist)
    if not dist.is_dir():
        print(f"error: {dist} is not a directory (build the site first)", file=sys.stderr)
        return 2

    broken, n_pages = check(dist)

    if broken:
        # Group by source page for a readable report.
        by_page = {}
        for page_rel, raw, reason in broken:
            by_page.setdefault(str(page_rel), []).append((raw, reason))
        for page in sorted(by_page):
            print(f"{page}:")
            for raw, reason in by_page[page]:
                print(f"  {raw}  ->  {reason}")
        print(f"\n{len(broken)} broken link(s) across {n_pages} page(s).")
        return 1 if args.check else 0

    print(f"OK: no broken internal links across {n_pages} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
