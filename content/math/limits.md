---
title: "Limits"
---

# Limits

A limit describes the value a function or sequence approaches as its input moves toward some point.
Biology is full of such limiting behaviors: as an epidemic runs its course the susceptible fraction approaches a fixed limit — the final epidemic size — and long-run averages of case counts converge.
Limits are the foundation of [derivatives](derivatives.md), [integrals](integrals.md), and the convergence theorems that make [statistical inference](statistical-inference.md) work.

## Intuitive and formal definition

Intuitively, $\lim_{n\to\infty} a_n = L$ means the terms $a_n$ get and stay arbitrarily close to $L$.
Formally ($\epsilon$-definition): for every $\epsilon > 0$ there exists an $N$ such that

\[
n > N \implies |a_n - L| < \epsilon.
\]

If such an $L$ exists the [sequence](sequences.md) **converges**; otherwise it **diverges**.

## Properties of limits

If $\lim a_n = A$ and $\lim b_n = B$, then

\[
\lim (a_n + b_n) = A + B,\quad
\lim (a_n b_n) = AB,\quad
\lim \frac{a_n}{b_n} = \frac{A}{B}\ (B \neq 0).
\]

## L'Hôpital's rule

For an indeterminate form $\tfrac{0}{0}$ or $\tfrac{\infty}{\infty}$,

\[
\lim_{x\to c}\frac{f(x)}{g(x)} = \lim_{x\to c}\frac{f'(x)}{g'(x)}.
\]

**Example:** $\displaystyle \lim_{x\to 0}\frac{\sin x}{x}$ is $\tfrac{0}{0}$.
Differentiating top and bottom gives $\lim_{x\to 0}\frac{\cos x}{1} = \cos 0 = 1$.
The same $\tfrac{0}{0}$ manoeuvre appears in disease models when taking small-time or large-population approximations, such as recovering a per-capita infection rate as a time interval shrinks to zero.

## Worked example

Consider $a_n = \frac{3n + 1}{n}= 3 + \frac{1}{n}$. As $n$ grows, $1/n \to 0$, so $a_n \to 3$. Checking $\epsilon = 0.01$: we need $|a_n - 3| = 1/n < 0.01$, i.e. $n > 100$.

## Computing it

### R

```r
# Numerically approach lim_{x->0} sin(x)/x
x <- 10^(-(1:6))
sin(x) / x        # 0.9983..., -> 1
```

### Python

```python
import sympy as sp

x, n = sp.symbols("x n")
print(sp.limit(sp.sin(x)/x, x, 0))        # 1
print(sp.limit((3*n + 1)/n, n, sp.oo))    # 3
```

<!-- python-output:auto -->
```text
1
3
```
<!-- /python-output:auto -->

### Julia

```julia
using Symbolics

@variables x
# Numeric check of sin(x)/x near 0
xs = 10.0 .^ (-(1:6))
sin.(xs) ./ xs        # -> 1.0
```

## Why it matters for statistics

Convergence of sequences of random quantities is the engine of large-sample theory.
The Weak [Law of Large Numbers](law-of-large-numbers.md) says the sample mean **converges in probability** to the true mean, $\bar{X}_n \xrightarrow{p} \mu$ — a probabilistic limit.
Understanding ordinary limits first makes these stochastic versions far less mysterious.

## Related

- [Sequences](sequences.md)
- [Series](series.md)
- [Derivatives](derivatives.md)
- [Integrals](integrals.md)
- [Law of Large Numbers](law-of-large-numbers.md)
- [Quantitative Methods](../math.md)
