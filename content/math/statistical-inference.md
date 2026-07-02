---
title: "Statistical Inference"
---

# Statistical Inference

Statistical inference is how we reason from a limited *sample* back to the *population* that produced it. Every poll, clinical trial, and epidemiological estimate rests on this leap from "what we saw" to "what is true."

## The core pipeline

The logic of inference flows in a loop:

\[
\text{Population} \;\to\; \text{Parameter } \theta \;\to\; \text{Sample} \;\to\; \text{Estimate } \hat{\theta}
\]

- **Population**: the full set of units we care about (all adults in a country, all possible patients, every mosquito in a region). Often it is conceptual or infinite.
- **Parameter** ($\theta$): a fixed but unknown number describing the population, such as a mean $\mu$, a proportion $p$, or a rate $\lambda$.
- **Sample**: a finite subset of units we actually observe, $X_1, X_2, \dots, X_n$.
- **Statistic / estimator**: a function of the sample used to guess the parameter, written $\hat{\theta} = T(X_1, \dots, X_n)$. For example the sample mean $\bar{X} = \frac{1}{n}\sum_{i=1}^{n} X_i$ estimates $\mu$.

The goal of inference is to use the observable estimate $\hat{\theta}$ to say something rigorous about the unobservable parameter $\theta$.

## The data-generating process

Behind any dataset we imagine a **data-generating process (DGP)**: a probabilistic mechanism that produces the data. Formally we assume the observations are draws from a distribution indexed by the parameter,

\[
X_1, \dots, X_n \overset{\text{iid}}{\sim} f(x \mid \theta).
\]

The DGP is a *model* of reality. Inference asks: given data that plausibly came from $f(x\mid\theta)$, which values of $\theta$ are credible? Choosing a DGP makes the problem tractable and honest about assumptions.

## A statistic is random

The crucial insight: because the sample is random, **any statistic computed from it is also a [random variable](random-variables.md)**. Draw a different sample and you get a different $\hat{\theta}$. This sample-to-sample variability is not a nuisance to be ignored; it is exactly what lets us quantify uncertainty.

A good estimator has its distribution centered near $\theta$ (low bias) and tightly concentrated (low variance). The distribution of $\hat{\theta}$ across hypothetical repeated samples is called its [sampling distribution](sampling-distributions.md).

## Worked example

Suppose the DGP is $X \sim \text{Normal}(\mu = 170,\ \sigma = 10)$ (adult heights in cm). The parameter of interest is $\mu = 170$, which in real life we would not know.

We draw a single sample of $n = 25$ people and compute $\bar{X}$. We might get $\bar{X} = 168.4$. A different 25 people might give $\bar{X} = 171.2$. Neither equals $170$ exactly, yet both cluster around it. If we could repeat the sampling many times, the collection of $\bar{X}$ values would average to $\mu$ and have [standard deviation](measures-of-variability.md) $\sigma / \sqrt{n} = 10/5 = 2$.

## Simulation

We define a DGP, draw many samples, and watch the sample means scatter around the true parameter.

### R

```r
set.seed(1)
mu <- 170; sigma <- 10; n <- 25

# Draw 10,000 samples, compute the mean of each
means <- replicate(10000, mean(rnorm(n, mu, sigma)))

mean(means)  # ~170: estimator is (nearly) unbiased
sd(means)    # ~2.0: matches sigma / sqrt(n)
```

### Python

```python
import numpy as np
rng = np.random.default_rng(1)
mu, sigma, n = 170, 10, 25

# Each row is a sample; average across columns
samples = rng.normal(mu, sigma, size=(10_000, n))
means = samples.mean(axis=1)

print(means.mean())  # ~170
print(means.std())   # ~2.0  (= sigma / sqrt(n))
```

### Julia

```julia
using Random, Statistics, Distributions
Random.seed!(1)
mu, sigma, n = 170, 10, 25

dgp = Normal(mu, sigma)
means = [mean(rand(dgp, n)) for _ in 1:10_000]

mean(means)  # ~170
std(means)   # ~2.0  (= sigma / sqrt(n))
```

## Why it matters for statistics

Inference is the foundation of the entire discipline: estimation, [hypothesis testing](hypothesis-testing.md), and [confidence intervals](confidence-intervals.md) all describe the behavior of a random statistic relative to a fixed parameter. Recognizing that $\hat{\theta}$ has a *distribution* — not just a value — is what separates a point guess from a scientific claim with quantified uncertainty. In epidemiology, this is how a prevalence estimate from a [survey](survey-sampling.md) becomes a defensible statement about a whole population.

## Related

- [Sampling Distributions](sampling-distributions.md)
- [Expected Value](expected-value.md)
- [Maximum Likelihood](maximum-likelihood.md)
- [Central Limit Theorem](central-limit-theorem.md)
- [Confidence Intervals](confidence-intervals.md)
- [Quantitative Methods](../math.md)
