---
title: "Series"
---

# Series

A series is the sum of the terms of a [sequence](sequences.md).
Series let us add up infinitely many contributions in closed form — the trick behind [expected values](expected-value.md) of count [distributions](distributions-overview.md) and many probability generating functions.

## Partial sums

Given a sequence $\{a_n\}$, the $N$-th **partial sum** is $S_N = \sum_{n=1}^{N} a_n$.
An infinite series $\sum_{n=1}^{\infty} a_n$ **converges** to $S$ if $S_N \to S$ as $N \to \infty$; otherwise it **diverges**.

## Arithmetic series

With first term $a$ and common difference $d$, the terms are $a, a+d, a+2d, \dots$ and the finite sum is

\[
\sum_{i=1}^{n} \big(a + (i-1)d\big) = \frac{n}{2}\,\big(2a + (n-1)d\big).
\]

## Geometric series

With ratio $r$, the terms are $a, ar, ar^2, \dots$. When $|r| < 1$ the infinite series converges:

\[
\sum_{n=1}^{\infty} a\,r^{\,n-1} = \frac{a}{1 - r}.
\]

## Power series

A power series $\sum_{n=0}^{\infty} c_n x^n$ defines a function on its interval of convergence.
The key example is

\[
\frac{1}{1 - x} = \sum_{n=0}^{\infty} x^{n},\qquad |x| < 1.
\]

Note the **harmonic series** $\sum_{n=1}^{\infty} \tfrac{1}{n}$ **diverges**, even though its terms shrink to $0$ — small terms are not enough for convergence.

## Worked example

Let $a = 1$, $r = 1/2$.
The infinite geometric series is

\[
\sum_{n=1}^{\infty} \left(\tfrac{1}{2}\right)^{n-1} = \frac{1}{1 - \tfrac12} = 2.
\]

The partial sum to $n = 10$ terms is $2 - (1/2)^{9} \approx 1.99805$, already very close to $2$.

## Computing it

### R

```r
r <- 0.5; a <- 1; n <- 10
partial <- sum(a * r^(0:(n - 1)))   # 1.998047
closed  <- a / (1 - r)              # 2
c(partial, closed)
```

### Python

```python
r, a, n = 0.5, 1, 10
partial = sum(a * r**k for k in range(n))   # 1.998046875
closed  = a / (1 - r)                        # 2.0
print(partial, closed)
```

### Julia

```julia
r, a, n = 0.5, 1, 10
partial = sum(a * r^k for k in 0:(n - 1))   # 1.998046875
closed  = a / (1 - r)                        # 2.0
partial, closed
```

## Why it matters for statistics

Geometric series give the mean of the geometric distribution and normalize infinite discrete distributions.
Power series underlie moment and probability generating functions, and [Taylor series](taylor-series.md) (a special power series) drive approximations like the delta method.
Recognizing when a series converges tells you whether an expectation is even finite.

## Related

- [Sequences](sequences.md)
- [Taylor and Maclaurin Series](taylor-series.md)
- [Limits](limits.md)
- [Expected Value](expected-value.md)
- [Quantitative Methods](../math.md)
