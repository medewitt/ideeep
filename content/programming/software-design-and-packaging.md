---
title: "Software Design & Packaging"
---

# Software Design & Packaging

Most scientific code starts as one long script that grows until nobody — including its author six months later — can safely change it.
A little **software design** keeps code understandable and reusable as it grows, and **packaging** turns a pile of useful functions into a tool your whole lab can install, test, and cite.

You do not need to become a software engineer.
A handful of principles — small functions, clear interfaces, and knowing when to make a package — carry almost all the benefit.

## The Progression: Script → Function → Package

Analysis code matures along a predictable path:

1. **A script** — top-to-bottom code for one analysis.
   Fine for a one-off.
2. **Functions** — repeated or logically distinct steps pulled into named functions.
3. **A module** — related functions grouped into a file you can reuse across scripts.
4. **A package** — that module bundled with documentation, tests, and dependency information so others (and future you) can install and rely on it.

![On the left, one 600-line script mixes data cleaning, modelling, plotting, and copy-pasted helpers; on the right it is refactored into a package of small single-purpose functions with tests and docs, called by a short 20-line analysis script.](../assets/figures/package-anatomy.svg)

The payoff of moving right is concrete: the tangled script can't be reused or tested, while the package's functions are each small, testable, and shared — and the analysis script shrinks to a readable few lines that just call them.

## Modularity: Small Functions, One Job Each

The core design principle is **separation of concerns**: keep data cleaning, modelling, and plotting in separate functions rather than interleaved in one block.
Each function should do **one thing**, have a name that says what, and be short enough to read at a glance — the same advice as [Good Programming Practices](good-programming-practices.md), now applied at the scale of a whole project.

Modularity pays off because you can test, fix, reuse, and reason about one piece without holding the entire program in your head.
And **don't repeat yourself (DRY)**: when you catch yourself copy-pasting a block, that is the signal to make it a function.

## Interfaces: A Function Is a Contract

A function's **interface** — its name, its arguments, and what it returns — is a **contract** with whoever calls it (including future you).
Callers depend on the interface, not the internals, which means you can rewrite the guts for speed or correctness without breaking anything downstream, as long as the contract holds.
Good functions are **pure** where possible (output depends only on inputs, no hidden global state), and they **validate their inputs** rather than silently returning nonsense.

```python
def attack_rate(cases, population):
    """Fraction of a population that became cases, in [0, 1]."""
    if population <= 0:
        raise ValueError("population must be positive")
    return cases / population

# the contract, exercised like a miniature test
print("attack_rate(30, 200) =", attack_rate(30, 200))
print("zero cases          =", attack_rate(0, 200))
try:
    attack_rate(5, 0)
except ValueError as e:
    print("rejects bad input   =", e)
```

<!-- python-output:auto -->
```text
attack_rate(30, 200) = 0.15
zero cases          = 0.0
rejects bad input   = population must be positive
```
<!-- /python-output:auto -->

Document that contract where the code lives — a **docstring** (Python/Julia) or **roxygen** comment (R) — so the function is usable from its help page alone, without reading its source.

## When to Make a Package

Turn your functions into a real package when any of these is true:

- You **reuse** the same helpers across more than one project.
- You want to **share** them with collaborators or the wider field.
- You want **tests** and **versioning** to travel with the code.
- You want to **publish and be cited** (CRAN, PyPI, a Julia registry, or a Zenodo DOI).

Even a private "lab package" of your group's standard functions is worth it — it is how you stop emailing `utils.R` around.
A package has a standard skeleton:

| | R | Python | Julia |
|---|-----|--------|-------|
| Metadata | `DESCRIPTION` | `pyproject.toml` | `Project.toml` |
| Code | `R/` | `src/pkg/` | `src/` |
| Tests | `tests/` | `tests/` | `test/` |
| Docs | `man/`, vignettes | docstrings, Sphinx | docstrings, Documenter |
| Scaffolding tool | `usethis`, `devtools` | `hatch`, `poetry` | `PkgTemplates.jl` |

```r
# R: scaffold, document, and test a package with usethis + devtools
usethis::create_package("mypkg")
usethis::use_r("attack_rate")      # create R/attack_rate.R
usethis::use_test("attack_rate")   # create tests/testthat/test-attack_rate.R
devtools::document(); devtools::check()
```

```bash
# Python: a modern package is just a pyproject.toml + a src/ layout
mypkg/
├── pyproject.toml
├── src/mypkg/__init__.py
└── tests/test_attack_rate.py
```

## Dependencies, Versions, and the Rest

A package also pins down what it **needs to run**, which is where design meets [reproducibility](reproducibility.md):

- **Declare your dependencies** (in `DESCRIPTION` / `pyproject.toml` / `Project.toml`) so an install brings them along.
- **Version your package** with semantic versioning — `MAJOR.MINOR.PATCH`, where a breaking change bumps MAJOR — so users know when an update might break their code.
- **Ship tests** ([testing](testing-scientific-code.md)) and keep it in [version control](version-control-git.md); a package without tests is a liability the first time you change it.

## A Short Checklist

- **Refactor repeated or distinct steps into small, single-purpose functions.**
- **Separate concerns** — cleaning, modelling, plotting — and keep the analysis script thin.
- **Design clear interfaces**, validate inputs, prefer pure functions, and document the contract.
- **Make a package** once code is reused, shared, or worth testing and versioning.
- **Declare dependencies and version** with semver; ship tests under version control.

## Related

- [Good Programming Practices](good-programming-practices.md) — the function-level habits this builds on
- [Testing & Verification for Scientific Code](testing-scientific-code.md) — the tests a package should ship with
- [Version Control with Git & GitHub](version-control-git.md) — where package source lives
- [Reproducibility](reproducibility.md) — declared dependencies and pinned versions
- [Project Workflow](project-workflow.md) — organizing the project a package grows out of
- [Programming & Computing](../programming.md)
