---
title: "Functions and Graphs"
---

# Functions and Graphs

A function maps each input to exactly one output, $f: x \mapsto f(x)$.
Recognizing the shapes of common functions lets you read transformations, link functions, and model curves at a glance.

## Common functions in statistics

- **Linear:** $f(x) = a + bx$ — a straight line, slope $b$, intercept $a$.
- **Quadratic:** $f(x) = ax^2 + bx + c$ — a parabola (e.g. squared error).
- **Absolute value:** $f(x) = |x|$ — a V shape (e.g. L1 loss).
- **Square root:** $f(x) = \sqrt{x}$ — defined for $x \ge 0$ ([standard errors](measures-of-variability.md) scale like $1/\sqrt{n}$).
- **[Exponential](exponentials-and-logarithms.md):** $f(x) = e^{x}$ — always positive, grows rapidly.
- **Natural log:** $f(x) = \ln x$ — defined for $x > 0$, the inverse of $e^x$.

## Domain and range

The **domain** is the set of allowed inputs; the **range** is the set of achievable outputs.
For example $\sqrt{x}$ has domain $[0, \infty)$ and range $[0, \infty)$, while $\ln x$ has domain $(0, \infty)$ and range $\mathbb{R}$.
Exponential $e^x$ has domain $\mathbb{R}$ and range $(0, \infty)$ — which is why it is used to keep modeled rates positive.

## Piecewise functions

A **piecewise** function uses different rules on different parts of its domain.
A worked example:

\[
f(x) =
\begin{cases}
-x & x < 0 \\
x^2 & 0 \le x \le 1 \\
1 & x > 1
\end{cases}
\]

Evaluating: $f(-3) = 3$, $f(0.5) = 0.25$, and $f(4) = 1$.
The pieces meet continuously at $x = 0$ (both give $0$) and at $x = 1$ (both give $1$).

## Computing it

### R

```r
# Plot several functions on one panel
curve(x^2, from = -2, to = 2, ylab = "f(x)")
curve(abs(x), add = TRUE, col = "red")
curve(exp(x), from = -2, to = 2, col = "blue")

# Piecewise function
f <- function(x) ifelse(x < 0, -x, ifelse(x <= 1, x^2, 1))
f(c(-3, 0.5, 4))   # 3.00 0.25 1.00
```

### Python

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 400)
plt.plot(x, x**2, label="x^2")
plt.plot(x, np.abs(x), label="|x|")
plt.plot(x, np.exp(x), label="e^x")
plt.legend()

# Piecewise function
f = lambda x: np.piecewise(x, [x < 0, (x >= 0) & (x <= 1), x > 1],
                           [lambda v: -v, lambda v: v**2, 1.0])
print(f(np.array([-3, 0.5, 4])))   # [3.   0.25 1.  ]
```

<!-- python-output:auto -->
```text
[3.   0.25 1.  ]
```
<!-- /python-output:auto -->

### Julia

```julia
using Plots

x = range(-2, 2, length = 400)
plot(x, x.^2, label = "x^2")
plot!(x, abs.(x), label = "|x|")
plot!(x, exp.(x), label = "e^x")

# Piecewise function
f(x) = x < 0 ? -x : (x <= 1 ? x^2 : 1.0)
f.([-3, 0.5, 4])   # [3.0, 0.25, 1.0]
```

## Why it matters for statistics

Nearly every model is a function: regression lines, link functions in GLMs (log, logit), loss functions, and density curves.
Knowing domains keeps you from taking $\ln$ of a negative number or a square root of a negative variance, and recognizing shapes helps you diagnose fit and transformations.

## Related

- [Exponentials and Logarithms](exponentials-and-logarithms.md)
- [Mathematical Notation](mathematical-notation.md)
- [Derivatives](derivatives.md)
- [Limits](limits.md)
- [Quantitative Methods](../math.md)
