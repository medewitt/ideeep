---
title: "Measures of Variability"
---

# Measures of Variability

Spread is as important as center: two datasets with the same [mean](measures-of-center.md) can behave completely differently.
Measures of variability quantify that spread — and one of them, the standard error, is the engine of [statistical inference](statistical-inference.md).

## Variance and standard deviation

The **population variance** is the mean squared deviation from the mean $\mu$: \[ \sigma^2 = \mathbb{E}\big[(X-\mu)^2\big]. \] Its square root, the **standard deviation** $\sigma$, is in the same units as the data.

From a sample $x_1,\dots,x_n$ the **sample variance** uses divisor $n-1$: \[ s^2 = \frac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar{x})^2. \] The $n-1$ (Bessel's correction) makes $s^2$ an unbiased estimator of $\sigma^2$; dividing by $n$ underestimates spread because deviations are taken from the estimated mean $\bar{x}$, not the true $\mu$.

## Covariance and correlation

For two variables, **covariance** measures how they move together: \[ \operatorname{Cov}(X,Y) = \mathbb{E}\big[(X-\mu_X)(Y-\mu_Y)\big]. \] **Correlation** rescales it to $[-1,1]$: \[ \rho = \frac{\operatorname{Cov}(X,Y)}{\sigma_X\,\sigma_Y}. \] Note $\operatorname{Cov}(X,X) = \operatorname{Var}(X)$.

## Standard deviation vs. standard error

This distinction trips up almost everyone.
The **standard deviation** $\sigma$ describes the spread of individual observations.
The **standard error of the mean** describes the spread of the *sample mean* $\bar{X}$ across repeated samples: \[ \operatorname{SE}(\bar{X}) = \frac{\sigma}{\sqrt{n}}. \] As $n$ grows, $\sigma$ stays fixed (it is a property of the population) but the SE **shrinks** like $1/\sqrt{n}$: averaging cancels noise.
In practice we estimate it by $s/\sqrt{n}$.

## Worked example

Data: $\{2, 4, 6, 8\}$, so $\bar{x} = 5$, $n = 4$.

Squared deviations: $(2-5)^2 + (4-5)^2 + (6-5)^2 + (8-5)^2 = 9 + 1 + 1 + 9 = 20$.

- Sample variance: $s^2 = \frac{20}{4-1} = \frac{20}{3} \approx 6.67$, so $s \approx 2.58$.
- Population variance (divisor $n$): $\frac{20}{4} = 5$, so $\sigma \approx 2.24$.
- Estimated SE of the mean: $s/\sqrt{n} = 2.58/2 \approx 1.29$.

## Simulation

The SE shrinks like $1/\sqrt{n}$: quadruple $n$ and the SE roughly halves.

### R

```r
set.seed(42)
sigma <- 3
for (n in c(25, 100, 400)) {
  se <- replicate(2000, mean(rnorm(n, mean = 10, sd = sigma)))
  cat("n =", n, " empirical SE =", round(sd(se), 3),
      " theory =", round(sigma / sqrt(n), 3), "\n")
}
# basic estimators
x <- rnorm(50); var(x); sd(x)
y <- 2 * x + rnorm(50); cov(x, y); cor(x, y)
```

### Python

```python
import numpy as np
np.random.seed(42)

sigma = 3
for n in (25, 100, 400):
    means = [np.random.normal(10, sigma, n).mean() for _ in range(2000)]
    print(f"n={n:>3} empirical SE={np.std(means, ddof=1):.3f} "
          f"theory={sigma/np.sqrt(n):.3f}")

x = np.random.normal(size=50)
print(np.var(x, ddof=1), np.std(x, ddof=1))     # sample var, sd
y = 2 * x + np.random.normal(size=50)
print(np.cov(x, y)[0, 1], np.corrcoef(x, y)[0, 1])
```

<!-- python-output:auto -->
```text
n= 25 empirical SE=0.612 theory=0.600
n=100 empirical SE=0.304 theory=0.300
n=400 empirical SE=0.152 theory=0.150
0.9205774355567683 0.9594672665374094
1.6812880543796045 0.8856975784726173
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics
Random.seed!(42)

sigma = 3.0
for n in (25, 100, 400)
    means = [mean(randn(n) .* sigma .+ 10) for _ in 1:2000]
    println("n=$n empirical SE=", round(std(means), digits=3),
            " theory=", round(sigma / sqrt(n), digits=3))
end

x = randn(50)
println(var(x), " ", std(x))          # sample var, sd (n-1)
y = 2 .* x .+ randn(50)
println(cov(x, y), " ", cor(x, y))
```

## Why it matters for statistics

Variance and standard deviation calibrate how surprising a value is.
Covariance and correlation are the raw material of regression.
And the standard error — not the standard deviation — sets the width of [confidence intervals](confidence-intervals.md) and the scale of [test statistics](hypothesis-testing.md): it is precisely how uncertainty about an estimate scales down with sample size.

## Related

- [Measures of Center](measures-of-center.md)
- [Sampling Distributions](sampling-distributions.md)
- [The Central Limit Theorem](central-limit-theorem.md)
- [Confidence Intervals](confidence-intervals.md)
- [Quantitative Methods](../math.md)
