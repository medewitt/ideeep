---
title: "The Poisson Distribution"
---

# The Poisson Distribution

The Poisson distribution models the number of rare, [independent](probability-basics.md) events that occur in a fixed interval of time or space: new disease cases reported per week, mutations per genome, radioactive decays per second, or calls arriving at a help line.
It is the go-to model for count data when events happen at a steady average rate.

## Definition

Let $X\sim\mathrm{Poisson}(\lambda)$ count events in a fixed window with average rate $\lambda$.
Its probability mass function is $$P(X=k)=\frac{\lambda^{k}e^{-\lambda}}{k!}.$$

- **Support:** $k\in\{0,1,2,\dots\}$.
- **Parameter:** rate $\lambda>0$ (the [expected number](expected-value.md) of events in the window).
- **Mean:** $\mathbb{E}[X]=\lambda$.
- **Variance:** $\mathrm{Var}(X)=\lambda$.

A striking feature is that the **[mean](measures-of-center.md) and [variance](measures-of-variability.md) are equal**, both $\lambda$.
Real count data with variance much larger than the mean are called *overdispersed* and signal that a plain Poisson model is too simple.

## Limit of the binomial

The Poisson arises as the limit of a [binomial](binomial-distribution.md) with many trials, each individually unlikely.
If $n\to\infty$ and $p\to 0$ while the product $np\to\lambda$ stays fixed, then $$\binom{n}{k}p^k(1-p)^{n-k}\;\longrightarrow\;\frac{\lambda^{k}e^{-\lambda}}{k!}.$$ This is why the Poisson is called the "law of rare events": it counts many opportunities for an event, each with tiny probability.

## When it arises

The Poisson applies to **counts of independent events at a constant rate**: epidemiological case counts, incidence of rare diseases, defects per batch, or arrivals in a queue.
It connects directly to the [exponential distribution](exponential-distribution.md): if event counts are Poisson, the waiting times between consecutive events are exponential.

## In code

### R

```r
# pmf, cdf, quantile, and sampling for Poisson(lambda = 4)
dpois(2, lambda = 4)    # P(X = 2)
ppois(2, lambda = 4)    # P(X <= 2)
qpois(0.95, lambda = 4) # 95% quantile

set.seed(123)
x <- rpois(10000, lambda = 4)  # random sample
hist(x, breaks = seq(-0.5, max(x) + 0.5, 1), freq = FALSE)  # histogram
points(0:15, dpois(0:15, 4))                                # overlay the pmf
```

### Python

```python
import numpy as np
from scipy import stats

lam = 4
stats.poisson.pmf(2, lam)    # P(X = 2)
stats.poisson.cdf(2, lam)    # P(X <= 2)
stats.poisson.ppf(0.95, lam) # 95% quantile

rng = np.random.default_rng(123)
x = rng.poisson(lam, size=10000)  # random sample
# plt.hist(x, bins=range(0, 16), density=True); overlay stats.poisson.pmf(range(16), lam)
```

### Julia

```julia
using Distributions, Random

d = Poisson(4)      # Poisson(lambda)
pdf(d, 2)           # P(X = 2)   (pdf = pmf for discrete)
cdf(d, 2)           # P(X <= 2)
quantile(d, 0.95)   # 95% quantile

Random.seed!(123)
x = rand(d, 10_000) # random sample
# histogram(x, normalize=:pdf); scatter!(0:15, pdf.(d, 0:15)) to overlay the pmf
```

## Simulation

Many Poisson draws have empirical mean and variance both close to $\lambda$ — the signature equality of the distribution.

```r
set.seed(7)
x <- rpois(1e6, lambda = 4)
mean(x)  # ~ 4.00  (theoretical mean = lambda)
var(x)   # ~ 4.00  (theoretical variance = lambda; mean == variance)
```

## Why it matters for statistics

The Poisson is the foundation of count-data modeling, including Poisson regression for rates (cases per person-year) and the analysis of contingency tables.
Recognizing when the mean-equals-variance assumption fails — overdispersion — guides the choice of richer models such as the negative binomial.
It links proportions ([binomial](binomial-distribution.md)) and waiting times ([exponential](exponential-distribution.md)) into one coherent picture of event processes.

## Related

- [Exponential Distribution](exponential-distribution.md)
- [Binomial Distribution](binomial-distribution.md)
- [Probability Basics](probability-basics.md)
- [Expected Value](expected-value.md)
- [Distributions Overview](distributions-overview.md)
- [Quantitative Methods](../math.md)
