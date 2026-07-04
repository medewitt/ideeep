---
title: "Posterior Predictive Checks"
description: "After fitting, draw replicated datasets from the posterior predictive and compare them to the observed data to expose model misfit."
---

# Posterior Predictive Checks

Once a model is fit, a posterior predictive check asks a simple question: could this model have produced the data we actually saw?
You answer it by drawing replicated datasets from the fitted model and comparing them, graphically and numerically, against the observations.
Systematic gaps between replicates and data point to features the model is missing.

![Replicate count distributions drawn from a fitted Poisson-gamma model are too tight; the observed variance sits far in the tail of the replicate reference distribution, giving a small posterior predictive p-value.](../assets/figures/posterior-predictive-checks.svg)

## The posterior predictive distribution

After conditioning on data $y$, the model predicts a new dataset $\tilde y$ by averaging the sampling distribution over the posterior instead of the prior:

\[
p(\tilde y\mid y)=\int p(\tilde y\mid\theta)\,p(\theta\mid y)\,d\theta.
\]

Sampling mirrors the [prior predictive check](prior-predictive-checks.md) but uses the posterior: draw $\theta^{(s)}\sim p(\theta\mid y)$, then $\tilde y^{(s)}\sim p(\tilde y\mid\theta^{(s)})$.
Each $\tilde y^{(s)}$ is a full replicate dataset the fitted model considers plausible.
Because the draws propagate posterior uncertainty, the replicates already account for what the data left unresolved about $\theta$.

## Graphical checks

The first look is visual: overlay summaries of the replicate datasets on the same summary of the observed data.
If the observed histogram, time series, or empirical distribution looks like one more draw from the replicate cloud, the model reproduces that feature; if it falls outside the cloud, it does not.
Density overlays expose the wrong shape, and plotting a residual against a covariate exposes structure the mean model omits.
Graphical checks are the most informative step because they show you *where* and *how* a model fails, not just *that* it fails.

## Posterior predictive p-values

To make a check quantitative, pick a **test statistic** $T(y)$ that targets a feature you care about, such as the sample variance, the number of zeros, or the maximum.
Compare the observed value $T(y)$ against the distribution of $T(\tilde y)$ across replicates through a **posterior predictive p-value**:

\[
p_B=\Pr\!\big(T(\tilde y)\ge T(y)\mid y\big)\approx\frac{1}{S}\sum_{s=1}^{S}\mathbf{1}\!\left\{T(\tilde y^{(s)})\ge T(y)\right\}.
\]

A value near $0$ or $1$ flags a systematic discrepancy: the model rarely generates data as extreme as observed in that statistic.
Values near $0.5$ mean the statistic is consistent with the model.

> [!NOTE]
> A posterior predictive p-value is a model check, not a hypothesis test.
> It reuses the data for fitting and checking, so it is conservative and its calibration is not that of a classical p-value; read it as a diagnostic, not a decision rule.

## What a discrepancy tells you

A failed check names the missing ingredient.
Excess zeros beyond what the replicates produce suggest a zero-inflation or reporting process the model ignores.
Observed variance far above the replicate variance is the signature of **overdispersion**: a Poisson mean-variance link that is too rigid, usually cured by a negative-binomial or a random effect.
A misfit in the tail maximum points to heavy tails; a misfit in an autocorrelation statistic points to unmodeled dependence.
The check turns "the model is wrong" into a specific, fixable claim.

## A worked example

Take $40$ counts that are genuinely overdispersed, generated from a negative-binomial process, and fit them with a Poisson model using a conjugate $\text{Gamma}(1,1)$ prior on the rate.
The [Gamma-Poisson](bayesian-inference.md) update gives a $\text{Gamma}(1+\sum y_i,\ 1+n)$ posterior, from which we draw rates and simulate replicate datasets.
Choose the sample variance as the test statistic, since a Poisson forces the variance to equal the mean.
The observed variance lands far above almost every replicate variance, so the posterior predictive p-value is close to $0$, correctly rejecting the Poisson assumption in favor of an overdispersed alternative.
Counting zeros tells the same story more mildly.

## In code

Conjugate update, posterior predictive replicates, and posterior predictive p-values for two test statistics.

### R

```r
set.seed(1834)
y <- rnbinom(40, size = 2, prob = 2 / 5)   # overdispersed counts
n <- length(y); s <- sum(y)

# Poisson-gamma: Gamma(1,1) prior -> Gamma(1+s, 1+n)
a_post <- 1 + s; b_post <- 1 + n
M <- 4000
lam <- rgamma(M, a_post, b_post)
y_rep <- matrix(rpois(M * n, rep(lam, each = n)), nrow = M, byrow = TRUE)

ppc_p <- function(Tfun) {
  t_obs <- Tfun(y)
  t_rep <- apply(y_rep, 1, Tfun)
  mean(t_rep >= t_obs)
}
cat("variance ppc-p :", round(ppc_p(var), 3), "\n")
cat("num-zeros ppc-p:", round(ppc_p(function(d) sum(d == 0)), 3), "\n")
```

### Python

```python
import numpy as np

rng = np.random.default_rng(1834)
y = rng.negative_binomial(2, 2 / 5, size=40)   # overdispersed counts
n, s = len(y), y.sum()

# Poisson-gamma: Gamma(1,1) prior -> Gamma(1+s, 1+n)
a_post, b_post = 1.0 + s, 1.0 + n
M = 4000
lam = rng.gamma(a_post, 1.0 / b_post, M)
y_rep = rng.poisson(lam[:, None], size=(M, n))

stats = {
    "variance": lambda d: d.var(axis=-1),
    "num zeros": lambda d: (d == 0).sum(axis=-1),
}
for name, T in stats.items():
    t_obs, t_rep = T(y), T(y_rep)
    p = np.mean(t_rep >= t_obs)
    print(f"{name}: observed={t_obs:.2f}, "
          f"replicate mean={t_rep.mean():.2f}, ppc-p={p:.3f}")
```

<!-- python-output:auto -->
```text
variance: observed=11.48, replicate mean=2.74, ppc-p=0.000
num zeros: observed=9.00, replicate mean=2.52, ppc-p=0.003
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Distributions, Statistics
Random.seed!(1834)
y = rand(NegativeBinomial(2, 2 / 5), 40)     # overdispersed counts
n, s = length(y), sum(y)

# Poisson-gamma: Gamma(1,1) prior -> Gamma(1+s, 1+n)
a_post, b_post = 1 + s, 1 + n
M = 4000
lam = rand(Gamma(a_post, 1 / b_post), M)
y_rep = [rand(Poisson(l), n) for l in lam]

function ppc_p(Tfun)
    t_obs = Tfun(y)
    t_rep = Tfun.(y_rep)
    mean(t_rep .>= t_obs)
end
println("variance ppc-p : ", round(ppc_p(var), digits=3))
println("num-zeros ppc-p: ", round(ppc_p(d -> count(==(0), d)), digits=3))
```

## Why it matters

Posterior predictive checks are how you find out whether a fitted model is fit for purpose before you trust its forecasts or estimates.
For infectious-disease models they catch the failures that matter operationally, from unmodeled overdispersion in case counts to missed reporting delays and wrong tail behavior.
They connect naturally to [proper scoring rules](proper-scoring-rules.md), which grade predictive distributions on held-out data, and to the [prior predictive check](prior-predictive-checks.md) that guards the same model before it ever sees data.

## Related

- [Bayesian Inference](bayesian-inference.md)
- [Markov Chain Monte Carlo](mcmc.md)
- [Proper Scoring Rules](proper-scoring-rules.md)
- [Prior Predictive Checks](prior-predictive-checks.md)
- [Quantitative Methods](../math.md)
