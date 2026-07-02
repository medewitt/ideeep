---
title: "Derivatives"
---

# Derivatives

A derivative measures the *instantaneous rate of change* of a function — the slope of the line tangent to its graph at a point. It is the engine behind [optimization](optimization.md), [maximum likelihood](maximum-likelihood.md) estimation, and the differential equations used in disease modeling.

## The limit definition

The derivative of $f$ at $x$ is the [limit](limits.md) of the average rate of change (the slope of a secant line) as the interval shrinks to zero:

\[
f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
\]

Geometrically, $\frac{f(x+h)-f(x)}{h}$ is the slope of the secant through $(x, f(x))$ and $(x+h, f(x+h))$. As $h \to 0$ that secant rotates into the *tangent line*, whose slope is $f'(x)$.

## Notation

The same object is written many ways:

\[
f'(x) = \frac{df}{dx} = \frac{d}{dx}f(x) = Df(x) = \dot{f} .
\]

Lagrange's $f'$ and Leibniz's $\frac{df}{dx}$ are the most common; $\dot{f}$ (Newton) is typical for time derivatives in dynamical systems.

## Differentiable implies continuous

If $f$ is differentiable at $x$, then it is continuous at $x$. The converse fails: $f(x) = |x|$ is continuous at $0$ but has no derivative there (the left slope is $-1$, the right slope is $+1$). Differentiability is the stronger, smoother condition.

## Worked example: $x^2$ from the definition

Let $f(x) = x^2$. Apply the limit definition:

\[
\begin{aligned}
f'(x) &= \lim_{h \to 0} \frac{(x+h)^2 - x^2}{h} \\
      &= \lim_{h \to 0} \frac{x^2 + 2xh + h^2 - x^2}{h} \\
      &= \lim_{h \to 0} \frac{2xh + h^2}{h} \\
      &= \lim_{h \to 0} (2x + h) = 2x .
\end{aligned}
\]

So $f'(x) = 2x$; the tangent to $y = x^2$ at $x = 3$ has slope $6$.

## Computing it

### R

```r
# Symbolic derivative with base R
f <- expression(x^2)
D(f, "x")            # 2 * x

# Numeric derivative at x = 3
library(numDeriv)
grad(function(x) x^2, 3)   # 6

# Function and its tangent line at x = 3
x  <- seq(-1, 5, length.out = 200)
a  <- 3; slope <- 2 * a
plot(x, x^2, type = "l")
abline(a = a^2 - slope * a, b = slope, lty = 2)  # tangent y = 6x - 9
```

### Python

```python
import sympy as sp

x = sp.symbols("x")
sp.diff(x**2, x)          # 2*x

# Numeric (finite difference) at x = 3
import numpy as np
f = lambda x: x**2
h = 1e-6
(f(3 + h) - f(3 - h)) / (2 * h)   # ~6.0 (central difference)

# Plot with tangent line at x = 3
import matplotlib.pyplot as plt
xs = np.linspace(-1, 5, 200)
a, slope = 3, 6
plt.plot(xs, xs**2)
plt.plot(xs, slope * (xs - a) + a**2, "--")   # y = 6(x-3) + 9
plt.show()
```

### Julia

```julia
using Symbolics
@variables x
Symbolics.derivative(x^2, x)   # 2x

using ForwardDiff
ForwardDiff.derivative(t -> t^2, 3.0)   # 6.0

using Plots
xs = range(-1, 5, length = 200)
a, slope = 3, 6
plot(xs, xs .^ 2)
plot!(xs, slope .* (xs .- a) .+ a^2, ls = :dash)  # tangent
```

## Why it matters for statistics

Derivatives locate the maxima and minima that drive statistical inference: setting the derivative of a log-likelihood to zero yields maximum likelihood estimates, and the second derivative (curvature) quantifies their precision through the Fisher information. They are also the building block of the [gradients](gradient.md) used to fit essentially every modern model.

## Related

- [Common Derivatives](common-derivatives.md)
- [Product Rule](product-rule.md)
- [Chain Rule](chain-rule.md)
- [Partial Derivatives](partial-derivatives.md)
- [Limits](limits.md)
- [Optimization](optimization.md)
- [Maximum Likelihood](maximum-likelihood.md)
- [Quantitative Methods](../math.md)
