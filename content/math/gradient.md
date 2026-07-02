---
title: "The Gradient"
---

# The Gradient

The gradient collects all of a function's [partial derivatives](partial-derivatives.md) into a single vector that points in the direction of steepest ascent. It is the workhorse of [optimization](optimization.md): gradient descent and [maximum likelihood](maximum-likelihood.md) estimation both follow (or climb) the gradient.

## Definition

For a scalar-valued function $f(x_1, \dots, x_n)$, the gradient is the vector of partial derivatives:

\[
\nabla f = \left(\frac{\partial f}{\partial x_1},\; \frac{\partial f}{\partial x_2},\; \dots,\; \frac{\partial f}{\partial x_n}\right).
\]

## Direction of steepest ascent

At any point, $\nabla f$ points in the direction in which $f$ increases fastest, and its magnitude $\lVert \nabla f \rVert$ is that maximum rate of increase. The negative gradient $-\nabla f$ points in the direction of steepest *descent* — which is exactly why we step along $-\nabla f$ to minimize a loss. Where $f$ is at a maximum or minimum, $\nabla f = \mathbf{0}$.

## Relation to the Jacobian

The gradient is the [Jacobian](jacobians.md) of a scalar-valued function — specifically its single row (or, by convention, that row transposed into a column). More generally the Jacobian stacks the gradients of each component of a vector-valued function as its rows.

## Worked example: $f(x,y) = x^2 + 3y^2$

The partials are $\dfrac{\partial f}{\partial x} = 2x$ and $\dfrac{\partial f}{\partial y} = 6y$, so

\[
\nabla f(x, y) = (2x,\; 6y).
\]

At $(1, 1)$, $\nabla f = (2, 6)$: $f$ climbs steepest heading in that direction, and $-(2, 6)$ is the descent direction toward the minimum at the origin.

## Computing it

### R

```r
library(numDeriv)
f <- function(v) v[1]^2 + 3 * v[2]^2
grad(f, c(1, 1))   # 2  6
```

### Python

```python
import sympy as sp
x, y = sp.symbols("x y")
f = x**2 + 3*y**2
[sp.diff(f, x), sp.diff(f, y)]      # [2*x, 6*y]

# Numeric gradient with numpy
import numpy as np
g = lambda v: v[0]**2 + 3*v[1]**2
def num_grad(g, v, h=1e-6):
    v = np.asarray(v, float)
    return np.array([(g(v + h*e) - g(v - h*e)) / (2*h)
                     for e in np.eye(len(v))])
num_grad(g, [1, 1])                 # [2., 6.]
```

### Julia

```julia
using ForwardDiff
f(v) = v[1]^2 + 3v[2]^2
ForwardDiff.gradient(f, [1.0, 1.0])   # [2.0, 6.0]
```

## Gradient descent in one snippet

Follow $-\nabla f$ downhill toward the minimum at the origin:

```julia
using ForwardDiff
f(v) = v[1]^2 + 3v[2]^2
x = [5.0, 5.0]
η = 0.1                              # learning rate
for _ in 1:100
    x -= η * ForwardDiff.gradient(f, x)
end
x   # ≈ [0.0, 0.0]
```

## Why it matters for statistics

Fitting a model almost always means optimizing an objective — minimizing a loss or maximizing a log-likelihood — and the gradient is the compass. Gradient ascent on the log-likelihood drives maximum likelihood estimation, while stochastic gradient descent trains the large models used in modern data science and disease forecasting.

## Related

- [Partial Derivatives](partial-derivatives.md)
- [Jacobians](jacobians.md)
- [Derivatives](derivatives.md)
- [Optimization](optimization.md)
- [Maximum Likelihood](maximum-likelihood.md)
- [Chain Rule](chain-rule.md)
- [Quantitative Methods](../math.md)
