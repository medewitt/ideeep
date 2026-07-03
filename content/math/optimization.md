---
title: "Optimization and Critical Points"
---

# Optimization and Critical Points

Optimization is the search for a function's highest or lowest value.
It is the mathematical core of [maximum likelihood](maximum-likelihood.md) estimation, least squares, and fitting disease models to data.
Estimating a pathogen's transmission rate by maximum likelihood, or choosing the vaccination coverage that minimizes total cases, are both optimization problems — and in each the optimum sits where the derivative is zero.

![At a maximum the first derivative is zero and the second derivative is negative.](../assets/figures/optimization-max.svg)

## Critical points

At a smooth interior maximum or minimum, the tangent line is flat, so the [derivative](derivatives.md) is zero.
Points where

\[
f'(x) = 0
\]

are called **critical points** (candidates for extrema).
They may be maxima, minima, or saddle/inflection points, so they must be classified.

## The second-derivative test

For a critical point $x^*$ with $f'(x^*) = 0$:

- if $f''(x^*) > 0$, the curve bends upward — $x^*$ is a **local minimum**;
- if $f''(x^*) < 0$, the curve bends downward — $x^*$ is a **local maximum**;
- if $f''(x^*) = 0$, the test is inconclusive.

## Convex vs. concave

A function with $f'' > 0$ everywhere is **convex** (bowl-shaped): any critical point is a *global* minimum.
A function with $f'' < 0$ everywhere is **concave** (dome-shaped): any critical point is a *global* maximum.
This global guarantee is why convexity/concavity is so prized in optimization.

## Worked example: a quadratic

Maximize $f(x) = -(x-3)^2 + 5$.
Differentiate and set to zero:

\[
f'(x) = -2(x-3) = 0 \ \Longrightarrow\ x^* = 3 .
\]

Check the second derivative: $f''(x) = -2 < 0$, so $x^* = 3$ is a maximum.
The maximum value is $f(3) = -(0)^2 + 5 = 5$.

## Monotonic transformations preserve the argmax

If $g$ is a strictly increasing function, then $x$ maximizes $f(x)$ if and only if it maximizes $g(f(x))$ — the *location* of the maximum is unchanged (only the height changes).
Since $\ln$ is strictly increasing, maximizing a likelihood $L(\theta)$ and maximizing the log-likelihood $\ell(\theta) = \ln L(\theta)$ give the *same* estimate.
Because the log turns products into sums, $\ell$ is far easier to differentiate — this is why MLE almost always works with the log-likelihood.

## Worked example: a 1-D likelihood

Suppose we observe $k$ successes in $n$ independent trials with success probability $p$.
The log-likelihood is

\[
\ell(p) = k\ln p + (n-k)\ln(1-p) .
\]

Setting $\ell'(p) = \frac{k}{p} - \frac{n-k}{1-p} = 0$ and solving gives the intuitive estimate $\hat p = k/n$.
With $k=7$, $n=10$, $\hat p = 0.7$.

## Computing it

### R

```r
# Maximize f(x) = -(x-3)^2 + 5  (optimize minimizes, so negate)
f <- function(x) -(x - 3)^2 + 5
optimize(function(x) -f(x), interval = c(-10, 10))
# $minimum ~ 3, $objective ~ -5  => maximum of f is 5 at x = 3

# Find the critical point directly via root-finding on f'(x) = -2(x-3)
uniroot(function(x) -2*(x - 3), interval = c(-10, 10))$root   # 3
```

### Python

```python
from scipy.optimize import minimize_scalar

f = lambda x: -(x - 3)**2 + 5
res = minimize_scalar(lambda x: -f(x))
print(res.x, -res.fun)          # 3.0000000...  5.0

# MLE example: maximize the binomial log-likelihood, k=7, n=10
import numpy as np
k, n = 7, 10
nll = lambda p: -(k*np.log(p) + (n-k)*np.log(1-p))
r = minimize_scalar(nll, bounds=(1e-6, 1-1e-6), method="bounded")
print(r.x)                      # 0.6999... = k/n
```

<!-- python-output:auto -->
```text
3.0000000000000004 5.0
0.7000003717141288
```
<!-- /python-output:auto -->

### Julia

```julia
using Optim

f(x) = -(x - 3)^2 + 5
res = optimize(x -> -f(x), -10.0, 10.0)   # Brent's method
println(Optim.minimizer(res), " ", -Optim.minimum(res))  # 3.0  5.0

# Root-finding on the derivative via Optim's bracket is fine;
# for f'(x)=0 directly you can use Roots.jl:
# using Roots; find_zero(x -> -2*(x-3), (-10, 10))  # 3.0
```

## Why it matters for statistics

Nearly every estimation method is an optimization: maximum likelihood maximizes $\ell(\theta)$, least squares minimizes a sum of squared residuals, and MAP estimation maximizes a posterior.
The first-order condition $f'(\theta)=0$ produces the *estimating equations*, and the second-derivative (Hessian) governs both which extremum you found and the estimator's [variance](measures-of-variability.md).

## Related

- [Maximum Likelihood](maximum-likelihood.md)
- [Monotonic Transformations](monotonic-transformations.md)
- [Derivatives](derivatives.md)
- [Partial Derivatives](partial-derivatives.md)
- [Gradient](gradient.md)
- [Jensen's Inequality](jensens-inequality.md)
- [Exponentials and Logarithms](exponentials-and-logarithms.md)
- [Quantitative Methods](../math.md)
