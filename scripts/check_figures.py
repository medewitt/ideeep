#!/usr/bin/env python3
"""Staleness check for committed figures.

Figures are Python scripts under `figures/` that render committed SVGs
(`just figures`). Because the SVGs are committed and the site build never
runs Python, a script can be edited without re-rendering, leaving the SVG on
the site out of sync with the code that supposedly produced it. This is the
figure-side analogue of `inject_python_output.py --check`.

It works by recording a manifest of `sha256(script source)` for every figure
script (`figures/*.py`, excluding the `_`-prefixed helpers `_style.py` and
`_card_motifs`'s shared helpers are matched by the same underscore rule the
`just figures` recipe uses -- see note below). `--check` recomputes those
hashes and fails if any script was added, removed, or edited since the
manifest was last written by `--write` (which `just figures` runs after a
successful render).

Scope note: this proves the committed figures match the *current* scripts at
the time `just figures` last ran. It does not re-render to diff pixels, so a
hand-edited SVG whose script is unchanged is out of scope (matplotlib SVG
output is not byte-reproducible -- it embeds a timestamp -- so a render diff
would be flaky). The staleness this guards against is the common one: code
changed, figure not regenerated.

Usage:
    python3 scripts/check_figures.py --write   # record manifest (after render)
    python3 scripts/check_figures.py --check    # CI: fail if stale

Stdlib only.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

FIGURES_DIR = Path("figures")
MANIFEST = FIGURES_DIR / ".figures-manifest.json"


def figure_scripts():
    """The scripts `just figures` renders: figures/*.py minus `_`-prefixed helpers.

    The recipe skips `_style.py`; every other `_`-prefixed file is a shared
    helper too (e.g. `_card_motifs.py` writes card art, not a tracked figure),
    so we exclude the whole `_*` class to stay in step with it.
    """
    return sorted(
        p for p in FIGURES_DIR.glob("*.py") if not p.name.startswith("_")
    )


def current_hashes():
    return {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in figure_scripts()
    }


def write():
    hashes = current_hashes()
    MANIFEST.write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n")
    print(f"wrote {MANIFEST} ({len(hashes)} figure scripts)")
    return 0


def check():
    if not MANIFEST.exists():
        print(
            f"error: {MANIFEST} is missing; run `just figures` to create it.",
            file=sys.stderr,
        )
        return 1

    recorded = json.loads(MANIFEST.read_text())
    current = current_hashes()

    added = sorted(set(current) - set(recorded))
    removed = sorted(set(recorded) - set(current))
    changed = sorted(
        name for name in set(current) & set(recorded)
        if current[name] != recorded[name]
    )

    if not (added or removed or changed):
        print(f"OK: {len(current)} figure(s) match committed output.")
        return 0

    for name in changed:
        print(f"stale: figures/{name} changed since its figure was rendered")
    for name in added:
        print(f"unrendered: figures/{name} has no recorded figure output")
    for name in removed:
        print(f"orphan: figures/{name} in manifest but no longer present")
    print(
        "\nRun `just figures` to regenerate the SVGs and refresh the manifest, "
        "then commit the result."
    )
    return 1


def main():
    ap = argparse.ArgumentParser(description="Check committed figures are up to date.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true", help="record the manifest")
    g.add_argument("--check", action="store_true", help="fail if figures are stale")
    args = ap.parse_args()

    if not FIGURES_DIR.is_dir():
        print("error: figures/ not found (run from repo root)", file=sys.stderr)
        return 2

    return write() if args.write else check()


if __name__ == "__main__":
    sys.exit(main())
