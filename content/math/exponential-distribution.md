---
title: "The Exponential Distribution"
---

# The Exponential Distribution

The exponential distribution models the waiting time until the next event in a process where events occur at a constant average rate: the time between new infections, the length of an infectious period, the interval between radioactive decays, or the time until a component fails.
It is the continuous companion of the [Poisson distribution](poisson-distribution.md).

![The exponential density; the mean 1/lambda marks the average waiting time.](../assets/figures/exponential-pdf.svg)

## Definition

Let $X\sim\mathrm{Exponential}(\lambda)$ be the waiting time with rate $\lambda$.
Its [probability density function](random-variables.md) is $$f(x)=\lambda e^{-\lambda x},\qquad x\ge 0,$$ with cumulative distribution function $F(x)=1-e^{-\lambda x}$.

- **Support:** $x\in[0,\infty)$.
- **Parameter:** rate $\lambda>0$ (events per unit time).
  The reciprocal $1/\lambda$ is the [mean](measures-of-center.md) waiting time, sometimes called the *scale*.
- **Mean:** $\mathbb{E}[X]=\dfrac{1}{\lambda}$.
- **Variance:** $\mathrm{Var}(X)=\dfrac{1}{\lambda^2}$.

:::spoiler Show the mean, variance, and memoryless property

**Mean and variance.** Integrate by parts with the density $f(x) = \lambda e^{-\lambda x}$ on $[0,\infty)$:

\[
\mathbb{E}[X] = \int_0^{\infty} x\,\lambda e^{-\lambda x}\,dx = \Big[-x e^{-\lambda x}\Big]_0^{\infty} + \int_0^{\infty} e^{-\lambda x}\,dx = 0 + \frac{1}{\lambda} = \frac{1}{\lambda} .
\]

A second integration by parts gives $\mathbb{E}[X^2] = \int_0^\infty x^2 \lambda e^{-\lambda x}\,dx = 2/\lambda^2$, so

\[
\operatorname{Var}(X) = \mathbb{E}[X^2] - \big(\mathbb{E}[X]\big)^2 = \frac{2}{\lambda^2} - \frac{1}{\lambda^2} = \frac{1}{\lambda^2} .
\]

**Memorylessness.** The survival function is $P(X > t) = \int_t^\infty \lambda e^{-\lambda x}\,dx = e^{-\lambda t}$, so

\[
P(X > s + t \mid X > s) = \frac{P(X > s+t)}{P(X > s)} = \frac{e^{-\lambda(s+t)}}{e^{-\lambda s}} = e^{-\lambda t} = P(X > t) .
\]

Having already waited a time $s$ tells you nothing about the remaining wait — the defining property of the exponential.

:::

## The memoryless property

The exponential is the only continuous distribution that is **memoryless**: $$P(X>s+t\mid X>s)=P(X>t).$$ Having already waited $s$ units tells you nothing about how much longer you must wait — the process "forgets" the past.
This is why it models the time to the *next* event in a constant-rate process, and why it is a common (if simplistic) model for infectious periods that end at a constant hazard.

## Link to the Poisson

If events occur according to a [Poisson](poisson-distribution.md) process with rate $\lambda$ — so the *count* in any window is Poisson($\lambda\cdot\text{length}$) — then the *waiting times between* consecutive events are [independent](probability-basics.md) Exponential($\lambda$) variables.
Counting events and timing events are two views of the same underlying process.

## When it arises

The exponential arises for **inter-event times** at a constant rate: time between infections in early epidemic growth, duration of an infectious or latent period, survival times with constant hazard, and service or arrival times in queues.

## In code

Watch the parametrization carefully.
R uses the **rate** $\lambda$, SciPy uses a **scale** $=1/\lambda$, and Julia's `Exponential(θ)` also uses the **scale** $\theta=1/\lambda$.

### R

```r
# R parametrizes by rate = lambda
dexp(1, rate = 0.5)    # density at x = 1
pexp(1, rate = 0.5)    # P(X <= 1) = 1 - exp(-0.5)
qexp(0.95, rate = 0.5) # 95% quantile

set.seed(123)
x <- rexp(10000, rate = 0.5)  # random sample, mean = 1/0.5 = 2
hist(x, breaks = 40, freq = FALSE)     # histogram
curve(dexp(x, rate = 0.5), add = TRUE) # overlay the density
```

### Python

```python
import numpy as np
from scipy import stats

# scipy.stats.expon uses SCALE = 1/lambda (not the rate!)
lam = 0.5
stats.expon.pdf(1, scale=1/lam)    # density at 1
stats.expon.cdf(1, scale=1/lam)    # P(X <= 1)
stats.expon.ppf(0.95, scale=1/lam) # 95% quantile

rng = np.random.default_rng(123)
x = rng.exponential(scale=1/lam, size=10000)  # numpy also uses scale = 1/lambda
# plt.hist(x, bins=40, density=True); overlay stats.expon.pdf on a grid
```

### Julia

```julia
using Distributions, Random

# Julia's Exponential(theta) uses the SCALE theta = 1/lambda, NOT the rate.
lam = 0.5
d = Exponential(1 / lam)  # scale theta = 1/0.5 = 2  => rate lambda = 0.5
pdf(d, 1)                 # density at 1
cdf(d, 1)                 # P(X <= 1)
quantile(d, 0.95)         # 95% quantile

Random.seed!(123)
x = rand(d, 10_000)       # random sample, mean = theta = 2
# histogram(x, normalize=:pdf); plot!(t -> pdf(d, t)) to overlay the density
```

## Simulation

Many draws with rate $\lambda=0.5$ have empirical mean near $1/\lambda=2$ and variance near $1/\lambda^2=4$.

```r
set.seed(7)
x <- rexp(1e6, rate = 0.5)
mean(x)  # ~ 2.0  (theoretical mean = 1/lambda)
var(x)   # ~ 4.0  (theoretical variance = 1/lambda^2)
```

## Why it matters for statistics

The exponential is the building block of survival analysis and reliability, the simplest hazard model, and the inter-arrival law of Poisson processes used throughout epidemiology and queueing theory.
Understanding its rate-vs-scale parametrization prevents a common and costly software bug when moving between R, Python, and Julia.

## Related

- [Poisson Distribution](poisson-distribution.md)
- [Normal Distribution](normal-distribution.md)
- [Probability Basics](probability-basics.md)
- [Expected Value](expected-value.md)
- [Distributions Overview](distributions-overview.md)
- [Quantitative Methods](../math.md)
