---
title: "Direct, Indirect, Total, and Overall Vaccine Effects"
description: "Why vaccinating one person changes another's risk: dependent happenings, the Halloran-Struchiner decomposition into direct, indirect, total, and overall effects, and the study designs needed to measure each."
---

# Direct, Indirect, Total, and Overall Vaccine Effects

Vaccines do something no ordinary drug does: protecting one person changes the risk faced by everyone around them.
A vaccinated person who does not get infected also does not transmit, so unvaccinated bystanders are protected too.
This **dependent happening** — one person's outcome depends on others' — means a single "vaccine effect" is not enough, and the [test-negative estimate of individual protection](vaccine-effectiveness.md) captures only part of a program's benefit.
Halloran and Struchiner formalized the rest into four distinct effects, each answering a different question and each needing a different comparison.

![A bar chart of attack rates in unvaccinated people with no program, unvaccinated people within a program, vaccinated people within a program, and the whole program community, with brackets marking the direct, indirect, total, and overall effect contrasts.](../assets/figures/vaccine-effects-direct-indirect.svg)

## Dependent happenings

In non-infectious epidemiology, one person's outcome is independent of another's, and a single relative risk summarizes an intervention.
Infection breaks that independence: whether you are infected depends on whether the people you contact are infected, which depends on whether *they* are vaccinated.
Ronald Ross called these **dependent happenings**, and they are why a vaccine's population benefit exceeds the sum of its individual protections — the extra piece is the transmission it prevents, the same herd effect that produces a [herd immunity threshold](../math/final-size-and-herd-immunity.md).
Measuring it requires comparing not just vaccinated to unvaccinated people, but populations with a program to populations without one.

## The four effects

The Halloran-Struchiner framework (Halloran and Struchiner 1991) reads four effects off comparisons of attack rates across two kinds of contrast: individuals within a community, and whole communities against each other.

**Direct effect** — vaccinated versus unvaccinated *within the same program community*.
This is individual protection holding the transmission environment fixed, and it is what a randomized efficacy trial or a test-negative study estimates.

**Indirect effect** — unvaccinated people *in a program community* versus unvaccinated people *in a comparison community with no program*.
Both groups are unvaccinated, so any difference is pure herd protection: the benefit of living among vaccinated others.

**Total effect** — vaccinated people *in a program community* versus unvaccinated people *in a no-program community*.
This combines direct and indirect protection and is the most relevant number for an individual deciding whether to be vaccinated in a setting where others are too.

**Overall effect** — the *whole* program community, vaccinated and unvaccinated together, versus the *whole* comparison community.
This is the population-level effectiveness of the program as a policy, the quantity that matters for deciding whether to run the program at all.

## The comparisons in the figure

The figure lays out the attack rates the four effects are built from.
Unvaccinated people with no program sit highest.
Unvaccinated people inside a program are lower — that drop is the **indirect** effect.
Vaccinated people inside a program are lower still; the step down from their unvaccinated neighbors is the **direct** effect, and the full drop from the no-program reference is the **total** effect.
The whole program community's average against the no-program reference is the **overall** effect.
Because these effects can diverge — a program with modest direct efficacy can have a large overall effect if it interrupts transmission — reporting only one of them can badly misstate a vaccine's value.

## Study designs

The effects dictate the design.
Direct effects come from **individually randomized** trials or observational designs within one population.
Indirect, total, and overall effects require variation in *program coverage across communities*, so they are estimated by **cluster-randomized trials** that randomize whole communities to a program or not, or by stepped-wedge and observational community comparisons.
This is why vaccine programs are increasingly evaluated at the cluster level: only a design with unvaccinated-but-exposed and no-program comparison groups can see the herd effects that individual trials are blind to.

## A worked example

From attack rates in the four groups, we compute each effect as a relative reduction in risk.

## In code

### R

```r
ar_unvax_noprog <- 90     # attack rate per 1000, unvaccinated, no program
ar_unvax_prog   <- 55     # unvaccinated, within program (indirectly protected)
ar_vax_prog     <- 20     # vaccinated, within program
ar_whole_prog   <- 32     # whole program community average

direct   <- 1 - ar_vax_prog   / ar_unvax_prog
indirect <- 1 - ar_unvax_prog / ar_unvax_noprog
total    <- 1 - ar_vax_prog   / ar_unvax_noprog
overall  <- 1 - ar_whole_prog / ar_unvax_noprog

round(c(direct = direct, indirect = indirect,
        total = total, overall = overall), 3)
```

### Python

```python
ar_unvax_noprog = 90   # attack rate per 1000, unvaccinated, no program
ar_unvax_prog = 55     # unvaccinated, within program (indirectly protected)
ar_vax_prog = 20       # vaccinated, within program
ar_whole_prog = 32     # whole program community average

direct = 1 - ar_vax_prog / ar_unvax_prog
indirect = 1 - ar_unvax_prog / ar_unvax_noprog
total = 1 - ar_vax_prog / ar_unvax_noprog
overall = 1 - ar_whole_prog / ar_unvax_noprog

print(f"direct effect   = {direct:.1%}")
print(f"indirect effect = {indirect:.1%}")
print(f"total effect    = {total:.1%}")
print(f"overall effect  = {overall:.1%}")
```

<!-- python-output:auto -->
```text
direct effect   = 63.6%
indirect effect = 38.9%
total effect    = 77.8%
overall effect  = 64.4%
```
<!-- /python-output:auto -->

### Julia

```julia
ar_unvax_noprog = 90   # attack rate per 1000, unvaccinated, no program
ar_unvax_prog   = 55   # unvaccinated, within program (indirectly protected)
ar_vax_prog     = 20   # vaccinated, within program
ar_whole_prog   = 32   # whole program community average

direct   = 1 - ar_vax_prog   / ar_unvax_prog
indirect = 1 - ar_unvax_prog / ar_unvax_noprog
total    = 1 - ar_vax_prog   / ar_unvax_noprog
overall  = 1 - ar_whole_prog / ar_unvax_noprog

(direct = direct, indirect = indirect, total = total, overall = overall)
```

The direct effect understates the program: the total protection an individual gets, and the overall benefit to the community, are both larger because vaccination also suppresses transmission.

## Why it matters

Quoting a vaccine's direct efficacy alone hides the part of its value that comes from interrupting transmission, which for a program is often the larger part.
The four-effect decomposition keeps the questions separate — how well it protects the vaccinated, how much it shelters everyone else, and what the program does to a whole community — and makes clear that answering the herd-effect questions demands community-randomized designs, not individual ones.
It is the study-design consequence of the same dependent happenings that give epidemics their [threshold behavior](../math/final-size-and-herd-immunity.md).

## Related

- [Vaccine Effectiveness and the Test-Negative Design](vaccine-effectiveness.md) — estimating the direct effect
- [Epidemiologic Study Designs](study-designs.md) — cluster-randomized and community designs
- [Measures of Association and Impact](measures-of-association-and-impact.md) — attack rates and relative reductions
- [Final Size, Herd Immunity, and Overshoot](../math/final-size-and-herd-immunity.md) — the herd effect these designs measure
- [Causal Inference](../math/causal-inference.md) — interference and dependent happenings
