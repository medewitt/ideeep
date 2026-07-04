---
title: "Prior Predictive Checks"
description: "Simulate observable data from the prior before seeing the real data to check that priors imply scientifically plausible observations."
---

# Prior Predictive Checks

A prior predictive check pushes the prior through the model to simulate the data you might observe, before looking at the real data.
The point is to ask whether the priors, together with the likelihood, imply observations that a domain expert would call plausible.
Priors that look harmless on a parameter scale can imply absurd data, and this check catches that early.

![A vague Normal prior on a logit-scale intercept implies a U-shaped prior on prevalence, piling mass at 0 and 1; a tighter prior implies a plausible spread.](../assets/figures/prior-predictive-checks.svg)

## The prior predictive distribution

Before any data arrive, the model already makes predictions.
Averaging the sampling distribution over the prior gives the **prior predictive distribution** of a hypothetical observation $\tilde y$:

\[
p(\tilde y)=\int p(\tilde y\mid\theta)\,p(\theta)\,d\theta.
\]

You sample from it in two steps: draw a parameter $\theta^{(s)}\sim p(\theta)$ from the prior, then draw data $\tilde y^{(s)}\sim p(\tilde y\mid\theta^{(s)})$ from the likelihood.
The collection $\{\tilde y^{(s)}\}$ is a sample of datasets the model considers possible a priori.
If those datasets look nothing like anything the science permits, the prior is telling you something before the data do.

## Vague on one scale is not vague on another

Priors are usually written on a convenient scale, often a link scale such as logit or log, because that is where the model is linear.
A wide prior there need not be wide on the scale you actually care about.

Take a logit-scale intercept $\alpha\sim\text{Normal}(0,\sigma)$ with implied prevalence $p=\mathrm{logit}^{-1}(\alpha)$.
A "weakly informative" choice like $\sigma=10$ feels flat, but $\mathrm{logit}^{-1}$ saturates: almost every draw of $\alpha$ lands where $p$ is essentially $0$ or $1$.
The implied prior on $p$ is U-shaped, asserting that a disease is either absent or universal and almost never in between.
A tighter $\sigma=1.5$ spreads $p$ across the unit interval and keeps most mass in a plausible range.
The same reversal happens with a $\log$ link, where a vague Normal prior on a log-rate implies a heavy-tailed prior that can place substantial mass on impossibly large rates.

> [!WARNING]
> A flat prior on a coefficient is not a flat prior on the outcome.
> Nonlinear links, such as $\mathrm{logit}^{-1}$ or $\exp$, reshape the prior, so always inspect it on the scale of the observable.

## Iterating toward a sensible prior

The check is a loop, not a verdict.
Simulate from the prior predictive, compare the implied observations against what the science allows, and if they are implausible, tighten or reshape the prior and repeat.
The target is not a prior that already knows the answer, but one whose predictions cover the plausible range without wasting mass on the impossible.
Doing this before fitting also keeps the check honest, because you are not tuning the prior to the very data you will condition on later.

## A worked example

Model a positive fraction with a logit-scale intercept $\alpha$ and $n=50$ trials, so $y\sim\text{Binomial}(50,\ \mathrm{logit}^{-1}(\alpha))$.
Compare a vague prior $\alpha\sim\text{Normal}(0,10)$ against a sensible $\alpha\sim\text{Normal}(0,1.5)$.
Under the vague prior the implied prevalence sits below $0.02$ or above $0.98$ roughly three-quarters of the time, and the simulated counts are almost always $0$ or $50$.
Under the sensible prior the prevalence spreads across the unit interval with a median near $0.5$, and the counts range over believable values.
Same likelihood, same nominal "weak" prior on a coefficient, very different claims about the data.

## In code

Draw from the prior, push through the likelihood, and summarize the implied observable for each prior.

### R

```r
set.seed(1834)
inv_logit <- function(x) 1 / (1 + exp(-x))
n_draws <- 20000; n_trials <- 50

prior_pred <- function(sigma) {
  alpha <- rnorm(n_draws, 0, sigma)   # prior on the logit scale
  p <- inv_logit(alpha)               # implied prevalence
  y <- rbinom(n_draws, n_trials, p)   # simulated observable
  list(p = p, y = y)
}

for (s in c(10, 1.5)) {
  pp <- prior_pred(s)
  q <- quantile(pp$p, c(0.05, 0.5, 0.95))
  extreme <- mean(pp$p < 0.02 | pp$p > 0.98)
  cat(sprintf("sigma=%.1f  p 5/50/95%%=%.3f/%.3f/%.3f  extreme=%.2f\n",
              s, q[1], q[2], q[3], extreme))
}
```

### Python

```python
import numpy as np
from scipy.special import expit

rng = np.random.default_rng(1834)
n_draws, n_trials = 20000, 50


def prior_pred(sigma):
    alpha = rng.normal(0.0, sigma, n_draws)   # prior on the logit scale
    p = expit(alpha)                          # implied prevalence
    y = rng.binomial(n_trials, p)             # simulated observable
    return p, y


for label, sigma in [("vague  sd=10", 10.0), ("sensible sd=1.5", 1.5)]:
    p, y = prior_pred(sigma)
    q = np.quantile(p, [0.05, 0.5, 0.95])
    extreme = np.mean((p < 0.02) | (p > 0.98))
    print(f"{label}: p 5/50/95% = {q[0]:.3f}/{q[1]:.3f}/{q[2]:.3f}, "
          f"frac extreme = {extreme:.2f}")
```

<!-- python-output:auto -->
```text
vague  sd=10: p 5/50/95% = 0.000/0.461/1.000, frac extreme = 0.69
sensible sd=1.5: p 5/50/95% = 0.076/0.495/0.924, frac extreme = 0.01
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Distributions, Statistics
Random.seed!(1834)
inv_logit(x) = 1 / (1 + exp(-x))
n_draws, n_trials = 20000, 50

function prior_pred(sigma)
    alpha = rand(Normal(0, sigma), n_draws)      # prior on the logit scale
    p = inv_logit.(alpha)                        # implied prevalence
    y = rand.(Binomial.(n_trials, p))            # simulated observable
    return p, y
end

for sigma in (10.0, 1.5)
    p, y = prior_pred(sigma)
    q = quantile(p, [0.05, 0.5, 0.95])
    extreme = mean((p .< 0.02) .| (p .> 0.98))
    println("sigma=$sigma  p 5/50/95%=", round.(q, digits=3),
            "  extreme=", round(extreme, digits=2))
end
```

## Why it matters

In epidemiology the observable scale is where domain knowledge lives: a prevalence, an attack rate, a doubling time, a case count.
Checking the prior predictive keeps those quantities in a range experts recognize and stops a "vague" prior from smuggling in extreme assumptions that then distort the posterior.
It pairs naturally with its after-the-fact counterpart, the [posterior predictive check](posterior-predictive-checks.md), and with [identifiability](identifiability.md) analysis, since a sensible prior can regularize directions the data barely constrain.

## Related

- [Bayesian Inference](bayesian-inference.md)
- [Markov Chain Monte Carlo](mcmc.md)
- [Posterior Predictive Checks](posterior-predictive-checks.md)
- [Identifiability](identifiability.md)
- [Fitting Dynamic Models to Data](model-calibration.md)
- [Quantitative Methods](../math.md)
