---
title: "The Law of Large Numbers"
---

# The Law of Large Numbers

The law of large numbers is the guarantee that averaging works: pile up enough independent observations and the sample mean settles on the true mean.
It is the formal reason a long-run average is a trustworthy estimate.

![Running averages of die rolls converge to the true mean of 3.5 as the sample grows.](../assets/figures/law-of-large-numbers.svg)

## Statement

Let $X_1, X_2, \dots$ be [independent](probability-basics.md) and identically distributed with mean $\mu = \mathbb{E}[X_i]$, and let \[ \bar{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i. \] The **weak law of large numbers** says $\bar{X}_n$ converges to $\mu$ in probability: for any tolerance $\varepsilon > 0$, \[
P\big(|\bar{X}_n - \mu| > \varepsilon\big) \to 0 \quad\text{as } n \to \infty.
\] Informally, $\bar{X}_n \to \mu$.
The stronger version (the strong law) gives convergence with probability one.

### Connection to limits

This is a probabilistic [limit](limits.md).
Recall $\operatorname{SD}(\bar{X}_n) = \sigma/\sqrt{n} \to 0$: as the [standard error](measures-of-variability.md) vanishes, the [sampling distribution](sampling-distributions.md) of $\bar{X}_n$ collapses onto the single point $\mu$.
Note the LLN describes *where* $\bar{X}_n$ lands; the [central limit theorem](central-limit-theorem.md) describes the *shape* of its fluctuations along the way.

## Worked example

A fair coin scores $1$ for heads, $0$ for tails, so $\mu = \mathbb{E}[X] = 0.5$.
After $n$ flips the sample proportion of heads is $\bar{X}_n$.
With $n = 10$ a run of $7$ heads ($\bar{X}_{10} = 0.7$) is unremarkable, but by $n = 10{,}000$ the proportion is almost surely within a hundredth of $0.5$, because the standard error has dropped to $0.5/\sqrt{10000} = 0.005$.

## Simulation

Track the *running* mean and watch it converge to the true value.

### R

```r
set.seed(3)
flips <- rbinom(10000, size = 1, prob = 0.5)
running <- cumsum(flips) / seq_along(flips)
plot(running, type = "l", ylim = c(0, 1),
     xlab = "n", ylab = "running mean")
abline(h = 0.5, col = "red")
tail(running, 1)     # close to 0.5
```

### Python

```python
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(3)

flips = np.random.binomial(1, 0.5, size=10000)
running = np.cumsum(flips) / np.arange(1, len(flips) + 1)

plt.plot(running)
plt.axhline(0.5, color="red")
plt.xlabel("n"); plt.ylabel("running mean")
print(running[-1])   # close to 0.5
```

### Julia

```julia
using Random, Statistics
Random.seed!(3)

flips = rand(0:1, 10000)
running = cumsum(flips) ./ (1:length(flips))
println(running[end])   # close to 0.5
```

## Why it matters for statistics

The LLN justifies estimation itself: sample means, proportions, and Monte Carlo integrals are reliable because they converge to the quantities they estimate.
It is also the foundation of [simulation](../programming/simulation-toolkit.md) — every "run it many times and average" argument on this site rests on it, including the empirical means used to approximate an [expected value](expected-value.md).

## Related

- [Limits](limits.md)
- [Expected Value](expected-value.md)
- [The Central Limit Theorem](central-limit-theorem.md)
- [Sampling Distributions](sampling-distributions.md)
- [Quantitative Methods](../math.md)
