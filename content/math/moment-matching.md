---
title: "Moment Matching"
description: "Choosing a distribution's parameters so its moments match target values — the method of moments for estimation, and moment matching for approximating an intractable distribution by a tractable one."
---

# Moment Matching

Suppose you have a fistful of numbers — incubation periods, say — and you want a smooth distribution that summarizes them.
Moment matching answers this by a simple rule: pick the parameters so that the distribution's **moments** — its mean, its variance, and so on — equal the moments you can measure in the data.
The same idea, run in reverse, lets you replace an awkward, intractable distribution with a friendly one that shares its first couple of moments.

![A right-skewed sample with a moment-matched gamma density (which captures the skew) and a moment-matched normal (same mean and variance, but symmetric and spilling below zero).](../assets/figures/moment-matching.svg)

## The method of moments

The oldest recipe for fitting a distribution is the **method of moments**, introduced by Karl Pearson in the 1890s.
A distribution with $k$ unknown parameters has population moments — the [expected value](expected-value.md) $\mu = \mathbb{E}[X]$, the variance $\sigma^2 = \mathbb{E}[(X-\mu)^2]$, and higher moments — that are functions of those parameters.
The data supply matching **sample moments**: the sample mean $\bar{x} = \frac{1}{n}\sum_i x_i$, the sample variance $s^2 = \frac{1}{n}\sum_i (x_i-\bar{x})^2$, and so on.
The method sets the first $k$ population moments equal to the first $k$ sample moments and solves the resulting equations for the parameters.

The whole procedure is: write each moment as a formula in the parameters, substitute the numbers computed from the data, and solve.
Because you need one equation per unknown, a two-parameter family is pinned down by its first two moments — the mean and the variance.

### The gamma example

The gamma distribution with shape $\alpha$ and rate $\beta$ has mean and variance $$\mu = \frac{\alpha}{\beta}, \qquad \sigma^2 = \frac{\alpha}{\beta^2}.$$ Solving these two equations for the two parameters gives the moment estimators $$\alpha = \frac{\mu^2}{\sigma^2}, \qquad \beta = \frac{\mu}{\sigma^2},$$ so you compute the sample mean and variance and read the parameters straight off.
Equivalently the scale is $\theta = 1/\beta = \sigma^2/\mu$, which says the gamma's spread-to-center ratio fixes its scale while its squared coefficient of variation fixes its shape.

### The beta example

The beta distribution on $[0,1]$ with parameters $\alpha$ and $\beta$ has $$\mu = \frac{\alpha}{\alpha+\beta}, \qquad \sigma^2 = \frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}.$$ Introducing the shorthand $\kappa = \frac{\mu(1-\mu)}{\sigma^2} - 1$ (which must be positive, i.e. $\sigma^2 < \mu(1-\mu)$), the moment estimators are $$\alpha = \mu\,\kappa, \qquad \beta = (1-\mu)\,\kappa.$$ This is the standard way to turn an elicited mean and variance for a probability — a prevalence, a sensitivity, a vaccine efficacy — into a beta prior.

## A worked example

Take a small sample of measured serial intervals (in days): $$3,\ 5,\ 4,\ 8,\ 6,\ 5,\ 9,\ 4,\ 7,\ 6.$$ The sample mean is $\bar{x} = 5.7$ and the (population-form) sample variance is $s^2 = 3.21$.
Matching a gamma gives $$\alpha = \frac{\bar{x}^2}{s^2} = \frac{5.7^2}{3.21} \approx 10.12, \qquad \beta = \frac{\bar{x}}{s^2} = \frac{5.7}{3.21} \approx 1.78,$$ a distribution centered near six days with the mild right skew that serial intervals typically show.

The maximum-likelihood fit would instead solve the [likelihood](maximum-likelihood.md) equations, which for the gamma involve the digamma function and the geometric mean of the data and have no closed form.
On tidy, roughly-gamma data the two fits are close; the moment fit is just less efficient, meaning it uses the sample slightly less fully than [maximum likelihood](maximum-likelihood.md) and so scatters a bit more around the truth from sample to sample.
Its virtue is that it drops out of two elementary summaries with no iteration at all.

## Moment matching as approximation

The second face of the same idea is **distributional approximation**: replace a distribution you cannot work with by a tractable one that shares its low-order moments.
A mixture of several components, or the sum of a handful of dependent delays, may have no clean closed form, yet its mean and variance are often easy to compute exactly.
Matching a single normal or gamma to just those two moments yields a stand-in that is analytically convenient and usually accurate near the center.

> [!NOTE]
> A single normal matched to a mixture's mean and variance reproduces its center and spread but erases any skew, bimodality, or heavy tail — the moments it was not asked to match.

This trick is the engine behind several inference methods.
In **assumed-density filtering** and **expectation propagation**, each update produces a complicated posterior that is immediately projected back onto a simple family (typically a [normal](normal-distribution.md)) by matching moments — the moment-matched member of an exponential family is exactly the one that minimizes the Kullback–Leibler divergence from the true posterior, which is why the projection takes this form.
The same move appears in epidemic modeling when an aggregated delay or a sum over compartments — the convolution of several sojourn-time distributions in a compartmental or delay model — is approximated by one gamma matched to the total mean and variance, keeping the model closed-form instead of tracking every stage.

## Strengths and pitfalls

Moment matching is prized for being simple and often **closed-form**: no optimizer, no iteration, just a few sample summaries plugged into an algebraic solution.
That makes it an excellent way to get a quick parameterization or a starting point.

Its weaknesses are the mirror image of its simplicity.
It is generally **statistically inefficient** relative to [maximum likelihood](maximum-likelihood.md), extracting somewhat less information from the same data and so giving noisier estimates.
It is **blind to shape and tails**: by construction it only sees the moments you match, so two very different distributions with the same mean and variance look identical to it, and matched higher moments can even fall outside a family's valid range (a beta needs $\sigma^2 < \mu(1-\mu)$; a required $\kappa>0$ can fail).
And because it can lean on high-order moments, which are dominated by extreme observations, moment estimators using third or fourth moments are notably sensitive to outliers.

## In code

We fit a gamma to a sample by matching its mean and variance, recovering $\alpha = \mu^2/\sigma^2$ and $\beta = \mu/\sigma^2$.

### R

```r
x <- c(3, 5, 4, 8, 6, 5, 9, 4, 7, 6)   # serial intervals (days)
m <- mean(x)
v <- mean((x - m)^2)                    # population-form variance

shape <- m^2 / v                        # alpha = mean^2 / var
rate  <- m / v                          # beta  = mean / var
cat(sprintf("mean=%.2f var=%.2f\n", m, v))
cat(sprintf("gamma: shape=%.3f rate=%.3f\n", shape, rate))

# maximum-likelihood comparison (no closed form; iterative)
# MASS::fitdistr(x, "gamma")
```

### Python

```python
import numpy as np

rng = np.random.default_rng(0)          # seeded; unused here but reproducible
x = np.array([3, 5, 4, 8, 6, 5, 9, 4, 7, 6], dtype=float)

m = x.mean()
v = x.var()                             # population-form variance (ddof=0)
shape = m**2 / v                        # alpha = mean^2 / var
rate = m / v                            # beta  = mean / var

print(f"mean = {m:.3f}, var = {v:.3f}")
print(f"gamma moment-match: shape = {shape:.3f}, rate = {rate:.3f}")
print(f"implied scale = {1/rate:.3f}")

# vs MLE (iterative, no closed form) -- see scipy.stats.gamma.fit
from scipy import stats
a_hat, loc_hat, scale_hat = stats.gamma.fit(x, floc=0)
print(f"gamma MLE:          shape = {a_hat:.3f}, rate = {1/scale_hat:.3f}")
```

<!-- python-output:auto -->
```text
mean = 5.700, var = 3.210
gamma moment-match: shape = 10.121, rate = 1.776
implied scale = 0.563
gamma MLE:          shape = 9.997, rate = 1.754
```
<!-- /python-output:auto -->

### Julia

```julia
using Statistics

x = [3, 5, 4, 8, 6, 5, 9, 4, 7, 6]      # serial intervals (days)
m = mean(x)
v = mean((x .- m).^2)                    # population-form variance

shape = m^2 / v                          # alpha = mean^2 / var
rate  = m / v                            # beta  = mean / var
println("mean=$(round(m, digits=2)) var=$(round(v, digits=2))")
println("gamma: shape=$(round(shape, digits=3)) rate=$(round(rate, digits=3))")

# using Distributions; fit_mle(Gamma, x)  # MLE comparison
```

## Why it matters

Moment matching is the fast, back-of-the-envelope route from data or moments to a usable distribution.
Epidemiologists use it to parameterize [serial-interval and incubation-period](../epidemiology/epidemiological-intervals.md) distributions from a reported mean and variance when the raw line list is unavailable, turning two published numbers into a full gamma or lognormal.
It supplies cheap starting values that seed the iterative optimizers behind [maximum-likelihood](maximum-likelihood.md) and Bayesian fits, and its approximation face keeps analytic [Bayesian inference](bayesian-inference.md) tractable by collapsing intractable posteriors onto simple families.
Whenever you only need the center and spread right — and can live without the tails — matching moments is often all the machinery required.

## Related

- [Expected Value](expected-value.md)
- [Measures of Variability](measures-of-variability.md)
- [Moment Generating Functions](moment-generating-functions.md)
- [Maximum Likelihood Estimation](maximum-likelihood.md)
- [Common Distributions: An Overview](distributions-overview.md)
- [Quantitative Methods](../math.md)
