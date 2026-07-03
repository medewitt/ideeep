---
title: "Partial Derivatives"
---

# Partial Derivatives

A partial derivative measures how a multivariable function changes as you vary **one** input while holding the others fixed.
They are the foundation of the [gradient](gradient.md) and the [Jacobian](jacobians.md), and of [optimizing](optimization.md) [likelihoods](maximum-likelihood.md) that depend on several parameters.

## Definition and notation

For $f(x, y)$, the partial derivative with respect to $x$ treats $y$ as a constant:

\[
\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x + h,\, y) - f(x,\, y)}{h}.
\]

Common notations include $\dfrac{\partial f}{\partial x}$, $f_x$, and $\partial_x f$.
The curly $\partial$ (instead of $d$) signals that other variables are being held constant.

## Worked example: $f(x,y) = x^2 y + \sin(y)$

Differentiate with respect to $x$, treating $y$ as constant (so $\sin y$ is a constant and drops out):

\[
\frac{\partial f}{\partial x} = 2xy .
\]

Differentiate with respect to $y$, treating $x$ as constant:

\[
\frac{\partial f}{\partial y} = x^2 + \cos(y) .
\]

At the point $(x, y) = (1, 0)$: $f_x = 2(1)(0) = 0$ and $f_y = 1^2 + \cos 0 = 2$.

## Connection to the gradient and Jacobian

Stacking the partials of a scalar function into a vector gives the **gradient**:

\[
\nabla f = \left(\frac{\partial f}{\partial x},\; \frac{\partial f}{\partial y}\right).
\]

For a vector-valued function, arranging all partials into a matrix gives the **Jacobian**.
Partial derivatives are the individual entries from which both objects are built.

## Computing it

### R

```r
# Symbolic partials with base R
f <- expression(x^2 * y + sin(y))
D(f, "x")   # 2 * x * y
D(f, "y")   # x^2 + cos(y)

# Numeric gradient at (1, 0)
library(numDeriv)
grad(function(v) v[1]^2 * v[2] + sin(v[2]), c(1, 0))   # 0  2
```

### Python

```python
import sympy as sp
x, y = sp.symbols("x y")
f = x**2 * y + sp.sin(y)
sp.diff(f, x)   # 2*x*y
sp.diff(f, y)   # x**2 + cos(y)

# Numeric partials at (1, 0)
import numpy as np
g = lambda v: v[0]**2 * v[1] + np.sin(v[1])
h = 1e-6
[(g([1 + h, 0]) - g([1 - h, 0])) / (2*h),   # ~0
 (g([1, 0 + h]) - g([1, 0 - h])) / (2*h)]   # ~2
```

### Julia

```julia
using Symbolics
@variables x y
f = x^2 * y + sin(y)
Symbolics.derivative(f, x)   # 2x*y
Symbolics.derivative(f, y)   # x^2 + cos(y)

using ForwardDiff
g(v) = v[1]^2 * v[2] + sin(v[2])
ForwardDiff.gradient(g, [1.0, 0.0])   # [0.0, 2.0]
```

## Why it matters for statistics

Log-likelihoods usually depend on several parameters at once (a mean and a variance, or a whole regression coefficient vector).
Setting each partial derivative to zero produces the system of score equations solved to find maximum likelihood estimates, and the matrix of second partials becomes the observed information.

## Related

- [Derivatives](derivatives.md)
- [The Gradient](gradient.md)
- [Jacobians](jacobians.md)
- [Chain Rule](chain-rule.md)
- [Optimization](optimization.md)
- [Maximum Likelihood](maximum-likelihood.md)
- [Quantitative Methods](../math.md)
