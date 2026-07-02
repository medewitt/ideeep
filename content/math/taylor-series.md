---
title: "Taylor and Maclaurin Series"
---

# Taylor and Maclaurin Series

A Taylor series approximates a smooth function by a polynomial built from its derivatives at a point. This local approximation is the workhorse behind the delta method, Newton-type optimization, and many large-sample expansions.

## Taylor expansion

If $f$ is infinitely differentiable near $a$,

\[
f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}\,(x - a)^{n}
= f(a) + f'(a)(x - a) + \frac{f''(a)}{2!}(x - a)^2 + \cdots
\]

A **Maclaurin series** is the special case $a = 0$.

## Key expansions

\[
\begin{aligned}
e^{x} &= \sum_{n=0}^{\infty} \frac{x^{n}}{n!} = 1 + x + \frac{x^2}{2} + \frac{x^3}{6} + \cdots \\
\sin x &= x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots \\
\ln(1 + x) &= x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots \quad (|x| < 1)
\end{aligned}
\]

## Worked example: approximating $e^{0.1}$

Using the Maclaurin series for $e^x$ at $x = 0.1$:

\[
e^{0.1} \approx 1 + 0.1 + \frac{0.1^2}{2} + \frac{0.1^3}{6}
= 1 + 0.1 + 0.005 + 0.000167 = 1.105167.
\]

The true value is $e^{0.1} = 1.105171\ldots$, so three terms past the constant already give an error of about $4 \times 10^{-6}$.

## Computing it

### R

```r
x <- 0.1
approx <- sum(x^(0:3) / factorial(0:3))   # 1.105167
error  <- exp(x) - approx                 # ~4.25e-6
c(approx, error)
```

### Python

```python
import sympy as sp

x = sp.symbols("x")
print(sp.series(sp.exp(x), x, 0, 5))   # 1 + x + x**2/2 + x**3/6 + x**4/24 + O(x**5)

import math
approx = sum(0.1**n / math.factorial(n) for n in range(4))  # 1.10516666...
print(approx, math.exp(0.1) - approx)                        # error ~4.25e-6
```

### Julia

```julia
using Symbolics

# Numeric truncated series and approximation error
x = 0.1
approx = sum(x^n / factorial(n) for n in 0:3)   # 1.1051666...
error  = exp(x) - approx                         # ~4.25e-6
approx, error
```

## Why it matters for statistics

The delta method approximates the variance of a transformed estimator $g(\hat\theta)$ via a first-order Taylor expansion, $g(\hat\theta) \approx g(\theta) + g'(\theta)(\hat\theta - \theta)$. Second-order expansions of the log-likelihood give the Fisher information and Newton-Raphson updates for maximum likelihood. In short, Taylor series turn intractable nonlinear quantities into tractable linear or quadratic ones.

## Related

- [Series](series.md)
- [Derivatives](derivatives.md)
- [Limits](limits.md)
- [Maximum Likelihood](maximum-likelihood.md)
- [Quantitative Methods](../math.md)
