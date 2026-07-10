---
title: "The Normal Distribution"
---

# The Normal Distribution

The normal (Gaussian) distribution is the bell-shaped curve that appears whenever many small, independent influences add together: measurement error, biological variation in heights or blood pressure, and — crucially for statistics — the [sampling distribution](sampling-distributions.md) of an average.
Its ubiquity is not a coincidence but a consequence of the [central limit theorem](central-limit-theorem.md).

![The normal distribution and the 68–95–99.7 rule.](../assets/figures/normal-distribution.svg)

## Definition

A [random variable](random-variables.md) $X\sim\mathcal{N}(\mu,\sigma^2)$ has probability density function $$f(x)=\frac{1}{\sigma\sqrt{2\pi}}\,e^{-(x-\mu)^2/(2\sigma^2)}.$$

- **Support:** $x\in(-\infty,\infty)$.
- **Parameters:** [mean](measures-of-center.md) $\mu\in\mathbb{R}$ (location) and variance $\sigma^2>0$ (spread); $\sigma$ is the [standard deviation](measures-of-variability.md).
- **Mean:** $\mathbb{E}[X]=\mu$.
- **Variance:** $\mathrm{Var}(X)=\sigma^2$.

The curve is symmetric about $\mu$, with inflection points at $\mu\pm\sigma$.

## The standard normal

Setting $\mu=0$ and $\sigma=1$ gives the **standard normal** $Z\sim\mathcal{N}(0,1)$ with density $$\phi(z)=\frac{1}{\sqrt{2\pi}}\,e^{-z^2/2}.$$ Any normal variable can be standardized by the $z$-score $Z=\dfrac{X-\mu}{\sigma}$, which is why a single table (or the `pnorm` function) suffices for all normal probabilities.
Its cdf is written $\Phi(z)=P(Z\le z)$.

:::spoiler Show that the parameters are the mean and variance

Standardize with $Z = (X-\mu)/\sigma$, so $X = \mu + \sigma Z$ and $Z$ has the standard normal density $\phi(z) = \frac{1}{\sqrt{2\pi}}e^{-z^2/2}$.
Because $\phi$ is symmetric about $0$, the odd integrand $z\phi(z)$ integrates to zero, so $\mathbb{E}[Z] = 0$ and hence $\mathbb{E}[X] = \mu + \sigma\,\mathbb{E}[Z] = \mu$.
For the variance, integrate $\mathbb{E}[Z^2] = \int_{-\infty}^{\infty} z^2 \phi(z)\,dz$ by parts with $u = z$ and $dv = z\phi(z)\,dz$, using $\phi'(z) = -z\phi(z)$ so that $v = -\phi(z)$:

\[
\mathbb{E}[Z^2] = \Big[-z\phi(z)\Big]_{-\infty}^{\infty} + \int_{-\infty}^{\infty}\phi(z)\,dz = 0 + 1 = 1 .
\]

Therefore $\operatorname{Var}(X) = \sigma^2\,\mathbb{E}[Z^2] = \sigma^2$, confirming that $\mu$ and $\sigma^2$ are exactly the mean and variance.

:::

## The 68–95–99.7 rule

For any normal distribution, the probability mass within a few standard deviations of the mean is fixed:

- about $68\%$ of values fall in $\mu\pm\sigma$,
- about $95\%$ fall in $\mu\pm 2\sigma$,
- about $99.7\%$ fall in $\mu\pm 3\sigma$.

This "empirical rule" is a fast sanity check: a value more than $3\sigma$ from the mean is genuinely unusual.

## When it arises

The normal distribution arises whenever a quantity is the **sum or average of many independent small effects**.
By the [central limit theorem](central-limit-theorem.md), the sample mean of almost any distribution is approximately normal for large $n$, which is why normal-based tests and confidence intervals are so widely applicable even when the raw data are not themselves normal.

## In code

### R

```r
# pdf, cdf, quantile, and sampling for N(mu = 100, sd = 15)
dnorm(115, mean = 100, sd = 15)   # density at x = 115
pnorm(115, mean = 100, sd = 15)   # P(X <= 115) ~ 0.8413
qnorm(0.975, mean = 100, sd = 15) # 97.5% quantile

set.seed(123)
x <- rnorm(10000, mean = 100, sd = 15)  # random sample
hist(x, breaks = 40, freq = FALSE)       # histogram of the sample
curve(dnorm(x, 100, 15), add = TRUE)     # overlay the true density
```

### Python

```python
import numpy as np
from scipy import stats

mu, sigma = 100, 15
stats.norm.pdf(115, mu, sigma)   # density at 115
stats.norm.cdf(115, mu, sigma)   # P(X <= 115) ~ 0.8413
stats.norm.ppf(0.975, mu, sigma) # 97.5% quantile

rng = np.random.default_rng(123)
x = rng.normal(mu, sigma, size=10000)  # random sample
# plt.hist(x, bins=40, density=True); overlay stats.norm.pdf on a grid
```

### Julia

```julia
using Distributions, Random

d = Normal(100, 15)   # Normal(mean, sd)
pdf(d, 115)           # density at 115
cdf(d, 115)           # P(X <= 115) ~ 0.8413
quantile(d, 0.975)    # 97.5% quantile

Random.seed!(123)
x = rand(d, 10_000)   # random sample
# histogram(x, normalize=:pdf); plot!(t -> pdf(d, t)) to overlay the density
```

## Simulation

Simulating draws and comparing the histogram to $f(x)$ shows the match, and the sample statistics recover the parameters.

```r
set.seed(7)
x <- rnorm(1e6, mean = 100, sd = 15)
mean(x)  # ~ 100  (theoretical mean = mu)
sd(x)    # ~ 15   (theoretical sd = sigma)
mean(abs(x - 100) <= 15)  # ~ 0.68, matching the 68% rule
```

## Why it matters for statistics

The normal distribution is the backbone of classical inference.
Because sample means are approximately normal, $z$- and $t$-based [confidence intervals](confidence-intervals.md) and [hypothesis tests](hypothesis-testing.md) rest on it.
It is also the reference against which "unusual" observations are judged, and the limiting shape of the [t-distribution](t-distribution.md) as degrees of freedom grow.

## Related

- [t-Distribution](t-distribution.md)
- [Central Limit Theorem](central-limit-theorem.md)
- [Sampling Distributions](sampling-distributions.md)
- [Confidence Intervals](confidence-intervals.md)
- [Distributions Overview](distributions-overview.md)
- [Quantitative Methods](../math.md)
