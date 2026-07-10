---
title: "Moment Generating Functions"
---

# Moment Generating Functions

The moment generating function (MGF) is a single function that encodes an entire probability distribution.
As its name promises, it manufactures the moments of a random variable through differentiation, and it turns sums of independent variables into products.

## Definition

For a random variable $X$, the moment generating function is $$M_X(t) = \mathbb{E}[e^{tX}],$$ defined for values of $t$ in a neighborhood of $0$ where this [expectation](expected-value.md) is finite.
For a discrete variable $M_X(t)=\sum_k e^{tk}P(X=k)$, and for a continuous one $M_X(t)=\int e^{tx} f(x)\,dx$.
Not every distribution has an MGF (heavy-tailed ones may fail to converge), but when it exists near $0$ it is extremely useful.

## It generates moments

Expand the exponential as a [Taylor series](taylor-series.md), $e^{tX}=\sum_{n\ge 0} \frac{t^n X^n}{n!}$, and take expectations term by term: $$M_X(t) = \sum_{n=0}^{\infty} \frac{\mathbb{E}[X^n]}{n!}\, t^n.$$ The moments $\mathbb{E}[X^n]$ are exactly the Taylor coefficients, so differentiating and setting $t=0$ picks them off: $$M_X^{(n)}(0) = \mathbb{E}[X^n].$$ In particular $M_X'(0)=\mathbb{E}[X]$ and $M_X''(0)=\mathbb{E}[X^2]$, from which the [variance](measures-of-variability.md) follows as $$\operatorname{Var}(X) = M_X''(0) - \big(M_X'(0)\big)^2.$$

## Two defining properties

**Uniqueness.** When the MGF exists in an open interval around $0$, it uniquely determines the distribution: two variables with the same MGF have the same law.
This makes the MGF a fingerprint for identifying distributions.

**Sums become products.** If $X$ and $Y$ are [independent](probability-basics.md), then $$M_{X+Y}(t) = \mathbb{E}[e^{t(X+Y)}] = \mathbb{E}[e^{tX}]\,\mathbb{E}[e^{tY}] = M_X(t)\,M_Y(t).$$ Adding independent variables corresponds to multiplying their MGFs.
This factorization is the engine behind one standard proof of the [central limit theorem](central-limit-theorem.md): the MGF of a standardized sum converges to $e^{t^2/2}$, the MGF of the standard normal.

## MGFs of standard distributions

| Distribution | MGF $M_X(t)$ | Valid for |
|---|---|---|
| Normal $\mathcal{N}(\mu,\sigma^2)$ | $e^{\mu t + \sigma^2 t^2/2}$ | all $t$ |
| Poisson $(\lambda)$ | $e^{\lambda(e^{t}-1)}$ | all $t$ |
| Exponential $(\lambda)$ | $\dfrac{\lambda}{\lambda - t}$ | $t<\lambda$ |
| Gamma (shape $\alpha$, rate $\lambda$) | $\left(\dfrac{\lambda}{\lambda - t}\right)^{\alpha}$ | $t<\lambda$ |

See the [normal](normal-distribution.md) and [Poisson](poisson-distribution.md) distributions for the parent densities.
The exponential is the gamma with shape $\alpha = 1$, and a gamma is a sum of $\alpha$ independent exponentials — which is exactly why its MGF is the exponential's raised to the $\alpha$ (sums become products).

## The cumulant generating function

Taking logs gives the cumulant generating function $$K(t) = \log M_X(t),$$ whose derivatives at $0$ generate the cumulants: $K'(0)=\mathbb{E}[X]$ is the mean and $K''(0)=\operatorname{Var}(X)$ is the variance.
Cumulants are often more convenient than moments because $K(t)$ simply adds over independent variables.
The convex function $K(t)$ is also the object whose [Legendre transform](legendre-transform.md) yields the rate function of large-deviations theory.

## The discrete analogue

For nonnegative integer counts, the parallel tool is the probability generating function $$G(s) = \mathbb{E}[s^{X}] = \sum_{k\ge 0} P(X=k)\, s^{k}.$$ It relates to the MGF by $G(e^t)=M_X(t)$, and it is the workhorse for [branching processes](branching-processes.md), where composing $G$ with itself tracks successive generations.

## Worked example: Poisson mean and variance

Let $X\sim\mathrm{Poisson}(\lambda)$ with $M(t)=e^{\lambda(e^{t}-1)}$.
Differentiate using the chain rule: $$M'(t) = \lambda e^{t}\, e^{\lambda(e^{t}-1)}.$$ At $t=0$, $e^{0}=1$ and the exponential factor is $e^{0}=1$, so $$M'(0) = \lambda = \mathbb{E}[X].$$ Differentiate again: $$M''(t) = \lambda e^{t}\,e^{\lambda(e^{t}-1)} + \big(\lambda e^{t}\big)^2 e^{\lambda(e^{t}-1)},$$ so $M''(0) = \lambda + \lambda^2 = \mathbb{E}[X^2]$.
Therefore $$\operatorname{Var}(X) = M''(0) - \big(M'(0)\big)^2 = (\lambda + \lambda^2) - \lambda^2 = \lambda,$$ recovering the familiar fact that a Poisson variable has equal mean and variance.

## Worked example: the gamma second moment

The gamma MGF is a clean case where the second moment $\mathbb{E}[X^2] = M''(0)$ falls out with two applications of the chain rule.
Let $X \sim \mathrm{Gamma}(\alpha, \lambda)$ (shape $\alpha$, rate $\lambda$) with $M(t) = \left(1 - t/\lambda\right)^{-\alpha}$ for $t < \lambda$.

:::spoiler Show the derivation of $\mathbb{E}[X^2]$

Write the MGF as a power so the chain rule is mechanical:

\[
M(t) = \left(1 - \frac{t}{\lambda}\right)^{-\alpha}, \qquad t < \lambda .
\]

**First derivative.** Differentiate the outer power and multiply by the inner derivative $\frac{d}{dt}\!\left(1 - t/\lambda\right) = -1/\lambda$:

\[
M'(t) = -\alpha\left(1 - \frac{t}{\lambda}\right)^{-\alpha - 1}\!\left(-\frac{1}{\lambda}\right) = \frac{\alpha}{\lambda}\left(1 - \frac{t}{\lambda}\right)^{-\alpha - 1} .
\]

Setting $t = 0$ (where $1 - t/\lambda = 1$) gives the mean:

\[
M'(0) = \frac{\alpha}{\lambda} = \mathbb{E}[X] .
\]

**Second derivative.** Differentiate $M'(t)$ the same way — the exponent drops by one again and another factor of $-1/\lambda$ appears:

\[
M''(t) = \frac{\alpha}{\lambda}\cdot(-\alpha - 1)\left(1 - \frac{t}{\lambda}\right)^{-\alpha - 2}\!\left(-\frac{1}{\lambda}\right) = \frac{\alpha(\alpha + 1)}{\lambda^{2}}\left(1 - \frac{t}{\lambda}\right)^{-\alpha - 2} .
\]

Evaluating at $t = 0$ reads off the **second moment**:

\[
\mathbb{E}[X^2] = M''(0) = \frac{\alpha(\alpha + 1)}{\lambda^{2}} .
\]

**Sanity check via the variance.** Subtracting the squared mean recovers the known gamma variance:

\[
\operatorname{Var}(X) = M''(0) - \big(M'(0)\big)^2 = \frac{\alpha(\alpha + 1)}{\lambda^{2}} - \frac{\alpha^{2}}{\lambda^{2}} = \frac{\alpha}{\lambda^{2}} .
\]

Setting $\alpha = 1$ collapses everything to the exponential: $\mathbb{E}[X^2] = 2/\lambda^2$ and $\operatorname{Var}(X) = 1/\lambda^2$.

:::

## In code

### R

```r
# Check Poisson moments from the MGF against a large sample
lambda <- 4
set.seed(1)
x <- rpois(1e6, lambda)
mean(x)  # ~ 4.00  -> M'(0)  = lambda
var(x)   # ~ 4.00  -> M''(0) - M'(0)^2 = lambda

# Numerical derivatives of M(t) = exp(lambda*(exp(t)-1)) at t = 0
M <- function(t) exp(lambda * (exp(t) - 1))
h <- 1e-4
(M(h)  - M(-h)) / (2 * h)          # ~ 4  (mean)
(M(h)  - 2 * M(0) + M(-h)) / h^2   # ~ 20 (E[X^2] = lambda + lambda^2)
```

### Python

```python
import sympy as sp

t, lam = sp.symbols('t lambda', positive=True)
M = sp.exp(lam * (sp.exp(t) - 1))          # Poisson MGF
mean = sp.diff(M, t).subs(t, 0)            # lambda
EX2  = sp.diff(M, t, 2).subs(t, 0)         # lambda + lambda**2
var  = sp.simplify(EX2 - mean**2)          # lambda
print(mean, sp.simplify(EX2), var)         # lambda  lambda**2 + lambda  lambda
```

<!-- python-output:auto -->
```text
lambda lambda*(lambda + 1) lambda
```
<!-- /python-output:auto -->

### Julia

```julia
using Symbolics

@variables t λ
M = exp(λ * (exp(t) - 1))                    # Poisson MGF
D = Differential(t)
mean = substitute(expand_derivatives(D(M)), Dict(t => 0))        # λ
EX2  = substitute(expand_derivatives(D(D(M))), Dict(t => 0))     # λ^2 + λ
println(mean, "  ", simplify(EX2 - mean^2))                      # λ   λ
```

## Why it matters

The MGF is a Swiss-army knife: it extracts means, variances, and higher moments by differentiation, identifies distributions by uniqueness, and collapses convolutions of independent variables into simple products.
Those properties make it the cleanest route to results like the central limit theorem and the additivity of normal and Poisson variables.
Through its logarithm, the cumulant generating function, it also opens the door to large-deviations theory and the Legendre-transform duality at the heart of statistical mechanics.

## Related

- [Expected Value](expected-value.md)
- [Measures of Variability](measures-of-variability.md)
- [Taylor Series](taylor-series.md)
- [Central Limit Theorem](central-limit-theorem.md)
- [Legendre Transform](legendre-transform.md)
- [Normal Distribution](normal-distribution.md)
- [Poisson Distribution](poisson-distribution.md)
- [Branching Processes](branching-processes.md)
- [Spatial Moment Equations](spatial-moment-equations.md)
- [Quantitative Methods](../math.md)
