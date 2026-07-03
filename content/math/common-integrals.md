---
title: "Common Integrals"
---

# Common Integrals

A short reference table of antiderivatives you will use constantly, plus the rules that let you combine them.
These standard forms show up throughout biology: $\int e^{-kt}\,dt$ gives a drug's total exposure or the cumulative decay of a labeled tracer, the reciprocal integral $\int \tfrac1x\,dx$ produces the $\ln$ behind log-scaled assays, and the Gaussian integral at the end normalizes the [normal](normal-distribution.md) density of biological measurements.

## The table

Each row gives an indefinite integral (add a constant $C$ to any of them).

\[
\begin{aligned}
\int x^n\,dx &= \frac{x^{n+1}}{n+1} + C \quad (n \neq -1) \\[4pt]
\int \frac{1}{x}\,dx &= \ln|x| + C \\[4pt]
\int e^x\,dx &= e^x + C \\[4pt]
\int a^x\,dx &= \frac{a^x}{\ln a} + C \quad (a > 0,\ a \neq 1) \\[4pt]
\int \sin x\,dx &= -\cos x + C \\[4pt]
\int \cos x\,dx &= \sin x + C
\end{aligned}
\]

The $1/x$ case is the special exception to the power rule: it is the antiderivative that the formula $x^{n+1}/(n+1)$ cannot produce (division by zero when $n=-1$).

## Linearity rules

Integration is linear, which lets you break big integrals into small ones:

- **Constant multiple:** $\displaystyle\int c\,f(x)\,dx = c\int f(x)\,dx$ — pull constants outside.
- **Sum rule:** $\displaystyle\int \big(f(x) + g(x)\big)\,dx = \int f(x)\,dx + \int g(x)\,dx .$

## The Gaussian integral

The area under the "bell curve" kernel $e^{-x^2}$ over the whole real line is

\[
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi} .
\]

This has no elementary antiderivative, yet the total is finite and exact.
It is why the normal density $\frac{1}{\sqrt{2\pi}\,\sigma}\exp\!\big(-\frac{(x-\mu)^2}{2\sigma^2}\big)$ integrates to $1$ — the $\sqrt{2\pi}$ is precisely the normalizing constant.

## Worked example

Integrate the polynomial $\int_0^2 (3x^2 + 2x + 1)\,dx$.
Using the sum and constant-multiple rules with the power rule:

\[
\int (3x^2 + 2x + 1)\,dx = x^3 + x^2 + x + C .
\]

Evaluating from $0$ to $2$:

\[
\big[x^3 + x^2 + x\big]_0^2 = (8 + 4 + 2) - 0 = 14 .
\]

## Computing it

### R

```r
# Numeric check of the polynomial example
integrate(function(x) 3*x^2 + 2*x + 1, 0, 2)$value   # 14

# Gaussian integral
integrate(function(x) exp(-x^2), -Inf, Inf)$value    # 1.772454 = sqrt(pi)
sqrt(pi)                                              # 1.772454
```

### Python

```python
import sympy as sp
from scipy.integrate import quad
import numpy as np

x = sp.symbols("x")
print(sp.integrate(3*x**2 + 2*x + 1, (x, 0, 2)))     # 14
print(sp.integrate(sp.exp(-x**2), (x, -sp.oo, sp.oo)))  # sqrt(pi)

val, _ = quad(lambda t: np.exp(-t**2), -np.inf, np.inf)
print(val, np.sqrt(np.pi))                           # 1.7724538509... 1.7724538509...
```

<!-- python-output:auto -->
```text
14
sqrt(pi)
1.7724538509055159 1.7724538509055159
```
<!-- /python-output:auto -->

### Julia

```julia
using Symbolics, QuadGK

@variables x
D = Differential(x)  # (not needed here, shown for context)

# Numeric checks
println(quadgk(t -> 3t^2 + 2t + 1, 0, 2)[1])         # 14.0
println(quadgk(t -> exp(-t^2), -Inf, Inf)[1])        # 1.7724538509055159
println(sqrt(pi))                                    # 1.7724538509055159
```

## Why it matters for statistics

Densities are built from these functions: the [exponential density](exponential-distribution.md) uses $\int e^{-\lambda x}dx$, the normal uses the Gaussian integral, and moments ([means](measures-of-center.md), [variances](measures-of-variability.md)) reduce to power-rule integrals against a density.
Knowing the table by sight makes normalizing constants and expected values fast to derive.

## Related

- [Integrals](integrals.md)
- [u-Substitution](u-substitution.md)
- [Integration by Parts](integration-by-parts.md)
- [Common Derivatives](common-derivatives.md)
- [Normal Distribution](normal-distribution.md)
- [Exponential Distribution](exponential-distribution.md)
- [Quantitative Methods](../math.md)
