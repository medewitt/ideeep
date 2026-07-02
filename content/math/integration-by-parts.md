---
title: "Integration by Parts"
---

# Integration by Parts

Integration by parts is the *reverse of the product rule*. It turns an integral of a product into an easier one, and it is the standard way to compute the mean of the exponential and gamma distributions.

## The formula

Starting from the product rule $\frac{d}{dx}(uv) = u\,v' + u'\,v$ and integrating both sides, then rearranging, gives

\[
\int u\,dv = uv - \int v\,du .
\]

Here you split the integrand into a part $u$ (to differentiate) and a part $dv$ (to integrate): compute $du = u'\,dx$ and $v = \int dv$, then apply the formula and hope the new integral $\int v\,du$ is simpler.

## Choosing $u$ and $dv$: LIATE

A useful priority for picking $u$ (differentiate first what comes earliest):

- **L**ogarithmic — $\ln x$
- **I**nverse trig — $\arctan x$
- **A**lgebraic — $x, x^2$
- **T**rigonometric — $\sin x, \cos x$
- **E**xponential — $e^x$

Whatever is left becomes $dv$. The goal is for $\int v\,du$ to be easier than the original.

## Worked example

Compute $\displaystyle\int x\,e^{-x}\,dx$. By LIATE, the algebraic factor $x$ is $u$ and $e^{-x}dx$ is $dv$:

\[
u = x,\quad du = dx, \qquad dv = e^{-x}\,dx,\quad v = -e^{-x}.
\]

Apply the formula:

\[
\int x\,e^{-x}\,dx = -x e^{-x} - \int (-e^{-x})\,dx = -x e^{-x} - e^{-x} + C = -(x+1)e^{-x} + C .
\]

Definite version over $[0,\infty)$:

\[
\int_0^\infty x\,e^{-x}\,dx = \Big[-(x+1)e^{-x}\Big]_0^\infty = 0 - (-(0+1)\cdot 1) = 1 .
\]

## Computing it

### R

```r
# Numeric check: integral of x*exp(-x) from 0 to Inf equals 1
integrate(function(x) x * exp(-x), 0, Inf)$value   # 1
```

### Python

```python
import sympy as sp
from scipy.integrate import quad
import numpy as np

x = sp.symbols("x")
print(sp.integrate(x*sp.exp(-x), x))            # -x*exp(-x) - exp(-x)
print(sp.integrate(x*sp.exp(-x), (x, 0, sp.oo)))  # 1

val, _ = quad(lambda t: t*np.exp(-t), 0, np.inf)
print(val)                                      # 1.0000000000000002
```

### Julia

```julia
using Symbolics, QuadGK

@variables x
# Numeric verification
println(quadgk(t -> t*exp(-t), 0, Inf)[1])      # 1.0

# Symbolic check: d/dx[-(x+1)e^{-x}] = x e^{-x}
D = Differential(x)
expand_derivatives(D(-(x+1)*exp(-x)))           # x*exp(-x)
```

## Why it matters for statistics

The exponential distribution with rate $\lambda$ has density $\lambda e^{-\lambda x}$, and its mean is

\[
E[X] = \int_0^\infty x\,\lambda e^{-\lambda x}\,dx = \frac{1}{\lambda},
\]

which is exactly the integration-by-parts computation above (with a rescaling). The same technique produces the moments of the gamma distribution and appears whenever you integrate a polynomial against an exponential kernel.

## Related

- [Integrals](integrals.md)
- [Common Integrals](common-integrals.md)
- [u-Substitution](u-substitution.md)
- [Product Rule](product-rule.md)
- [Exponential Distribution](exponential-distribution.md)
- [Expected Value](expected-value.md)
- [Quantitative Methods](../math.md)
