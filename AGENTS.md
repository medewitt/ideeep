# AGENTS.md — how this site is built and how to contribute

This file is the design and build guide for the IDEEEP site.
It is written for future agents (and humans) so that new content matches the established conventions.
Read it before adding or editing pages.

## What this project is

This repository is a **custom static-site generator written in Rust** — a single-binary Markdown compiler (`src/main.rs`, crate `md-compiler`).
It is **not** Quarto, mdBook, Bookdown, Hugo, or Jupyter Book, even though the content contains R/Python/Julia code.

- Content is **plain Markdown** under `content/`, with YAML front matter whose only used field is `title:`.
- Math is rendered at build time with **KaTeX** (server-side); no MathJax runtime is needed.
- The build produces static HTML in `dist/` and an SQLite full-text **search index** (`dist/search.db`).
- Deployment is Netlify (`netlify.toml`); there is no GitHub Actions CI.

## Directory layout

```
content/            all site content (Markdown); discovered recursively
  math/             "Quantitative Methods" concept pages
  programming/      "Programming & Computing" concept pages
  epidemiology/     "Epidemiology" concept pages (intervals, delays)
  diagnostics/      "Diagnostics & Surveillance" method pages
  math.md, programming.md, epidemiology.md, diagnostics.md   section hub pages
  scientific-pathways.md, scientific-writing.md              single-page sections
  index.md, programs.md, research.md, people.md, *.md        top-level & syllabus pages
figures/            PEP-723 Python scripts -> assets/figures/*.svg (via `just figures`)
  _style.py         shared matplotlib style (palette, apply_style, save)
assets/             styles.css, nav.js, footer.html, fonts/ (Nunito Sans woff2), figures/*.svg, vendor/ (katex, sqljs, highlightjs)
scripts/            sentence_lint.py, inject_python_output.py (dev tools)
config.yaml         navbar order and dropdown definitions
justfile            build / lint / figures / preview recipes
src/main.rs         the generator
```

## How pages and navigation work

**Pages are auto-discovered.** `find_markdown_files` walks `content/` recursively and renders every `*.md` to `dist/<relative-path>.html`.
You do **not** register a page anywhere to get it compiled — dropping a file into `content/…` is enough.
Relative `.md` links are rewritten to `.html` at build time.

**Visibility comes from two places:**

1. **Hub pages.** Concept pages surface to readers only through hand-curated link lists on a section **hub** page (e.g. `content/math.md`, `content/diagnostics.md`), grouped under `##` headings. Add a bullet like `- [Title](diagnostics/qpcr.md) — short description` to the hub when you add a page.
2. **The navbar** is driven entirely by `config.yaml`:
   - `navbar_order` lists top-level items and dropdown names in display order.
   - `dropdowns:` maps a dropdown name to a list of page keys (a content path without extension, e.g. `epidemiology` → `content/epidemiology.md`).
   - Pages listed inside a dropdown are filtered out of the flat navbar.

To **add a new section**: create a hub page `content/<section>.md`, put its pages in `content/<section>/`, then add the hub key to a `dropdowns:` entry and place that dropdown in `navbar_order`.

## Page skeleton (match this)

See `content/math/logistic-growth.md` or `content/epidemiology/epidemiological-intervals.md` for exemplars. The standard structure is:

```markdown
---
title: "Page Title"
---

# Page Title

Two or three sentences motivating the topic.

![Descriptive alt text that doubles as the figure caption.](../assets/figures/name.svg)

## Concept sections
Prose and math, with ### subsections as needed.

## A worked example
Concrete numbers.

## In code
### R
### Python
### Julia

## Why it matters
Tie back to infectious-disease ecology / epidemiology.

## Related
- [Sibling Page](sibling.md)
- [Section Hub](../section.md)   <!-- always link back to the hub last -->
```

Notes on paths: nested pages (`content/<section>/page.md`) reference figures as `../assets/figures/…` and the hub as `../<section>.md`; top-level hub pages use `assets/figures/…` and `section/page.md`.

## Write to build intuition

The goal of a topical content page is **understanding**, not just reference.
Lead with the intuition — the mental picture or the "why" — before the formalism, and let concrete, biological examples carry the ideas (a specific pathogen, a specific timeline, a specific bias) rather than abstractions alone.

Illustrate generously.
Favor **many graphics and code snippets** over dense prose: a page should usually have at least one figure near the top and one wherever a concept turns visual (a timeline, a distribution, a bias, a curve), plus runnable `R`/`Python`/`Julia` code and a worked numeric example.
Every figure and code block should *do explanatory work* — make an idea click, expose a mechanism, or let the reader reproduce a result — not just decorate.
Prefer showing a mechanism (simulate it, plot it, fit it) over asserting it, and keep the reader able to run and modify what they see.

## Prose convention: one sentence per line

Prose is written **one sentence per line** (semantic line breaks), enforced by `scripts/sentence_lint.py`.
Front matter, fenced code, and display-math blocks are exempt.
This never changes the rendered HTML (Markdown collapses single newlines to spaces) — it just keeps diffs clean.

- Check: `just lint-prose`   ·   Auto-fix: `just fmt-prose`
- **When you add a new content directory, add it to `prose_dirs` in the `justfile`** so it is linted and gets Python output injected.

## Math

Inline math is `$…$`; display math is `\[ … \]` or `$$ … $$`.
Use conventional notation (`$\theta$`, `\frac`, `\mathbb{E}[\cdot]`, `\propto`).
KaTeX renders at build time; a malformed expression shows up as a `math-error` span in the HTML.

## Figures

Figures are **static SVGs** in `assets/figures/`, each generated by a self-contained PEP-723 script `figures/<stem>.py`.

- Import the shared style: `from _style import apply_style, save, PALETTE, INK, MUTED`, call `apply_style()`, and end with `save(fig, "assets/figures/<stem>.svg")`.
- Palette: `PALETTE = ["#2f6f9f", "#c1531f", "#3f8f5b", "#8a5cb0", "#b0842f"]`; ink `#26323f`. Transparent background, no top/right spines.
- **matplotlib only** (no plotly, mermaid, or tikz). Use `np.trapezoid` (not the removed `np.trapz`) on current NumPy.
- Build all figures with `just figures` (runs each script via `uv`). Committed SVGs mean the site build never needs Python.

## Executable Python: output injection

` ```python ` blocks are **executed** by `scripts/inject_python_output.py`, and their real stdout is injected beneath the block between `<!-- python-output:auto -->` markers (idempotent).

- Blocks on a page run **top-to-bottom in one shared namespace**.
- Allowed dependencies (fixed set): `numpy, scipy, sympy, pandas, polars, statsmodels, networkx, matplotlib, scikit-learn, numpyro, jax`. (`numpyro`/`jax` make the injector heavier to install and run — they are included so Bayesian examples can execute; keep such blocks small and fast, e.g. short MCMC runs.)
- Keep blocks **deterministic** (seed RNGs), **self-contained**, and **low-output** (capped at 15 lines).
- **R and Julia blocks are never executed** — they are illustrative, so they may reference any package.
- Add `# no-run` to skip a block; plot-only or intentionally-erroring blocks inject nothing.
- Run `just python-output` to (re)generate; `just python-output-check` verifies it is current.
- **Prefer [Polars](https://pola.rs) over pandas** in new Python examples.

## References and cross-links

There is **no bibliography system** (no `.bib`/`.csl`, no `@cite`). Cite sources as inline Markdown links to docs or papers.
Cross-reference other pages with relative `.md` links, which are rewritten to `.html` at build.

## Build & verify

```
just build            # cargo run --release -> dist/
just figures          # render figures/*.py -> assets/figures/*.svg
just python-output     # execute python blocks and inject stdout
just lint-prose        # one-sentence-per-line check
just preview           # build + serve dist/ on :8000
```

Before committing new content, run `just figures`, `just python-output`, `just lint-prose`, and `just build`, and confirm the new pages appear under the right navbar dropdown with figures rendering and internal links resolving.
