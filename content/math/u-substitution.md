---
title: "u-Substitution"
---

# u-Substitution

u-substitution is the *reverse of the [chain rule](chain-rule.md)*: it undoes a composition of functions inside an integral.
It is the workhorse for integrating the kernels of many [probability densities](random-variables.md), especially the [normal](normal-distribution.md).

## The idea

The chain rule says $\frac{d}{dx}F(g(x)) = F'(g(x))\,g'(x)$.
Reading that backwards gives the substitution rule: if an integrand looks like $f(g(x))$ multiplied by its inner derivative $g'(x)$, then

\[
\int f\big(g(x)\big)\,g'(x)\,dx = \int f(u)\,du, \qquad u = g(x),\ du = g'(x)\,dx .
\]

For a definite integral, change the limits too:

\[
\int_a^b f\big(g(x)\big)\,g'(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du .
\]

## Steps

1. Choose $u = g(x)$, an inner function whose derivative also appears (up to a constant).
2. Compute $du = g'(x)\,dx$ and solve for $dx$ or $g'(x)\,dx$.
3. Rewrite the whole integral in terms of $u$.
4. Integrate in $u$, then substitute $x$ back (indefinite) or change the limits (definite).

## Worked example

Compute $\displaystyle\int 2x\,e^{x^2}\,dx$.

Let $u = x^2$, so $du = 2x\,dx$ — and $2x\,dx$ is exactly what sits in front of the exponential.
The integral becomes

\[
\int e^{u}\,du = e^{u} + C = e^{x^2} + C .
\]

A closely related normal-density kernel: $\displaystyle\int x\,e^{-x^2}\,dx$.
Take $u = -x^2$, $du = -2x\,dx$, so $x\,dx = -\tfrac12\,du$:

\[
\int x\,e^{-x^2}\,dx = -\frac12\int e^{u}\,du = -\frac12 e^{-x^2} + C .
\]

As a definite check, $\displaystyle\int_0^\infty x\,e^{-x^2}\,dx = \Big[-\tfrac12 e^{-x^2}\Big]_0^\infty = 0 - \big(-\tfrac12\big) = \tfrac12 .$

## Computing it

### R

```r
# Numeric check: integral of x*exp(-x^2) from 0 to Inf should be 0.5
integrate(function(x) x * exp(-x^2), 0, Inf)$value   # 0.5
```

### Python

```python
import sympy as sp
from scipy.integrate import quad
import numpy as np

x = sp.symbols("x")
print(sp.integrate(2*x*sp.exp(x**2), x))       # exp(x**2)
print(sp.integrate(x*sp.exp(-x**2), (x, 0, sp.oo)))  # 1/2

val, _ = quad(lambda t: t*np.exp(-t**2), 0, np.inf)
print(val)                                     # 0.4999999999999999
```

### Julia

```julia
using Symbolics, QuadGK

@variables x
# Numeric verification of the substitution result
println(quadgk(t -> t*exp(-t^2), 0, Inf)[1])   # 0.5

# Symbolic antiderivative check: d/dx(-1/2 e^{-x^2}) = x e^{-x^2}
D = Differential(x)
expand_derivatives(D(-0.5*exp(-x^2)))          # x*exp(-x^2)
```

## Why it matters for statistics

Normalizing a density and computing moments constantly produces integrands of the form $g'(x)\,f(g(x))$.
For the normal density the substitution $u = (x-\mu)/\sigma$ reduces any Gaussian integral to the standard $\int e^{-u^2/2}\,du$; for the exponential and gamma families, $u = -\lambda x$ handles the exponential factor.

## Related

- [Integrals](integrals.md)
- [Common Integrals](common-integrals.md)
- [Integration by Parts](integration-by-parts.md)
- [Chain Rule](chain-rule.md)
- [Normal Distribution](normal-distribution.md)
- [Quantitative Methods](../math.md)
