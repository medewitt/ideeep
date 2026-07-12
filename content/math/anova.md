---
title: "Analysis of Variance"
description: "How ANOVA splits total variation into between-group and within-group parts, and turns their ratio into the F-test."
---

# Analysis of Variance

Analysis of variance answers a deceptively simple question: are these groups really different, or is the spread between their averages just the noise you would expect within any one group?
The trick is to compare two kinds of variation — how far the group means sit from the grand mean, versus how much individuals scatter around their own group mean — and read off their ratio.
It is the analytical engine underneath almost every designed experiment on this site, from [factorial](factorial-designs.md) and [Latin square](latin-square-designs.md) layouts to [split-plot](split-plot-designs.md) and [crossover](crossover-designs.md) trials.

![Three treatment groups plotted as points, with each group mean marked against the grand mean. The between-group signal is how far the coloured group means sit from the dashed grand mean; the within-group noise is the scatter of points around their own group mean. ANOVA asks whether the first is large relative to the second.](../assets/figures/anova.svg "fig:anova")

## Partitioning the variation

Take $k$ groups with $n_i$ observations each, $N = \sum_i n_i$ in total.
Write $y_{ij}$ for observation $j$ in group $i$, $\bar{y}_i$ for the group mean, and $\bar{y}$ for the grand mean.
The total spread of every point around the grand mean splits **exactly** into a between-group part and a within-group part:

\[
\underbrace{\sum_{i}\sum_{j} (y_{ij} - \bar{y})^2}_{\text{SST}}
= \underbrace{\sum_{i} n_i (\bar{y}_i - \bar{y})^2}_{\text{SSB}}
+ \underbrace{\sum_{i}\sum_{j} (y_{ij} - \bar{y}_i)^2}_{\text{SSW}}.
\label{eq:ss-decomp}
\]

The cross-term vanishes because deviations around each group mean sum to zero, so [@eq:ss-decomp] holds identically — no approximation.
**SSB** (between) measures the treatment signal; **SSW** (within) measures the residual noise.

## From sums of squares to the F-ratio

Each sum of squares carries a number of degrees of freedom: $k-1$ for between, $N-k$ for within.
Dividing gives **mean squares**, which are variances:

\[
\text{MSB} = \frac{\text{SSB}}{k-1}, \qquad \text{MSW} = \frac{\text{SSW}}{N-k}.
\]

If every group has the same mean, both estimate the same error variance $\sigma^2$ and their ratio hovers near one.
If the groups genuinely differ, SSB inflates and the ratio grows:

\[
F = \frac{\text{MSB}}{\text{MSW}}.
\]

Under the null hypothesis of equal means (with independent, roughly normal errors of constant variance), $F$ follows an $F_{k-1,\,N-k}$ distribution, which is what turns the ratio into a [p-value](p-values.md).

## A worked example

Three antibiotic regimens are each tried on four bacterial cultures; the response is log-reduction in colony count.

| Regimen | Values | Mean |
|---------|--------|------|
| A | 8, 9, 7, 8 | 8 |
| B | 10, 11, 12, 11 | 11 |
| C | 9, 8, 10, 9 | 9 |

The grand mean is $\bar{y} = 112/12 = 9.33$.
The between-group sum of squares is

\[
\text{SSB} = 4\big[(8-9.33)^2 + (11-9.33)^2 + (9-9.33)^2\big] = 18.67,
\]

and, adding the squared deviations inside each group ($2+2+2$),

\[
\text{SSW} = 6.
\]

With $k-1 = 2$ and $N-k = 9$ degrees of freedom, $\text{MSB} = 9.33$ and $\text{MSW} = 0.67$, so

\[
F = \frac{9.33}{0.67} = 14.0.
\]

Against the $F_{2,9}$ reference (5% critical value $\approx 4.26$) this is far into the tail — the regimens differ ([@fig:anova-effects]).

![The variance partition and the test. Left: SSB and SSW stack to SST, and dividing by their degrees of freedom gives the mean squares whose ratio is F. Right: the F(2,9) reference density with the 5% critical value at 4.26 and the observed F of 14.0 far into the upper tail.](../assets/figures/anova-effects.svg "fig:anova-effects")

## In code

### R

```r
d <- data.frame(
  y = c(8, 9, 7, 8, 10, 11, 12, 11, 9, 8, 10, 9),
  g = rep(c("A", "B", "C"), each = 4)
)
summary(aov(y ~ g, data = d))
#             Df Sum Sq Mean Sq F value  Pr(>F)
# g            2  18.67   9.333    14.0 0.00171 **
# Residuals    9   6.00   0.667
```

### Python

```python
import numpy as np
from scipy import stats

groups = {
    "A": [8, 9, 7, 8],
    "B": [10, 11, 12, 11],
    "C": [9, 8, 10, 9],
}
y = np.array([v for vs in groups.values() for v in vs], float)
grand = y.mean()
ssb = sum(len(v) * (np.mean(v) - grand) ** 2 for v in groups.values())
ssw = sum(((np.array(v) - np.mean(v)) ** 2).sum() for v in groups.values())
k, N = len(groups), y.size
F = (ssb / (k - 1)) / (ssw / (N - k))
p = stats.f.sf(F, k - 1, N - k)
print(f"SSB={ssb:.2f} SSW={ssw:.2f} F={F:.2f} p={p:.4f}")
```

<!-- python-output:auto -->
```text
SSB=18.67 SSW=6.00 F=14.00 p=0.0017
```
<!-- /python-output:auto -->

### Julia

```julia
using Statistics, Distributions
groups = Dict("A"=>[8,9,7,8], "B"=>[10,11,12,11], "C"=>[9,8,10,9])
y = reduce(vcat, values(groups))
grand = mean(y)
ssb = sum(length(v) * (mean(v) - grand)^2 for v in values(groups))
ssw = sum(sum((v .- mean(v)).^2) for v in values(groups))
k, N = length(groups), length(y)
F = (ssb / (k - 1)) / (ssw / (N - k))
p = ccdf(FDist(k - 1, N - k), F)
println("F=$(round(F, digits=2)) p=$(round(p, digits=4))")
```

## Why it matters for statistics

ANOVA is the bridge between experimental design and inference: the way a study is *blocked, crossed, or nested* determines exactly how the total variation is carved up, and each design in this section is really a different recipe for the sum-of-squares partition.
A [Latin square](latin-square-designs.md) peels off two blocking directions before testing treatments; a [split-plot](split-plot-designs.md) design produces two error strata, so the whole-plot and sub-plot factors are tested against different denominators; a [repeated-measures](repeated-measures.md) analysis pulls out a subject term to sharpen within-subject comparisons.
Understanding the partition is what lets you build the right $F$-test — and spot when a naïve one uses the wrong error term.

## Related

- [Split-Plot Designs](split-plot-designs.md)
- [Repeated Measures Designs](repeated-measures.md)
- [Latin Square Designs](latin-square-designs.md)
- [Balanced Incomplete Block Designs](balanced-incomplete-block-designs.md)
- [Factorial Designs](factorial-designs.md)
- [Experimental Design](experimental-design.md)
- [Hypothesis Testing](hypothesis-testing.md)
- [Linear Regression](linear-regression.md)
- [Quantitative Methods](../math.md)
