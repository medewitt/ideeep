---
title: "Quotient Rule"
---

# Quotient Rule

The quotient rule [differentiates](derivatives.md) a ratio of two functions. Ratios are everywhere in epidemiology — prevalence proportions, hazard ratios, and the logistic curve are all quotients whose rates of change we often need.

## The rule

\[
\frac{d}{dx}\left[\frac{f(x)}{g(x)}\right] = \frac{f'(x)\,g(x) - f(x)\,g'(x)}{\big[g(x)\big]^2}
\]

Order matters in the numerator: it is "derivative of top times bottom, minus top times derivative of bottom," all over the bottom squared.

## Intuition

Write the quotient as a product $f \cdot g^{-1}$ and apply the [product](product-rule.md) and [chain](chain-rule.md) rules:

\[
\frac{d}{dx}\big[f g^{-1}\big] = f' g^{-1} + f\,(-g^{-2} g') = \frac{f'}{g} - \frac{f g'}{g^2} = \frac{f' g - f g'}{g^2}.
\]

So the quotient rule is not a new idea — it is the product rule in disguise.

## Worked example: the logistic-type ratio $\dfrac{x}{1+x}$

Let $f(x) = x$ and $g(x) = 1 + x$, so $f'(x) = 1$ and $g'(x) = 1$:

\[
\frac{d}{dx}\left[\frac{x}{1+x}\right]
= \frac{(1)(1+x) - x(1)}{(1+x)^2}
= \frac{1}{(1+x)^2}.
\]

The derivative is always positive, so $\frac{x}{1+x}$ increases toward its saturating limit of $1$ — the same "diminishing returns" shape as a saturating incidence or dose-response curve. At $x = 1$ the slope is $\tfrac{1}{4}$.

## Computing it

### R

```r
# Symbolic
D(expression(x / (1 + x)), "x")
#   1/(1 + x) - x/(1 + x)^2   == 1/(1+x)^2

# Numeric check at x = 1
library(numDeriv)
grad(function(x) x / (1 + x), 1)   # 0.25
```

### Python

```python
import sympy as sp
x = sp.symbols("x")
sp.simplify(sp.diff(x / (1 + x), x))   # 1/(x + 1)**2

# Numeric check at x = 1
h = 1e-6
f = lambda x: x / (1 + x)
(f(1 + h) - f(1 - h)) / (2 * h)        # ~0.25
```

### Julia

```julia
using Symbolics
@variables x
simplify(Symbolics.derivative(x / (1 + x), x))   # (1 + x)^-2

using ForwardDiff
ForwardDiff.derivative(x -> x / (1 + x), 1.0)     # 0.25
```

## Why it matters for statistics

Proportions, rates, and probabilities are ratios, and models like logistic regression are built from them. Differentiating these quotients is how we obtain the score functions and delta-method [standard errors](measures-of-variability.md) for estimated proportions and odds.

## Related

- [Derivatives](derivatives.md)
- [Product Rule](product-rule.md)
- [Chain Rule](chain-rule.md)
- [Common Derivatives](common-derivatives.md)
- [Exponentials and Logarithms](exponentials-and-logarithms.md)
- [Quantitative Methods](../math.md)
