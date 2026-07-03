---
title: "Mathematical Notation"
---

# Mathematical Notation

A compact shared vocabulary of symbols used throughout math and statistics.
Knowing them lets you read [likelihoods](maximum-likelihood.md), [probability](probability-basics.md) statements, and model definitions without stumbling.

## Sets and logic

We often work with the real numbers $\mathbb{R}$.
A set $A$ can be a **subset** of another, $A \subset B$, and an object can be an **element** of a set, $x \in A$.
Two events combine via **union** $A \cup B$ (either) and **intersection** $A \cap B$ (both).

Logical shorthand: **for all** $\forall$, **there exists** $\exists$, and **implies** $\Rightarrow$.
In probability we write **distributed as** $X \sim \mathcal{N}(0,1)$, and **independence** as $X \perp Y$ (or the statistical form $X \perp\!\!\!\perp Y$).

## Sums, products, and counting

The **summation** $\sum_{i=1}^{n} a_i = a_1 + a_2 + \cdots + a_n$ adds terms; the **product** $\prod_{i=1}^{n} a_i = a_1 a_2 \cdots a_n$ multiplies them.
The **factorial** is $n! = n\,(n-1)\cdots 2 \cdot 1$, and the **binomial coefficient** counts subsets:

\[
\binom{n}{k} = \frac{n!}{k!\,(n-k)!}.
\]

## Symbol reference

| Symbol | Meaning | LaTeX |
| --- | --- | --- |
| $\mathbb{R}$ | real numbers | `\mathbb{R}` |
| $\in$ | element of | `\in` |
| $\subset$ | subset of | `\subset` |
| $\cup$ | union | `\cup` |
| $\cap$ | intersection | `\cap` |
| $\forall$ | for all | `\forall` |
| $\exists$ | there exists | `\exists` |
| $\Rightarrow$ | implies | `\Rightarrow` |
| $\sim$ | distributed as | `\sim` |
| $\perp\!\!\!\perp$ | independent | `\perp\!\!\!\perp` |
| $\sum$ | summation | `\sum` |
| $\prod$ | product | `\prod` |
| $n!$ | factorial | `n!` |
| $\binom{n}{k}$ | binomial coefficient | `\binom{n}{k}` |

## Writing formulas in LaTeX

- Fractions: `\frac{a}{b}` renders as $\frac{a}{b}$.
- Greek letters: `\alpha, \beta, \mu, \sigma` render as $\alpha, \beta, \mu, \sigma$.
- Sums and products: `\sum_{i=1}^{n} i` gives $\sum_{i=1}^{n} i$ and `\prod_{i=1}^{n} i` gives $\prod_{i=1}^{n} i$.
- Distributed as: `X \sim \mathcal{N}(\mu, \sigma^2)` gives $X \sim \mathcal{N}(\mu, \sigma^2)$.

## Worked example

For $n = 5$ and $k = 2$:

\[
\sum_{i=1}^{5} i = 15,\qquad \prod_{i=1}^{5} i = 5! = 120,\qquad \binom{5}{2} = \frac{120}{2 \cdot 6} = 10.
\]

## Computing it

### R

```r
n <- 5; k <- 2
sum(1:n)        # 15
prod(1:n)       # 120
factorial(n)    # 120
choose(n, k)    # 10
```

### Python

```python
import math
n, k = 5, 2
print(sum(range(1, n + 1)))       # 15
print(math.prod(range(1, n + 1))) # 120
print(math.factorial(n))          # 120
print(math.comb(n, k))            # 10
```

### Julia

```julia
n, k = 5, 2
sum(1:n)          # 15
prod(1:n)         # 120
factorial(n)      # 120
binomial(n, k)    # 10
```

## Why it matters for statistics

Statistical models are written in this notation: likelihoods are products $\prod_i f(x_i)$, [expectations](expected-value.md) are sums $\sum_i x_i p_i$, and independence assumptions ($X \perp\!\!\!\perp Y$) justify factoring joint [distributions](distributions-overview.md).
Fluency here is the prerequisite for everything that follows.

## Related

- [The Language of Mathematics](language-of-mathematics.md)
- [Functions and Graphs](functions-and-graphs.md)
- [Series](series.md)
- [Probability Basics](probability-basics.md)
- [Expected Value](expected-value.md)
- [Exponentials and Logarithms](exponentials-and-logarithms.md)
- [Quantitative Methods](../math.md)
