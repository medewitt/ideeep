---
title: "Measures of Center"
---

# Measures of Center

A measure of center summarizes a [distribution](distributions-overview.md) or dataset with a single "typical" value.
Choosing the right one — mean, median, or mode — depends on shape, skew, and how much you trust the extremes.

## The three classic measures

- **Mean** (arithmetic average): $\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$.
  The balance point of the data; the sample analogue of $\mathbb{E}[X]$.
- **Median**: the middle value when the data are sorted (the average of the two middle values if $n$ is even).
  Splits the data into two halves.
- **Mode**: the most frequent value (or the peak of a density).
  The only center that applies to purely categorical data.

### Quantiles, percentiles, and order statistics

Sorting the data $x_{(1)} \le x_{(2)} \le \dots \le x_{(n)}$ gives the **order statistics**; $x_{(1)}$ is the minimum and $x_{(n)}$ the maximum.
A **quantile** at level $q \in [0,1]$ is a value below which a fraction $q$ of the data fall; **percentiles** are quantiles expressed in percent.
The median is the $0.5$ quantile.

## When to use which

- **Symmetric, light-tailed data** (e.g. roughly [normal](normal-distribution.md)): mean and median nearly coincide; the mean is efficient.
- **Skewed data** (incomes, waiting times): the mean is pulled toward the long tail, so the median better reflects the "typical" case.
- **Outliers or contamination**: the median is **robust** — one wild value barely moves it — while a single large outlier can dominate the mean.
- **Categorical / multimodal data**: use the mode.

## Worked example

Dataset: $\{2, 4, 4, 5, 100\}$, with $n = 5$.

- Mean: $\frac{2+4+4+5+100}{5} = \frac{115}{5} = 23$.
- Median: sorted values are $2,4,\mathbf{4},5,100$, so the median is $4$.
- Mode: $4$ (appears twice).

The lone value $100$ drags the mean up to $23$, far from every other point, while the median $4$ stays representative.
This is robustness in action.

## Simulation

```r
x <- c(2, 4, 4, 5, 100)
mean(x)                 # 23
median(x)               # 4
quantile(x, c(.25, .5, .75))
# mode: value with highest frequency
as.numeric(names(which.max(table(x))))  # 4
```

### Python

```python
import numpy as np
from statistics import mode

x = np.array([2, 4, 4, 5, 100])
print(np.mean(x))                    # 23.0
print(np.median(x))                  # 4.0
print(np.quantile(x, [.25, .5, .75]))
print(mode(x.tolist()))              # 4
```

<!-- python-output:auto -->
```text
23.0
4.0
[4. 4. 5.]
4
```
<!-- /python-output:auto -->

### Julia

```julia
using Statistics, StatsBase

x = [2, 4, 4, 5, 100]
println(mean(x))                     # 23.0
println(median(x))                   # 4.0
println(quantile(x, [.25, .5, .75]))
println(mode(x))                     # 4
```

## Why it matters for statistics

The center you report shapes the story your data tell.
The mean feeds directly into [variances](measures-of-variability.md), standard errors, and the [central limit theorem](central-limit-theorem.md); the median and quantiles give robust, distribution-free summaries that survive outliers and skew.
Knowing when each is appropriate is the difference between an honest summary and a misleading one.

## Related

- [Expected Value](expected-value.md)
- [Measures of Variability](measures-of-variability.md)
- [Distributions Overview](distributions-overview.md)
- [Random Variables](random-variables.md)
- [Quantitative Methods](../math.md)
