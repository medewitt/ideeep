---
title: "Bayesian Inference"
---

# Bayesian Inference

Bayesian inference treats an unknown parameter as a random quantity and updates our beliefs about it as data arrive.
The engine is Bayes' theorem, which combines what we knew before with what the data tell us.

## Bayes' theorem for parameters

Let $\theta$ be a parameter and $y$ the observed data.
Bayesian inference computes the **posterior** distribution of $\theta$ given $y$:

\[
p(\theta\mid y)=\frac{p(y\mid\theta)\,p(\theta)}{p(y)}\propto \text{likelihood}\times\text{prior}.
\]

The pieces each have a name.

- The **prior** $p(\theta)$ encodes beliefs about $\theta$ before seeing the data.
- The **likelihood** $p(y\mid\theta)$ is the [probability](probability-basics.md) of the data as a function of $\theta$ (the same object maximized in [maximum likelihood estimation](maximum-likelihood.md)).
- The **posterior** $p(\theta\mid y)$ is the updated belief after combining prior and data.
- The **marginal likelihood** (or **evidence**) $p(y)$ normalizes the posterior so it integrates to one:

\[
p(y)=\int p(y\mid\theta)\,p(\theta)\,d\theta.
\]

Because $p(y)$ does not depend on $\theta$, we often work with the unnormalized form $p(\theta\mid y)\propto p(y\mid\theta)\,p(\theta)$ and restore the constant at the end.

## Conjugate priors

For some prior–likelihood pairs the posterior belongs to the same family as the prior, giving a closed-form update.
Such priors are called **conjugate**.

- **Beta–Binomial.** With a $\text{Beta}(a,b)$ prior on a proportion and $k$ successes in $n$ [Binomial](binomial-distribution.md) trials, the posterior is $\text{Beta}(a+k,\,b+n-k)$.
- **Gamma–Poisson.** With a $\text{Gamma}(a,b)$ prior on a rate and Poisson counts, observing total $s=\sum_i y_i$ over $n$ observations gives a $\text{Gamma}(a+s,\,b+n)$ posterior.
- **Normal–Normal.** With a [Normal](normal-distribution.md) prior on a mean and Normal data of known variance, the posterior is again Normal, its mean a precision-weighted average of prior mean and sample mean.

Conjugacy is convenient but not required; when it fails we sample from the posterior with [Markov chain Monte Carlo](mcmc.md).
The [distributions overview](distributions-overview.md) collects the families used above.

## Summarizing the posterior

The posterior is a full distribution, but we usually report a few summaries.

- **Posterior mean** $\mathbb{E}[\theta\mid y]$, a common point estimate.
- **MAP** (maximum a posteriori), the mode $\arg\max_\theta p(\theta\mid y)$.
- **Credible interval**, an interval containing a stated posterior probability, e.g. a central 95% interval between the 2.5% and 97.5% posterior quantiles.

Under a flat (constant) prior the posterior is proportional to the likelihood, so the MAP coincides with the maximum likelihood estimate.

### Credible vs. confidence intervals

A 95% **credible interval** admits the direct statement that, given the data and prior, $\theta$ lies in the interval with probability $0.95$.
A frequentist [confidence interval](confidence-intervals.md) makes no such probability claim about $\theta$: instead, 95% of intervals built by the same procedure across repeated samples would cover the fixed true value.
The Bayesian statement is about the parameter; the frequentist one is about the procedure.

## Worked example: estimating a proportion

Suppose we test a diagnostic assay on $n=20$ samples and observe $k=12$ positives, and we want the positive fraction $\theta$.
Start from a uniform prior $\text{Beta}(1,1)$, which expresses no preference among proportions.
The Beta–Binomial rule gives the posterior

\[
\theta\mid y \sim \text{Beta}(1+12,\ 1+20-12)=\text{Beta}(13,\,9).
\]

The posterior mean is $\dfrac{13}{13+9}=\dfrac{13}{22}\approx 0.591$, slightly shrunk from the raw fraction $12/20=0.6$ toward the prior mean $0.5$.
A 95% central credible interval runs between the 2.5% and 97.5% quantiles of $\text{Beta}(13,9)$, approximately $[0.385,\,0.782]$.
We conclude the positive fraction is most plausibly near 0.59, with the data leaving substantial uncertainty.

## In code

Analytic Beta–Binomial posterior plus a grid approximation that works even without conjugacy.

### R

```r
set.seed(1)
a <- 1; b <- 1        # Beta(1,1) prior
k <- 12; n <- 20      # data

# Analytic posterior: Beta(a+k, b+n-k)
ap <- a + k; bp <- b + n - k
post_mean <- ap / (ap + bp)
ci <- qbeta(c(0.025, 0.975), ap, bp)
c(mean = post_mean, lo = ci[1], hi = ci[2])
# mean 0.5909  lo 0.3847  hi 0.7817

# Grid approximation (no conjugacy needed)
grid <- seq(0, 1, length.out = 2001)
post <- dbeta(grid, a, b) * dbinom(k, n, grid)
post <- post / sum(post)                 # normalize on the grid
cdf  <- cumsum(post)
grid[c(which.min(abs(cdf - 0.025)), which.min(abs(cdf - 0.975)))]
# 0.385 0.782  (matches the analytic interval)
```

### Python

```python
import numpy as np
from scipy.stats import beta, binom

np.random.seed(1)
a, b = 1, 1          # prior
k, n = 12, 20        # data

ap, bp = a + k, b + n - k
print(ap / (ap + bp))                 # 0.5909 posterior mean
print(beta.ppf([0.025, 0.975], ap, bp))  # [0.3847 0.7817]

# Grid approximation
grid = np.linspace(0, 1, 2001)
post = beta.pdf(grid, a, b) * binom.pmf(k, n, grid)
post /= post.sum()
cdf = np.cumsum(post)
lo = grid[np.argmin(np.abs(cdf - 0.025))]
hi = grid[np.argmin(np.abs(cdf - 0.975))]
print(lo, hi)                          # 0.385 0.782
```

<!-- python-output:auto -->
```text
0.5909090909090909
[0.38435439 0.78180314]
0.384 0.7815
```
<!-- /python-output:auto -->

### Julia

```julia
using Distributions, Random
Random.seed!(1)
a, b = 1, 1
k, n = 12, 20

post = Beta(a + k, b + n - k)
println(mean(post))                    # 0.5909
println(quantile.(post, [0.025, 0.975]))  # [0.3847, 0.7817]

# Grid approximation
grid = range(0, 1, length = 2001)
w = pdf.(Beta(a, b), grid) .* pdf.(Binomial(n, collect(grid)), k)
w ./= sum(w)
cdf = cumsum(w)
lo = grid[argmin(abs.(cdf .- 0.025))]
hi = grid[argmin(abs.(cdf .- 0.975))]
println((lo, hi))                      # (0.385, 0.782)
```

For models without conjugate priors, probabilistic-programming tools such as Stan, PyMC, and Turing.jl draw posterior samples automatically.

## Why it matters

Bayesian inference gives a coherent way to combine prior knowledge with data and to express conclusions as probabilities about the quantities we actually care about.
It handles small samples, hierarchical structure, and prior information gracefully, and its credible intervals answer the question practitioners usually mean to ask.
These ideas underpin much of modern epidemiological modeling, from estimating prevalence to fitting transmission dynamics.

## Related

- [Probability Basics](probability-basics.md)
- [Maximum Likelihood Estimation](maximum-likelihood.md)
- [Markov Chain Monte Carlo](mcmc.md)
- [Binomial Distribution](binomial-distribution.md)
- [Normal Distribution](normal-distribution.md)
- [Confidence Intervals](confidence-intervals.md)
- [Distributions Overview](distributions-overview.md)
- [Quantitative Methods](../math.md)
