---
title: "Maximum Likelihood Estimation"
---

# Maximum Likelihood Estimation

Maximum likelihood estimation (MLE) is the workhorse for fitting statistical models in epidemiology, from case-fatality proportions to hazard rates.
It picks the parameter values that make the observed data most probable.

![The log-likelihood peaks at the maximum-likelihood estimate.](../assets/figures/likelihood.svg)

## The likelihood function

Given [independent](probability-basics.md) observations $x_1, \dots, x_n$ from a model with density (or mass function) $f(x;\theta)$, the **likelihood** is the joint probability of the data viewed as a function of the [parameter](statistical-inference.md) $\theta$:

\[
\mathcal{L}(\theta) = \prod_{i=1}^{n} f(x_i;\theta).
\]

The **maximum likelihood estimate** is the value that maximizes this:

\[
\hat{\theta} = \arg\max_\theta \mathcal{L}(\theta).
\]

### Why work with the log

Products of many small probabilities underflow numerically and are awkward to differentiate.
Taking the logarithm turns the product into a sum:

\[
\ell(\theta) = \log \mathcal{L}(\theta) = \sum_{i=1}^{n} \log f(x_i;\theta).
\]

Because $\log$ is a strictly increasing [monotonic transformation](monotonic-transformations.md), it preserves the location of the maximum: $\arg\max_\theta \ell(\theta) = \arg\max_\theta \mathcal{L}(\theta)$.
See [exponentials and logarithms](exponentials-and-logarithms.md).

### Finding the maximum

We locate the maximum with [calculus](derivatives.md): solve the **score equation**

\[
\ell'(\theta) = 0
\]

and confirm it is a maximum by checking $\ell''(\theta) < 0$.
When no closed form exists, maximize numerically (see [optimization](optimization.md)).

## Worked example: Bernoulli / Binomial $p$

Suppose $x_1,\dots,x_n$ are independent [Bernoulli](binomial-distribution.md) trials with success probability $p$, so $f(x;p)=p^{x}(1-p)^{1-x}$.
Let $k=\sum_i x_i$ be the number of successes.
The log-likelihood is

\[
\ell(p) = \sum_{i=1}^{n}\big[x_i\log p + (1-x_i)\log(1-p)\big] = k\log p + (n-k)\log(1-p).
\]

Differentiate and set to zero:

\[
\ell'(p) = \frac{k}{p} - \frac{n-k}{1-p} = 0
\quad\Longrightarrow\quad
k(1-p) = (n-k)p
\quad\Longrightarrow\quad
\hat{p} = \frac{k}{n} = \bar{x}.
\]

The second derivative $\ell''(p) = -k/p^2 - (n-k)/(1-p)^2 < 0$ confirms a maximum.
The MLE of a Bernoulli/Binomial proportion is simply the sample mean.

## In code

Below we maximize the same log-likelihood numerically and compare to the closed form $\hat{p}=k/n$.

### R

```r
set.seed(1)
x <- rbinom(200, size = 1, prob = 0.3)   # 200 Bernoulli trials
negloglik <- function(p) -sum(dbinom(x, size = 1, prob = p, log = TRUE))
fit <- optimize(negloglik, interval = c(1e-6, 1 - 1e-6))
c(numeric = fit$minimum, closed_form = mean(x))
```

### Python

```python
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import bernoulli

rng = np.random.default_rng(1)
x = rng.binomial(1, 0.3, size=200)
negloglik = lambda p: -np.sum(bernoulli.logpmf(x, p))
fit = minimize_scalar(negloglik, bounds=(1e-6, 1 - 1e-6), method="bounded")
print(fit.x, x.mean())   # numeric vs closed form
```

<!-- python-output:auto -->
```text
0.3049994360315715 0.305
```
<!-- /python-output:auto -->

### Julia

```julia
using Distributions, Optim, Random
Random.seed!(1)
x = rand(Bernoulli(0.3), 200)
negloglik(p) = -sum(logpdf.(Bernoulli(p[1]), x))
fit = optimize(negloglik, [0.5], BFGS())
println(Optim.minimizer(fit)[1], " ", sum(x)/length(x))
```

All three recover $\hat{p}\approx k/n$.

## Why it matters for statistics

MLE provides a general, principled recipe for estimating parameters of essentially any probabilistic model.
Its estimators are consistent and asymptotically normal, which underpins [standard errors](measures-of-variability.md), [confidence intervals](confidence-intervals.md), and likelihood-ratio tests used throughout inference and epidemiological modeling.

## Related

- [Optimization](optimization.md)
- [Derivatives](derivatives.md)
- [Monotonic transformations](monotonic-transformations.md)
- [Exponentials and logarithms](exponentials-and-logarithms.md)
- [Statistical inference](statistical-inference.md)
- [Linear Regression](linear-regression.md)
- [Logistic Regression](logistic-regression.md)
- [Bayesian Inference](bayesian-inference.md)
- [Quantitative Methods](../math.md)
