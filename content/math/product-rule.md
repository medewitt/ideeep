---
title: "Product Rule"
---

# Product Rule

The product rule tells you how to [differentiate](derivatives.md) a product of two functions. It shows up whenever a model multiplies quantities that both change — for example a time-varying rate times a shrinking susceptible pool.

## The rule

\[
\frac{d}{dx}\big[f(x)\,g(x)\big] = f'(x)\,g(x) + f(x)\,g'(x)
\]

A common mistake is to guess $f' g'$; the derivative of a product is **not** the product of derivatives.

## Intuition

Think of a rectangle with width $f$ and height $g$, so its area is $f g$. Nudge $x$ a little: the width grows by about $f'\,dx$ and the height by about $g'\,dx$. The area gains two thin strips — one of size $f'\,g$ (from the wider width) and one of size $f\,g'$ (from the taller height). The tiny corner $f' g' (dx)^2$ is negligible, leaving $f' g + f g'$.

## Worked example: $x^2 e^x$

Let $f(x) = x^2$ and $g(x) = e^x$, so $f'(x) = 2x$ and $g'(x) = e^x$:

\[
\begin{aligned}
\frac{d}{dx}\big[x^2 e^x\big] &= (2x)\,e^x + x^2\,e^x \\
&= e^x\,(2x + x^2) = x e^x (x + 2) .
\end{aligned}
\]

At $x = 1$ this equals $e(1)(3) = 3e \approx 8.155$.

## Computing it

### R

```r
# Symbolic
D(expression(x^2 * exp(x)), "x")
#   2 * x * exp(x) + x^2 * exp(x)

# Numeric check at x = 1
library(numDeriv)
grad(function(x) x^2 * exp(x), 1)   # 8.15485  == 3*e
3 * exp(1)                          # 8.154845
```

### Python

```python
import sympy as sp
x = sp.symbols("x")
sp.diff(x**2 * sp.exp(x), x)        # x**2*exp(x) + 2*x*exp(x)

# Numeric check at x = 1
import numpy as np
f = lambda x: x**2 * np.exp(x)
h = 1e-6
(f(1 + h) - f(1 - h)) / (2 * h)     # ~8.1548  == 3*e
```

### Julia

```julia
using Symbolics
@variables x
Symbolics.derivative(x^2 * exp(x), x)   # 2x*exp(x) + (x^2)*exp(x)

using ForwardDiff
ForwardDiff.derivative(x -> x^2 * exp(x), 1.0)   # 8.15485  == 3e
```

## Why it matters for statistics

[Likelihoods](maximum-likelihood.md) and moment calculations are full of products — a density times a weight, a rate times an exposure, or $x\,f(x)$ inside an [expected value](expected-value.md). The product rule (together with the [chain rule](chain-rule.md)) is what lets you differentiate these expressions to derive estimators and their variances.

## Related

- [Derivatives](derivatives.md)
- [Quotient Rule](quotient-rule.md)
- [Chain Rule](chain-rule.md)
- [Common Derivatives](common-derivatives.md)
- [Integration by Parts](integration-by-parts.md)
- [Quantitative Methods](../math.md)
