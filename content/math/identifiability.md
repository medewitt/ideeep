---
title: "Identifiability"
description: "When data cannot separate parameters, the likelihood has a flat ridge; structural and practical identifiability diagnose when estimates are meaningful."
---

# Identifiability

A parameter is identifiable when the data can, in principle, pin it down.
When two parameters only ever enter the model through their product or ratio, the data constrain that combination but not the parts, and the likelihood develops a flat ridge along which many parameter pairs fit equally well.
Recognizing this before you report an estimate saves you from trusting a number the data never determined.

![A Poisson model whose mean depends only on the product beta*N leaves the two parameters unidentified: the log-likelihood is flat along the hyperbola beta*N equals the sample mean.](../assets/figures/identifiability.svg)

## Structural vs practical identifiability

Two failures look similar but have different causes.

- **Structural non-identifiability** is a property of the model, independent of the data.
  If the likelihood satisfies $p(y\mid\theta_1)=p(y\mid\theta_2)$ for all $y$ at distinct $\theta_1\neq\theta_2$, no amount of data can separate them.
  The classic case is a mean that depends only on a product $\beta N$ or a ratio $\beta/\gamma$, so the individual factors are invisible.
- **Practical non-identifiability** is a property of the data at hand.
  The model is identifiable in principle, but the observations are too few, too noisy, or too weakly informative to constrain a direction, leaving a nearly flat ridge rather than an exactly flat one.

More data can cure the practical case but never the structural one.

## The signature: a ridge in the likelihood

Non-identifiability shows up as geometry.
Along the offending direction the log-likelihood is flat (structural) or nearly flat (practical), so the surface looks like a valley with a level floor rather than a single peak.
Any maximizer on that floor fits as well as any other, which is why an optimizer may return wildly different estimates from different starts while reporting the same fit.

The Bayesian view makes the same point through the posterior.
In a non-identified direction the likelihood contributes nothing, so the posterior in that direction simply returns the prior:

\[
p(\theta\mid y)\ \propto\ p(y\mid\theta)\,p(\theta)\ \xrightarrow[\text{flat likelihood}]{}\ p(\theta).
\]

If a marginal posterior looks identical to its prior, the data said nothing about that parameter.
A tight-looking joint posterior can still hide a long ridge, so inspect the correlations, not just the marginals.

## Profile likelihood as a diagnostic

The **profile likelihood** is the practical tool for finding a ridge.
For a parameter $\theta_1$ with the rest collected in $\theta_2$, profile out $\theta_2$ by maximizing over it at each fixed $\theta_1$:

\[
\ell_p(\theta_1)=\max_{\theta_2}\ \ell(\theta_1,\theta_2).
\]

A well-identified $\theta_1$ gives a profile with a clear peak that falls away on both sides; a non-identified $\theta_1$ gives a flat profile that never rises above its neighbors.
A profile that is flat over a whole range is the fingerprint of a ridge, and the width of a near-flat profile measures how weakly the data constrain the parameter.

## A worked example

Suppose case counts have mean $\beta N$, where $\beta$ is a per-contact transmission rate and $N$ is population size, modeled as $y_i\sim\text{Poisson}(\beta N)$.
Only the product enters the likelihood, so the maximum-likelihood surface is flat along every $(\beta, N)$ with $\beta N=\bar y$, the sample mean.
Pick $\beta=0.4,\ N=50$ or $\beta=0.1,\ N=200$ and the fit is identical, because both give $\beta N=20$.
Evaluating the log-likelihood along the ridge $\beta N=\bar y$ returns an essentially constant value, so the data identify the product $\beta N$ but neither factor alone.
To recover $\beta$ and $N$ separately you need extra information: an independent measurement of $N$, a prior, or an experiment that breaks the product.

## In code

Evaluate the log-likelihood on a $(\beta, N)$ grid and show that it is constant along the ridge $\beta N=\bar y$.

### R

```r
set.seed(1834)
beta_true <- 0.4; N_true <- 50
y <- rpois(30, beta_true * N_true)     # mean depends only on beta*N
s <- sum(y); n <- length(y); ybar <- mean(y)

loglik <- function(beta, N) {          # Poisson log-lik, dropping constant
  mu <- beta * N
  s * log(mu) - n * mu
}

betas <- seq(0.1, 1.0, length.out = 60)
ridge_ll <- sapply(betas, function(b) loglik(b, ybar / b))
cat("identified product ybar =", round(ybar, 2), "\n")
cat("log-lik range along ridge =",
    formatC(max(ridge_ll) - min(ridge_ll), format = "e", digits = 2), "\n")
```

### Python

```python
import numpy as np

rng = np.random.default_rng(1834)
beta_true, N_true = 0.4, 50.0
y = rng.poisson(beta_true * N_true, size=30)   # mean depends only on beta*N
s, n, ybar = y.sum(), len(y), y.mean()


def loglik(beta, N):                # Poisson log-lik, dropping constant
    mu = beta * N
    return s * np.log(mu) - n * mu


betas = np.linspace(0.1, 1.0, 60)
ridge_ll = np.array([loglik(b, ybar / b) for b in betas])
print(f"identified product ybar = {ybar:.2f}")
print(f"log-lik along ridge: min={ridge_ll.min():.4f}, "
      f"max={ridge_ll.max():.4f}, range={np.ptp(ridge_ll):.2e}")
```

<!-- python-output:auto -->
```text
identified product ybar = 18.97
log-lik along ridge: min=1105.3867, max=1105.3867, range=2.27e-13
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Distributions, Statistics
Random.seed!(1834)
beta_true, N_true = 0.4, 50.0
y = rand(Poisson(beta_true * N_true), 30)      # mean depends only on beta*N
s, n, ybar = sum(y), length(y), mean(y)

loglik(beta, N) = (mu = beta * N; s * log(mu) - n * mu)

betas = range(0.1, 1.0, length = 60)
ridge_ll = [loglik(b, ybar / b) for b in betas]
println("identified product ybar = ", round(ybar, digits=2))
println("log-lik range along ridge = ",
        maximum(ridge_ll) - minimum(ridge_ll))
```

## Why it matters

Transmission models are easy to over-parameterize, and identifiability is what separates a parameter you can report from one the data never touched.
A susceptibility and a contact rate that only appear as a product, or a rate and a reporting fraction that trade off, will look estimated when they are merely constrained as a combination.
Checking profiles and posteriors keeps you honest about which quantities the data determine, and it points to the design or prior information needed to break a ridge; the same weak directions are what a [global sensitivity analysis](sensitivity-analysis.md) surfaces as parameters the output barely responds to.

## Related

- [Maximum Likelihood Estimation](maximum-likelihood.md)
- [Fitting Dynamic Models to Data](model-calibration.md)
- [Global Sensitivity Analysis](sensitivity-analysis.md)
- [Bayesian Inference](bayesian-inference.md)
- [Prior Predictive Checks](prior-predictive-checks.md)
- [Quantitative Methods](../math.md)
