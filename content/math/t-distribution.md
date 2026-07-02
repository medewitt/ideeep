---
title: "The t-Distribution"
---

# The t-Distribution

Student's t-distribution is a bell-shaped curve that looks like the normal but with heavier tails. It arises when we standardize a sample mean but must **estimate** the population standard deviation from the same small sample — the everyday situation in experiments and epidemiological studies where $\sigma$ is unknown. The extra uncertainty from estimating $\sigma$ is exactly what fattens the tails.

## Definition

The t-distribution with $\nu$ degrees of freedom has density
$$f(t)=\frac{\Gamma\!\left(\frac{\nu+1}{2}\right)}{\sqrt{\nu\pi}\,\Gamma\!\left(\frac{\nu}{2}\right)}\left(1+\frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}},$$
where $\Gamma$ is the gamma function.

- **Support:** $t\in(-\infty,\infty)$.
- **Parameter:** degrees of freedom $\nu>0$ (for a one-sample mean, $\nu=n-1$).
- **Mean:** $\mathbb{E}[T]=0$ for $\nu>1$ (undefined for $\nu\le 1$).
- **Variance:** $\mathrm{Var}(T)=\dfrac{\nu}{\nu-2}$ for $\nu>2$ (infinite for $1<\nu\le 2$).

The distribution is symmetric about $0$, like the standard normal, but its variance exceeds $1$, reflecting the heavier tails.

## Heavier tails, approaching normal

For small $\nu$ the t-distribution puts noticeably more probability in the tails than the [normal](normal-distribution.md): extreme values are more likely, so critical values are larger and confidence intervals wider. As $\nu\to\infty$ the estimate of $\sigma$ becomes essentially exact and
$$f(t)\;\longrightarrow\;\phi(t)=\frac{1}{\sqrt{2\pi}}e^{-t^2/2},$$
the standard normal density. By around $\nu=30$ the two are already very close.

## When it arises (Student's t)

Suppose $X_1,\dots,X_n$ are an i.i.d. sample from a normal population with unknown mean $\mu$ and unknown $\sigma$. The standardized sample mean using the **sample** standard deviation $s$,
$$T=\frac{\bar{X}-\mu}{s/\sqrt{n}},$$
follows a t-distribution with $\nu=n-1$ degrees of freedom. If we knew $\sigma$ exactly, this would instead be standard normal; replacing $\sigma$ by the estimate $s$ is what produces the t.

## In code

### R

```r
# density, cdf, quantile, and sampling for t with df = 5
dt(1.5, df = 5)    # density at t = 1.5
pt(1.5, df = 5)    # P(T <= 1.5)
qt(0.975, df = 5)  # 97.5% quantile ~ 2.571 (vs 1.96 for the normal)

set.seed(123)
x <- rt(10000, df = 5)  # random sample
hist(x, breaks = 60, freq = FALSE, xlim = c(-6, 6))  # histogram
curve(dt(x, df = 5), add = TRUE)      # overlay the t density
curve(dnorm(x), add = TRUE, lty = 2)  # dashed normal for comparison
```

### Python

```python
import numpy as np
from scipy import stats

nu = 5
stats.t.pdf(1.5, nu)    # density at 1.5
stats.t.cdf(1.5, nu)    # P(T <= 1.5)
stats.t.ppf(0.975, nu)  # 97.5% quantile ~ 2.571

x = stats.t.rvs(df=nu, size=10000, random_state=123)  # random sample
# plt.hist(x, bins=60, density=True); overlay stats.t.pdf and stats.norm.pdf on a grid
```

### Julia

```julia
using Distributions, Random

d = TDist(5)        # Student's t with nu = 5 degrees of freedom
pdf(d, 1.5)         # density at 1.5
cdf(d, 1.5)         # P(T <= 1.5)
quantile(d, 0.975)  # 97.5% quantile ~ 2.571

Random.seed!(123)
x = rand(d, 10_000) # random sample
# histogram(x, normalize=:pdf); plot!(t -> pdf(d, t)); plot!(t -> pdf(Normal(), t))
```

## Simulation

As $\nu$ grows, the t-distribution's quantiles converge to the normal's, and its sample variance approaches $\nu/(\nu-2)$.

```r
set.seed(7)
qt(0.975, df = 5)    # ~ 2.571  (heavy tails: larger than 1.96)
qt(0.975, df = 100)  # ~ 1.984  (already close to the normal 1.96)
var(rt(1e6, df = 5)) # ~ 1.67   (theoretical nu/(nu-2) = 5/3 for nu = 5)
```

## Why it matters for statistics

The t-distribution is the workhorse of small-sample inference about means. It supplies the critical values for the one- and two-sample **t-tests** in [hypothesis testing](hypothesis-testing.md) and the multipliers for **t-based** [confidence intervals](confidence-intervals.md) for a mean. Using the t (rather than the normal) correctly accounts for the extra uncertainty of estimating $\sigma$ from limited data — the difference that keeps small-sample intervals honest.

## Related

- [Normal Distribution](normal-distribution.md)
- [Confidence Intervals](confidence-intervals.md)
- [Hypothesis Testing](hypothesis-testing.md)
- [Sampling Distributions](sampling-distributions.md)
- [Distributions Overview](distributions-overview.md)
- [Quantitative Methods](../math.md)
