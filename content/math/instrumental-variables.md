---
title: "Instrumental Variables"
---

# Instrumental Variables

When an unmeasured confounder distorts the relationship between an exposure and an outcome, ordinary regression estimates the wrong thing. Instrumental variables (IV) exploit a special variable $Z$ to recover the causal effect even when confounding cannot be measured or adjusted for.

## The problem: confounding bias

Suppose we want the causal effect $\beta$ of an exposure $X$ on an outcome $Y$, but an unmeasured confounder $U$ influences both:

\[
Y = \beta X + U + \varepsilon, \qquad X = \alpha U + \text{(other causes)}.
\]

Because $X$ and the error term share $U$, the regressor is correlated with the disturbance ($\operatorname{Cov}(X, U) \ne 0$). Ordinary least squares (OLS) is then **biased and inconsistent**: it estimates a mixture of the causal effect and the confounding association, not $\beta$.

## The instrument and its three assumptions

An **instrument** $Z$ is a variable that lets us isolate the part of $X$ that is "as good as randomly assigned." It must satisfy three assumptions:

1. **Relevance.** $Z$ is associated with the exposure: $\operatorname{Cov}(Z, X) \ne 0$. This is testable.
2. **Independence (exogeneity).** $Z$ is independent of the confounders: $\operatorname{Cov}(Z, U) = 0$. Not directly testable.
3. **Exclusion restriction.** $Z$ affects $Y$ **only through** $X$ — there is no direct path $Z \to Y$. Not directly testable.

Intuitively, $Z$ nudges $X$ without touching $U$ or $Y$ by any other route, so the induced change in $Y$ can be attributed to $X$ alone.

## Estimators

### The Wald ratio

With a single instrument, take covariances of the outcome equation with $Z$. Under independence and exclusion the confounder and direct terms drop out:

\[
\operatorname{Cov}(Z, Y) = \beta \,\operatorname{Cov}(Z, X) + \underbrace{\operatorname{Cov}(Z, U)}_{=\,0} + \underbrace{\operatorname{Cov}(Z, \varepsilon)}_{=\,0}.
\]

Solving for $\beta$ gives the **Wald (ratio) estimator**:

\[
\hat\beta = \frac{\operatorname{Cov}(Z, Y)}{\operatorname{Cov}(Z, X)}.
\]

For a binary instrument this equals the difference in mean outcome divided by the difference in mean exposure across the two groups.

### Two-stage least squares (2SLS)

With one or more instruments, the standard estimator is **2SLS**:

- **Stage 1.** Regress $X$ on $Z$ and keep the fitted values $\hat X$ — the projection of $X$ onto the instrument, free of the confounded variation.
- **Stage 2.** Regress $Y$ on $\hat X$. The coefficient on $\hat X$ is $\hat\beta_{2\text{SLS}}$.

With a single instrument, 2SLS is algebraically identical to the Wald ratio. In matrix form, with instrument matrix $Z$,

\[
\hat\beta_{2\text{SLS}} = \left(\hat X^\top \hat X\right)^{-1} \hat X^\top Y, \qquad \hat X = Z (Z^\top Z)^{-1} Z^\top X.
\]

### Weak-instrument bias

If relevance is only barely satisfied ($\operatorname{Cov}(Z,X)$ near zero), the denominator is small and estimates become unstable, biased toward the OLS estimate, with poor confidence-interval coverage. A common rule of thumb is a first-stage $F$-statistic above 10; weaker instruments demand caution.

## Worked simulation

We generate data where OLS is badly confounded, then show that 2SLS recovers the true effect $\beta = 2$.

### R

```r
set.seed(1)
n <- 5000
U <- rnorm(n)                          # unmeasured confounder
Z <- rnorm(n)                          # instrument
X <- 0.8 * Z + 1.0 * U + rnorm(n)      # exposure depends on Z and U
beta <- 2
Y <- beta * X + 2.0 * U + rnorm(n)     # U confounds X and Y

# Naive OLS: biased upward (U inflates the X-Y association)
coef(lm(Y ~ X))["X"]                   # ~ 2.66

# Wald ratio / manual 2SLS
cov(Z, Y) / cov(Z, X)                  # ~ 2.00

# 2SLS via AER
# install.packages("AER")
library(AER)
coef(ivreg(Y ~ X | Z))["X"]           # ~ 2.00
```

### Python

```python
import numpy as np
from linearmodels.iv import IV2SLS
import statsmodels.api as sm

rng = np.random.default_rng(1)
n = 5000
U = rng.normal(size=n)
Z = rng.normal(size=n)
X = 0.8 * Z + 1.0 * U + rng.normal(size=n)
beta = 2
Y = beta * X + 2.0 * U + rng.normal(size=n)

# Naive OLS: biased
sm.OLS(Y, sm.add_constant(X)).fit().params[1]      # ~ 2.66

# Wald ratio / manual 2SLS
np.cov(Z, Y)[0, 1] / np.cov(Z, X)[0, 1]            # ~ 2.00

# 2SLS via linearmodels: IV2SLS(dependent, exog, endog, instruments)
res = IV2SLS(Y, np.ones(n), X, Z).fit()
res.params["endog"]                                 # ~ 2.00
```

### Julia

```julia
using Random, Statistics

Random.seed!(1)
n = 5000
U = randn(n)
Z = randn(n)
X = 0.8 .* Z .+ 1.0 .* U .+ randn(n)
beta = 2
Y = beta .* X .+ 2.0 .* U .+ randn(n)

# Naive OLS slope: biased (~2.66)
Xo = hcat(ones(n), X)
(Xo \ Y)[2]

# Wald ratio (~2.00)
cov(Z, Y) / cov(Z, X)

# Manual 2SLS via least squares (\)
Zm  = hcat(ones(n), Z)
Xhat = Zm * (Zm \ X)            # stage 1 fitted exposure
Xh  = hcat(ones(n), Xhat)
(Xh \ Y)[2]                     # stage 2 slope ~ 2.00
```

## Why it matters for statistics

Instrumental variables extend causal estimation beyond the reach of adjustment: they identify effects when the confounders are unknown or unmeasured, which is the usual predicament in observational epidemiology and economics. Understanding the relevance, independence, and exclusion assumptions — and their untestability — is central to judging when an IV analysis is credible, and it underpies related designs such as Mendelian randomization and natural experiments.

## Related

- [Mendelian Randomization](mendelian-randomization.md)
- [Experimental Design](experimental-design.md)
- [Hypothesis Testing](hypothesis-testing.md)
- [Quantitative Methods](../math.md)
