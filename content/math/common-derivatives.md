---
title: "Common Derivatives"
---

# Common Derivatives

Most differentiation in practice is pattern matching: memorize a short table of [derivatives](derivatives.md) plus a few combination rules, and you can differentiate nearly any function that appears in statistics or disease modeling by inspection.

## Reference table

| Function $f(x)$ | Derivative $f'(x)$ |
| --- | --- |
| $c$ (constant) | $0$ |
| $x^n$ | $n\,x^{n-1}$ |
| $e^x$ | $e^x$ |
| $a^x$ | $a^x \ln a$ |
| $\ln x$ | $\dfrac{1}{x}$ |
| $\log_a x$ | $\dfrac{1}{x \ln a}$ |
| $\sin x$ | $\cos x$ |
| $\cos x$ | $-\sin x$ |
| $\tan x$ | $\sec^2 x = \dfrac{1}{\cos^2 x}$ |

## Combination rules

Constant multiple:

\[
\frac{d}{dx}\big[c\,f(x)\big] = c\,f'(x)
\]

Sum (and difference):

\[
\frac{d}{dx}\big[f(x) \pm g(x)\big] = f'(x) \pm g'(x)
\]

The **power rule** $\frac{d}{dx}x^n = n x^{n-1}$ holds for any real $n$, so it also covers roots ($x^{1/2}$) and reciprocals ($x^{-1}$).

## Worked example: differentiating a polynomial

Let $f(x) = 3x^4 - 5x^2 + 7x - 2$. Differentiate term by term using the power, constant-multiple, and sum rules:

\[
\begin{aligned}
f'(x) &= 3 \cdot 4x^{3} - 5 \cdot 2x^{1} + 7 \cdot 1 - 0 \\
      &= 12x^3 - 10x + 7 .
\end{aligned}
\]

At $x = 1$: $f'(1) = 12 - 10 + 7 = 9$.

## Computing it

### R

```r
D(expression(x^n), "x")        # x^n * (n * (1/x))  == n*x^(n-1)
D(expression(exp(x)), "x")     # exp(x)
D(expression(log(x)), "x")     # 1/x
D(expression(sin(x)), "x")     # cos(x)
D(expression(3*x^4 - 5*x^2 + 7*x - 2), "x")
#   3 * (4 * x^3) - 5 * (2 * x) + 7   == 12x^3 - 10x + 7
```

### Python

```python
import sympy as sp
x, a, n = sp.symbols("x a n")

sp.diff(x**n, x)        # n*x**n/x  == n*x**(n-1)
sp.diff(a**x, x)        # a**x*log(a)
sp.diff(sp.log(x), x)   # 1/x
sp.diff(sp.tan(x), x)   # tan(x)**2 + 1  == sec^2 x
sp.diff(3*x**4 - 5*x**2 + 7*x - 2, x)   # 12*x**3 - 10*x + 7
```

### Julia

```julia
using Symbolics
@variables x a

Symbolics.derivative(exp(x), x)   # exp(x)
Symbolics.derivative(log(x), x)   # 1 / x
Symbolics.derivative(sin(x), x)   # cos(x)
Symbolics.derivative(3x^4 - 5x^2 + 7x - 2, x)   # 7 + 12(x^3) - 10x
```

## Why it matters for statistics

These few rules cover the derivatives you meet constantly: polynomial regression terms, the $e^x$ in [exponential growth](exponentials-and-logarithms.md) and logistic models, and the $\ln x$ at the heart of every [log-likelihood](maximum-likelihood.md). Knowing them cold lets you derive score equations and standard errors without reaching for software.

## Related

- [Derivatives](derivatives.md)
- [Product Rule](product-rule.md)
- [Quotient Rule](quotient-rule.md)
- [Chain Rule](chain-rule.md)
- [Common Integrals](common-integrals.md)
- [Exponentials and Logarithms](exponentials-and-logarithms.md)
- [Quantitative Methods](../math.md)
