---
title: "Exponentials and Logarithms"
---

# Exponentials and Logarithms

Exponentials describe multiplicative growth and logarithms undo them. In statistics they are everywhere: [log-likelihoods](maximum-likelihood.md) turn products into sums, and log scales tame skewed, multiplicative data.

## Exponent rules

For any base $a > 0$:

\[
a^m a^n = a^{m+n},\qquad \frac{a^m}{a^n} = a^{m-n},\qquad (a^m)^n = a^{mn}.
\]

Negative and fractional exponents extend this: $a^{-n} = 1/a^{n}$ and $a^{1/n} = \sqrt[n]{a}$, so $a^0 = 1$.

## The natural base $e$

The constant $e \approx 2.71828$ arises as a [limit](limits.md) and as a [series](series.md):

\[
e = \lim_{n\to\infty}\left(1 + \frac{1}{n}\right)^{n},
\qquad
e^{x} = \sum_{n=0}^{\infty} \frac{x^{n}}{n!}.
\]

## Logarithm identities

The natural log $\ln$ is the inverse of $e^x$: $\ln(e^x) = x$ and $e^{\ln x} = x$ for $x > 0$. Its identities mirror the exponent rules:

\[
\ln(ab) = \ln a + \ln b,\quad
\ln\!\left(\tfrac{a}{b}\right) = \ln a - \ln b,\quad
\ln(a^{b}) = b\,\ln a.
\]

**Change of base:** $\log_b x = \dfrac{\ln x}{\ln b}$.

## Worked example

Take $a = 3$, $b = 4$. Then $\ln(3 \cdot 4) = \ln 12 \approx 2.4849$, while $\ln 3 + \ln 4 \approx 1.0986 + 1.3863 = 2.4849$ — the product identity holds. And with $n = 10{,}000$, $(1 + 1/n)^n \approx 2.71815$, already close to $e$.

## Computing it

### R

```r
# Verify the limit for e
n <- 1e6
(1 + 1/n)^n          # ~2.718280
exp(1)               # 2.718282

# log-of-product identity
all.equal(log(3 * 4), log(3) + log(4))   # TRUE
```

### Python

```python
import numpy as np

n = 10**6
print((1 + 1/n)**n)          # ~2.7182804
print(np.e)                  # 2.718281828...

# log-of-product identity
print(np.isclose(np.log(3 * 4), np.log(3) + np.log(4)))  # True
```

### Julia

```julia
n = 10^6
(1 + 1/n)^n           # ~2.7182804
exp(1)                # 2.718281828...

# log-of-product identity
isapprox(log(3 * 4), log(3) + log(4))   # true
```

## Why it matters for statistics

Likelihoods are products $\prod_i f(x_i)$ that underflow to zero numerically; taking $\ln$ converts them to sums $\sum_i \ln f(x_i)$ that are stable and easy to differentiate for maximum likelihood. Log scales also linearize exponential growth (epidemic curves) and symmetrize right-skewed data.

## Related

- [Functions and Graphs](functions-and-graphs.md)
- [Series](series.md)
- [Limits](limits.md)
- [Maximum Likelihood](maximum-likelihood.md)
- [Quantitative Methods](../math.md)
