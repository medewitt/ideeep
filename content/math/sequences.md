---
title: "Sequences"
---

# Sequences

A sequence is an ordered list of numbers indexed by the positive integers.
Sequences model iterative estimators, sampling schemes, and the limiting behavior that underlies [convergence](limits.md) results in statistics.

## Definition and notation

A sequence $\{a_n\}$ assigns a value $a_n$ to each index $n = 1, 2, 3, \dots$.
A **finite** sequence has a last term; an **infinite** one continues forever.
A sample of size $N$ is often written $\{x_i\}_{i=1}^{N}$.

## Bounded and monotonic sequences

- **Bounded:** there exist numbers $m, M$ with $m \le a_n \le M$ for all $n$.
- **Increasing:** $a_{n+1} \ge a_n$ for all $n$; **decreasing:** $a_{n+1} \le a_n$.
- **Strictly [monotonic](monotonic-transformations.md):** the inequality is strict, $a_{n+1} > a_n$ (or $<$), so no two terms are equal.

Strict monotonicity matters because a strictly increasing function is **invertible** — this is exactly why a continuous [cumulative distribution function (CDF)](random-variables.md), which is strictly increasing on its support, has a well-defined inverse (the [quantile](measures-of-center.md) function).

## Worked example

Let $a_n = \sqrt{n}$: the terms $1, 1.414, 1.732, 2, \dots$ are strictly increasing and unbounded above.

Let $b_n = 1/n$: the terms $1, 0.5, 0.333, 0.25, \dots$ are strictly decreasing, bounded in $(0, 1]$, and approach $0$ as $n \to \infty$.

## Computing it

### R

```r
n <- 1:10
a <- sqrt(n)     # increasing
b <- 1 / n       # decreasing to 0
plot(n, a, type = "b")
all(diff(a) > 0)   # TRUE (strictly increasing)
all(diff(b) < 0)   # TRUE (strictly decreasing)
```

### Python

```python
import numpy as np
import matplotlib.pyplot as plt

n = np.arange(1, 11)
a = np.sqrt(n)          # increasing
b = 1 / n               # decreasing to 0
plt.plot(n, a, marker="o")
print(np.all(np.diff(a) > 0))   # True
print(np.all(np.diff(b) < 0))   # True
```

### Julia

```julia
using Plots

n = 1:10
a = sqrt.(n)            # increasing
b = 1 ./ n              # decreasing to 0
plot(n, a, marker = :circle)
all(diff(a) .> 0)       # true
all(diff(b) .< 0)       # true
```

## Why it matters for statistics

Estimators computed over growing samples form sequences, and questions like "does $\bar{X}_n$ settle down?" are questions about sequence convergence.
Strict monotonicity of CDFs guarantees quantiles are uniquely defined, which underpins simulation, inverse-transform sampling, and [confidence intervals](confidence-intervals.md).

## Related

- [Limits](limits.md)
- [Series](series.md)
- [Law of Large Numbers](law-of-large-numbers.md)
- [Monotonic Transformations](monotonic-transformations.md)
- [Quantitative Methods](../math.md)
