# Writing for IDEEEP — an author's guide

This is the practical guide to **writing content** for the IDEEEP site: how to
lay out a page, and how to use every authoring feature (math, figures,
equations, callouts, spoilers, code that runs itself, reusable fragments, and
cross-references).

It is the companion to [`AGENTS.md`](AGENTS.md) — that file explains how the
generator is *built*; this file explains how to *write* for it. If you only read
one, read this one.

> [!NOTE]
> The site is a custom Rust static-site generator. You write plain Markdown in
> `content/`; a build (`just build`) turns each `content/…/page.md` into
> `dist/…/page.html`. You never register a page anywhere — dropping a `.md` file
> into `content/` is enough to compile it.

---

## 1. Where things live

```
content/            your Markdown pages (this is where you write)
  math/             Quantitative Methods pages
  programming/      Programming & Computing pages
  epidemiology/     Epidemiology pages
  diagnostics/      Diagnostics & Surveillance pages
  _fragments/       reusable snippets (NOT published on their own)
  <section>.md      section "hub" pages that link to the pages in <section>/
figures/            PEP-723 Python scripts -> assets/figures/*.svg
assets/             styles, fonts, images, generated figures
config.yaml         navbar order and dropdown menus
```

A new page under `content/math/` is reachable two ways, and you normally set up
both: link to it from the section **hub** (`content/math.md`) and, if it should
appear in the top navigation, add it in `config.yaml`. A page that is linked
from nowhere still builds and works by direct URL.

---

## 2. Page skeleton

Every page starts with YAML **front matter** (between `---` lines), then an H1,
then content. Copy this shape:

```markdown
---
title: "Epidemic Growth Rates"
description: "How the early exponential growth rate r relates to R0 and the generation interval."
---

# Epidemic Growth Rates

Two or three sentences of motivation — the intuition, the "why", before any
formalism.

![An epidemic curve rising exponentially then bending over as susceptibles deplete.](../assets/figures/epidemic-curve.svg)

## The idea
Prose and math.

## A worked example
Concrete numbers.

## In code
### R
### Python
### Julia

## Why it matters
Tie back to infectious-disease ecology / epidemiology.

## Related
- [A sibling page](sibling.md)
- [Quantitative Methods](../math.md)   <!-- link back to the hub last -->
```

### Front-matter fields

| Field | Required | What it does |
|-------|----------|--------------|
| `title` | **yes** | Page title; feeds the `<title>`, social cards, breadcrumbs. |
| `description` | no | One-sentence summary for search results and social cards. If omitted, the build derives one from your first paragraph — so **write a strong first sentence**. |
| `toc` | no | `true` adds an auto "On this page" list built from your `##`/`###` headings. Good for long or hub pages. Off by default. |
| `image` | no | A site-root-relative image for social/share cards, e.g. `assets/photos/serology.jpg`. Defaults to the shared site card. |
| `image_alt` | no | Alt text for that share image (falls back to the title). |
| `sort_schedule` | no | `true` sorts every table with a `Day`/`Time` column by weekday then start time. For agendas. |
| `hidden` | no | `true` makes the page **unlisted**: it still renders at its URL, but is kept out of search, the sitemap, and search engines. For drafts and share-by-link pages. |

> [!WARNING]
> `hidden: true` is *unlisted*, not *private* — anyone with the URL can read it.
> There is no access control at the page level.

### Prose convention: one sentence per line

Write prose **one sentence per line** (semantic line breaks). This never changes
the rendered page (Markdown joins single newlines with a space) — it just keeps
diffs clean. Checked by `just lint-prose`; auto-fix with `just fmt-prose`.

---

## 3. Math

Inline and display math are rendered at build time by **KaTeX** (no runtime
JavaScript, no MathJax).

| You write | You get |
|-----------|---------|
| `$R_0 = \beta/\gamma$` | inline math |
| `\( R_0 = \beta/\gamma \)` | inline math (alternative) |
| `\[ \frac{dS}{dt} = -\beta S I \]` | centered display math |
| `$$ \frac{dS}{dt} = -\beta S I $$` | centered display math (alternative) |

Use conventional notation (`\theta`, `\frac`, `\mathbb{E}[\cdot]`, `\propto`). A
malformed expression shows up as a red `math-error` span rather than breaking the
page, so it is easy to spot in preview.

### Numbering and referencing equations

Display equations are **not** numbered by default (most are derivation steps you
never cite). To number one, give it a `\label{eq:name}` **inside** the display
math. It then prints a right-aligned `(N)` and becomes referenceable:

```markdown
The infected compartment grows by mass-action transmission and decays by
recovery, equation [@eq:sir-i]:

\[ \frac{dI}{dt} = \beta S I - \gamma I \label{eq:sir-i} \]

Setting [@eq:sir-i] to zero at the peak gives the herd-immunity threshold.
```

- **Numbering is opt-in and per page.** Only labelled equations get a number, and
  they count `1, 2, 3…` in the order they appear — an unlabelled equation in
  between does not consume a number.
- **Reference with `[@eq:name]`** anywhere in the prose. It renders as a link
  reading `(N)` that jumps to the equation. The reference may appear *before or
  after* the equation.
- Labels must start with `eq:` (that prefix is how references find them).
- An unresolved `[@eq:typo]` renders a **loud marker**, so a broken reference is
  caught in review rather than silently vanishing.
- Labels are for single display equations; keep them out of multi-line `aligned`
  environments.

---

## 4. Figures and images

Insert an image with standard Markdown. **The alt text doubles as the caption**,
so write it as a real caption:

```markdown
![A pairwise invasibility plot with the singular strategy where the invasion boundary crosses the diagonal.](../assets/figures/adaptive-dynamics.svg)
```

Any image that sits alone in its own paragraph is automatically wrapped in a
numbered `<figure>`:

> **Figure 1.** A pairwise invasibility plot with the singular strategy …

- **Numbering is automatic and per page** — Figure 1, Figure 2, … in document
  order. You do nothing.
- **Path convention:** a nested page (`content/math/page.md`) references figures
  as `../assets/figures/name.svg`; a top-level page uses `assets/figures/name.svg`.
- **A decorative image** (one you don't want numbered) gets an **empty alt** —
  `![](../assets/divider.svg)` — and is left as a plain image.

### Numbering and referencing figures

To cite a figure by number, **label it** by giving the image a title that starts
with `fig:` (the quoted string after the path), then reference it with
`[@fig:name]`:

```markdown
![Susceptible depletion bends the curve over.](../assets/figures/curve.svg "fig:curve")

As [@fig:curve] shows, incidence peaks well before susceptibles are exhausted.
```

`[@fig:curve]` renders as a link reading `Figure N` (resolved in either order),
and the `fig:` title is stripped from the image so it never shows as a tooltip.
An unresolved `[@fig:typo]` renders a loud marker.

> [!TIP]
> References are uniform: `[@fig:name]` for figures, `[@eq:name]` for equations.
> Only the *labelling* differs — figures are labelled with an image title
> (`"fig:name"`), equations with `\label{eq:name}` inside the math.

### Where figures come from

Figures are **static SVGs** in `assets/figures/`, each generated by a
self-contained PEP-723 Python script in `figures/<name>.py` (matplotlib only,
shared house style). Build them with `just figures`; the committed SVG means the
site build itself never needs Python. See the **Figures** section of `AGENTS.md`
for the script template and palette.

---

## 5. Callouts (asides)

Use GitHub-style admonition blockquotes; the build renders them as styled boxes
with an icon.

```markdown
> [!TIP]
> Seed your RNG so simulations are reproducible.

> [!WARNING]
> This approximation breaks down once depletion is non-negligible.
```

Supported types: `[!NOTE]`, `[!TIP]`, `[!WARNING]`, `[!EXAMPLE]` (and
`[!IMPORTANT]` ≈ note, `[!CAUTION]` ≈ warning). Inline math, code, links, and
bold all work inside a callout. A plain `>` blockquote with no `[!TYPE]` is still
an ordinary quote.

---

## 6. Spoilers / disclosure blocks

Hide a worked solution, a long derivation, or an aside behind a click. It
compiles to a native `<details>` widget (no JavaScript), and the body is
**ordinary Markdown** — lists, math, code, even nested spoilers:

```markdown
:::spoiler Show the solution
Set the derivative to zero and solve for $I^\*$:

\[ \beta S I - \gamma I = 0 \;\Rightarrow\; S^\* = \gamma/\beta \]

- step one
- step two
:::
```

- The text after the keyword is the **clickable summary, and it is entirely up to
  you** — `:::spoiler Show the solution`, `:::spoiler Reveal the derivation`,
  `:::spoiler Hint`, whatever fits. A bare `:::spoiler` reads "Show more".
- `:::details` is an alias for `:::spoiler` — identical behavior, pick whichever
  reads better.
- The opener sits on its own line; the block ends at a line that is just `:::`.
  Keep both markers on their own line. The prose linter (`just fmt-prose`) knows
  about spoiler fences and will not merge them into your text, so you can run it
  freely; a blank line around the markers is optional.
- Blocks may **nest**.

---

## 7. Code — and running it

Fenced code blocks are syntax-highlighted (light/dark aware). The page skeleton
shows the same idea in three languages under `### R`, `### Python`, `### Julia`.
Every fenced block automatically gets a **language badge and a Copy button** — no
authoring change needed; just tag the fence with its language (` ```r `,
` ```python `, ` ```julia `) so the badge and highlighting are right.

### Python that executes itself

` ```python ` blocks are **actually run** at build time by
`just python-output`, and their real stdout is injected beneath the block (idempotently):

````markdown
```python
import numpy as np
rng = np.random.default_rng(0)      # seed everything — output is committed
print(rng.binomial(10, 0.3, size=5))
```
````

Rules that keep this reproducible:

- Blocks on a page share **one namespace, top to bottom** (later blocks see
  earlier variables).
- **Seed every RNG** (and pin any library randomness). The output is committed to
  the repo, so it must be deterministic.
- Keep output **small** (capped at ~15 lines) and blocks **fast**.
- Allowed libraries are a fixed set: `numpy, scipy, sympy, pandas, polars,
  statsmodels, networkx, matplotlib, scikit-learn, numpyro, jax, torch, mapie`.
  **Prefer Polars over pandas** in new examples. `torch` runs the CPU build; pretrained-weight
  downloads (torchvision models, YOLO) are blocked, so keep those `# no-run` and only
  run from-scratch models. Have deep-learning blocks print stable, converged numbers
  (accuracies, rounded losses) rather than exact floats, which can differ by version.
- Add `# no-run` as the first line to skip execution. Plot-only blocks inject
  nothing.
- **R and Julia blocks are never executed** — they are illustrative, so they may
  use any package.

Run `just python-output` after editing Python, and commit the injected output
(and the cache file it updates) alongside your change.

---

## 8. Reusable fragments

Content that is **identical across many pages** (shared course policies, a
standard notice) lives once in `content/_fragments/` and is pulled in with an
include shortcode on its own line:

```markdown
:::{course-policies.md}:::
```

- The `.md` is optional (`:::{course-policies}:::` also works).
- Edit the fragment once; every page that includes it updates on the next build.
- Includes may nest. A missing fragment renders a loud marker (never silent).
- Option after a `;`: `:::{fellow-schedule; schedule=true}:::` sorts the
  fragment's schedule tables by day/time as it is spliced in.
- Files in `content/_fragments/` are **never** published as pages of their own.

---

## 9. Links and cross-references

- **Link to another page** with a relative `.md` link — it is rewritten to
  `.html` at build: `[study designs](../epidemiology/study-designs.md)`.
- **Link within a page**: every `##`/`###` heading gets a stable id and a `#`
  permalink (revealed on hover). Link to a section with `[jump](#the-slug)`,
  where the slug is the lower-cased, hyphenated heading text.
- **Cite a figure or equation** with `[@fig:name]` / `[@eq:name]` (see above).
- **"Referenced by" is automatic.** Every page shows, at its foot, the list of
  other pages that link to it — a reverse index built from your `.md` links. You
  do nothing; just link pages together (especially the `## Related` list and the
  hub) and the backlinks appear. This is what makes the site read like an
  interlinked wiki, so link generously.
- There is **no bibliography system** — cite papers as inline Markdown links.

---

## 10. The glossary

The site keeps a central list of key terms in **`content/_glossary.yaml`**. You
don't mark terms up in your prose — **the build auto-links the first mention of
each term on every page**, with a hover/focus definition tooltip, and generates
a `/glossary.html` page whose entries list every page that discusses the term
(a reverse index).

**To add a term, edit that one file:**

```yaml
- term: Serial interval
  aliases: [serial intervals]        # other forms that should also link
  short: The time from symptom onset in a case to onset in the people they infect.
  see: epidemiology/epidemiological-intervals.md   # optional canonical page
```

- `term` + `short` are required; `aliases`, `long` (a fuller Markdown
  definition for the glossary page), and `see` are optional.
- Matching is **case-insensitive and whole-word**, and only the **first**
  occurrence on a page is linked (so a page isn't peppered with links).
- Terms inside **code, math, links, and headings are never linked** — only real
  prose.
- Keep aliases **specific**: a very common word would link on nearly every page.
- A page can **opt out** of auto-linking with `glossary: false` in its front
  matter.
- Adding a term makes it live everywhere on the next build — no per-page edits.
- Run `just glossary-check` to catch a term you defined but never used, or a
  `see:` that points nowhere.

---

## 11. Tables and lists

- Standard GFM tables work. A table with `Day`/`Time` columns can be
  auto-sorted (`sort_schedule: true` in front matter, or `; schedule=true` on a
  fragment include).
- A flat list of **4+ items that are all links** is automatically flowed into
  responsive columns — handy for hub-page link lists.

---

## 12. Build & preview

```
just preview          # build + serve on http://localhost:8000  (use this while writing)
just build            # build to dist/
just figures          # (re)render figures/*.py -> assets/figures/*.svg
just python-output     # run ```python blocks and inject their output
just lint-prose        # one-sentence-per-line check
```

Before you commit new content, run `just figures` (if you added/edited a
figure), `just python-output` (if you added/edited a Python block),
`just lint-prose`, and `just build`, and eyeball the page in `just preview`:
figures rendering, math correct, internal links resolving, and the page showing
up under the right navbar section.

---

## Quick reference

| I want to… | I write… |
|------------|----------|
| Inline math | `$R_0$` |
| Display math | `\[ … \]` or `$$ … $$` |
| Number an equation | `\[ … \label{eq:name} \]` |
| Reference an equation | `[@eq:name]` → `(N)` |
| A figure with caption | `![caption text](../assets/figures/x.svg)` |
| Label a figure | `![caption](x.svg "fig:name")` |
| Reference a figure | `[@fig:name]` → `Figure N` |
| An aside | `> [!NOTE]` / `[!TIP]` / `[!WARNING]` / `[!EXAMPLE]` |
| A collapsible block | `:::spoiler Your label` … `:::` |
| Reuse shared content | `:::{fragment-name}:::` |
| Link to another page | `[text](../section/page.md)` |
| Link to a section | `[text](#heading-slug)` |
| Run Python and show output | a ` ```python ` block (seed your RNG) |
| Define a glossary term | add it to `content/_glossary.yaml` (auto-links everywhere) |
| Hide a draft page | `hidden: true` in front matter |
