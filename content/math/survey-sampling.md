---
title: "Survey Sampling"
---

# Survey Sampling

Surveys are how epidemiologists estimate [population](statistical-inference.md) quantities—prevalence, coverage, exposure—without measuring everyone.
The sampling design determines both how to draw the sample and how to weight it so estimates generalize to the target population.

## Common sampling designs

- **Simple random sampling (SRS)** — every unit has an equal [probability](probability-basics.md) of selection, and every subset of size $n$ is equally likely.
  The baseline against which other designs are compared.
- **Stratified sampling** — partition the population into strata (e.g., age groups, regions) and sample within each.
  Guarantees representation of every stratum and, when strata are internally homogeneous, lowers [variance](measures-of-variability.md).
- **Cluster sampling** — randomly select groups (clusters, e.g., clinics or villages) and survey units within them.
  Cheaper for dispersed populations but usually less efficient because units within a cluster are correlated.
- **Probability-proportional-to-size (PPS)** — select clusters with probability proportional to their size, so larger clusters are more likely to be chosen; combined with weighting this can yield efficient, self-weighting designs.

## Weighting and post-stratification

When selection probabilities differ, each sampled unit represents a different number of population units.
The **design weight** is the inverse of the selection probability, $w_i = 1/\pi_i$.
A weighted [mean](measures-of-center.md) estimates the population mean:

\[
\hat{\bar{Y}} = \frac{\sum_i w_i\,y_i}{\sum_i w_i}.
\]

**Post-stratification** further adjusts weights so the sample's margins (e.g., by age and sex) match known population totals, correcting for coverage and non-response imbalance.

### Missing data and imputation

Non-response leaves gaps.
Beyond weighting adjustments, **imputation** fills in missing values—single imputation (e.g., mean or regression) or, preferably, **multiple imputation**, which fills each gap several times to propagate the added uncertainty into standard errors.

## Worked conceptual example

Suppose a district has 800 urban and 200 rural residents (1000 total) and we take a stratified sample of 80 urban and 20 rural (a 10% sample in each stratum).
Selection probabilities are equal at $\pi_i = 0.1$, so weights are $w_i = 10$ for everyone—a **self-weighting** design in which the unweighted sample mean already estimates the population mean.
If instead we oversampled rural residents (say 40 of 200, $\pi=0.2$) for precision there, their weight would be $5$ versus $10$ for urban, and we would weight by $w_i$ to avoid over-representing rural values.

In R the `survey` package handles such designs directly: build a design object and call `svymean` for design-consistent estimates and standard errors.

## In code

Draw an SRS and a stratified sample.

### R

```r
set.seed(1)
pop <- data.frame(id = 1:1000,
                  stratum = rep(c("urban", "rural"), c(800, 200)),
                  y = c(rnorm(800, 10), rnorm(200, 12)))

# Simple random sample of 100
srs <- pop[sample(nrow(pop), 100), ]

# Stratified: 10% within each stratum
strat <- do.call(rbind, lapply(split(pop, pop$stratum),
                  function(d) d[sample(nrow(d), 0.1 * nrow(d)), ]))

# Design-based estimate with the survey package:
# library(survey)
# des <- svydesign(ids = ~1, strata = ~stratum, fpc = ~rep(...), data = strat)
# svymean(~y, des)
```

### Python

```python
import numpy as np, pandas as pd
rng = np.random.default_rng(1)
pop = pd.DataFrame({
    "stratum": ["urban"] * 800 + ["rural"] * 200,
    "y": np.concatenate([rng.normal(10, 1, 800), rng.normal(12, 1, 200)]),
})
srs = pop.sample(n=100, random_state=1)                       # SRS
strat = pop.groupby("stratum", group_keys=False).apply(       # stratified 10%
    lambda d: d.sample(frac=0.1, random_state=1))
print(srs["y"].mean(), strat["y"].mean())
```

<!-- python-output:auto -->
```text
10.34350267409585 10.312518620234567
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics
Random.seed!(1)
y = vcat(randn(800) .+ 10, randn(200) .+ 12)
stratum = vcat(fill("urban", 800), fill("rural", 200))

srs = y[randperm(1000)[1:100]]                       # SRS
urban = findall(==("urban"), stratum)
rural = findall(==("rural"), stratum)
strat = vcat(y[shuffle(urban)[1:80]], y[shuffle(rural)[1:20]])  # stratified 10%
println(mean(srs), " ", mean(strat))
```

## Why it matters for statistics

Ignoring the sampling design biases estimates and understates uncertainty: weights and stratification are not optional bookkeeping but part of the estimator.
Sound survey sampling is what lets a few hundred measurements speak validly for an entire population.

## Related

- [Experimental design](experimental-design.md)
- [Statistical inference](statistical-inference.md)
- [Sampling distributions](sampling-distributions.md)
- [Confidence intervals](confidence-intervals.md)
- [Quantitative Methods](../math.md)
