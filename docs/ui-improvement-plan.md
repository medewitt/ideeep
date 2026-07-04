# UI & Design Improvement Plan — IDEEEP Site

A staged plan to bring the IDEEEP site from a functional-but-dated look to a
polished, professional educational website — without disrupting the content
pipeline or the custom Rust generator.

The content is already a strength (a deep, well-organized library of
quantitative-methods and infectious-disease pages). The gap is entirely in the
**presentation layer**: legacy CSS, fragmented styling, a dated layout, and an
inaccessible navbar. This plan fixes that, lowest-risk changes first.

---

## Diagnosis — what's holding the look back

1. **The stylesheet is a repurposed early-2000s blog theme.** `assets/styles.css`
   is largely a Movable Type template. ~60% of it is dead code that renders on
   no page: `.calendar`, `.calendarhead`, `.trackback-*`, `.comments-*`,
   `#banner`, `#banner-commentspop`, `.syndicate`, `.powered`, `.sidetitle`,
   `.side`, `.blog`, `.date`, `.posted`, `.title`.

2. **Styling is fragmented across three sources of truth**, none aware of the
   others:
   - `assets/styles.css` (the legacy sheet),
   - an inline `<style>` block inside `generate_html()` (`src/main.rs`),
   - a third inline `<style>` string inside `generate_navbar()` (`src/main.rs`).
   Colors (`#8C6D2C` gold, `#003366` link blue, `#000` nav) and font stacks are
   hardcoded independently in all three. There is no design-token layer.

3. **A broken layout leftover.** `#content { margin-left: 225px; width: 75%; }`
   is an offset for a left sidebar that no longer exists, so the content column
   sits pushed to the right rather than in a centered, comfortable reading
   measure.

4. **Incoherent typography.** Body text is Arial; `h1` is Garamond; the base
   sheet specifies Garamond/Palatino/Verdana. Links are heavy, fully underlined
   `#003366`. There is no modular type scale and no max line-length for
   prose-dense pages.

5. **An inaccessible, non-responsive navbar.** Dropdowns are **hover-only** —
   they fail on touch devices, are not keyboard-navigable, and expose no ARIA
   state. On narrow screens the whole menu simply stacks (no disclosure /
   hamburger pattern). Dropdown parents don't reflect the active section.

6. **Render-blocking third-party CDNs.** Every page pulls Font Awesome (kit
   script) and highlight.js from Cloudflare, despite the project's
   vendored-assets philosophy (a `vendor/` directory already holds KaTeX and
   SQL.js). This hurts load time, privacy, offline builds, and resilience.

7. **Dead-weight and unoptimized assets.** A 2 MB `assets/tex-svg.js` (MathJax)
   ships even though math is pre-rendered server-side with KaTeX. The navbar
   loads a 500 KB `logo-wide.png` on every page, and a 230 KB PNG is used as the
   favicon.

8. **Accessibility gaps.** No skip-to-content link, weak/absent focus-visible
   styles, hover-only menus, and unverified color contrast.

9. **No dark mode** and no `prefers-color-scheme` support.

10. **Flat hub pages.** Section hubs are long, ungrouped bullet lists
    (`math.md` is ~200 links). There's strong grouping in the Markdown, but
    visually it reads as an undifferentiated wall with no "start here" cues or
    scannable structure. The homepage has no hero and no visual hierarchy.

---

## Guiding principles

- **One source of truth for design.** Move all CSS into `assets/` behind a small
  set of design tokens (CSS custom properties). The Rust generator should emit
  structure and class names, not inline style strings.
- **No visual regressions to content.** Markdown authoring, math, figures, and
  the search index stay exactly as they are. This is a chrome-and-CSS effort.
- **Self-hosted and fast.** Vendor every asset; drop CDNs; ship less.
- **Accessible by default.** Keyboard, focus, contrast, and semantics are
  requirements, not polish.
- **Incremental and low-risk.** Each phase is independently shippable and
  reviewable.

---

## Phase 0 — Foundation: design tokens & CSS consolidation (highest leverage)

Goal: a single, coherent styling layer that everything else builds on.

- **Introduce a design-token layer** at the top of `assets/styles.css` using CSS
  custom properties on `:root`:
  - Color: `--color-ink`, `--color-muted`, `--color-bg`, `--color-surface`,
    `--color-accent` (the `#8C6D2C` gold), `--color-link`, `--color-border`.
    Align the accent and any data-adjacent colors with the figure palette
    (`#2f6f9f`, `#c1531f`, `#3f8f5b`, `#8a5cb0`, `#b0842f`, ink `#26323f`) so the
    site chrome and the figures read as one system.
  - Spacing scale: `--space-1` … `--space-8` (a consistent 4/8px rhythm).
  - Type scale, radii, shadows, max content width, transitions.
- **Delete the dead blog CSS** (all classes listed in Diagnosis #1). Verify with
  a grep that no emitted HTML references them.
- **Consolidate the three style sources into `assets/styles.css`.** Move the
  inline `<style>` from `generate_html()` and the nav `<style>` from
  `generate_navbar()` into the stylesheet. Leave only a single `<link>` in the
  template. Payoff: **CSS becomes editable without recompiling the Rust binary**,
  and there's one place to reason about the cascade.
- **Fix the broken content offset:** replace `margin-left: 225px; width: 75%`
  with a centered column — `margin-inline: auto; max-width: 72ch` for prose
  (wider for pages with figures/tables), with fluid side padding.

_Risk: low. Deliverable: identical pages, cleaner and centered, one stylesheet._

---

## Phase 1 — Typography & reading experience

- **Adopt one coherent type system.** A refined serif for headings (keeps the
  academic character) paired with a highly legible sans or system-UI stack for
  body and UI. Self-host the chosen faces (`assets/fonts/`, `@font-face`,
  `font-display: swap`) — no Google Fonts CDN.
- **Establish a modular scale** for `h1–h4`, body, small, and captions; set
  `line-height` (~1.6 body), and constrain measure to ~66–72 characters.
- **Refine links:** accent color, underline offset, no permanent heavy
  underline on every link; clear `:hover`/`:focus-visible`.
- **Style long-form elements consistently:** lists, tables (zebra/hairline
  borders, aligned numerics), `blockquote` (already partly styled — fold into
  tokens), figure captions, and inline `code`.

---

## Phase 2 — Navigation & layout

- **Rebuild the navbar as a semantic, accessible component:**
  - Real `<nav aria-label>` with a `<ul>`; move all styling to CSS classes.
  - Replace hover-only dropdowns with **click/tap disclosure** buttons
    (`<button aria-expanded aria-controls>`), keyboard operable (Enter/Space/Esc,
    arrow keys optional), closing on outside-click and `Escape`.
  - Add a **mobile hamburger** toggle (small progressive-enhancement JS, or a
    CSS checkbox pattern) instead of a raw stacked list.
  - **Active-state accuracy:** highlight the dropdown parent when the current
    page lives inside it (the generator already knows `current_page` — thread
    the section relationship through `generate_navbar`).
  - Consider a **sticky header** with a subtle shadow on scroll.
- **Add a "Search" affordance** in the header (icon + field or a `/` shortcut)
  rather than only a nav item, since the search index already exists.
- **Global layout:** header / main / footer landmarks, generous vertical rhythm,
  and a consistent content container shared by all page types (including the
  search page, whose bespoke inline styles should fold into the system).

---

## Phase 3 — Components & page templates

- **Homepage hero.** Give `index.md` a proper hero: program name, one-line
  positioning, primary CTAs (Programs / Research / People), and the logo at an
  appropriate size — not a bare `h1` + blockquote.
- **Card grids for hubs.** Turn the flat link lists on section hubs
  (`math.md`, `programming.md`, `epidemiology.md`, `diagnostics.md`) into
  scannable grouped **cards** with a title + one-line description, preserving the
  existing `##` groupings as visual sections. Add lightweight "Start here" /
  "Foundations" emphasis. (Can be done with a CSS convention over the existing
  Markdown, or a small generator hook.)
- **Code blocks.** Replace the highlight.js default theme with a self-hosted,
  accessible theme matched to the palette; add language labels and a
  copy-to-clipboard button; ensure horizontal scroll containment.
- **Callouts / notes.** Formalize the `> Note:` blockquote pattern into styled
  callouts (note / warning / example) via a small convention.
- **Figures & tables.** Consistent max-width, centering, caption styling
  (already partially present for `/figures/`), and responsive overflow wrappers
  for wide tables.
- **People page** and other front-facing pages: give faculty entries a clean
  card/roster treatment.

---

## Phase 4 — Performance & self-hosting

- **Drop the CDNs.** Vendor Font Awesome (or replace with a handful of inline
  SVG icons — the site uses very few) and highlight.js into `assets/vendor/`,
  matching the existing KaTeX/SQL.js pattern. Removes render-blocking external
  requests.
- **Delete `assets/tex-svg.js` (2 MB MathJax).** Math is server-side KaTeX;
  confirm nothing references it, then remove — it should not be copied to
  `dist/`.
- **Optimize images.** Compress/resize `logo-wide.png` (500 KB) for nav use and
  generate a proper small favicon set (16/32/180 + SVG) instead of a 230 KB PNG.
  Serve an appropriately sized nav logo (SVG preferred — `ideep_logo.svg` exists).
- **Defer/inline critical CSS**, add `rel="preload"` for fonts, and lazy-load
  below-the-fold images.

---

## Phase 5 — Accessibility & dark mode

- **Skip-to-content link**, visible `:focus-visible` rings site-wide, logical
  heading order, and descriptive alt text discipline (AGENTS.md already treats
  alt text as captions — good).
- **Contrast audit** all text/background/link/accent pairings to WCAG AA.
- **Dark mode** via `prefers-color-scheme` using the token layer (swap a handful
  of custom properties). Optional manual toggle persisted in `localStorage`.
- Ensure KaTeX and code themes have dark variants.

---

## Phase 6 — Polish & metadata

- **SEO/social metadata** in `generate_html()`: per-page `<meta name="description">`
  (from front matter or first paragraph), Open Graph / Twitter card tags, and a
  default share image.
- **Favicon set** and web-app manifest.
- **Print styles** (hide nav/footer chrome, ensure code/math print legibly).
- **Redesign the `404.md` page** to match the new system with helpful links.
- **Consistent footer** aligned to the new tokens.

---

## Suggested sequencing

| Order | Phase | Effort | Risk | Why here |
|------:|-------|:------:|:----:|----------|
| 1 | Phase 0 — tokens + consolidation + layout fix | M | Low | Unblocks everything; immediate visible win (centered content) |
| 2 | Phase 1 — typography | S–M | Low | Biggest perceived "professionalism" jump per unit effort |
| 3 | Phase 4 — drop CDNs / trim assets | S | Low | Fast, measurable; independent of visual work |
| 4 | Phase 2 — nav & layout | M | Med | Structural; touches the generator |
| 5 | Phase 3 — components & templates | M–L | Med | Where the site starts to feel designed |
| 6 | Phase 5 — a11y & dark mode | M | Low | Rides on the token layer |
| 7 | Phase 6 — polish & metadata | S | Low | Finishing pass |

**Quick wins (could land in a first PR):** delete dead CSS, introduce tokens,
fix the `margin-left: 225px` content offset, unify fonts, drop the two CDNs, and
remove `tex-svg.js`. Together these noticeably lift the look with near-zero risk.

## Build & verification notes

- All changes are validated with the existing pipeline: `just build`
  (`cargo run --release` → `dist/`) and `just preview` (serves `dist/` on
  `:8000`). No new toolchain is introduced.
- Where a change moves CSS out of `src/main.rs`, re-run `just build` and diff the
  emitted HTML to confirm class names line up with the new stylesheet.
- Keep the one-sentence-per-line prose convention and `just lint-prose` intact;
  none of this touches content authoring.
