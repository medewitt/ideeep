---
title: "Common Distributions: An Overview"
---

# Common Distributions: An Overview

A handful of probability distributions describe a huge range of natural, epidemiological, and experimental data: coin-flip-like proportions, counts of rare events, waiting times between infections, and the bell-shaped noise that emerges whenever many small effects add up.
This page is a map to the five workhorse distributions and when each one arises.

## The five workhorses

- **[Normal](normal-distribution.md)** — continuous, symmetric bell curve.
  Arises whenever many small independent effects add up (heights, measurement error, sample means via the [central limit theorem](central-limit-theorem.md)).
- **[Binomial](binomial-distribution.md)** — discrete count of "successes" in $n$ independent yes/no trials.
  Arises in proportion testing (vaccinated vs. not, cured vs. not).
- **[Poisson](poisson-distribution.md)** — discrete count of rare events in a fixed window.
  Arises for case counts, mutations, or arrivals when events are independent and the rate is constant.
- **[Exponential](exponential-distribution.md)** — continuous waiting time until the next event.
  Arises for time between infections or the length of an infectious period; it is the memoryless partner of the Poisson.
- **[Student's t](t-distribution.md)** — continuous, bell-shaped but heavier-tailed than the normal.
  Arises for the standardized sample mean when the population $\sigma$ is estimated from data.

## Comparison table

| Distribution | Type | Support | Parameters | Mean | Variance | R sampler |
|---|---|---|---|---|---|---|
| Normal | Continuous | $x\in(-\infty,\infty)$ | $\mu,\ \sigma^2$ | $\mu$ | $\sigma^2$ | `rnorm(n, mean, sd)` |
| Binomial | Discrete | $k\in\{0,1,\dots,n\}$ | $n,\ p$ | $np$ | $np(1-p)$ | `rbinom(N, n, p)` |
| Poisson | Discrete | $k\in\{0,1,2,\dots\}$ | $\lambda>0$ | $\lambda$ | $\lambda$ | `rpois(n, lambda)` |
| Exponential | Continuous | $x\ge 0$ | rate $\lambda>0$ | $1/\lambda$ | $1/\lambda^2$ | `rexp(n, rate)` |
| Student's t | Continuous | $x\in(-\infty,\infty)$ | df $\nu>0$ | $0$ (for $\nu>1$) | $\frac{\nu}{\nu-2}$ (for $\nu>2$) | `rt(n, df)` |

## The R d/p/q/r naming convention

R names distribution functions by a **prefix + root**.
The root is the distribution (`norm`, `binom`, `pois`, `exp`, `t`), and the prefix picks the operation:

- `d*` — **d**ensity (pdf) or probability mass (pmf): $f(x)$.
- `p*` — cumulative **p**robability (cdf): $P(X\le x)$.
- `q*` — **q**uantile (inverse cdf): the $x$ with $P(X\le x)=p$.
- `r*` — **r**andom sampling: draw variates.

So `dnorm`, `pnorm`, `qnorm`, `rnorm` are the four faces of the normal distribution, and the same pattern holds for every distribution below.

## In code

### R

```r
set.seed(42)

# One sampler per distribution (r* prefix)
rnorm(3, mean = 0, sd = 1)   # Normal
rbinom(3, size = 10, prob = 0.3)  # Binomial
rpois(3, lambda = 4)         # Poisson
rexp(3, rate = 0.5)          # Exponential
rt(3, df = 5)                # Student's t

# d/p/q faces of the normal
dnorm(0)          # density at 0  -> 0.3989
pnorm(1.96)       # cdf at 1.96   -> 0.975
qnorm(0.975)      # quantile      -> 1.96
```

### Python

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)

rng.normal(0, 1, size=3)                 # Normal
rng.binomial(n=10, p=0.3, size=3)        # Binomial
rng.poisson(lam=4, size=3)               # Poisson
rng.exponential(scale=1/0.5, size=3)     # Exponential (scale = 1/rate)
stats.t.rvs(df=5, size=3, random_state=42)  # Student's t

stats.norm.pdf(0)      # density  -> 0.3989
stats.norm.cdf(1.96)   # cdf      -> 0.975
stats.norm.ppf(0.975)  # quantile -> 1.96
```

### Julia

```julia
using Distributions, Random
Random.seed!(42)

rand(Normal(0, 1), 3)      # Normal
rand(Binomial(10, 0.3), 3) # Binomial
rand(Poisson(4), 3)        # Poisson
rand(Exponential(2), 3)    # Exponential (scale = 1/rate = 2)
rand(TDist(5), 3)          # Student's t

pdf(Normal(0, 1), 0)       # density  -> 0.3989
cdf(Normal(0, 1), 1.96)    # cdf      -> 0.975
quantile(Normal(0, 1), 0.975)  # quantile -> 1.96
```

## Simulation

A quick check that samples converge to their theoretical means.
Averaging many Poisson($\lambda=4$) draws should land near $4$.

```r
set.seed(1)
mean(rpois(1e6, lambda = 4))  # ~ 4.00 (theoretical mean = lambda = 4)
var(rpois(1e6, lambda = 4))   # ~ 4.00 (Poisson: variance = mean)
```

As the sample size grows the empirical mean and variance both approach $\lambda$, exactly as the [law of large numbers](law-of-large-numbers.md) predicts.

## Why it matters for statistics

Every inferential method assumes a probability model for the data.
Choosing the right distribution — counts vs. proportions vs. continuous measurements — determines which [estimator](statistical-inference.md), test, and [confidence interval](confidence-intervals.md) are valid.
Recognizing the mechanism that generates each distribution (adding effects → normal, counting rare events → Poisson, waiting for events → exponential) lets you pick models from first principles rather than by trial and error.

## Related

- [Normal Distribution](normal-distribution.md)
- [Binomial Distribution](binomial-distribution.md)
- [Poisson Distribution](poisson-distribution.md)
- [Exponential Distribution](exponential-distribution.md)
- [t-Distribution](t-distribution.md)
- [Random Variables](random-variables.md)
- [Expected Value](expected-value.md)
- [Quantitative Methods](../math.md)
