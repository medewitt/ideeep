# AGENTS.md — how this site is built and how to contribute

This file is the design and build guide for the IDEEEP site.
It is written for future agents (and humans) so that new content matches the established conventions.
Read it before adding or editing pages.

> **Just writing a content page?** See [`for-authors.md`](for-authors.md) — the
> task-oriented authoring guide (page structure, math, figures, equations,
> callouts, spoilers, runnable code, cross-references). This file (`AGENTS.md`)
> covers how the generator itself is built.

## What this project is

This repository is a **custom static-site generator written in Rust** — a single-binary Markdown compiler (`src/main.rs`, crate `md-compiler`).
It is **not** Quarto, mdBook, Bookdown, Hugo, or Jupyter Book, even though the content contains R/Python/Julia code.

- Content is **plain Markdown** under `content/`, with YAML front matter: `title:` (required), plus optional `description:` (meta/social) and `toc: true` (adds an "On this page" list).
- Math is rendered at build time with **KaTeX** (server-side); no MathJax runtime is needed.
- The build produces static HTML in `dist/` and an SQLite full-text **search index** (`dist/search.db`).
- Deployment is Netlify (`netlify.toml`). GitHub Actions CI (`.github/workflows/ci.yml`) runs the guardrails on every push/PR: the Rust regression suite (`just test`), the dev-tool unit tests (`just test-scripts`: the Python-output injector and the spoiler-aware sentence linter), the prose linter (`just lint-prose`), figure staleness (`just figures-check`), injected-output freshness (`just python-output-check`), a full build plus internal-link check (`just check-links`), and glossary consistency (`just glossary-check`). Keep these green locally before pushing.

## Directory layout

```
content/            all site content (Markdown); discovered recursively
  math/             "Quantitative Methods" concept pages
  programming/      "Programming & Computing" concept pages
  epidemiology/     "Epidemiology" concept pages (intervals, delays)
  diagnostics/      "Diagnostics & Surveillance" method pages
  _fragments/       reusable Markdown fragments injected via `:::{name.md}:::` (NOT compiled to pages)
  math.md, programming.md, epidemiology.md, diagnostics.md   section hub pages
  scientific-pathways.md, scientific-writing.md              single-page sections
  index.md, programs.md, research.md, people.md, *.md        top-level & syllabus pages
figures/            PEP-723 Python scripts -> assets/figures/*.svg (via `just figures`)
  _style.py         shared matplotlib style (palette, apply_style, save)
assets/             styles.css, nav.js, footer.html, emblem.png, fonts/ (Nunito Sans woff2), figures/*.svg, cards/*.svg (home-page card art), vendor/ (katex, sqljs, highlightjs)
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

Hub (and other long) pages can set `toc: true` in front matter to get an
auto-generated "On this page" table of contents built from their `##` headings;
it is off by default. Flat link lists (4+ items, all links) are automatically
flowed into responsive columns.

Any page can set `hidden: true` in front matter to be **unlisted**: it renders
at its URL and is reachable by direct link, but is served with a `noindex`
`robots` tag and kept out of `sitemap.xml` and the on-site search index. Navbar
placement is separate (driven by `config.yaml`), so a hidden page is simply left
out of `navbar_order`/`dropdowns`. This is the general mechanism for drafts and
share-by-link pages; it is off by default. (Note: unlisted is not private —
anyone with the URL can view it. Real access control needs Netlify-level auth.)
The built-in `404` and `interest-thank-you` pages are always handled specially
regardless of this flag. See `is_indexable`/`is_search_indexable` in `src/main.rs`.

Schedule pages can set `sort_schedule: true` in front matter. At build time the
generator sorts every Markdown table on the page that has a `Day` and/or `Time`
column by weekday then start time, so a hand-edited agenda re-orders itself
instead of leaving rows where they were typed. Time parsing is meridiem-aware
for this program's day (9–11 AM, 12 noon, 1–3 PM), so `1-1:50` sorts after
`11-11:50`; a `p`/`a` suffix (`12-1p`) forces the meridiem. Tables without a
`Day` or `Time` header, and all surrounding prose, are left untouched. It is off
by default. See `sort_schedule_tables` in `src/main.rs`.

## Reusable template fragments (`:::{name.md}:::`)

Content that is **identical across many pages** — the shared course policies,
the university policies, the syllabus change notice — lives once in
`content/_fragments/` and is pulled into each page with an include shortcode:

```markdown
:::{course-policies.md}:::
:::{university-policies.md}:::
:::{syllabus-change-notice.md}:::
```

- The shortcode must sit **on its own line**. The `.md` extension is optional
  (`:::{course-policies}:::` also works).
- **Options** may follow the name after a `;`: `:::{fellow-schedule-2026; schedule=true}:::`.
  The only option today is `schedule` (bare or truthy), which sorts the
  fragment's schedule tables by day then start time as it is spliced in — so a
  reusable agenda fragment can be embedded on any page and stay ordered after
  hand-edits. Unknown options are ignored, so the syntax can grow safely.
  (The same sort is available page-wide via the `sort_schedule: true` front-matter
  flag for tables written directly in a page.)
- The fragment's Markdown is spliced in **before** parsing, so it renders exactly
  as if written inline — headings, tables, callouts and math all work. Includes
  may nest (a fragment can include another).
- Edit the fragment once and every page that references it updates on the next
  build. To centralise a new shared block: drop a `content/_fragments/<name>.md`
  file, then replace the repeated text on each page with `:::{<name>.md}:::`.
- `content/_fragments/` (any `_`-prefixed directory under `content/`) is **not**
  compiled to standalone pages — fragments exist only to be injected.
- A shortcode pointing at a missing file (or trying to escape the fragments
  directory with `..`) renders a loud `.fragment-error` marker and logs a build
  warning, so a dropped section is caught rather than silently lost.

Not every syllabus shares the same wording — some courses have course-specific
attendance or late-work policies, or a longer university-policy block. Those keep
their text inline; only the byte-identical sections are centralised.

## Page skeleton (match this)

See `content/math/logistic-growth.md` or `content/epidemiology/epidemiological-intervals.md` for exemplars. The standard structure is:

```markdown
---
title: "Page Title"
description: "Optional 1-sentence summary for search results and social cards."
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
- The linter is **spoiler-aware**: `:::spoiler`/`:::details`/`:::` fence lines and
  `:::{include}:::` shortcodes are passed through untouched, so auto-fixing never
  corrupts a disclosure block (regression-tested in `scripts/test_sentence_lint.py`).

## Math

Inline math is `$…$`; display math is `\[ … \]` or `$$ … $$`.
Use conventional notation (`$\theta$`, `\frac`, `\mathbb{E}[\cdot]`, `\propto`).
KaTeX renders at build time; a malformed expression shows up as a `math-error` span in the HTML.

**Numbered equations (opt-in).** A display equation carrying a `\label{eq:name}`
is assigned the next per-page number, rendered with a KaTeX `\tag{N}` so "(N)"
prints at the right margin, and wrapped in `<span id="eq-name">` so it can be
linked. Reference it anywhere with `[@eq:name]`, which resolves to a numbered
`(N)` link (either document order); an unresolved reference renders a loud
marker. Only labelled display equations are numbered — plain derivation steps are
left unnumbered. See `render_display_math`/`resolve_equation_refs` in
`src/main.rs`. (Figures are the analogue: block images auto-number and are
labelled with a `"fig:name"` image title, referenced with `[@fig:name]` — see
the Figures section.)

## Callouts

Use GitHub-style admonition blockquotes for asides; the build renders them as
styled callouts with an icon. Supported types: `[!NOTE]`, `[!TIP]`,
`[!WARNING]`, `[!EXAMPLE]`.

```markdown
> [!TIP]
> Seed your RNG so simulations are reproducible.
```

Inline math, code, links, and bold all work inside a callout. A plain `>`
blockquote (no `[!TYPE]`) still renders as an ordinary quote.

## Spoilers / disclosure blocks (`:::spoiler … :::`)

Hide a worked solution, a long derivation, or an aside behind a click with a
fenced spoiler block. It compiles to a native `<details>`/`<summary>` widget —
no JavaScript — and the body is **ordinary Markdown** (lists, math, code, even
nested spoilers all work):

```markdown
:::spoiler Show the solution
Substitute $R_0 = \beta / \gamma$ and simplify.

- step one
- step two
:::
```

- The text after the keyword is the clickable **summary, and it is fully
  configurable** — `:::spoiler Show the solution`, `:::spoiler Reveal`,
  `:::spoiler Hint`, anything. A bare `:::spoiler` uses "Show more".
- `:::details` is an alias for `:::spoiler` (identical behavior).
- The opener sits on its own line; the block ends at a line that is exactly
  `:::`. Blocks may **nest**. An opener with no matching `:::` close is left
  untouched, so stray text is never swallowed.
- **Keep the `:::spoiler`/`:::details` opener and the closing `:::` each on their
  own line** (a blank line around them is fine but not required). The prose
  linter is spoiler-aware and never reflows these fence lines, so
  `just fmt-prose` will not glue the summary onto the first sentence or detach
  the closer — but hand-editing them onto a prose line still breaks the block.
  As a backstop the parser also recovers from a closer accidentally glued to the
  previous sentence (`… last sentence. :::`); see `fence_close_body`.
- See `expand_spoilers` in `src/main.rs` (and its tests, e.g.
  `spoiler_recovers_from_glued_closer`).

## Section permalinks

Every `##`/`###` heading is emitted with a stable `id` **and** a `#` permalink
anchor (revealed on hover) so any section can be deep-linked. This is automatic;
you do nothing. See `add_heading_ids` in `src/main.rs`.

## Code blocks

Every fenced code block is wrapped at build time in a `.code-block` container
with a language badge and a **Copy** button (`enhance_code_blocks` in
`src/main.rs`); the button is wired by `assets/nav.js`. Tag the fence with its
language so the badge and highlight.js coloring are correct.

## Glossary

`content/_glossary.yaml` is a central list of terms (`term`, `short`, optional
`aliases`/`long`/`see`). The build (1) auto-links the **first** occurrence of
each term/alias in every page's prose with a definition tooltip — skipping code,
math, links, and headings — and (2) generates `/glossary.html`, whose entries
carry a reverse index of the pages that mention each term. Matching is
whole-word and case-insensitive; a page opts out with `glossary: false` in front
matter; an empty/absent listing makes the feature inert. The `Glossary` keyword
is a built-in navbar item (like `Search`) and is added to `config.yaml`'s
`navbar_order`. See `load_glossary`/`decorate_glossary`/`glossary_page_content`
in `src/main.rs`. `content/_glossary.yaml` is data, not a page — like
`_fragments/`, it is never compiled to HTML. `just glossary-check`
(`scripts/check_glossary.py`, in CI) fails if a term is defined but never
auto-linked on any page, a `see:` target does not resolve, or two terms collide
on one slug.

## Backlinks ("Referenced by")

Before rendering, the build reads every page's Markdown and resolves its
internal links (the same rules as `convert_internal_links`) into a reverse index
— for each page, the set of pages that link to it. A "Referenced by" list is
appended at the foot of each page. Hidden pages are excluded as *sources* so a
draft never advertises itself. See `extract_internal_targets`/
`resolve_link_target`/`build_backlinks_section` in `src/main.rs`. Links inside
included fragments are attributed to the fragment author's intent, not the host
page (extraction runs on the page's own Markdown), which is a deliberate
simplification.

## Home page

`content/index.md` uses a raw-HTML hero and a grid of image-backed section
cards (`<a class="card" href="…" style="background-image: url(assets/cards/…)">`).
The card art in `assets/cards/*.svg` are on-brand scientific motifs generated by
`figures/_card_motifs.py` (regenerated by `just figures`). To use photographs
instead (e.g. NIH BIOART), drop images into `assets/cards/` and point each
card's `background-image` at them — no other markup changes are needed.

## Photos and image credits

Non-generated images (photographs, NIH BioArt illustrations, logos, icons) live
in `assets/` and `assets/photos/`. Two files document them and **must stay in
sync with the images and with each other**:

- `assets/README.md` — the developer catalog of every non-Python-generated
  image: what each one depicts, where it is used, and its credit/license.
- `content/credits.md` — the public credits page, rendered at `/credits.html`
  and linked from `assets/footer.html`.

**Whenever you add (or a maintainer loads) a new photo or other non-generated
image, update both files in the same change:** add a row/entry to
`assets/README.md` (file, description, credit, where it is used) and add the
credit to `content/credits.md`. Record the photographer/source and license;
photographs are by Michael E. DeWitt unless the maintainer says otherwise, NIH
BioArt illustrations are public domain (courtesy of NIAID), and historical scans
are public domain by age. Do not credit a photo to a person or organization
without confirmation — ask if the source is unstated.

## Figures

Figures are **static SVGs** in `assets/figures/`, each generated by a self-contained PEP-723 script `figures/<stem>.py`.

- Import the shared style: `from _style import apply_style, save, PALETTE, INK, MUTED`, call `apply_style()`, and end with `save(fig, "assets/figures/<stem>.svg")`.
- Palette: `PALETTE = ["#2f6f9f", "#c1531f", "#3f8f5b", "#8a5cb0", "#b0842f"]`; ink `#26323f`. Transparent background, no top/right spines.
- **matplotlib only** (no plotly, mermaid, or tikz). Use `np.trapezoid` (not the removed `np.trapz`) on current NumPy.
- Build all figures with `just figures` (runs each script via `uv`). Committed SVGs mean the site build never needs Python.

### Numbering, captions, and cross-references

Any **block image** (a paragraph that is just `![alt](src)`, the standard page
convention) is automatically wrapped in a numbered `<figure>` at build time, and
the **alt text becomes the visible caption**:

> Figure 1. *(your alt text)*

Numbering is per page. To **cross-reference** a figure from prose, give the image
a title that starts with `fig:` and then refer to it with `[@fig:…]` anywhere on
the page (either order):

```markdown
![Epidemic curve over time](../assets/figures/curve.svg "fig:curve")

As shown in [@fig:curve], incidence peaks early.
```

`[@fig:curve]` renders as a link reading "Figure N" pointing at the figure; the
`fig:` sentinel is stripped from the `<img>`. An **empty alt with no label** is
left as a plain, un-numbered image (use it for purely decorative art), and an
**unresolved `[@fig:…]`** renders a loud marker rather than silently vanishing.
See `process_figures` in `src/main.rs`.

## Executable Python: output injection

` ```python ` blocks are **executed** by `scripts/inject_python_output.py`, and their real stdout is injected beneath the block between `<!-- python-output:auto -->` markers (idempotent).

- Blocks on a page run **top-to-bottom in one shared namespace**.
- Allowed dependencies (fixed set): `numpy, scipy, sympy, pandas, polars, statsmodels, networkx, matplotlib, scikit-learn, numpyro, jax`. (`numpyro`/`jax` make the injector heavier to install and run — they are included so Bayesian examples can execute; keep such blocks small and fast, e.g. short MCMC runs.)
- Keep blocks **deterministic** (seed RNGs), **self-contained**, and **low-output** (capped at 15 lines).
- **R and Julia blocks are never executed** — they are illustrative, so they may reference any package.
- Add `# no-run` to skip a block; plot-only or intentionally-erroring blocks inject nothing.
- Run `just python-output` to (re)generate; `just python-output-check` verifies it is current.
- **Prefer [Polars](https://pola.rs) over pandas** in new Python examples.

**Execution is cached by content hash.** A page's injected output is a pure
function of its ordered ```python blocks, so the injector fingerprints those
blocks and records the fingerprint in `scripts/.python-output-cache.json` after
a successful `--write`. A later run skips executing any page whose fingerprint
still matches — so a full `just python-output-check` no longer re-runs the heavy
MCMC/`jax` pages every time, and editing only prose on such a page does not
trigger re-sampling. **Commit the cache file** alongside the injected outputs
(both are written by `just python-output`); it is what lets CI's `--check` only
execute the pages whose code actually changed. The cache self-heals — a missing
or stale entry just falls back to running that page — so deleting it is safe and
only costs a one-time recompute. Bump `FORMAT_TAG` in the script if you change
the injection format so every fingerprint invalidates.

The injector has its own regression suite, `scripts/test_inject_python_output.py`
(stdlib only), run with `just test-scripts` — which also runs
`scripts/test_sentence_lint.py`, the sentence-linter suite that locks in the
one-sentence-per-line reflow and its spoiler-awareness (fence lines are never
merged into prose). It follows the same test-driven
rule as the Rust generator: changes to `inject_python_output.py` — injection,
`# no-run` / truncation handling, fingerprinting, or caching — should come with a
test. Keep injected Python **deterministic**: seed every RNG *and* pin any
library-internal randomness (e.g. `PCA(svd_solver="full")`, which avoids
scikit-learn's unseeded randomized SVD), so a page's committed output is stable
and the fingerprint cache stays trustworthy.

## SEO & PWA

The generator emits search-engine and installable-app metadata automatically — you rarely touch it, but a few authoring habits make it better.

**What the build produces (per page, in `src/main.rs`):**

- A descriptive `<title>` (`Page Title · IDEEEP`), `<meta name="description">`, and a `<link rel="canonical">` pointing at the production URL (currently `https://id3es.com`).
- Open Graph and Twitter Card tags (title/description/image) so links unfurl on social and chat, using `assets/og-image.png` as the share image.
- JSON-LD structured data: `WebPage` + `WebSite` (with an on-site `SearchAction`), plus a `BreadcrumbList` (Home › Section hub › Page) on nested pages.
- PWA hooks: `<link rel="manifest">`, `apple-touch-icon`, `theme-color`, and a registered service worker (`sw.js`) for offline support.
- The `content/404.md` page is emitted with `noindex` (Netlify already serves it with an HTTP 404 status); every other page is indexable.

**Site-wide files written to `dist/` at build time:**
`sitemap.xml` (all pages except 404), `robots.txt` (points at the sitemap), `manifest.webmanifest`, `sw.js`, and Netlify `_headers`.

**How to help the metadata:**

- **Write a strong first paragraph.** When a page has no `description:` in its front matter, the build derives the meta description from the first real prose paragraph (headings and block quotes are skipped), truncated to ~160 characters. Lead with a self-contained sentence that reads well out of context.
- **Set `description:` explicitly** for hub pages or anywhere the opening prose does not summarize the page.
- **Give share-worthy pages a per-page social image.** By default every page unfurls with the shared `assets/og-image.png` card. A page can override it with front matter `image:` (a site-root-relative asset path, e.g. `image: assets/photos/serology-antibody-test.jpg`) plus optional `image_alt:`; the build points `og:image` and `twitter:image` at it, infers the MIME type from the extension, and falls back to the page title for alt text. Use a topical, high-quality image (landscape, ideally near 1200×630) — a generic or off-topic card is worse for click-through than the branded default. Credit any such image in `assets/README.md` and `content/credits.md` as usual.
- **Keep the H1 and `title:` meaningful** — they feed the `<title>` and social cards.
- **If the production domain changes**, edit the `homepage` field in `Cargo.toml` (no trailing slash) and rebuild; canonical URLs, social cards, JSON-LD, the sitemap, robots.txt, and the manifest all derive from it. No code edit needed.
- **Bump the `CACHE` constant in `write_service_worker`** if you change cached core assets and need clients to refresh.

Regenerate the icons (`assets/icon-*.png`, `apple-touch-icon.png`, `og-image.png`) from `assets/logo.png` / `logo-wide.png` only if the logo changes.

## References and cross-links

There is **no bibliography system** (no `.bib`/`.csl`, no `@cite`). Cite sources as inline Markdown links to docs or papers.
Cross-reference other pages with relative `.md` links, which are rewritten to `.html` at build.

## Build & verify

```
just build            # cargo run --release -> dist/
just test             # cargo test --release (md-compiler unit tests)
just figures          # render figures/*.py -> assets/figures/*.svg
just python-output     # execute python blocks and inject stdout
just lint-prose        # one-sentence-per-line check
just preview           # build + serve dist/ on :8000
```

Before committing new content, run `just figures`, `just python-output`, `just lint-prose`, and `just build`, and confirm the new pages appear under the right navbar dropdown with figures rendering and internal links resolving.

## Working on the generator (`src/main.rs`) — test-driven

Changes to the Rust generator follow **test-driven development**. The unit
tests live in the `#[cfg(test)] mod tests` block at the bottom of `src/main.rs`
and run with `just test` (`cargo test --release`).

- **Every fixed bug needs a test.** When you fix a bug in a Rust file, first add
  a test that reproduces it (it should fail on the unfixed code), then make it
  pass. Confirm the test is meaningful by checking it actually fails when the fix
  is reverted — a test that passes both ways guards nothing.
- **Changes to `src/main.rs` should include a test where possible.** New or
  modified rendering behavior (Markdown/KaTeX handling, link rewriting, callouts,
  metadata) should come with a test that exercises it through the real pipeline —
  most rendering tests can call `markdown_to_html(md, &HashSet::new())` and assert
  on the HTML. If a change genuinely has no testable surface (e.g. a log message),
  say so in the commit rather than skipping silently.
- **Run `just test` before committing** any Rust change, alongside `just build`.

There is no CI, so these tests only run when you run them — treat `just test` as a
required local gate for generator changes.
