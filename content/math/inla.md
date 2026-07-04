---
title: "Bayesian Spatial Models with INLA"
description: "INLA approximates posterior marginals for latent Gaussian models — GLMMs, CAR/BYM areal models, and geostatistics — with nested Laplace approximations instead of MCMC."
---

# Bayesian Spatial Models with INLA

Fitting a spatial Bayesian model usually means MCMC: run a sampler for hours, then squint at trace plots to decide whether it converged.
For the enormous class of models built on a latent Gaussian field — mixed models, disease-mapping models, geostatistics — there is a faster, deterministic alternative.
Integrated Nested Laplace Approximation ([Rue, Martino & Chopin 2009](https://rss.onlinelibrary.wiley.com/doi/10.1111/j.1467-9868.2008.00700.x)) computes the posterior marginals directly, with no sampling and no convergence diagnostics, by exploiting the sparsity that these models carry.

![A finite-element SPDE mesh triangulating a spatial domain, with scattered observation points; INLA fits a continuous-space Matérn field as a sparse Gaussian Markov random field defined on this mesh.](../assets/figures/inla.svg)

## The latent Gaussian model

INLA is not a general-purpose engine; it is fast because it targets one specific, but very broad, structure.
A **latent Gaussian model** has three layers.
First, a vector of hyperparameters $\theta$ (a handful of variances, correlation ranges, and likelihood dispersions) with some prior $\pi(\theta)$.
Second, a **latent field** $x$ that, given $\theta$, is multivariate Gaussian, $x \mid \theta \sim \mathcal{N}(0, Q(\theta)^{-1})$.
Third, observations $y$ that are **conditionally independent** given the latent field, $\pi(y \mid x, \theta) = \prod_i \pi(y_i \mid x_i, \theta)$, through any likelihood you like (Poisson counts, binomial prevalences, Gaussian measurements).

The whole method turns on the structure of the **precision matrix** $Q(\theta)$, the inverse of the covariance.
When the latent field is a [Gaussian Markov random field](gaussian-processes.md) (GMRF), $Q$ is **sparse**: $Q_{ij}=0$ whenever nodes $i$ and $j$ are conditionally independent given the rest, which for a spatial field means whenever they are not neighbors.
Most of the classical spatial toolbox lives inside this template.
A [GLMM](hierarchical-models.md) has $x$ collecting fixed and random effects; a [CAR or BYM areal model](areal-models-car.md) has $x$ a field over regions with $Q$ built from the adjacency graph; a geostatistical model has $x$ a continuous spatial surface.
Sparsity is the free lunch: linear algebra on a sparse $Q$ — Cholesky factorization, solves, log-determinants — costs a fraction of the dense equivalent, and that is what makes the approximations below cheap.

## How INLA approximates the posterior

We rarely want the full joint posterior; we want the **marginals** — a posterior for each latent value $\pi(x_i \mid y)$ and each hyperparameter $\pi(\theta_j \mid y)$.
INLA builds them in two nested stages.

Start from the identity $$\pi(x_i \mid y) = \int \pi(x_i \mid \theta, y)\,\pi(\theta \mid y)\,d\theta.$$ The outer factor $\pi(\theta \mid y)$ is a density over just a few hyperparameters, so it can be explored on a grid.
The inner factor $\pi(x_i \mid \theta, y)$ is where the Laplace approximation does its work.

### The Laplace approximation

A Laplace approximation replaces an intractable density by the Gaussian that matches its **mode** and its **curvature** at the mode.
If $g(x)=\log \pi(x \mid \theta, y)$, expand to second order around the mode $x^\star$ where $g'(x^\star)=0$: $$g(x) \approx g(x^\star) - \tfrac{1}{2}(x-x^\star)^\top H (x-x^\star), \qquad H = -g''(x^\star),$$ which is exactly the log-density of $\mathcal{N}\!\big(x^\star, H^{-1}\big)$.
The mode is found by a few Newton steps, and the curvature $H$ inherits the sparsity of $Q$, so factorizing it is cheap.
INLA uses this idea twice: once to approximate $\pi(\theta \mid y)$ (the Laplace approximation to the marginal likelihood), and again — as a more careful, skew-corrected "nested" Laplace step — for each $\pi(x_i \mid \theta, y)$.

Putting it together, INLA (1) locates the mode of $\pi(\theta \mid y)$ and lays down a small set of integration points $\{\theta^{(k)}\}$ with weights $\{\Delta_k\}$ around it, (2) at each $\theta^{(k)}$ forms the nested Laplace approximation of $\pi(x_i \mid \theta^{(k)}, y)$, and (3) sums them, $\pi(x_i \mid y) \approx \sum_k \pi(x_i \mid \theta^{(k)}, y)\,\pi(\theta^{(k)} \mid y)\,\Delta_k$.
There is no Markov chain, so there is nothing to converge and no autocorrelation to thin — the cost is deterministic and the answer is the same every run.

## The SPDE approach: continuous space as a GMRF

Areal models are GMRFs by construction, but classical geostatistics works in **continuous space** with a dense covariance, the usual obstacle to using INLA for point-referenced data.
The bridge is the SPDE approach of [Lindgren, Rue & Lindström (2011)](https://rss.onlinelibrary.wiley.com/doi/10.1111/j.1467-9868.2011.00777.x).
Their starting point is a classical fact: a Gaussian field with a **Matérn** covariance is the stationary solution of the stochastic partial differential equation $$(\kappa^2 - \Delta)^{\alpha/2}\, x(s) = \mathcal{W}(s),$$ where $\Delta$ is the Laplacian, $\mathcal{W}$ is Gaussian white noise, and $\alpha$ sets the smoothness.

Solving that SPDE by the **finite-element method** — triangulate the domain with a mesh (the figure above), represent the field by a value at each mesh node, and interpolate linearly inside triangles — turns the continuous field into a GMRF on the mesh nodes with a sparse precision $Q(\kappa, \tau)$ assembled from the mesh geometry.
So a continuous Matérn surface is fit *as if* it were an areal GMRF, and INLA's sparsity machinery applies unchanged.
The two hyperparameters are usually reported as interpretable quantities: the Matérn **range** $\rho = \sqrt{8\nu}/\kappa$, the distance at which spatial correlation drops to about $0.1$, and the marginal standard deviation $\sigma$ of the field.
Mesh resolution matters — it must be fine relative to the range where you have data — and observations are tied to the field through a sparse projection from mesh nodes to observation locations.

## When to prefer INLA over MCMC

The rule of thumb is simple: use INLA when your model *is* a latent Gaussian model, and reach for [MCMC](mcmc.md) when it is not.

> [!TIP]
> INLA is fast and accurate precisely for latent Gaussian models with a sparse precision $Q$ and few hyperparameters.
> It is not a general-purpose sampler: many hyperparameters, non-Gaussian latent structure, or a likelihood that does not factorize conditionally on $x$ all push you back to MCMC.

For a BYM disease-mapping model or an SPDE geostatistical model, INLA returns in seconds what MCMC delivers in minutes to hours, with marginals that are typically indistinguishable from a long, well-mixed chain.
Its limitations are the flip side of its assumptions: the latent field must be Gaussian, the number of hyperparameters should be small (each one adds a dimension to the numerical integration over $\theta$), and unusual likelihoods or hard constraints may fall outside what the approximation handles well.

## In code

INLA is distributed as the **R-INLA** package, so the realistic, full example is in R; the Python and Julia blocks below illustrate the underlying ideas instead.

### R

A typical SPDE workflow: build a mesh, define a Matérn field with penalized-complexity priors, project it onto the data, and fit.

```r
library(INLA)

# --- point-referenced prevalence data: coords (x, y), cases, n trials ---
coords <- as.matrix(dat[, c("x", "y")])

# 1. Triangulated mesh over the study region
mesh <- inla.mesh.2d(loc = coords, max.edge = c(0.3, 1), cutoff = 0.05)

# 2. Matern SPDE with PC priors: P(range < 0.5) = 0.05, P(sigma > 1) = 0.05
spde <- inla.spde2.pcmatern(mesh,
          prior.range = c(0.5, 0.05),
          prior.sigma = c(1.0, 0.05))

# 3. Projector matrix A maps mesh nodes -> observation locations
A <- inla.spde.make.A(mesh, loc = coords)
s.index <- inla.spde.make.index("spatial", n.spde = spde$n.spde)

# 4. Stack the data, the projector, and an intercept
stk <- inla.stack(
  data    = list(y = dat$cases),
  A       = list(A, 1),
  effects = list(s.index, list(intercept = rep(1, nrow(dat)))),
  tag     = "est")

# 5. Fit: binomial likelihood, spatial Matern field
form <- y ~ 0 + intercept + f(spatial, model = spde)
fit  <- inla(form,
             family            = "binomial",
             Ntrials           = dat$n,
             data              = inla.stack.data(stk),
             control.predictor = list(A = inla.stack.A(stk)),
             control.compute   = list(dic = TRUE, waic = TRUE))

summary(fit)                       # posterior marginals for intercept, range, sigma
fit$summary.hyperpar               # Matern range and marginal SD, posterior quantiles
```

For a **BYM areal model** the field is defined on an adjacency graph instead of a mesh: `f(region, model = "bym2", graph = adj)` replaces the SPDE term, with `adj` built from region neighbors by `inla.read.graph`.

### Python

INLA itself is R-only, but its engine is the **Laplace approximation** — match a Gaussian to the mode and curvature of the conditional posterior.
Here is that step in miniature for a latent Gaussian toy: one Poisson count with a Gaussian prior on the log-rate.

```python
import numpy as np

rng = np.random.default_rng(0)  # deterministic; toy has no randomness

# Latent Gaussian toy: y ~ Poisson(exp(x)) with prior x ~ N(0, s2).
# log posterior (up to a constant): y*x - exp(x) - x^2 / (2 s2)
y, s2 = 8.0, 1.0

# Newton iteration to the mode: g'(x) = y - exp(x) - x/s2, g''(x) = -exp(x) - 1/s2
x = 0.0
for _ in range(20):
    x -= (y - np.exp(x) - x / s2) / (-np.exp(x) - 1 / s2)
prec = np.exp(x) + 1 / s2        # -g''(mode): the Laplace (Gaussian) precision
sd = prec ** -0.5

# Gold standard: normalize the exact posterior on a fine grid.
xs = np.linspace(-2, 4, 20001)
w = np.exp(y * xs - np.exp(xs) - xs**2 / (2 * s2))
w /= np.trapezoid(w, xs)
mean = np.trapezoid(xs * w, xs)
var = np.trapezoid((xs - mean) ** 2 * w, xs)

print(f"Laplace: mode={x:.3f}  sd={sd:.3f}")
print(f"Grid:    mean={mean:.3f}  sd={var ** 0.5:.3f}")
```

<!-- python-output:auto -->
```text
Laplace: mode=1.821  sd=0.373
Grid:    mean=1.761  sd=0.381
```
<!-- /python-output:auto -->

The Laplace Gaussian nearly reproduces the exact posterior mean and spread; INLA's added refinement is to correct the small remaining skew and to integrate this step over the hyperparameters.

### Julia

The same Laplace step, and the sparsity that makes it scale, are natural in Julia.

```julia
using LinearAlgebra, SparseArrays

# Newton to the mode of the Poisson-Gaussian toy posterior
y, s2 = 8.0, 1.0
x = 0.0
for _ in 1:20
    g1 = y - exp(x) - x / s2          # first derivative
    g2 = -exp(x) - 1 / s2             # second derivative
    x -= g1 / g2
end
sd = 1 / sqrt(exp(x) + 1 / s2)        # Laplace precision -> SD
println("mode = ", round(x, digits=3), "  sd = ", round(sd, digits=3))

# A GMRF precision is sparse: e.g. a 1-D random walk on n nodes
n = 6
Q = spdiagm(-1 => fill(-1.0, n - 1), 0 => [1.0; fill(2.0, n - 2); 1.0],
            1 => fill(-1.0, n - 1))   # tridiagonal -> cheap Cholesky
```

## Why it matters

Disease mapping is INLA's flagship application.
A [BYM areal model](areal-models-car.md) smooths noisy county-level rates by borrowing strength from neighbors, separating genuine spatial signal from small-count noise, and INLA fits it for a whole country in seconds.
For point-referenced data — prevalence surveys, pollutant exposures, vector abundance — the SPDE approach fits a continuous [Matérn surface](covariance-functions.md) and predicts at unsampled locations, the Bayesian counterpart of [kriging](kriging.md) with full uncertainty on the range and variance.
Environmental epidemiology leans on the same machinery to link modeled exposure surfaces to health outcomes while propagating spatial uncertainty end to end.
Because the fit is fast and reproducible, INLA turns spatial model *comparison* — swapping covariates, priors, or mesh resolutions and reading off DIC or WAIC — into something you can do interactively rather than overnight.

## Related

- [Bayesian Inference](bayesian-inference.md)
- [Markov Chain Monte Carlo](mcmc.md)
- [Hierarchical Models](hierarchical-models.md)
- [Areal Models and CAR](areal-models-car.md)
- [Kriging](kriging.md)
- [Gaussian Processes](gaussian-processes.md)
- [Covariance Functions](covariance-functions.md)
- [Quantitative Methods](../math.md)
