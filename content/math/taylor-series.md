---
title: "Taylor and Maclaurin Series"
---

# Taylor and Maclaurin Series

A Taylor series approximates a smooth function by a polynomial built from its [derivatives](derivatives.md) at a point.
This local approximation is the workhorse behind the delta method, Newton-type [optimization](optimization.md), and many large-sample expansions.

## Taylor expansion

If $f$ is infinitely differentiable near $a$,

\[
f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}\,(x - a)^{n}
= f(a) + f'(a)(x - a) + \frac{f''(a)}{2!}(x - a)^2 + \cdots
\]

A **Maclaurin series** is the special case $a = 0$.

## Key expansions

\[
\begin{aligned}
e^{x} &= \sum_{n=0}^{\infty} \frac{x^{n}}{n!} = 1 + x + \frac{x^2}{2} + \frac{x^3}{6} + \cdots \\
\sin x &= x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots \\
\ln(1 + x) &= x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots \quad (|x| < 1)
\end{aligned}
\]

:::spoiler Show where these coefficients come from

Every Maclaurin coefficient is a derivative at $0$ divided by a factorial, $f(x) = \sum_{n\ge 0} \frac{f^{(n)}(0)}{n!}x^n$.
For $f(x) = e^x$ every derivative is again $e^x$, so $f^{(n)}(0) = e^0 = 1$ for all $n$:

\[
e^x = \sum_{n=0}^{\infty} \frac{1}{n!}x^n = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots .
\]

For $f(x) = \sin x$ the derivatives cycle $\cos x, -\sin x, -\cos x, \sin x, \dots$, so at $x = 0$ the values $f^{(n)}(0)$ cycle $0, 1, 0, -1$.
Only the odd powers survive, with alternating sign:

\[
\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots = \sum_{k=0}^{\infty} \frac{(-1)^k}{(2k+1)!}x^{2k+1} .
\]

The same bookkeeping on $\cos x$ keeps only the even powers.

:::

## Worked example: successive polynomials for $\sin x$

Watching the approximation improve term by term is the best way to build intuition.
The Maclaurin polynomials of $\sin x$ use only odd powers; write $T_N$ for the degree-$N$ truncation.

![Taylor polynomials of sin x of degree 1, 3, 5, 7: each added term hugs the curve over a wider interval before peeling away.](../assets/figures/taylor-series.svg)

Each higher-degree polynomial tracks $\sin x$ over a wider window before peeling off.
Evaluate them at $x = \tfrac{\pi}{2} \approx 1.5708$, where the true value is $\sin(\pi/2) = 1$:

\[
\begin{aligned}
T_1 &= x = 1.5708 &&(\text{error } +0.5708) \\
T_3 &= x - \tfrac{x^3}{3!} = 0.9248 &&(\text{error } -0.0752) \\
T_5 &= T_3 + \tfrac{x^5}{5!} = 1.0045 &&(\text{error } +0.0045) \\
T_7 &= T_5 - \tfrac{x^7}{7!} = 0.99985 &&(\text{error } -0.00015)
\end{aligned}
\]

Each extra pair of terms cuts the error by more than an order of magnitude near the center of expansion.

## How good is the approximation? The remainder

Truncating after the degree-$N$ term leaves the **Lagrange remainder**

\[
f(x) - T_N(x) = \frac{f^{(N+1)}(\xi)}{(N+1)!}\,(x - a)^{N+1}
\]

for some $\xi$ between $a$ and $x$.
For $\sin x$ every derivative is bounded by $1$, so $|f(x) - T_N(x)| \le \dfrac{|x - a|^{N+1}}{(N+1)!}$.
At $x = \pi/2$ with $N = 7$ this bounds the error by $\dfrac{(\pi/2)^8}{8!} \approx 9.2\times 10^{-4}$, comfortably above the $1.5\times 10^{-4}$ we actually saw.
The factorial in the denominator is why Taylor series converge so fast close to $a$ and why the error explodes once $|x-a|$ grows large — exactly the peeling-off you see in the figure.

## Computing it

### R

```r
x <- pi / 2
Tn <- function(N) sum(sapply(seq(1, N, by = 2),
                             \(n) (-1)^((n - 1) / 2) * x^n / factorial(n)))
approx <- sapply(c(1, 3, 5, 7), Tn)
rbind(approx, error = sin(x) - approx)
#            [,1]     [,2]     [,3]      [,4]
# approx  1.57080  0.92483  1.00452  0.999849
# error  -0.57080  0.07517 -0.00452  0.000151
```

### Python

```python
import sympy as sp
x = sp.symbols("x")
print(sp.series(sp.sin(x), x, 0, 8))   # x - x**3/6 + x**5/120 - x**7/5040 + O(x**8)

import math
xv = math.pi / 2
Tn = lambda N: sum((-1)**((n - 1)//2) * xv**n / math.factorial(n)
                   for n in range(1, N + 1, 2))
for N in (1, 3, 5, 7):
    print(N, Tn(N), math.sin(xv) - Tn(N))   # error shrinks ~10x each step
```

<!-- python-output:auto -->
```text
x - x**3/6 + x**5/120 - x**7/5040 + O(x**8)
1 1.5707963267948966 -0.5707963267948966
3 0.9248322292886504 0.07516777071134961
5 1.0045248555348174 -0.004524855534817407
7 0.9998431013994987 0.00015689860050127624
```
<!-- /python-output:auto -->

### Julia

```julia
using Symbolics
xv = pi / 2
Tn(N) = sum((-1)^((n - 1) ÷ 2) * xv^n / factorial(n) for n in 1:2:N)
[(N, Tn(N), sin(xv) - Tn(N)) for N in (1, 3, 5, 7)]
# error: -0.571, +0.075, -0.0045, +0.00015
```

## Why it matters for statistics

The delta method approximates the [variance](measures-of-variability.md) of a transformed estimator $g(\hat\theta)$ via a first-order Taylor expansion, $g(\hat\theta) \approx g(\theta) + g'(\theta)(\hat\theta - \theta)$, so that $\operatorname{Var}(g(\hat\theta)) \approx [g'(\theta)]^2 \operatorname{Var}(\hat\theta)$.
For example, a proportion $\hat p$ has variance $p(1-p)/n$; the log-odds $g(p) = \log\frac{p}{1-p}$ has derivative $g'(p) = \frac{1}{p(1-p)}$, so the delta method gives $\operatorname{Var}(\log\text{-odds}) \approx \frac{1}{n\,p(1-p)}$ — with $p = 0.2$, $n = 100$ that is a standard error of $0.25$, exactly the log-odds standard error a [logistic regression](logistic-regression.md) reports.
Second-order expansions of the [log-likelihood](maximum-likelihood.md) give the Fisher information and Newton-Raphson updates for maximum likelihood.
In epidemiology the same idea linearizes a nonlinear transmission rate around an operating point so a model can be studied near an equilibrium, and the delta method then propagates measurement error into the resulting estimates.
In short, Taylor series turn intractable nonlinear quantities into tractable linear or quadratic ones.

## Related

- [Series](series.md)
- [Derivatives](derivatives.md)
- [Limits](limits.md)
- [Optimization](optimization.md)
- [Maximum Likelihood](maximum-likelihood.md)
- [Quantitative Methods](../math.md)
