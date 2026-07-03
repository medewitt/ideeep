---
title: "The Molecular Clock and Phylodynamics"
---

# The Molecular Clock and Phylodynamics

Because mutations accumulate steadily over time, the number of genetic differences between two sequences acts like a ticking clock.
Reading that clock lets us date evolutionary events and, for pathogens, turn a set of sampled genomes into a timeline of an outbreak.

![Root-to-tip regression: the slope estimates the substitution rate and the x-intercept the tMRCA.](../assets/figures/molecular-clock-rtt.svg)

## Substitutions as a clock

If substitutions fix at an approximately constant rate $\mu$ per site per unit time, then over an interval $t$ the expected number of substitutions per site is $$\mathbb{E}[d] \approx \mu\, t.$$ Genetic distance therefore grows roughly linearly with elapsed time, and dividing an observed distance by the rate recovers the time.
The underlying process is well modeled as random arrivals of substitutions, so the *count* over an interval is approximately [Poisson](poisson-distribution.md) with mean $\mu t$ and the *waiting time* between substitutions is approximately [exponential](exponential-distribution.md); the linear relationship $\mathbb{E}[d]\approx\mu t$ is exactly the mean of that Poisson process.

## Strict vs. relaxed clocks

A **strict clock** assumes a single rate $\mu$ shared by every lineage, so all tips descending from a common ancestor have drifted apart by the same expected amount.
Real lineages violate this: generation times, replication machinery, and selective pressures differ, so rates vary across the tree.
A **relaxed clock** lets $\mu$ vary from branch to branch (drawn from a distribution, or correlated between neighboring branches), trading the strict clock's simplicity for realism.
Either way the clock must be **calibrated** to convert genetic distance into calendar time, and for fast-evolving pathogens the sampling dates of the sequences themselves supply that calibration.

## Root-to-tip regression

The simplest way to read and calibrate the clock is **root-to-tip regression**.
For each tip, measure its genetic distance from the root of the tree, then plot that distance against the tip's sampling date.
Under a clock the points fall on a line, $$d_i \approx \mu\,(\text{date}_i - t_{\text{MRCA}}),$$ and fitting it by least squares gives two quantities at once.
The **slope** estimates the substitution rate $\mu$ (substitutions per site per unit time), and the **x-intercept** — where root-to-tip distance is zero — estimates the date of the [most recent common ancestor](coalescent-theory.md), $t_{\text{MRCA}}$.
A good linear fit is also evidence of "temporal signal," a prerequisite for any molecular dating.

## Phylodynamics

The reach of the clock goes beyond dating single events.
A pathogen's genealogy is not shaped in isolation — it is molded by the epidemic that produced it, because who infects whom determines which lineages leave descendants.
**Phylodynamics** exploits this: since the shape of a reconstructed tree encodes the history of transmission, sequence data can estimate epidemiological quantities that are hard to observe directly, such as the trajectory of the effective population size and even the basic reproduction number $R_0$ of the [compartmental SIR model](sir.md).
A rapidly branching, star-like genealogy signals explosive early growth; a tree that stops branching signals an epidemic brought under control.
In this way a phylogeny estimated from genomes becomes a window onto transmission dynamics, complementing case counts with an independent evolutionary readout — and the per-site substitution rate it reveals connects directly to selection analyses like [$d_N/d_S$](dn-ds.md).

## Worked example

Suppose we sample five sequences of a fast-evolving virus and, from a rooted tree, record each tip's root-to-tip distance (substitutions per site):

| Sampling date (year) | Root-to-tip distance |
|---|---|
| 2018.0 | 0.0100 |
| 2019.0 | 0.0145 |
| 2020.0 | 0.0190 |
| 2021.0 | 0.0235 |
| 2022.0 | 0.0280 |

The distances rise by $0.0045$ per year, so the slope — the substitution rate — is $$\mu \approx 4.5\times10^{-3}\ \text{substitutions per site per year}.$$ Extrapolating the line back to zero distance solves $0 = \mu\,(t - t_{\text{MRCA}})$; running the fit gives an intercept at $$t_{\text{MRCA}} \approx 2018.0 - \frac{0.0100}{0.0045} \approx 2015.8.$$ So this clock estimates a common ancestor in late 2015 and a rate near $4.5\times10^{-3}$ per site per year, in the range seen for RNA viruses.

## In code

Each snippet fits the root-to-tip line and reports the slope (rate) and x-intercept ($t_{\text{MRCA}}$).

### R

```r
date <- c(2018, 2019, 2020, 2021, 2022)
dist <- c(0.0100, 0.0145, 0.0190, 0.0235, 0.0280)

fit <- lm(dist ~ date)
rate  <- coef(fit)[["date"]]                    # slope ~ 0.0045 subs/site/year
tmrca <- -coef(fit)[["(Intercept)"]] / rate     # x-intercept ~ 2015.8
c(rate = rate, tMRCA = tmrca)

# In practice: use ape to build/read the tree and get root-to-tip distances,
#   library(ape); dist <- node.depth.edgelength(tree)[tips]
```

### Python

```python
import numpy as np
from scipy.stats import linregress

date = np.array([2018, 2019, 2020, 2021, 2022])
dist = np.array([0.0100, 0.0145, 0.0190, 0.0235, 0.0280])

res = linregress(date, dist)
rate  = res.slope                 # ~ 0.0045 subs/site/year
tmrca = -res.intercept / rate     # ~ 2015.8
print(round(rate, 5), round(tmrca, 1))   # 0.0045 2015.8
```

<!-- python-output:auto -->
```text
0.0045 2015.8
```
<!-- /python-output:auto -->

### Julia

```julia
using GLM, DataFrames, Statistics

df = DataFrame(date = [2018, 2019, 2020, 2021, 2022],
               dist = [0.0100, 0.0145, 0.0190, 0.0235, 0.0280])

fit = lm(@formula(dist ~ date), df)
b0, rate = coef(fit)              # intercept, slope
tmrca = -b0 / rate                # x-intercept
println(round(rate, digits = 5), " ", round(tmrca, digits = 1))  # 0.0045 2015.8

# Manual least-squares check:
# rate = cov(df.date, df.dist) / var(df.date)
```

## Why it matters

The molecular clock lets genomes tell time: with only sampled sequences and their collection dates, root-to-tip regression estimates how fast a pathogen mutates and when its lineages last shared an ancestor.
Layering phylodynamics on top turns that same evolutionary signal into epidemiology — reconstructing when an outbreak began, how fast it grew, and what its reproduction number was — which is why genomic surveillance has become a front-line tool for tracking emerging infectious diseases.

## Related

- [Coalescent Theory](coalescent-theory.md)
- [Detecting Selection with dN/dS](dn-ds.md)
- [The Exponential Distribution](exponential-distribution.md)
- [The Poisson Distribution](poisson-distribution.md)
- [Compartmental Models in Biology](sir.md)
- [Quantitative Methods](../math.md)
