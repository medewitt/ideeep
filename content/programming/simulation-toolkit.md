---
title: "A Simulation Toolkit"
---

# A Simulation Toolkit

Simulation is the statistician's laboratory: when you can't derive a result on paper, you can generate fake data from a known process and *watch* what an estimator does. Because you control the truth, you can check whether a method recovers it. This page collects the practical tools for doing that in R, Python, and Julia.

## Start from a known data-generating process

The core move is to invent a **data-generating process (DGP)** with parameters you choose, draw data from it, and then apply your method. Any gap between your estimate and the known truth is bias, [variance](../math/measures-of-variability.md), or a bug.

```r
set.seed(1)                      # reproducibility first
n <- 100
beta_true <- 2.0
x <- rnorm(n)
y <- beta_true * x + rnorm(n)    # truth is beta = 2
coef(lm(y ~ x - 1))              # does OLS recover ~2?
```

## Core verbs, across three languages

Most simulation work is some mix of: draw random numbers, repeat many times, [optimize](../math/optimization.md), root-find, [integrate](../math/integrals.md), and [differentiate](../math/derivatives.md). Here is the same toolbox in each language.

| Task | R | Python (NumPy/SciPy) | Julia |
|---|---|---|---|
| Set seed | `set.seed(1)` | `np.random.default_rng(1)` | `Random.seed!(1)` |
| Normal draws | `rnorm(n)` | `rng.normal(size=n)` | `randn(n)` |
| Binomial draws | `rbinom(n, k, p)` | `rng.binomial(k, p, n)` | `rand(Binomial(k, p), n)` |
| Repeat an expression | `replicate(B, expr)` | list comp / `np.array([... for _ in range(B)])` | `[expr for _ in 1:B]` |
| Map over inputs | `sapply(xs, f)` | `np.vectorize(f)(xs)` / comprehension | `map(f, xs)` / `f.(xs)` |
| Minimize (multivar.) | `optim(par, fn)` | `scipy.optimize.minimize` | `optimize(f, x0)` (Optim.jl) |
| Minimize (1-D) | `optimize(f, interval)` | `scipy.optimize.minimize_scalar` | `optimize(f, a, b)` (Optim.jl) |
| Find a root | `uniroot(f, interval)` | `scipy.optimize.brentq` | `find_zero(f, x0)` (Roots.jl) |
| Numerical integral | `integrate(f, a, b)` | `scipy.integrate.quad` | `quadgk(f, a, b)` (QuadGK.jl) |
| Derivative | `deriv()` / `numDeriv::grad` | `scipy.misc`/autograd, or finite diff | `ForwardDiff.derivative` |

```python
import numpy as np
from scipy import optimize, integrate
rng = np.random.default_rng(1)

optimize.minimize_scalar(lambda t: (t - 3)**2)      # minimize
optimize.brentq(lambda t: t**2 - 2, 0, 2)           # root: sqrt(2)
integrate.quad(lambda t: np.exp(-t**2), 0, 1)       # integral
```

```julia
using Random, Distributions, Optim, QuadGK, ForwardDiff, Roots
Random.seed!(1)

optimize(t -> (t[1] - 3)^2, [0.0])                  # minimize
find_zero(t -> t^2 - 2, 1.0)                        # root: sqrt(2)
quadgk(t -> exp(-t^2), 0, 1)                        # integral
ForwardDiff.derivative(t -> t^3, 2.0)               # exact derivative = 12
```

## Worked mini simulation study: coverage of a confidence interval

Question: for the sample mean of $n$ [normal](../math/normal-distribution.md) observations, does the usual 95% t-interval actually contain the true mean 95% of the time? We can *check* by simulation.

The recipe is the workhorse pattern — **generate, fit, record, repeat**:

```r
set.seed(2026)

mu_true    <- 5
n          <- 20
n_sims     <- 10000
conf_level <- 0.95

covered <- replicate(n_sims, {
  y  <- rnorm(n, mean = mu_true, sd = 1)   # 1. generate from known DGP
  ci <- t.test(y, conf.level = conf_level)$conf.int  # 2. fit / estimate
  ci[1] <= mu_true && mu_true <= ci[2]     # 3. record: did it cover?
})

mean(covered)   # should be ~0.95
#> [1] 0.9503
```

The same study in Python:

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(2026)
mu_true, n, n_sims = 5, 20, 10_000

covered = np.empty(n_sims, dtype=bool)
for i in range(n_sims):
    y = rng.normal(mu_true, 1.0, size=n)          # generate
    lo, hi = stats.t.interval(0.95, n - 1,        # fit
                              loc=y.mean(),
                              scale=stats.sem(y))
    covered[i] = lo <= mu_true <= hi              # record

covered.mean()   # ~0.95
```

And in Julia:

```julia
using Random, Statistics, Distributions

Random.seed!(2026)
mu_true, n, n_sims = 5.0, 20, 10_000

covered = falses(n_sims)
for i in 1:n_sims
    y  = rand(Normal(mu_true, 1.0), n)            # generate
    m  = mean(y); se = std(y) / sqrt(n)
    tc = quantile(TDist(n - 1), 0.975)            # fit
    covered[i] = (m - tc*se) <= mu_true <= (m + tc*se)   # record
end

mean(covered)   # ~0.95
```

## Why this works

Repeating the draw-and-estimate loop many times approximates the estimator's **[sampling distribution](../math/sampling-distributions.md)**, and the average of an indicator (like "did the interval cover?") converges to its true probability by the [law of large numbers](../math/law-of-large-numbers.md). That is the engine behind every coverage check, power calculation, and bias estimate you'll run by simulation.

Practical tips:

- **Seed once, at the top**, and report the seed.
- **Vary one thing at a time** (e.g. loop over `n`) to see how behavior scales.
- **Start small** (`n_sims <- 100`) to debug, then crank it up for the final numbers.
- **Vectorize or use `replicate`/comprehensions** rather than growing objects in a loop.

## Related

- [Reproducibility](reproducibility.md)
- [Good Programming Practices](good-programming-practices.md)
- [Project Workflow](project-workflow.md)
- [Law of Large Numbers](../math/law-of-large-numbers.md)
- [Sampling Distributions](../math/sampling-distributions.md)
- [Maximum Likelihood](../math/maximum-likelihood.md)
- [Programming & Computing](../programming.md)
