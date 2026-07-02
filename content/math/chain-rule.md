---
title: "Chain Rule"
---

# Chain Rule

The chain rule [differentiates](derivatives.md) a *composition* of functions — a function of a function. It is arguably the single most important differentiation rule: it powers backpropagation in neural networks and the delta method in statistics.

## The rule

If $y = f(g(x))$, then

\[
\frac{d}{dx} f\big(g(x)\big) = f'\big(g(x)\big)\,g'(x).
\]

In Leibniz notation, with $u = g(x)$,

\[
\frac{dy}{dx} = \frac{dy}{du}\,\frac{du}{dx}.
\]

## Intuition

Differentiate the *outer* function (leaving the inside alone), then multiply by the derivative of the *inside*. The rates multiply: if $u$ changes twice as fast as $x$ and $y$ changes three times as fast as $u$, then $y$ changes six times as fast as $x$.

## Worked example 1: $e^{-\lambda x}$

The exponential survival/decay term $y = e^{-\lambda x}$ is $f(u) = e^{u}$ composed with $u = g(x) = -\lambda x$, where $g'(x) = -\lambda$:

\[
\frac{d}{dx} e^{-\lambda x} = e^{-\lambda x}\cdot(-\lambda) = -\lambda\,e^{-\lambda x}.
\]

## Worked example 2: $(3x^2 + 1)^5$

Here $f(u) = u^5$ and $u = g(x) = 3x^2 + 1$, so $f'(u) = 5u^4$ and $g'(x) = 6x$:

\[
\frac{d}{dx}\big(3x^2 + 1\big)^5 = 5\,(3x^2 + 1)^4 \cdot 6x = 30x\,(3x^2 + 1)^4 .
\]

At $x = 1$: $30 \cdot 1 \cdot (4)^4 = 30 \cdot 256 = 7680$.

## Computing it

### R

```r
# Symbolic
D(expression((3*x^2 + 1)^5), "x")
#   5 * (3 * x^2 + 1)^4 * (3 * (2 * x))   == 30x(3x^2+1)^4

# Numeric check at x = 1
library(numDeriv)
grad(function(x) (3*x^2 + 1)^5, 1)   # 7680
```

### Python

```python
import sympy as sp
x, lam = sp.symbols("x lambda")
sp.diff(sp.exp(-lam * x), x)          # -lambda*exp(-lambda*x)
sp.diff((3*x**2 + 1)**5, x)           # 30*x*(3*x**2 + 1)**4

# Numeric check at x = 1
h = 1e-6
f = lambda x: (3*x**2 + 1)**5
(f(1 + h) - f(1 - h)) / (2 * h)       # ~7680.0
```

### Julia

```julia
using Symbolics
@variables x λ
Symbolics.derivative(exp(-λ * x), x)        # -λ*exp(-λ*x)
Symbolics.derivative((3x^2 + 1)^5, x)        # 30x*(1 + 3(x^2))^4

using ForwardDiff
ForwardDiff.derivative(x -> (3x^2 + 1)^5, 1.0)   # 7680.0
```

## Why it matters for statistics

The chain rule underlies the **delta method**, which approximates the [variance](measures-of-variability.md) of a transformed [estimator](statistical-inference.md) $h(\hat\theta)$ using $\big[h'(\hat\theta)\big]^2 \operatorname{Var}(\hat\theta)$. It is also how [gradients](gradient.md) propagate through the layers of a model during **backpropagation**, making automatic differentiation and modern machine learning possible.

## Related

- [Derivatives](derivatives.md)
- [Product Rule](product-rule.md)
- [Quotient Rule](quotient-rule.md)
- [Common Derivatives](common-derivatives.md)
- [U-Substitution](u-substitution.md)
- [Monotonic Transformations](monotonic-transformations.md)
- [Quantitative Methods](../math.md)
