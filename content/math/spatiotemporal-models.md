---
title: "Spatiotemporal Models"
description: "Extending spatial models to space and time: separable versus nonseparable covariance, Knorr-Held space-time interaction types for areal counts, spatiotemporal Gaussian processes, and mapping evolving risk in surveillance."
---

# Spatiotemporal Models

Disease does not sit still.
An outbreak starts somewhere, spreads to neighboring places, and rises and falls on its own clock, so a snapshot map throws away half the information.
A spatiotemporal model treats risk as a surface over both space and time, borrowing strength from nearby locations and from adjacent time steps at once, which is what lets surveillance turn a stream of dated, located case counts into an evolving risk map.

![Four weekly slices of a simulated spatiotemporal risk field showing a single cluster whose center drifts across the map and whose amplitude grows over time.](../assets/figures/spatiotemporal-models.svg)

## Separable space-time covariance

The simplest way to build a spatiotemporal correlation structure is to multiply a spatial one by a temporal one.
Write the covariance between values at locations $s, s'$ and times $t, t'$ as a product \[ C\big((s,t),(s',t')\big) = \sigma^2\, C_S\big(\lVert s - s'\rVert\big)\, C_T\big(\lvert t - t'\rvert\big), \] where $C_S$ is a purely spatial [correlation function](covariance-functions.md), such as an exponential or [Matérn](covariance-functions.md), and $C_T$ is a purely temporal one, such as an AR(1) decay $\rho^{\lvert t - t'\rvert}$.
This is a **separable** kernel.
It is cheap because its covariance matrix is a Kronecker product of a small spatial matrix and a small temporal matrix, so factorizations that would be impossible on the full space-time grid become routine.
The price is a strong assumption: separability forces the spatial correlation range to be the same at every time lag and the temporal decay to be the same at every distance.

Separability shows itself in a factorization you can check directly.
The correlation between two space-time points equals the product of the space-only correlation at that distance and the time-only correlation at that lag, \[ \mathrm{Corr}\big((s,t),(s',t')\big) = C_S\big(\lVert s - s'\rVert\big)\cdot C_T\big(\lvert t - t'\rvert\big), \] and a **nonseparable** kernel breaks that product.
Real transmission is usually nonseparable, because a pathogen needs time to travel through space, so correlation across distance grows with the time lag rather than staying fixed.
Nonseparable families, such as the Gneiting class, introduce space-time interaction directly in the kernel and reduce to a separable kernel as a special case.

## Space-time interaction in areal models

For counts aggregated to regions and time periods, the spatiotemporal model is usually an extension of the [BYM areal model](areal-models-car.md).
A log-relative-risk for region $i$ in period $t$ is built from additive pieces \[ \log \mu_{it} = \alpha + u_i + v_i + \gamma_t + \phi_t + \delta_{it}, \] where $u_i + v_i$ is the familiar BYM spatial term (a smooth [CAR/ICAR](areal-models-car.md) field plus unstructured heterogeneity), $\gamma_t + \phi_t$ is a temporal trend (a smooth random walk plus unstructured time noise), and $\delta_{it}$ is a **space-time interaction** that captures departures from a purely additive space-plus-time pattern.

Knorr-Held classified the interaction $\delta_{it}$ into four types by which main effects interact.
**Type I** treats the interaction as unstructured in both space and time, independent noise per cell.
**Type II** lets each region follow its own independent temporal trend (interaction structured in time, unstructured in space).
**Type III** lets each time period have its own independent spatial pattern (structured in space, unstructured in time).
**Type IV** makes the interaction structured in both, so a region's trend depends on its neighbors' trends, which is the fully coupled space-time model appropriate when the process genuinely spreads through the region graph over time.
Choosing the type is choosing what kind of local departure you expect the data to show.

## Spatiotemporal Gaussian processes

When locations are points rather than regions, the continuous analogue is a [Gaussian process](gaussian-processes.md) over space and time.
The latent log-intensity or log-risk is a zero-mean GP with a spatiotemporal covariance, separable or not, and everything from [kriging](kriging.md) carries over: predicting risk at an unobserved location and time is a conditional-normal calculation, and the [covariance function](covariance-functions.md) sets how far in space and how far in time the data inform that prediction.
Fitting a full spatiotemporal GP is expensive because the covariance matrix grows with locations times time steps, so practical work leans on structure, either a separable Kronecker covariance or a sparse representation, which is where [INLA](inla.md) with an SPDE spatial term and a temporal random walk becomes the standard route.

## A worked example

Build a separable covariance from an exponential spatial kernel and an AR(1) temporal kernel.
Take the spatial correlation $C_S(h) = e^{-h/\phi}$ with range $\phi = 2$ and the temporal correlation $C_T(u) = \rho^{\lvert u\rvert}$ with $\rho = 0.7$, and set the marginal variance to $1$ so covariance equals correlation.
At zero separation the correlation is $1$.
Move two units in space at the same time and it drops to $C_S(2) = e^{-1} \approx 0.368$.
Move one step in time at the same location and it drops to $C_T(1) = 0.7$.
The separability check is that the correlation at the joint lag equals the product of the two marginal drops: $C(2,1) = e^{-1}\cdot 0.7 \approx 0.258$, which is exactly $C_S(2)\, C_T(1)$.
The joint correlation carries no information beyond the two one-dimensional decays, which is both the strength and the limitation of a separable model.

## In code

### R

```r
library(INLA)   # BYM + temporal RW + Knorr-Held Type IV interaction

# df: region id (i), time id (t), count y, expected E; g: adjacency graph
formula <- y ~ 1 +
  f(i, model = "bym2", graph = g, scale.model = TRUE) +   # spatial
  f(t, model = "rw1") +                                    # temporal trend
  f(it, model = "iid",                                     # space-time interaction
    group = t.group, control.group = list(model = "besag", graph = g))

fit <- inla(formula, family = "poisson", E = E, data = df,
            control.predictor = list(compute = TRUE))
summary(fit)

# Separable spatiotemporal kriging with gstat: a space-time variogram
library(gstat); library(spacetime)
v_st <- variogramST(z ~ 1, data = stfdf, tlags = 0:6)
fit_st <- fit.StVariogram(v_st, vgmST("separable",
              space = vgm(1, "Exp", 200), time = vgm(1, "Exp", 3), sill = 1))
```

### Python

Construct a separable spatiotemporal covariance and print correlations at a few space-time lags, then check that the joint correlation factorizes.

```python
import numpy as np

# Separable covariance C(h, u) = sigma^2 * Cs(h) * Ct(u):
# exponential in space (range phi), AR(1) in time (correlation rho).
sigma2, phi, rho = 1.0, 2.0, 0.7


def c_space(h):
    return np.exp(-h / phi)


def c_time(u):
    return rho ** np.abs(u)


def cov(h, u):
    return sigma2 * c_space(h) * c_time(u)


# sigma^2 = 1, so covariance equals correlation here.
for h, u in [(0, 0), (2, 0), (0, 1), (2, 1), (4, 2)]:
    print(f"h={h}, u={u}:  corr = {cov(h, u):.3f}")

# Separability: the joint correlation is the product of the marginal decays.
joint = cov(2, 1)
product = cov(2, 0) * cov(0, 1)
print(f"C(2,1) = {joint:.3f}  vs  C(2,0)*C(0,1) = {product:.3f}  -> separable")
```

<!-- python-output:auto -->
```text
h=0, u=0:  corr = 1.000
h=2, u=0:  corr = 0.368
h=0, u=1:  corr = 0.700
h=2, u=1:  corr = 0.258
h=4, u=2:  corr = 0.066
C(2,1) = 0.258  vs  C(2,0)*C(0,1) = 0.258  -> separable
```
<!-- /python-output:auto -->

### Julia

```julia
# Separable spatiotemporal covariance: exponential in space, AR(1) in time.
sigma2, phi, rho = 1.0, 2.0, 0.7

c_space(h) = exp(-h / phi)
c_time(u)  = rho^abs(u)
cov(h, u)  = sigma2 * c_space(h) * c_time(u)

for (h, u) in [(0, 0), (2, 0), (0, 1), (2, 1), (4, 2)]
    println("h=$h, u=$u:  corr = ", round(cov(h, u), digits = 3))
end

# Separability check.
println(round(cov(2, 1), digits = 3), " vs ",
        round(cov(2, 0) * cov(0, 1), digits = 3), "  -> separable")
```

## Why it matters

Spatiotemporal models are how modern surveillance maps evolving risk.
By pooling information across neighboring areas and adjacent weeks, they stabilize small-area estimates that would be too noisy period by period, and they let an analyst ask directional questions a static map cannot: is the cluster growing, is it moving toward a new population, is the trend in one district running ahead of its neighbors.
The separable-versus-nonseparable choice is not just computational bookkeeping; it encodes whether you believe space and time act independently or whether the process spreads, and getting it wrong understates how correlation builds up along the path an epidemic actually takes.
Detecting that a cluster exists at all is the job of [spatial cluster detection](spatial-cluster-detection.md); a spatiotemporal model is what you fit once you want to track and forecast it.

## Related

- [Areal Models: CAR, ICAR, and BYM](areal-models-car.md)
- [Gaussian Processes](gaussian-processes.md)
- [Covariance Functions and the Matérn Family](covariance-functions.md)
- [Bayesian Spatial Models with INLA](inla.md)
- [Kriging and Geostatistics](kriging.md)
- [Spatial Cluster Detection](spatial-cluster-detection.md)
- [Quantitative Methods](../math.md)
