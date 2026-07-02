---
title: "Confidence Intervals"
---

# Confidence Intervals

A confidence interval reports a range of plausible values for a parameter—a mean incubation time, a prevalence—together with an estimate's uncertainty. It shifts attention from a single point estimate to the precision behind it.

## The idea

A **confidence interval (CI)** is an interval, computed from data, designed so that the procedure captures the true parameter a specified fraction of the time (the *confidence level*, e.g. 95%) across repeated samples.

For a population mean with unknown variance, the standard $100(1-\alpha)\%$ CI is

\[
\bar{x} \pm t_{\alpha/2,\,n-1}\,\frac{s}{\sqrt{n}},
\]

where $\bar{x}$ is the sample mean, $s$ the sample standard deviation, $n$ the sample size, and $t_{\alpha/2,\,n-1}$ the upper-$\alpha/2$ critical value of the [$t$-distribution](t-distribution.md) with $n-1$ degrees of freedom. The term $s/\sqrt{n}$ is the standard error.

### Correct interpretation

The frequentist statement is about the **procedure**, not a fixed interval:

> If we repeated the sampling many times and built a 95% CI each time, about 95% of those intervals would contain the true parameter.

For one particular observed interval, the parameter either is or is not inside it—so it is **incorrect** to say $\Pr(\theta \in \text{CI}) = 0.95$ for that fixed interval. The 95% describes long-run coverage of the method (see [sampling distributions](sampling-distributions.md)).

## Worked example

For $n=10$, $\bar{x}=5.8$, $s=1.2$, a 95% CI for the mean uses $t_{0.025,9}\approx 2.262$:

\[
5.8 \pm 2.262 \times \frac{1.2}{\sqrt{10}} = 5.8 \pm 2.262 \times 0.3795 = 5.8 \pm 0.858,
\]

giving $(4.94,\ 6.66)$. Because the reference value $5$ lies inside, this agrees with a two-sided $t$-test at $\alpha=0.05$ that does not reject $H_0:\mu=5$.

## In code

### R

```r
set.seed(42)
x <- rnorm(10, mean = 5.8, sd = 1.2)
t.test(x, mu = 5)$conf.int      # 95% CI for the mean
```

### Python

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(42)
x = rng.normal(5.8, 1.2, size=10)
print(stats.t.interval(0.95, df=len(x)-1,
                       loc=x.mean(), scale=stats.sem(x)))
```

### Julia

```julia
using HypothesisTests, Random, Distributions
Random.seed!(42)
x = rand(Normal(5.8, 1.2), 10)
println(confint(OneSampleTTest(x)))   # 95% CI
```

## Simulation: coverage

Build many 95% CIs from a known population and count how many cover the true mean—about 95% should.

```r
set.seed(1)
mu <- 5
covered <- replicate(10000, {
  x  <- rnorm(20, mean = mu, sd = 2)
  ci <- t.test(x)$conf.int
  ci[1] <= mu && mu <= ci[2]
})
mean(covered)   # ~0.95
```

## Why it matters for statistics

Confidence intervals communicate both the estimate and its uncertainty on the natural scale of the parameter, making results easier to judge than a bare p-value. Their coverage guarantee is the interval-based counterpart to hypothesis testing and is central to reporting effect sizes in epidemiology.

## Related

- [Hypothesis testing](hypothesis-testing.md)
- [t-distribution](t-distribution.md)
- [Sampling distributions](sampling-distributions.md)
- [p-Values](p-values.md)
- [Quantitative Methods](../math.md)
