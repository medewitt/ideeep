---
title: "Jensen's Inequality and Nonlinear Averaging"
---

# Jensen's Inequality and Nonlinear Averaging

The average of a nonlinear function is *not* the function of the average.
This single fact explains why plugging mean parameters into a nonlinear model gives biased predictions — a recurring trap in statistics and epidemiology.

## The inequality

Let $g$ be a **convex** function and $X$ a [random variable](random-variables.md) with finite [mean](measures-of-center.md).
Then \[ \mathbb{E}[g(X)] \ge g\big(\mathbb{E}[X]\big). \] For a **concave** function the inequality reverses: $\mathbb{E}[g(X)] \le g(\mathbb{E}[X])$.
Equality holds if and only if $g$ is linear on the support of $X$, or $X$ is (almost surely) constant.

The intuition is geometric.
Convexity means the chord lies above the curve, and more precisely every point of the curve has a supporting line beneath it.
Taking expectations of that supporting line at $\mu = \mathbb{E}[X]$ gives the bound.

### Second-order intuition: the variance gap

A [Taylor expansion](taylor-series.md) of $g$ about $\mu = \mathbb{E}[X]$ (the delta method) makes the size of the gap explicit: \[ g(X) \approx g(\mu) + g'(\mu)(X-\mu) + \tfrac12 g''(\mu)(X-\mu)^2 . \] Taking expectations, the linear term vanishes ($\mathbb{E}[X-\mu]=0$), leaving \[ \mathbb{E}[g(X)] - g(\mu) \approx \tfrac12\, g''(\mu)\,\operatorname{Var}(X). \] When $g$ is convex, $g''(\mu) \ge 0$, so the gap is non-negative — Jensen again.
The gap grows with the curvature $g''$ and with the [spread](measures-of-variability.md) $\operatorname{Var}(X)$.

## Examples

- **AM–GM inequality.** With $g(x) = -\log x$ (convex) and $X$ uniform on $\{x_1,\dots,x_n\}$, Jensen gives $\tfrac1n\sum -\log x_i \ge -\log\big(\tfrac1n\sum x_i\big)$, i.e. $\big(\prod x_i\big)^{1/n} \le \tfrac1n\sum x_i$: the geometric mean never exceeds the arithmetic mean.
- **Log of a mean.** Since $\log$ is concave, $\mathbb{E}[\log X] \le \log \mathbb{E}[X]$.
  Averaging on the log scale and exponentiating underestimates the mean.
- **Reciprocals.** Since $g(x)=1/x$ is convex on $x>0$, $\overline{1/x} = \tfrac1n\sum 1/x_i \ge 1/\bar x$: the mean of reciprocals exceeds the reciprocal of the mean.
  Harmonic mean $\le$ arithmetic mean.
- **Heterogeneous transmission.** If a transmission rate $\beta$ varies across subgroups, a quantity like $\mathbb{E}[\beta^2]$ (relevant to reproduction-number and final-size calculations) exceeds $(\mathbb{E}[\beta])^2$ by exactly $\operatorname{Var}(\beta)$.
  Using a single average $\bar\beta$ systematically understates the impact of heterogeneity.

## Worked example

Let $X$ take the values $1$ and $3$, each with probability $\tfrac12$, and take the convex function $g(x) = x^2$.

- Mean: $\mathbb{E}[X] = \tfrac12(1) + \tfrac12(3) = 2$, so $g(\mathbb{E}[X]) = 2^2 = 4$.
- Function average: $\mathbb{E}[g(X)] = \tfrac12(1^2) + \tfrac12(3^2) = \tfrac{1+9}{2} = 5$.

So $\mathbb{E}[g(X)] = 5 \ge 4 = g(\mathbb{E}[X])$, with a gap of $1$.

Check the variance-gap formula: $\operatorname{Var}(X) = \mathbb{E}[X^2] - \mu^2 = 5 - 4 = 1$ and $g''(x) = 2$, so \[ \tfrac12 g''(\mu)\operatorname{Var}(X) = \tfrac12(2)(1) = 1, \] which matches the gap exactly — the approximation is exact here because $g$ is quadratic (higher derivatives vanish).

## A biological example: performance in a fluctuating environment

Most biological rates — development, metabolism, photosynthesis, even pathogen transmission — depend on temperature through a curved **thermal performance curve** that peaks at an optimum and falls off on either side.
Near that optimum the curve is *concave*, so Jensen's inequality bites: an organism experiencing a *fluctuating* temperature performs worse, on average, than one held at the same *mean* temperature.
Ecologists call plugging the mean temperature into a nonlinear rate the "fallacy of the averages" ([Ruel & Ayres, 2001](https://doi.org/10.1016/S0169-5347%2801%2902095-0)).

![A concave thermal performance curve: because performance is concave near the optimum, the average of performance at 20 °C and 36 °C (0.37) sits far below the performance at their mean temperature of 28 °C (1.00).](../assets/figures/jensens-biology.svg)

Take a performance curve peaking at $T_\text{opt} = 28^\circ\text{C}$ and a habitat that spends half its time at $20^\circ$ and half at $36^\circ$ — mean temperature exactly $28^\circ$.
Performance *at the mean* temperature is the maximum, $P(\bar T) = 1.00$, but the *mean performance* is only $\tfrac12[P(20) + P(36)] = 0.37$: variability alone costs 63% of performance, with no change in the average temperature.
This is why climate **variability**, not just mean warming, reshapes development rates, vector activity, and transmission — and why a model fed the mean temperature over-predicts.
The sign can flip: in the accelerating, *convex* low-temperature tail of the same curve, added variability would *raise* mean performance, exactly as $\tfrac12 P''(\mu)\operatorname{Var}(T)$ predicts.

```python
import numpy as np
Topt, width = 28.0, 8.0
P = lambda T: np.exp(-((T - Topt) / width) ** 2)   # concave near the optimum

T = np.array([20.0, 36.0])          # two equally likely temperatures, mean 28
print("P(mean T)  =", round(float(P(T.mean())), 3))   # 1.0   performance at the mean
print("E[P(T)]    =", round(float(P(T).mean()), 3))   # 0.368 mean performance
print("Jensen gap =", round(float(P(T.mean()) - P(T).mean()), 3))  # 0.632
```

<!-- python-output:auto -->
```text
P(mean T)  = 1.0
E[P(T)]    = 0.368
Jensen gap = 0.632
```
<!-- /python-output:auto -->

## Simulation

### R

```r
set.seed(42)
g <- function(x) x^2
X <- runif(1e6, 0, 1)           # Uniform(0,1): mu = 1/2, Var = 1/12
lhs <- mean(g(X)); rhs <- g(mean(X))
c(E_gX = lhs, g_EX = rhs, gap = lhs - rhs)
# E_gX ~ 0.3333  g_EX ~ 0.25  gap ~ 0.0833  (>= 0, confirms Jensen)

gpp <- 2                        # g''(x) = 2
0.5 * gpp * var(X)              # ~ 0.0833: variance-gap approximation
```

### Python

```python
import numpy as np
np.random.seed(42)
g = lambda x: x**2
X = np.random.uniform(0, 1, 1_000_000)
lhs, rhs = g(X).mean(), g(X.mean())
print(lhs, rhs, lhs - rhs)      # ~0.3333 ~0.25 ~0.0833 (gap >= 0)
print(0.5 * 2 * X.var())        # ~0.0833: (1/2) g''(mu) Var(X)
```

<!-- python-output:auto -->
```text
0.3336193530309505 0.2503345980567165 0.08328475497423404
0.08328475497423413
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics
Random.seed!(42)
g(x) = x^2
X = rand(1_000_000)             # Uniform(0,1)
lhs, rhs = mean(g.(X)), g(mean(X))
println((lhs, rhs, lhs - rhs))  # ~(0.3333, 0.25, 0.0833)
println(0.5 * 2 * var(X))       # ~0.0833
```

For $\text{Uniform}(0,1)$ the exact gap is $\mathbb{E}[X^2] - (\mathbb{E}X)^2 = \tfrac13 - \tfrac14 = \tfrac{1}{12}\approx 0.0833$, matching both the simulation and the second-order formula.

## Why it matters for statistics

Jensen's inequality is the reason "average the inputs, then apply the model" disagrees with "apply the model, then average" whenever the model is nonlinear.
It underlies the bias of plug-in estimators, the direction of the delta-method correction, the fact that $\mathbb{E}[\log \text{likelihood}]$ bounds motivate the EM algorithm and variational inference, and warnings against using mean parameters in nonlinear epidemic models.
Knowing the sign (from convexity) and size (from the variance gap) of the discrepancy lets you correct for it.

## Related

- [Optimization](optimization.md)
- [Expected Value](expected-value.md)
- [Taylor Series](taylor-series.md)
- [Monotonic Transformations](monotonic-transformations.md)
- [The Legendre Transform](legendre-transform.md)
- [Measures of Variability](measures-of-variability.md)
- [Quantitative Methods](../math.md)
