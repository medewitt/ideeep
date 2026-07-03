---
title: "Hierarchical (Multilevel) Models"
---

# Hierarchical (Multilevel) Models

Real data are usually nested: patients within hospitals, cases within regions, measurements within individuals.
Hierarchical models estimate group-level quantities while letting each group borrow strength from all the others, striking a principled balance between lumping everyone together and treating every group in isolation.

![No-pooling estimates (noisy) shrink toward the overall mean under partial pooling; small groups shrink most.](../assets/figures/shrinkage.svg)

## Three ways to handle groups

Suppose you want the disease rate in each of $J$ small areas.
*Complete pooling* ignores the grouping and reports one overall rate for everyone, which is stable but hides real between-area differences.
*No pooling* fits a separate estimate to each area's data alone, which is unbiased but wildly noisy when some areas have only a handful of cases.
*Partial pooling* is the middle path: a multilevel model that estimates each area while assuming the area rates themselves come from a common distribution.

## Varying intercepts

The core device is to let a parameter vary by group and give those group-level values their own distribution.
A varying-intercept model writes the outcome for observation $i$ in group $j$ as \[ y_{ij} = \alpha_j + \varepsilon_{ij}, \qquad \alpha_j \sim \mathcal{N}(\mu, \tau^2), \qquad \varepsilon_{ij}\sim\mathcal{N}(0,\sigma^2). \] The group intercepts $\alpha_j$ are drawn from a [normal distribution](normal-distribution.md) with overall mean $\mu$ and between-group variance $\tau^2$, while $\sigma^2$ is the within-group [variance](measures-of-variability.md).
You can extend this to varying slopes, $y_{ij}=\alpha_j + \beta_j x_{ij} + \varepsilon_{ij}$, where the pair $(\alpha_j,\beta_j)$ is drawn from a shared bivariate distribution so that group-specific effects also pool toward a common trend.

## Shrinkage

The partial-pooling estimate for a group is a precision-weighted compromise between that group's own mean $\bar y_j$ and the overall mean $\mu$.
For a group with $n_j$ observations the estimate is \[ \hat\alpha_j = \mu + w_j\,(\bar y_j - \mu), \qquad w_j = \frac{\tau^2}{\tau^2 + \sigma^2/n_j}. \] The weight $w_j$ is the reliability of the group's data: when a group is large or between-group variation is big, $w_j\to 1$ and the estimate barely moves from its raw value.
When a group is small or noisy, $w_j$ is near zero and the estimate is pulled hard toward the overall mean.
This is *shrinkage*, and it is exactly why the small groups in the figure travel farthest.

## Connection to Bayesian inference

A hierarchical model is a [Bayesian](bayesian-inference.md) model in which the group-level distribution $\mathcal{N}(\mu,\tau^2)$ acts as a prior on the $\alpha_j$, and the data update it into a posterior for each group.
The shrinkage formula above is the posterior mean of $\alpha_j$ under that prior.
When the hyperparameters $\mu,\tau^2,\sigma^2$ are themselves estimated from the data (rather than fixed by hand) and then plugged in, the procedure is called *empirical Bayes*; the closely related James–Stein estimator shrinks several group means toward their grand mean and provably beats the raw means in total squared error.
Fully Bayesian versions place priors on the hyperparameters too and are typically fit with [MCMC](mcmc.md).

## Worked example: disease rates across small areas

Imagine measured rates in a dozen districts, where some districts contribute many cases and others only a few.
The no-pooling rates for the small districts swing far above and below the truth simply from sampling noise.
An empirical-Bayes fit estimates the between-district spread $\tau^2$, forms each $w_j$, and shrinks every raw rate toward the grand mean in proportion to how little data it rests on.
The result is a set of stabilized rates that are usually closer to the truth, especially for the sparse districts.

## In code

### R

```r
set.seed(1)
J <- 12
n <- sample(3:60, J, replace = TRUE)
true <- rnorm(J, 5, 1.6)
raw <- true + rnorm(J, 0, 3 / sqrt(n))   # no-pooling means

grand <- mean(raw)
tau2 <- var(raw)                          # between-group variance (rough)
w <- tau2 / (tau2 + (3^2) / n)            # shrinkage weights
shrunk <- grand + w * (raw - grand)       # partial-pooling estimates
data.frame(n, raw = round(raw, 2), shrunk = round(shrunk, 2))
```

### Python

```python
import numpy as np

rng = np.random.default_rng(1)
J = 12
n = rng.integers(3, 60, size=J)
true = rng.normal(5, 1.6, size=J)
sigma = 3.0
raw = true + rng.normal(0, sigma / np.sqrt(n))   # no-pooling means

grand = raw.mean()
tau2 = raw.var(ddof=1)                            # between-group variance
w = tau2 / (tau2 + sigma**2 / n)                  # shrinkage weights
shrunk = grand + w * (raw - grand)                # partial pooling

print(round(grand, 3))                            # grand mean ~4.7
for i in np.argsort(n)[:3]:                        # smallest groups shrink most
    print(n[i], round(raw[i], 2), round(shrunk[i], 2), round(w[i], 2))
# e.g.  4 8.03 5.28 0.19   (raw far out, shrunk pulled back hard)
```

<!-- python-output:auto -->
```text
5.038
4 6.99 5.85 0.42
11 6.79 6.2 0.66
17 4.1 4.33 0.75
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics
Random.seed!(1)
J = 12
n = rand(3:60, J)
true_a = 5 .+ 1.6 .* randn(J)
sigma = 3.0
raw = true_a .+ (sigma ./ sqrt.(n)) .* randn(J)

grand = mean(raw)
tau2 = var(raw)
w = tau2 ./ (tau2 .+ sigma^2 ./ n)
shrunk = grand .+ w .* (raw .- grand)   # partial-pooling estimates
```

## Why it matters

Multilevel models are the standard tool whenever data arrive in clusters, from small-area disease mapping to hospital performance comparisons to repeated measures on the same subject.
By shrinking unreliable estimates toward the group average, they avoid overreacting to noise in sparse groups while still surfacing genuine differences, giving more accurate and more honest group-level answers than either extreme of pooling.

## Related

- [Bayesian inference](bayesian-inference.md)
- [MCMC](mcmc.md)
- [Linear regression](linear-regression.md)
- [Generalized linear models](generalized-linear-models.md)
- [Maximum likelihood](maximum-likelihood.md)
- [Normal distribution](normal-distribution.md)
- [Measures of variability](measures-of-variability.md)
- [Expected value](expected-value.md)
- [Quantitative Methods](../math.md)
