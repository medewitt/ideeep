---
title: "Note-Taking with Org Mode"
---

# Note-Taking with Org Mode

[Org mode](https://orgmode.org) is a plain-text outliner, task manager, and literate-programming environment built into [Emacs](https://www.gnu.org/software/emacs/).
For a researcher it doubles as a lab notebook: one `.org` file can hold your outline, to-dos, links, tables, and *runnable* code, then export to a PDF or slides — all in version-controllable plain text.

## Why plain-text notes

- Everything is a `.org` text file: greppable, diffable, and safe under [version control](version-control-git.md), with no proprietary lock-in.
- One format spans outlines, tasks, references, data tables, and analysis code, so your thinking and your work live together.
- It exports to HTML, LaTeX/PDF, Markdown, and Beamer slides, so the same notes become a report or a talk.

## Outlining

Structure is just headlines marked with asterisks; depth is the number of stars.

```org
* Project: spillover risk
** Background
** Analysis
*** Data cleaning
*** Model fit
** Meeting notes
```

Press `TAB` on a headline to fold or unfold its subtree, and `S-TAB` to cycle the whole document between overview, contents, and full detail.
`M-<up>`/`M-<down>` move a subtree, and `M-<left>`/`M-<right>` promote or demote it — so reorganizing a document is a few keystrokes, not cut-and-paste.

## Tasks, tags, and the agenda

Any headline becomes a task by giving it a keyword; `C-c C-t` cycles `TODO` → `DONE`.
Add `:tags:`, priorities, and timestamps to make notes actionable.

```org
** TODO Refit model with waning immunity :analysis:urgent:
   DEADLINE: <2026-07-10 Fri>
** DONE Send draft to co-authors
   CLOSED: [2026-07-02 Thu]
```

`C-c c` (org-capture) drops a quick note or task into an inbox from anywhere without losing your place, and `C-c a` (the agenda) collects deadlines and scheduled items across all your files into one calendar view.

## Links, tables, and citations

Link to a URL, a file, or another headline with `C-c C-l`; the syntax is `[[target][description]]`.
Tables are just text with `|` separators — press `TAB` and Org auto-aligns the columns, and it even supports spreadsheet-style formulas.

```org
See [[https://doi.org/10.1038/nature02104][Antia et al. 2003]] and [[file:notes.org::*Model fit][the model section]].

| strain    | R0  | note         |
|-----------+-----+--------------|
| wildtype  | 0.9 | subcritical  |
| mutant    | 1.5 | supercritical|
```

## Literate notebooks with Babel

Org's killer feature for analysis is **Babel**: embed source blocks in many languages, execute them in place with `C-c C-c`, and capture the results in the document.
This makes a `.org` file a language-agnostic, reproducible notebook (see [reproducibility](reproducibility.md)).

```org
#+begin_src R :results output
  set.seed(1)
  mean(rnorm(1000))
#+end_src
```

Because prose, code, and output share one file, you can weave a full analysis — much like R Markdown or Jupyter — and the same math notation you would use in [LaTeX](latex-and-documents.md) renders on export.

## Exporting

`C-c C-e` opens the export dispatcher: choose HTML, LaTeX → PDF, Markdown, or Beamer slides from the same source.
Your notes, a manuscript, and a talk can all come from one file, which keeps them in sync.

## A Zettelkasten with org-roam

For interlinked, atomic notes, [org-roam](https://www.orgroam.com) adds a lightweight Zettelkasten on top of Org: each note is a file, notes link to each other, and a backlinks buffer shows everything that points at the current note.
It is an excellent way to grow a personal knowledge base of papers, methods, and ideas over a whole program.

## Getting started

- With vanilla Emacs, Org is already included — open any `.org` file and start typing.
- The fastest fully-featured setup is [Doom Emacs](https://github.com/doomemacs/doomemacs): enable its `org` module (and `org-roam`) and you get sensible defaults plus Vim keybindings.
- Keep the [official manual](https://orgmode.org/manual/) and the community wiki, [Worg](https://orgmode.org/worg/), handy as references.

### A minimal cheat sheet

| Keys        | Action                                  |
|-------------|-----------------------------------------|
| `TAB`       | fold / unfold the current subtree       |
| `S-TAB`     | cycle global folding                    |
| `C-c C-t`   | cycle TODO state                        |
| `C-c C-l`   | insert or edit a link                   |
| `C-c c`     | capture a quick note or task            |
| `C-c a`     | open the agenda                         |
| `C-c C-c`   | execute a code block / act on context   |
| `C-c C-e`   | export dispatcher                       |

## Related

- [Good Programming Practices](good-programming-practices.md)
- [Reproducibility](reproducibility.md)
- [LaTeX and Technical Documents](latex-and-documents.md)
- [Project Workflow](project-workflow.md)
- [Version Control with Git](version-control-git.md)
- [Programming & Computing](../programming.md)
