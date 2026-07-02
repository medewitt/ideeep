---
title: "Linear Regression"
---

# Linear Regression

Linear regression models a continuous outcome as a straight-line function of one or more predictors.
It is the workhorse of quantitative data analysis: estimating how exposures, doses, or covariates shift an average response, and providing the foundation for the whole family of regression models used in epidemiology.

## The model

We assume each outcome $y_i$ is a linear function of predictors plus random noise: \[ y = X\beta + \varepsilon,\qquad \varepsilon\sim\mathcal N(0,\sigma^2 I). \] Here $y$ is the $n\times 1$ vector of responses, $X$ is the $n\times p$ [design matrix](matrix-notation.md) (with a column of ones for the intercept), $\beta$ is the $p\times 1$ vector of coefficients, and $\varepsilon$ is mean-zero error.
For a single observation this reads $y_i = x_i^\top\beta + \varepsilon_i$.

## Ordinary least squares

Ordinary least squares (OLS) chooses $\hat\beta$ to minimize the sum of squared residuals: \[ \hat\beta = \arg\min_\beta \sum_i \left(y_i - x_i^\top\beta\right)^2 = \arg\min_\beta \lVert y - X\beta\rVert^2. \] Setting the gradient to zero gives the *normal equations* $X^\top X\,\hat\beta = X^\top y$, whose closed-form solution is \[ \hat\beta = (X^\top X)^{-1}X^\top y. \] This uses standard [matrix operations](matrix-operations.md) and the [inverse](matrix-inverse-and-determinant.md) of the $p\times p$ matrix $X^\top X$, which exists as long as the columns of $X$ are not collinear.

## Interpreting coefficients

Each slope $\hat\beta_j$ is the expected change in $y$ per one-unit increase in $x_j$, holding the other predictors fixed.
The intercept $\hat\beta_0$ is the expected $y$ when all predictors are zero.
The coefficient of determination \[ R^2 = 1 - \frac{\sum_i (y_i - \hat y_i)^2}{\sum_i (y_i - \bar y)^2} \] is the fraction of the outcome's [variance](measures-of-variability.md) explained by the model, ranging from $0$ to $1$.

## Assumptions

OLS is unbiased and efficient when four conditions hold:

- **Linearity:** the mean of $y$ is truly linear in the predictors.
- **Independent errors:** the $\varepsilon_i$ are uncorrelated across observations.
- **Homoscedasticity:** the errors have constant variance $\sigma^2$.
- **Normality:** the errors are approximately normal (needed mainly for exact small-sample inference).

Residuals $r_i = y_i - \hat y_i$ are the diagnostic tool: plotting them against fitted values should show a formless band with no trend or fanning.

## Inference for coefficients

The estimated coefficient covariance is $\widehat{\operatorname{Var}}(\hat\beta) = \hat\sigma^2 (X^\top X)^{-1}$, where $\hat\sigma^2 = \frac{1}{n-p}\sum_i r_i^2$.
The square roots of its diagonal are the standard errors $\operatorname{SE}(\hat\beta_j)$.
A [hypothesis test](hypothesis-testing.md) of $H_0:\beta_j=0$ uses the $t$ statistic $t = \hat\beta_j / \operatorname{SE}(\hat\beta_j)$, compared to a $t$ distribution with $n-p$ degrees of freedom.
A [confidence interval](confidence-intervals.md) for $\beta_j$ is $\hat\beta_j \pm t_{1-\alpha/2,\,n-p}\,\operatorname{SE}(\hat\beta_j)$.

Under the normal-error assumption, OLS coincides exactly with [maximum likelihood](maximum-likelihood.md): minimizing squared error is the same as maximizing the Gaussian log-likelihood.

## Worked example: simple linear regression by hand

With a single predictor, the estimates have a clean closed form.
The slope is the ratio of the covariance of $x$ and $y$ to the variance of $x$: \[ \hat\beta_1 = \frac{\operatorname{Cov}(x,y)}{\operatorname{Var}(x)} = \frac{\sum_i (x_i-\bar x)(y_i-\bar y)}{\sum_i (x_i-\bar x)^2},\qquad \hat\beta_0 = \bar y - \hat\beta_1\bar x. \] Take the four points $(1,2),(2,2),(3,4),(4,5)$.
Then $\bar x = 2.5$ and $\bar y = 3.25$.
The cross-products give $\sum (x_i-\bar x)(y_i-\bar y) = (-1.5)(-1.25)+(-0.5)(-1.25)+(0.5)(0.75)+(1.5)(1.75) = 5.5$.
The spread gives $\sum (x_i-\bar x)^2 = 2.25+0.25+0.25+2.25 = 5$.
So $\hat\beta_1 = 5.5/5 = 1.1$ and $\hat\beta_0 = 3.25 - 1.1(2.5) = 0.5$.
The fitted line is $\hat y = 0.5 + 1.1\,x$.

## In code

### R

```r
set.seed(1)
x <- 1:20
y <- 0.5 + 1.1 * x + rnorm(20, sd = 1.5)

fit <- lm(y ~ x)
summary(fit)          # coefficients, SEs, t-tests, R^2
confint(fit)          # 95% CIs for the coefficients

# closed form via matrix ops
X <- cbind(1, x)
beta_hat <- solve(t(X) %*% X, t(X) %*% y)
beta_hat               # matches coef(fit): ~0.5 and ~1.1
```

### Python

```python
import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(1)
x = np.arange(1, 21)
y = 0.5 + 1.1 * x + rng.normal(0, 1.5, size=20)

X = sm.add_constant(x)
fit = sm.OLS(y, X).fit()
print(fit.params)          # intercept ~0.5, slope ~1.1
print(fit.conf_int())      # 95% CIs

# closed form: beta = (X'X)^-1 X'y
beta_hat = np.linalg.solve(X.T @ X, X.T @ y)
print(beta_hat)            # same as fit.params
```

### Julia

```julia
using GLM, DataFrames, Random
Random.seed!(1)
x = 1:20
y = 0.5 .+ 1.1 .* x .+ randn(20) .* 1.5
df = DataFrame(x = x, y = y)

fit = lm(@formula(y ~ x), df)
coef(fit)            # intercept ~0.5, slope ~1.1
confint(fit)         # 95% CIs

# closed form
X = [ones(20) collect(x)]
beta_hat = (X' * X) \ (X' * y)   # matches coef(fit)
```

## Why it matters

Linear regression turns messy scatter into an interpretable slope with a standard error, letting analysts quantify associations and adjust for confounders.
It is also the conceptual template for [logistic regression](logistic-regression.md) and the broader class of [generalized linear models](generalized-linear-models.md), which extend the same machinery to binary and count outcomes.

## Related

- [Matrix operations](matrix-operations.md)
- [Matrix inverse and determinant](matrix-inverse-and-determinant.md)
- [Maximum likelihood](maximum-likelihood.md)
- [Measures of variability](measures-of-variability.md)
- [Hypothesis testing](hypothesis-testing.md)
- [Confidence intervals](confidence-intervals.md)
- [Logistic regression](logistic-regression.md)
- [Generalized linear models](generalized-linear-models.md)
- [Quantitative Methods](../math.md)
