---
title: "Expected Value"
---

# Expected Value

The expected value is the probability-weighted average of a [random variable](random-variables.md) — the number a long run of draws settles around.
In epidemiology the basic reproduction number $R_0$ is exactly such an expectation: the expected number of secondary infections produced by one case in a fully susceptible population, just as expected survival time is the mean time a patient lives.
It anchors nearly every summary in statistics, from the [mean](measures-of-center.md) of a distribution to the target of an estimator.

## Definition

For a discrete random variable $X$ with probability mass function $p(x)$, \[ \mathbb{E}[X] = \sum_x x\,p(x). \]

For a continuous random variable with density $f(x)$, \[ \mathbb{E}[X] = \int_{-\infty}^{\infty} x\,f(x)\,dx. \]

The sum or [integral](integrals.md) must converge absolutely for the expectation to exist.

### Interpretation as a long-run average

If you draw $X$ independently many times, the running average of those draws approaches $\mathbb{E}[X]$.
This is not a metaphor — it is the [law of large numbers](law-of-large-numbers.md), and it is why $\mathbb{E}[X]$ is often called the "mean" of $X$.

## Linearity

Expectation is linear.
For constants $a, b$, \[ \mathbb{E}[aX + b] = a\,\mathbb{E}[X] + b, \] and for any two random variables, \[ \mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y]. \] The second identity holds even when $X$ and $Y$ are dependent — a fact used constantly to compute means of sums.

### Law of the unconscious statistician

To find the expected value of a function $g(X)$ you do **not** need the distribution of $g(X)$; you can weight $g$ by the distribution of $X$: \[ \mathbb{E}[g(X)] = \sum_x g(x)\,p(x) \quad\text{or}\quad \int g(x)\,f(x)\,dx. \]

## Worked example

**Fair die.** With $p(x) = 1/6$ for $x \in \{1,\dots,6\}$, \[ \mathbb{E}[X] = \frac{1+2+3+4+5+6}{6} = \frac{21}{6} = 3.5. \] The expected value need not be an attainable outcome.

**[Exponential](exponential-distribution.md).** For $X$ with density $f(x) = \lambda e^{-\lambda x}$ on $x \ge 0$, \[ \mathbb{E}[X] = \int_0^\infty x\,\lambda e^{-\lambda x}\,dx = \frac{1}{\lambda}. \] With rate $\lambda = 2$, the mean waiting time is $0.5$.

## Simulation

The sample average of many draws should land near $\mathbb{E}[X]$.

### R

```r
set.seed(1)
die <- sample(1:6, size = 1e6, replace = TRUE)
mean(die)              # ~ 3.5

exp_draws <- rexp(1e6, rate = 2)
mean(exp_draws)        # ~ 0.5
```

### Python

```python
import numpy as np
np.random.seed(1)

die = np.random.randint(1, 7, size=1_000_000)
print(die.mean())            # ~ 3.5

exp_draws = np.random.exponential(scale=1/2, size=1_000_000)
print(exp_draws.mean())      # ~ 0.5
```

<!-- python-output:auto -->
```text
3.503028
0.5008809237171852
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics
Random.seed!(1)

die = rand(1:6, 1_000_000)
println(mean(die))           # ~ 3.5

exp_draws = randexp(1_000_000) ./ 2   # rate 2 => mean 0.5
println(mean(exp_draws))     # ~ 0.5
```

## Why it matters for statistics

Expectation defines what an estimator is aiming at: an [estimator](statistical-inference.md) is unbiased when its expected value equals the parameter.
Linearity makes the mean of a sample average trivial to compute, and the law of the unconscious statistician gives [variances](measures-of-variability.md), moments, and likelihoods without ever deriving a new distribution.

## Related

- [Integrals](integrals.md)
- [Measures of Center](measures-of-center.md)
- [Measures of Variability](measures-of-variability.md)
- [Random Variables](random-variables.md)
- [The Law of Large Numbers](law-of-large-numbers.md)
- [Quantitative Methods](../math.md)
