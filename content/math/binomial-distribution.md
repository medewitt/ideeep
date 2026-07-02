---
title: "The Binomial Distribution"
---

# The Binomial Distribution

The binomial distribution counts how many "successes" occur in a fixed number of [independent](probability-basics.md) yes/no trials — how many of $n$ vaccinated people avoid infection, how many of $n$ tossed coins land heads, how many of $n$ patients respond to a treatment. It is the natural model behind testing a proportion.

## Definition

Let $X\sim\mathrm{Binomial}(n,p)$ count the successes in $n$ independent trials, each with success probability $p$. Its probability mass function is
$$P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}.$$

- **Support:** $k\in\{0,1,2,\dots,n\}$.
- **Parameters:** number of trials $n\in\{1,2,\dots\}$ and success probability $p\in[0,1]$.
- **Mean:** $\mathbb{E}[X]=np$.
- **Variance:** $\mathrm{Var}(X)=np(1-p)$.

The binomial coefficient $\binom{n}{k}=\frac{n!}{k!\,(n-k)!}$ counts the number of ways to arrange $k$ successes among $n$ trials.

## Sum of Bernoulli trials

A single trial with outcome $1$ (success, probability $p$) or $0$ (failure) is a **Bernoulli** [random variable](random-variables.md) with [mean](measures-of-center.md) $p$ and [variance](measures-of-variability.md) $p(1-p)$. A binomial variable is just the sum of $n$ independent Bernoulli trials:
$$X=\sum_{i=1}^{n}B_i,\qquad B_i\sim\mathrm{Bernoulli}(p).$$
Because expectation and (for independent terms) variance add, this immediately gives $\mathbb{E}[X]=np$ and $\mathrm{Var}(X)=np(1-p)$.

## When it arises

The binomial arises whenever you count successes among a **fixed number of independent, identical trials**: proportion testing (fraction cured, fraction defective), survey responses (yes/no), and quality control. The sample proportion $\hat p=X/n$ is the basis for inference about an unknown $p$.

### Extension: the multinomial

When each trial has more than two possible outcomes (say categories $1,\dots,m$ with probabilities $p_1,\dots,p_m$ summing to $1$), the counts follow the **multinomial** distribution
$$P(X_1=k_1,\dots,X_m=k_m)=\frac{n!}{k_1!\cdots k_m!}\,p_1^{k_1}\cdots p_m^{k_m},$$
the direct generalization of the binomial to several categories.

## In code

### R

```r
# pmf, cdf, quantile, and sampling for Binomial(n = 20, p = 0.3)
dbinom(6, size = 20, prob = 0.3)   # P(X = 6)
pbinom(6, size = 20, prob = 0.3)   # P(X <= 6)
qbinom(0.95, size = 20, prob = 0.3) # 95% quantile

set.seed(123)
x <- rbinom(10000, size = 20, prob = 0.3)  # random sample
hist(x, breaks = seq(-0.5, 20.5, 1), freq = FALSE)  # histogram
points(0:20, dbinom(0:20, 20, 0.3))                 # overlay the pmf
```

### Python

```python
import numpy as np
from scipy import stats

n, p = 20, 0.3
stats.binom.pmf(6, n, p)    # P(X = 6)
stats.binom.cdf(6, n, p)    # P(X <= 6)
stats.binom.ppf(0.95, n, p) # 95% quantile

rng = np.random.default_rng(123)
x = rng.binomial(n, p, size=10000)  # random sample
# plt.hist(x, bins=range(0, 22), density=True); overlay stats.binom.pmf(range(21), n, p)
```

### Julia

```julia
using Distributions, Random

d = Binomial(20, 0.3)   # Binomial(n, p)
pdf(d, 6)               # P(X = 6)   (pdf = pmf for discrete)
cdf(d, 6)               # P(X <= 6)
quantile(d, 0.95)       # 95% quantile

Random.seed!(123)
x = rand(d, 10_000)     # random sample
# histogram(x, normalize=:pdf); scatter!(0:20, pdf.(d, 0:20)) to overlay the pmf
```

## Simulation

The empirical mean of many binomial draws converges to $np$ and the variance to $np(1-p)$.

```r
set.seed(7)
x <- rbinom(1e6, size = 20, prob = 0.3)
mean(x)  # ~ 6.0   (theoretical mean = np = 20 * 0.3)
var(x)   # ~ 4.2   (theoretical variance = np(1-p) = 20 * 0.3 * 0.7)
```

## Why it matters for statistics

The binomial underpins inference for proportions: confidence intervals for $p$, tests comparing two proportions, and the reasoning behind [p-values](p-values.md) in exact tests. For large $n$ it is well approximated by the [normal distribution](normal-distribution.md), and for large $n$ with small $p$ it approaches the [Poisson distribution](poisson-distribution.md).

## Related

- [Poisson Distribution](poisson-distribution.md)
- [Normal Distribution](normal-distribution.md)
- [Probability Basics](probability-basics.md)
- [Expected Value](expected-value.md)
- [Distributions Overview](distributions-overview.md)
- [Quantitative Methods](../math.md)
