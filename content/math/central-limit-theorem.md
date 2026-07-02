---
title: "The Central Limit Theorem"
---

# The Central Limit Theorem

The central limit theorem explains why the bell curve is everywhere: add up or average many independent effects and the result is approximately [normal](normal-distribution.md), no matter what the individual pieces look like. It is the reason normal-based inference works so broadly.

## Statement

Let $X_1, \dots, X_n$ be iid with mean $\mu$ and finite [variance](measures-of-variability.md) $\sigma^2$. As $n \to \infty$, the standardized sample mean [converges](limits.md) in distribution to a standard normal:
\[
\frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \to \mathcal{N}(0, 1).
\]
Equivalently, $\bar{X}$ is approximately $\mathcal{N}\!\big(\mu,\, \sigma^2/n\big)$ for large $n$. The remarkable part: this holds **regardless of the shape of the parent distribution** — skewed, discrete, bimodal — as long as the variance is finite.

### LLN vs. CLT

The [law of large numbers](law-of-large-numbers.md) says $\bar{X} \to \mu$ (the mean stops moving). The CLT is the finer statement: the leftover fluctuations, magnified by $\sqrt{n}$, are Gaussian. LLN gives the location; CLT gives the shape.

## Worked example

Suppose service times are [exponential](exponential-distribution.md) with rate $\lambda = 1$, so $\mu = 1$ and $\sigma = 1$ — a strongly right-skewed parent. Average $n = 50$ of them. The CLT says
\[
\bar{X} \approx \mathcal{N}\!\left(1,\ \frac{1}{50}\right), \qquad \operatorname{SD}(\bar{X}) = \frac{1}{\sqrt{50}} \approx 0.141.
\]
So $P(\bar{X} > 1.2) \approx P\!\left(Z > \frac{1.2 - 1}{0.141}\right) = P(Z > 1.41) \approx 0.079$, even though a single exponential draw exceeding $1.2$ has probability $e^{-1.2} \approx 0.30$. Averaging tames the skew.

## Simulation

Take means of samples from a skewed parent (exponential) and watch the histogram of means become bell-shaped as $n$ grows.

### R

```r
set.seed(11)
for (n in c(1, 5, 30)) {
  means <- replicate(10000, mean(rexp(n, rate = 1)))
  hist(means, breaks = 40, main = paste("n =", n), xlab = "sample mean")
  cat("n =", n, " skewness shrinks; SD =", round(sd(means), 3),
      " theory =", round(1 / sqrt(n), 3), "\n")
}
```

### Python

```python
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(11)

for i, n in enumerate((1, 5, 30)):
    means = np.array([np.random.exponential(1.0, n).mean()
                      for _ in range(10000)])
    plt.subplot(1, 3, i + 1); plt.hist(means, bins=40)
    plt.title(f"n={n}")
    print(f"n={n:>2} SD={means.std(ddof=1):.3f} theory={1/np.sqrt(n):.3f}")
plt.tight_layout()
```

### Julia

```julia
using Random, Statistics
Random.seed!(11)

for n in (1, 5, 30)
    means = [mean(randexp(n)) for _ in 1:10000]
    println("n=$n SD=", round(std(means), digits=3),
            " theory=", round(1 / sqrt(n), digits=3))
end
```

## Why it matters for statistics

The CLT is why $z$- and $t$-based [confidence intervals](confidence-intervals.md) and tests apply to means from almost any population, not just normal ones. It underwrites the normal approximation for proportions and sums, and it tells us how large a sample is "large enough" for inference to be trustworthy. Nearly every classical procedure leans on it.

## Related

- [Normal Distribution](normal-distribution.md)
- [Sampling Distributions](sampling-distributions.md)
- [The Law of Large Numbers](law-of-large-numbers.md)
- [Statistical Inference](statistical-inference.md)
- [Confidence Intervals](confidence-intervals.md)
- [Quantitative Methods](../math.md)
