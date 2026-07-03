---
title: "Markov Chain Monte Carlo"
---

# Markov Chain Monte Carlo

Many posteriors have no closed form, so we cannot write down their mean or quantiles directly.
Markov chain Monte Carlo (MCMC) sidesteps this by drawing samples from the target distribution and summarizing them.

![Metropolis–Hastings: the chain's trace (left) and the sampled histogram matching the target density (right).](../assets/figures/mcmc.svg)

## The idea

The goal of [Bayesian inference](bayesian-inference.md) is to learn a posterior $p(\theta\mid y)$, but for most models the normalizing constant is an intractable integral.
MCMC builds a Markov chain — a sequence $\theta^{(1)},\theta^{(2)},\dots$ where each state depends only on the previous one — whose **stationary distribution** is exactly the target $p(\theta\mid y)$.
Run the chain long enough and its states behave like (correlated) draws from the posterior, so sample averages estimate posterior [expectations](expected-value.md).
Crucially, the chain only needs the target up to a constant, so the unknown normalizer never has to be computed.

## Metropolis–Hastings

The **Metropolis–Hastings** algorithm turns any proposal mechanism into a valid sampler.
From the current state $\theta$, propose $\theta'$ from a proposal density $q(\theta'\mid\theta)$ and accept it with probability

\[
\alpha=\min\!\left(1,\ \frac{p(\theta')\,q(\theta\mid\theta')}{p(\theta)\,q(\theta'\mid\theta)}\right),
\]

where $p(\cdot)$ is the (unnormalized) target.
If the proposal is rejected, the chain stays at $\theta$.
With a symmetric proposal such as a [Normal](normal-distribution.md) random walk, $q(\theta\mid\theta')=q(\theta'\mid\theta)$ and the ratio reduces to $\min(1,\,p(\theta')/p(\theta))$: always move to higher density, and sometimes move downhill.

**Gibbs sampling** is a special case for multi-parameter models: cycle through the parameters, drawing each from its full conditional distribution given the current values of the others, accepting every draw.

## Diagnostics

Because samples are correlated and the chain starts away from the target, we check convergence and mixing before trusting the output.

- **Trace plots.** Plot each parameter against iteration; a well-mixed chain looks like a stationary "fuzzy caterpillar" with no drift.
- **Burn-in / warm-up.** Discard early iterations before the chain reaches the target region.
- **Thinning.** Optionally keep every $m$-th draw to reduce storage and autocorrelation (though it discards information).
- **Potential scale reduction factor $\hat R$.** Run several chains from different starts; $\hat R$ compares within-chain to between-chain variance and should be near $1.0$ (values above ~1.01 signal non-convergence).
- **Effective sample size.** Autocorrelation means $N$ draws carry the information of fewer independent ones; the effective sample size quantifies how many.

Modern samplers reduce random-walk inefficiency by using gradient information: **Hamiltonian Monte Carlo** and its adaptive variant **NUTS** power Stan, PyMC, and Turing.jl.

## Worked example: sampling a Poisson rate

Suppose we observe counts $y=(2,3,1,4,2)$ and model them as Poisson with rate $\lambda$, using a $\text{Gamma}(2,1)$ prior.
This case is actually conjugate — the posterior is $\text{Gamma}\big(2+\sum y_i,\ 1+n\big)=\text{Gamma}(14,\,6)$ with mean $14/6\approx 2.33$ — which lets us check the sampler against the truth.
We run a random-walk Metropolis sampler on $\log\lambda$ (so proposals stay positive) targeting the unnormalized posterior $p(\lambda)\propto \lambda^{\sum y_i}e^{-n\lambda}\cdot\lambda^{1}e^{-\lambda}$.
After discarding burn-in, the sample mean should land near $2.33$ and a 95% interval near the analytic $\text{Gamma}(14,6)$ quantiles $[1.28,\,3.72]$.

## In code

A Metropolis sampler from scratch, with the analytic answer for comparison.

### R

```r
set.seed(1)
y <- c(2, 3, 1, 4, 2); n <- length(y)
# Unnormalized log-posterior for lambda > 0 (Gamma(2,1) prior, Poisson likelihood)
log_post <- function(lam) {
  if (lam <= 0) return(-Inf)
  sum(dpois(y, lam, log = TRUE)) + dgamma(lam, 2, 1, log = TRUE)
}

N <- 20000; lam <- 1; draws <- numeric(N)
for (i in 1:N) {
  prop <- lam * exp(rnorm(1, 0, 0.3))          # random walk on log scale
  logA <- log_post(prop) - log_post(lam) + log(prop) - log(lam)  # + Jacobian
  if (log(runif(1)) < logA) lam <- prop
  draws[i] <- lam
}
draws <- draws[-(1:2000)]                       # burn-in
c(mean = mean(draws), quantile(draws, c(0.025, 0.975)))
# mean ~2.33, ~[1.28, 3.72]; analytic: Gamma(14, 6)
qgamma(c(0.025, 0.975), 14, 6)                  # 1.28 3.72
# plot(draws, type = "l"); hist(draws)          # trace + histogram
```

### Python

```python
import numpy as np
from scipy.stats import poisson, gamma

np.random.seed(1)
y = np.array([2, 3, 1, 4, 2]); n = len(y)

def log_post(lam):
    if lam <= 0:
        return -np.inf
    return poisson.logpmf(y, lam).sum() + gamma.logpdf(lam, 2, scale=1)

N, lam = 20000, 1.0
draws = np.empty(N)
for i in range(N):
    prop = lam * np.exp(np.random.normal(0, 0.3))       # random walk on log scale
    logA = log_post(prop) - log_post(lam) + np.log(prop) - np.log(lam)
    if np.log(np.random.rand()) < logA:
        lam = prop
    draws[i] = lam
draws = draws[2000:]                                    # burn-in
print(draws.mean(), np.quantile(draws, [0.025, 0.975]))
# ~2.33  [~1.28, ~3.72]
print(gamma.ppf([0.025, 0.975], 14, scale=1/6))         # analytic: 1.28 3.72
```

### Julia

```julia
using Distributions, Random, Statistics
Random.seed!(1)
y = [2, 3, 1, 4, 2]; n = length(y)
log_post(lam) = lam <= 0 ? -Inf :
    sum(logpdf.(Poisson(lam), y)) + logpdf(Gamma(2, 1), lam)

N, lam = 20000, 1.0
draws = zeros(N)
for i in 1:N
    prop = lam * exp(0.3 * randn())                     # random walk on log scale
    logA = log_post(prop) - log_post(lam) + log(prop) - log(lam)
    if log(rand()) < logA
        lam = prop
    end
    draws[i] = lam
end
draws = draws[2001:end]                                 # burn-in
println(mean(draws), " ", quantile(draws, [0.025, 0.975]))
# ~2.33  [~1.28, ~3.72]
println(quantile(Gamma(14, 1/6), [0.025, 0.975]))       # 1.28 3.72
```

In practice you would reach for a probabilistic-programming system — Stan, PyMC, or Turing.jl — which implements NUTS, adapts the proposal, and reports $\hat R$ and effective sample size automatically.
See the [simulation toolkit](../programming/simulation-toolkit.md) for sampler tooling and [reproducibility](../programming/reproducibility.md) for seeding and archiving runs.

## Why it matters

MCMC made Bayesian inference practical for realistic models by replacing intractable integrals with samples.
It is the computational backbone behind fitting hierarchical models, transmission models, and phylogenies, wherever the posterior cannot be written in closed form.
Understanding its diagnostics is what separates a trustworthy fit from a chain that merely looks busy.

## Related

- [Bayesian Inference](bayesian-inference.md)
- [Markov Chains](markov-chains.md)
- [Probability Basics](probability-basics.md)
- [Normal Distribution](normal-distribution.md)
- [Simulation Toolkit](../programming/simulation-toolkit.md)
- [Reproducibility](../programming/reproducibility.md)
- [Quantitative Methods](../math.md)
