---
title: "Logistic Regression"
---

# Logistic Regression

Logistic regression models the probability of a binary outcome, such as diseased versus healthy or exposed versus not.
It is the standard tool for risk modeling and case-control studies in epidemiology, because its coefficients translate directly into odds ratios.

![Binary outcomes with the fitted logistic (sigmoid) probability curve.](../assets/figures/logistic-regression.svg)

## From probability to log-odds

A [linear regression](linear-regression.md) can predict values outside $[0,1]$, which makes no sense for a probability.
Logistic regression instead models the *log-odds* as a linear function of the predictors: \[ \operatorname{logit}(p) = \log\frac{p}{1-p} = x^\top\beta. \] Solving for $p$ gives the logistic (sigmoid) function, which is bounded between $0$ and $1$: \[ p = \frac{1}{1 + e^{-x^\top\beta}}. \] The building blocks here are the odds $p/(1-p)$ and the [logarithm](exponentials-and-logarithms.md) that maps them onto the whole real line.

## Coefficients are log-odds-ratios

Because the linear predictor lives on the log-odds scale, a one-unit increase in $x_j$ adds $\beta_j$ to the log-odds.
Exponentiating recovers a multiplicative effect on the odds, so $e^{\beta_j}$ is an *odds ratio*: \[ \text{OR}_j = e^{\beta_j}. \] An odds ratio above $1$ means the predictor increases the odds of the outcome; below $1$ means it decreases them; exactly $1$ means no association.

## Fitting by maximum likelihood

Each observation is a Bernoulli trial with success [probability](probability-basics.md) $p_i = 1/(1+e^{-x_i^\top\beta})$.
The log-likelihood is \[ \ell(\beta) = \sum_i \left[ y_i \log p_i + (1-y_i)\log(1-p_i) \right]. \] Unlike OLS there is no closed form, so we maximize $\ell(\beta)$ numerically by [maximum likelihood](maximum-likelihood.md).
The standard algorithm is Newton–Raphson, which for this model takes the form of *iteratively reweighted least squares* (IRLS): repeatedly solving a weighted linear regression until the coefficients converge.

## Deviance and fit

Model fit is summarized by the *deviance*, $D = -2\ell(\hat\beta)$, the logistic analogue of the residual sum of squares.
Comparing the deviance of nested models gives a likelihood-ratio test for whether added predictors improve fit.
Coefficient standard errors come from the curvature of the log-likelihood, yielding Wald tests and confidence intervals for each $\beta_j$ (and, after exponentiating, for each odds ratio).

## Worked example: reading a coefficient

Suppose a model of infection uses a single predictor, hours of exposure, and returns $\hat\beta_0 = -2.0$ and $\hat\beta_1 = 0.7$.
The slope's odds ratio is $e^{0.7}\approx 2.01$: each additional hour of exposure roughly *doubles* the odds of infection.

Now convert a linear predictor to a probability for someone with $3$ hours of exposure.
The linear predictor is $x^\top\beta = -2.0 + 0.7(3) = 0.1$.
Then \[ p = \frac{1}{1+e^{-0.1}} \approx 0.525, \] about a $52.5\%$ predicted probability of infection.

## In code

### R

```r
set.seed(1)
x <- rnorm(300)
p <- 1 / (1 + exp(-(-0.5 + 1.2 * x)))
y <- rbinom(300, 1, p)

fit <- glm(y ~ x, family = binomial)
summary(fit)                 # coefficients on log-odds scale
exp(coef(fit))               # odds ratios; slope ~ exp(1.2) ~ 3.3
predict(fit, type = "response")[1:5]   # fitted probabilities
```

### Python

```python
import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(1)
x = rng.normal(size=300)
p = 1 / (1 + np.exp(-(-0.5 + 1.2 * x)))
y = rng.binomial(1, p)

X = sm.add_constant(x)
fit = sm.Logit(y, X).fit()
print(fit.params)            # log-odds scale
print(np.exp(fit.params))    # odds ratios; slope ~ exp(1.2) ~ 3.3
print(fit.predict(X)[:5])    # fitted probabilities
```

### Julia

```julia
using GLM, DataFrames, Random
Random.seed!(1)
x = randn(300)
p = 1 ./ (1 .+ exp.(-(-0.5 .+ 1.2 .* x)))
y = rand.(Bernoulli.(p))
df = DataFrame(x = x, y = Int.(y))

fit = glm(@formula(y ~ x), df, Binomial(), LogitLink())
coef(fit)              # log-odds scale
exp.(coef(fit))        # odds ratios; slope ~ exp(1.2) ~ 3.3
predict(fit)[1:5]      # fitted probabilities
```

## Why it matters

Logistic regression is the default model whenever the outcome is yes/no, and its odds ratios are the currency of epidemiological risk reporting.
It scales from a single exposure to genome-wide association studies ([GWAS](gwas.md)), where each variant's effect on disease status is fit as a logistic coefficient across millions of tests.

## Related

- [Linear regression](linear-regression.md)
- [Generalized linear models](generalized-linear-models.md)
- [Maximum likelihood](maximum-likelihood.md)
- [Exponentials and logarithms](exponentials-and-logarithms.md)
- [Probability basics](probability-basics.md)
- [GWAS](gwas.md)
- [Quantitative Methods](../math.md)
