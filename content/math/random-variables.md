---
title: "Random Variables"
---

# Random Variables

A random variable turns messy real-world outcomes into numbers we can add, average, and model.
It is the bridge between raw [probability](probability-basics.md) and the [distributions](distributions-overview.md) used throughout statistics and epidemiology.

## Definition

A **random variable** $X$ is a function that maps each outcome in the sample space to a real number:

\[
X : \Omega \to \mathbb{R}.
\]

For a coin flip, $\Omega = \{\text{heads}, \text{tails}\}$ and we might set $X(\text{heads}) = 1$, $X(\text{tails}) = 0$.
The randomness lives in which outcome occurs; $X$ just records it numerically.

## Discrete vs. continuous

- A **discrete** random variable takes values in a countable set (0, 1, 2, …): counts of cases, number of successes.
- A **continuous** random variable takes values in an interval of $\mathbb{R}$: heights, waiting times, concentrations.

## pmf vs. pdf

For a **discrete** RV, the **probability mass function (pmf)** gives the probability of each value:

\[
p(x) = \Pr(X = x), \qquad \sum_x p(x) = 1.
\]

For a **continuous** RV, single points have probability zero, so we use a **probability density function (pdf)** $f(x)$.
Probability is *[area under the density](integrals.md)*:

\[
\Pr(a \le X \le b) = \int_a^b f(x)\,dx, \qquad \int_{-\infty}^{\infty} f(x)\,dx = 1.
\]

The density integrating to 1 is the continuous analogue of the pmf summing to 1.

## The cumulative distribution function

Both types share the **cumulative distribution function (CDF)**:

\[
F(x) = \Pr(X \le x).
\]

The CDF is well-behaved for every random variable and has three defining properties:

1. **Non-decreasing**: if $x_1 \le x_2$ then $F(x_1) \le F(x_2)$.
2. **Limits**: $\displaystyle \lim_{x \to -\infty} F(x) = 0$ and $\displaystyle \lim_{x \to +\infty} F(x) = 1$.
3. **Right-continuous**.

For a continuous RV, the pdf is the [derivative](derivatives.md) of the CDF, $f(x) = F'(x)$.

## Worked example: a discrete RV

Let $X \sim \text{Binomial}(n = 3, p = 0.5)$ — the number of heads in three fair flips.
The pmf is $p(x) = \binom{3}{x}(0.5)^3$:

\[
p(0) = \tfrac{1}{8},\quad p(1) = \tfrac{3}{8},\quad p(2) = \tfrac{3}{8},\quad p(3) = \tfrac{1}{8}.
\]

These sum to 1.
The CDF steps upward: $F(1) = \Pr(X \le 1) = \tfrac{1}{8} + \tfrac{3}{8} = \tfrac{1}{2}$.

## Worked example: a continuous RV

Let $X \sim \text{Exponential}(\lambda = 2)$ with pdf $f(x) = 2 e^{-2x}$ for $x \ge 0$.
Its CDF is

\[
F(x) = \int_0^x 2 e^{-2t}\,dt = 1 - e^{-2x}.
\]

So $\Pr(X \le 1) = 1 - e^{-2} \approx 0.865$, and $F$ rises smoothly from 0 to 1.

## Computing it

Evaluate pmf/pdf and CDF directly with built-in distribution functions.

### R

```r
# Discrete: Binomial(3, 0.5)
dbinom(1, size = 3, prob = 0.5)   # pmf  P(X=1) = 0.375
pbinom(1, size = 3, prob = 0.5)   # cdf  P(X<=1) = 0.5

# Continuous: Normal(0, 1)
dnorm(0)                          # pdf at 0 = 0.3989
pnorm(1.96)                       # cdf  P(X<=1.96) = 0.975
```

### Python

```python
from scipy import stats

# Discrete: Binomial(3, 0.5)
print(stats.binom.pmf(1, n=3, p=0.5))   # 0.375
print(stats.binom.cdf(1, n=3, p=0.5))   # 0.5

# Continuous: Normal(0, 1)
print(stats.norm.pdf(0))                # 0.3989
print(stats.norm.cdf(1.96))             # 0.975
```

<!-- python-output:auto -->
```text
0.3750000000000001
0.5
0.3989422804014327
0.9750021048517795
```
<!-- /python-output:auto -->

### Julia

```julia
using Distributions

# Discrete: Binomial(3, 0.5)
pdf(Binomial(3, 0.5), 1)   # pmf = 0.375
cdf(Binomial(3, 0.5), 1)   # 0.5

# Continuous: Normal(0, 1)
pdf(Normal(0, 1), 0)       # 0.3989
cdf(Normal(0, 1), 1.96)    # 0.975
```

## Why it matters for statistics

Random variables are the objects statistics is *about*: an estimator is a random variable, a test statistic is a random variable, and data are realizations of random variables.
The pmf/pdf and CDF are the two universal descriptions of their behavior — the CDF in particular underlies [quantiles](measures-of-center.md), p-values, and the monotonic transformations used in simulation and maximum likelihood.

## Related

- [Distributions Overview](distributions-overview.md)
- [Monotonic Transformations](monotonic-transformations.md)
- [Probability Basics](probability-basics.md)
- [Expected Value](expected-value.md)
- [Integrals](integrals.md)
- [Quantitative Methods](../math.md)
