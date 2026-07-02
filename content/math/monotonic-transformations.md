---
title: "Monotonic Transformations"
---

# Monotonic Transformations

A monotonic transformation reshapes a scale without scrambling its order. This simple property is why we can maximize a log-likelihood instead of a likelihood, and why the CDF gives a universal recipe for simulating any random variable.

## Definition

A function $g$ is **monotonically increasing** if it preserves order:

\[
x_1 < x_2 \implies g(x_1) < g(x_2),
\]

and **monotonically decreasing** if $x_1 < x_2 \implies g(x_1) > g(x_2)$. When the inequalities are strict, $g$ is *strictly* monotone. Examples of strictly increasing functions on their domains: $g(x) = \log x$, $g(x) = e^x$, $g(x) = x^3$.

## Order and argmax are preserved

The key consequence: applying a **strictly increasing** $g$ does not change *where* a function attains its maximum or minimum.

\[
\arg\max_{\theta}\, h(\theta) = \arg\max_{\theta}\, g\big(h(\theta)\big).
\]

The *location* $\theta^\ast$ of the peak is identical; only the *height* changes.

### Why log-likelihood works

The likelihood of iid data is a product,

\[
L(\theta) = \prod_{i=1}^n f(x_i \mid \theta),
\]

which is numerically awkward (products of many small numbers underflow). Because $\log$ is strictly increasing, maximizing the **log-likelihood**

\[
\ell(\theta) = \log L(\theta) = \sum_{i=1}^n \log f(x_i \mid \theta)
\]

yields the **same** maximizer $\hat{\theta}$ — turning a product into a friendly sum without changing the answer. See [maximum likelihood](maximum-likelihood.md).

## CDFs are non-decreasing

Every cumulative distribution function $F(x) = \Pr(X \le x)$ is monotonically non-decreasing, rising from 0 to 1. This monotonicity is what makes the next result possible.

## The probability integral transform

If $X$ is continuous with CDF $F$, then feeding $X$ through its *own* CDF produces a standard uniform variable:

\[
F(X) \sim \text{Uniform}(0, 1).
\]

Reading this backward gives **inverse-CDF (inverse-transform) sampling**: to simulate $X$, draw $U \sim \text{Uniform}(0,1)$ and set

\[
X = F^{-1}(U).
\]

Because $F$ is monotone it has a (quantile) inverse $F^{-1}$, so uniform draws map cleanly onto draws from any target distribution.

## Worked example

Let $X \sim \text{Exponential}(\lambda)$ with $F(x) = 1 - e^{-\lambda x}$. Solving $U = 1 - e^{-\lambda X}$ for $X$:

\[
X = -\frac{1}{\lambda}\log(1 - U).
\]

So exponential samples come free from uniform samples. And since $1 - U$ is also $\text{Uniform}(0,1)$, one often writes $X = -\tfrac{1}{\lambda}\log U$.

## Simulation

We demonstrate two facts: (1) $F(X)$ is uniform, and (2) $\log$ preserves the argmax.

### R

```r
set.seed(7)
# (1) Probability integral transform: F(X) ~ Uniform(0,1)
x <- rnorm(1e5, mean = 5, sd = 2)
u <- pnorm(x, 5, 2)          # apply the true CDF
c(mean(u), var(u))            # ~0.5 and ~0.0833 (= 1/12): uniform

# (2) log preserves the argmax of a positive function
theta <- seq(0.1, 10, by = 0.01)
h <- dgamma(theta, shape = 3, rate = 1)   # a positive curve
theta[which.max(h)] == theta[which.max(log(h))]   # TRUE
```

### Python

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(7)

# (1) F(X) ~ Uniform(0,1)
x = rng.normal(5, 2, 100_000)
u = stats.norm.cdf(x, 5, 2)
print(u.mean(), u.var())      # ~0.5, ~0.0833 (= 1/12)

# (2) log preserves the argmax
theta = np.arange(0.1, 10, 0.01)
h = stats.gamma.pdf(theta, a=3, scale=1)
print(theta[h.argmax()] == theta[np.log(h).argmax()])   # True
```

### Julia

```julia
using Random, Statistics, Distributions
Random.seed!(7)

# (1) F(X) ~ Uniform(0,1)
d = Normal(5, 2)
x = rand(d, 100_000)
u = cdf.(d, x)
mean(u), var(u)               # ~0.5, ~0.0833 (= 1/12)

# (2) log preserves the argmax
theta = 0.1:0.01:10
h = pdf.(Gamma(3, 1), theta)
argmax(h) == argmax(log.(h))  # true
```

## Why it matters for statistics

Monotonic transformations underpin two workhorses of statistical practice. Optimization on the log scale makes maximum likelihood numerically stable while leaving the estimate untouched, and the probability integral transform is the foundation of random-number generation, quantile methods, and copulas. Recognizing that order-preserving maps leave argmax and rankings intact lets you swap scales freely for convenience.

## Related

- [Maximum Likelihood](maximum-likelihood.md)
- [Optimization](optimization.md)
- [Random Variables](random-variables.md)
- [Exponentials and Logarithms](exponentials-and-logarithms.md)
- [Distributions Overview](distributions-overview.md)
- [Quantitative Methods](../math.md)
