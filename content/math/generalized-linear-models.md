---
title: "Generalized Linear Models"
---

# Generalized Linear Models

Generalized linear models (GLMs) are a single framework that unifies linear, logistic, and Poisson regression.
By separating the outcome's distribution from the way its mean depends on predictors, GLMs let epidemiologists model continuous measurements, binary events, and event counts with the same fitting machinery.

## Three components

Every GLM is built from three pieces:

- **Random component:** the outcome $y$ follows an exponential-family [distribution](distributions-overview.md) (normal, binomial, Poisson, gamma, ...) with mean $\mu$.
- **Linear predictor:** a linear combination of covariates, $\eta = x^\top\beta$.
- **Link function:** an invertible function $g$ connecting the mean to the linear predictor, $g(\mu) = \eta$.

The link is what frees the model from the constraints of ordinary [linear regression](linear-regression.md): it maps a bounded mean (a probability in $[0,1]$, a positive rate) onto the unbounded scale where a linear predictor can roam freely.

## Three familiar special cases

Choosing the distribution and link recovers the standard models:

| Distribution | Link $g(\mu)$ | Model |
|---|---|---|
| Normal | identity, $\mu$ | linear regression |
| Binomial | logit, $\log\frac{\mu}{1-\mu}$ | [logistic regression](logistic-regression.md) |
| Poisson | log, $\log\mu$ | Poisson regression |

So the identity link with a normal outcome is exactly the linear model $\mu = x^\top\beta$, while the logit link with a binomial outcome is logistic regression.

## Poisson regression for counts and rates

For count outcomes we use the [Poisson distribution](poisson-distribution.md) with a log link: \[ \log\mu = x^\top\beta \quad\Longleftrightarrow\quad \mu = e^{x^\top\beta}. \] The log link guarantees a positive mean and makes covariate effects multiplicative: $e^{\beta_j}$ is a *rate ratio*.
To model a *rate* rather than a raw count, we add an *offset* $\log(\text{exposure})$ with a fixed coefficient of $1$: \[ \log\mu = \log(\text{exposure}) + x^\top\beta, \] so that $\mu = \text{exposure}\cdot e^{x^\top\beta}$.
The exposure is typically person-time or population size, turning the model into one for cases per unit of population.

## Fitting: deviance and IRLS

All GLMs are fit by [maximum likelihood](maximum-likelihood.md), using *iteratively reweighted least squares* (IRLS): each iteration solves a weighted linear regression on a linearized version of the response until the coefficients converge.
Goodness of fit is measured by the *deviance*, twice the gap between the log-likelihood of the fitted model and that of a saturated model; it generalizes the residual sum of squares and drives likelihood-ratio tests between nested models.

## Overdispersion

The Poisson model assumes the variance equals the mean.
Real count data are often *overdispersed*: their variance exceeds the mean, inflating precision and shrinking standard errors if ignored.
Two common remedies are *quasi-Poisson*, which multiplies the variance by an estimated dispersion parameter $\phi$ so that $\operatorname{Var}(y) = \phi\mu$, and the *negative binomial*, which adds an explicit extra-variance parameter through a different exponential-family distribution.

## Worked example: case counts with a population offset

Two districts report new cases over a year.
District A has $30$ cases in a population of $10{,}000$; District B has $60$ cases in a population of $40{,}000$.
Fit $\log\mu = \beta_0 + \beta_1\,\text{B} + \log(\text{pop})$, where $\text{B}$ indicates District B. The rates are $30/10000 = 0.0030$ and $60/40000 = 0.0015$ per person-year.
The rate ratio for B versus A is $0.0015/0.0030 = 0.5$, so $\hat\beta_1 = \log(0.5) \approx -0.69$ and $e^{\hat\beta_1} = 0.5$: District B has half the incidence rate.
Without the offset, District B's larger raw count would misleadingly suggest a higher burden.

## In code

### R

```r
district <- c("A", "B")
cases <- c(30, 60)
pop   <- c(10000, 40000)

fit <- glm(cases ~ district, family = poisson,
           offset = log(pop))
summary(fit)
exp(coef(fit))     # districtB rate ratio ~ 0.5
```

### Python

```python
import numpy as np
import statsmodels.api as sm

cases = np.array([30, 60])
pop   = np.array([10000, 40000])
X = sm.add_constant([0, 1])          # 0 = A, 1 = B

fit = sm.GLM(cases, X, family=sm.families.Poisson(),
             offset=np.log(pop)).fit()
print(np.exp(fit.params))            # B rate ratio ~ 0.5
```

### Julia

```julia
using GLM, DataFrames
df = DataFrame(cases = [30, 60],
               district = ["A", "B"],
               logpop = log.([10000, 40000]))

fit = glm(@formula(cases ~ district), df, Poisson(), LogLink();
          offset = df.logpop)
exp.(coef(fit))        # districtB rate ratio ~ 0.5
```

## Why it matters

GLMs give analysts one coherent language for regression across continuous, binary, and count outcomes, so the same ideas of coefficients, standard errors, and deviance carry over unchanged.
This unification is why incidence-rate models, dose-response curves, and risk models can all be fit, compared, and interpreted with a single well-understood toolkit.

## Related

- [Linear regression](linear-regression.md)
- [Logistic regression](logistic-regression.md)
- [Poisson distribution](poisson-distribution.md)
- [Maximum likelihood](maximum-likelihood.md)
- [Distributions overview](distributions-overview.md)
- [Quantitative Methods](../math.md)
