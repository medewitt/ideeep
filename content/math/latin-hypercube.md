---
title: "Latin Hypercube Sampling"
---

# Latin Hypercube Sampling

[Latin Hypercube Sampling (LHS)](https://en.wikipedia.org/wiki/Latin_hypercube_sampling) is a space-filling design for sweeping a multi-dimensional parameter space efficiently, and helps you to sample parameter space without having to test every possible combination of values.
This is really important for developing models, estimating parameters, and exploring sensitivity to values when building computations models.
For example, sampling an [SIR model's](sir.md) transmission rate $\beta$ and recovery rate $\gamma$ so that a few dozen runs cover the plausible space far better than plain Monte Carlo in finite time.

![Latin hypercube sampling versus plain Monte Carlo, $n=5$ in the unit square on a $5\times5$ grid. Left: independent uniform draws clump and can leave whole marginal bins empty (shaded strata with no point). Right: LHS places exactly one point in each bin of every input — one per row and per column, like a Latin square — so no marginal stratum is missed.](../assets/figures/latin-hypercube.svg "fig:lhs")

## The idea: stratify, then permute

Suppose we want $n$ sample points in a $k$-dimensional unit cube $[0,1]^k$.

1. **Stratify.** Cut each dimension's $[0,1]$ range into $n$ equal-probability bins (intervals of width $1/n$).
2. **Permute.** For each dimension, place exactly one sample in each bin, in a random order.
   Independently choosing a random permutation per dimension pairs the bins across dimensions.

The result is that every one of the $n$ bins of every input is used **exactly once**.
This generalizes a Latin square (an $n\times n$ grid with one mark per row and per column) to a "Latin hypercube" in $k$ dimensions.

A point is then drawn as \[ u_{ij} = \frac{\pi_j(i) - 1 + U_{ij}}{n}, \qquad U_{ij}\sim\text{Uniform}(0,1), \] where $\pi_j$ is the permutation for dimension $j$ and $U_{ij}$ jitters the point within its bin.
Setting $U_{ij}=\tfrac12$ centers the points instead.

### Why it beats plain Monte Carlo

With $n$ independent uniform draws, the marginal coverage of each input is random — you can get clumps and gaps.
LHS forces each input's marginal to be perfectly stratified into $n$ strata, which reduces the [variance](measures-of-variability.md) of estimated means of functions that are close to additive in the inputs.
At the same $n$, LHS typically gives smoother, lower-variance estimates.

### Maximin LHS

The permutations only control marginals, so points can still lie close together in the full cube.
**Maximin LHS** searches over permutations to *maximize the minimum pairwise distance* $\min_{i\ne i'} \lVert u_i - u_{i'}\rVert$, spreading points out for better joint coverage.

### Arbitrary marginals via inverse CDFs

LHS lives on $[0,1]^k$.
To give input $j$ any target [distribution](distributions-overview.md) with CDF $F_j$, apply the inverse-CDF (quantile) transform $x_{ij} = F_j^{-1}(u_{ij})$.
Because $F_j^{-1}$ is [monotonic](monotonic-transformations.md), it maps the equal-probability bins of $[0,1]$ onto equal-probability strata of the target, so the Latin property is preserved.
For example $F^{-1}=\,$`qnorm` gives a [normal](normal-distribution.md) margin; scaling to $[a,b]$ gives a uniform margin.

## Worked example: $n = 5$, two dimensions

Take $k=2$ inputs and $n=5$ samples.
Each axis is split into 5 equal bins: $[0,0.2), [0.2,0.4), [0.4,0.6), [0.6,0.8), [0.8,1.0)$.

Choose the identity permutation for input 1 and the permutation $\pi_2 = (3,5,1,4,2)$ for input 2.
Centering points at bin midpoints ($U=\tfrac12$) gives the five design points:

| Sample $i$ | bin$_1$ | bin$_2=\pi_2(i)$ | $u_{i1}$ | $u_{i2}$ |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 1 | 3 | 0.1 | 0.5 |
| 2 | 2 | 5 | 0.3 | 0.9 |
| 3 | 3 | 1 | 0.5 | 0.1 |
| 4 | 4 | 4 | 0.7 | 0.7 |
| 5 | 5 | 2 | 0.9 | 0.3 |

Reading down each column, the five bins $\{1,2,3,4,5\}$ each appear exactly once — one point per row and per column of the $5\times5$ grid, just like a Latin square.
Plain random sampling could easily have left, say, bin 4 of input 2 empty; LHS cannot ([@fig:lhs]).

## In code

### R

```r
# install.packages("lhs")
library(lhs)
set.seed(1)

n <- 20; k <- 2
U  <- randomLHS(n, k)      # plain LHS on the unit square
Um <- maximinLHS(n, k)     # extra-spread variant

# Map columns to SIR parameter marginals via inverse CDFs:
beta  <- qunif(U[, 1], min = 0.10, max = 0.60)   # transmission rate
gamma <- qnorm(U[, 2], mean = 0.20, sd = 0.03)   # recovery rate
R0    <- beta / gamma                            # basic reproduction number
head(round(cbind(beta, gamma, R0), 3))
# Each column's 20 values are perfectly stratified into 20 quantile bins.
```

### Python

```python
import numpy as np
from scipy.stats import norm
from scipy.stats.qmc import LatinHypercube, scale
np.random.seed(0)

n, d = 20, 2
sampler = LatinHypercube(d=d, seed=0)
U = sampler.random(n)                      # LHS on [0,1]^2

# Uniform margins via qmc.scale; normal margin via inverse CDF (ppf):
XU = scale(U, l_bounds=[0.10, 0.0], u_bounds=[0.60, 1.0])
beta  = XU[:, 0]                           # Uniform(0.10, 0.60)
gamma = norm.ppf(U[:, 1], loc=0.20, scale=0.03)
R0 = beta / gamma
print(np.round(np.c_[beta, gamma, R0][:5], 3))
```

<!-- python-output:auto -->
```text
[[0.584 0.236 2.472]
 [0.124 0.192 0.645]
 [0.255 0.121 2.099]
 [0.31  0.181 1.712]
 [0.286 0.25  1.144]]
```
<!-- /python-output:auto -->

### Julia

```julia
using QuasiMonteCarlo, Distributions, Random
Random.seed!(0)

n  = 20
lb = [0.10, 0.0]; ub = [0.60, 1.0]
S  = QuasiMonteCarlo.sample(n, lb, ub, LatinHypercubeSample())  # 2 x n matrix

beta  = S[1, :]                                   # Uniform(0.10, 0.60)
u2    = (S[2, :] .- lb[2]) ./ (ub[2] - lb[2])     # back to [0,1]
gamma = quantile.(Normal(0.20, 0.03), u2)         # inverse-CDF transform
R0    = beta ./ gamma
println(round.(hcat(beta, gamma, R0)[1:5, :], digits = 3))
```

## Why it matters for statistics

Many statistical and epidemiological questions boil down to "how does model output vary as uncertain inputs vary?"
Estimating output means, quantiles, and [sensitivity indices](sensitivity-analysis.md) requires a design of input points.
LHS gives low-variance, [reproducible](../programming/reproducibility.md) coverage at a fixed budget $n$, which is decisive when each model run is expensive (large simulations, ODE solves, or Bayesian posterior evaluations).
It is the standard front end for variance-based sensitivity analysis and for building emulators of costly models.

## Related

- [Global Sensitivity Analysis](sensitivity-analysis.md)
- [The SIR Model](sir.md)
- [Distributions Overview](distributions-overview.md)
- [Survey Sampling](survey-sampling.md)
- [Quantitative Methods](../math.md)
