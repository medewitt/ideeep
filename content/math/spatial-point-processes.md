---
title: "Spatial Point Processes"
description: "Modeling event locations in space as a random point pattern: the Poisson process, complete spatial randomness, and clustered Cox and log-Gaussian Cox processes."
---

# Spatial Point Processes

Where a thing happens is often as informative as how often it happens.
The nests of a bird, the trees of a species, the households reporting a new infection — each is a set of *locations* scattered across a map, and a spatial point process is the probability model for that scatter.
Instead of predicting a value at every point (as a spatial field would), it treats the number and positions of the points themselves as random.

![Three simulated spatial point patterns on the unit square: complete spatial randomness, an inhomogeneous Poisson trend, and a clustered log-Gaussian Cox process, all with a comparable expected count.](../assets/figures/spatial-point-processes.svg)

## The intensity function

A point process on a region is described by its **intensity function** $\lambda(s)$, the expected density of points per unit area at location $s$.
Over any sub-region $A$ the expected number of points is the integral of the intensity, $$\mathbb{E}[N(A)] = \int_A \lambda(s)\,\mathrm{d}s \equiv \Lambda(A),$$ where $N(A)$ counts the points that fall in $A$ and $\Lambda(A)$ is the **integrated intensity**.
When $\lambda(s)\equiv\lambda$ is constant, this reduces to $\mathbb{E}[N(A)] = \lambda\,\lvert A\rvert$, intensity times area.
The intensity is a first-order property: it tells you *how many* points to expect and *where* they concentrate, but not whether points attract or repel one another.

## The homogeneous Poisson process

The reference model — the spatial analogue of "nothing is going on" — is the **homogeneous Poisson process**, which encodes **complete spatial randomness (CSR)**.
It is defined by two properties.

1. **Poisson counts.** For any region $A$, the count $N(A)$ follows a [Poisson distribution](poisson-distribution.md) with mean $\lambda\,\lvert A\rvert$: $$N(A)\sim\mathrm{Poisson}\!\left(\lambda\,\lvert A\rvert\right).$$
2. **Complete independence.** For disjoint regions $A_1,\dots,A_k$, the counts $N(A_1),\dots,N(A_k)$ are mutually [independent](probability-basics.md) random variables.

A remarkable consequence follows: **conditional on the total count $N(A)=n$, the $n$ points are independent and uniformly distributed over $A$**.
So you can simulate CSR in two steps — draw how many points there are from a Poisson distribution, then throw each of them down uniformly at random, independently of the others.
Because the mean equals the variance for a Poisson, CSR has $\operatorname{Var}(N(A))=\mathbb{E}[N(A)]$, the benchmark against which real patterns are judged over- or under-dispersed.

## The inhomogeneous Poisson process

Real environments are not uniform: cases cluster where people live, nests concentrate where habitat is good.
The **inhomogeneous Poisson process** keeps the independence but lets the intensity vary in space, $\lambda(s)$.
Counts are still Poisson and disjoint regions are still independent — only the mean changes, $$N(A)\sim\mathrm{Poisson}\!\left(\int_A \lambda(s)\,\mathrm{d}s\right).$$ Given $N(A)=n$, the points are now independent draws from the density $\lambda(s)/\Lambda(A)$ rather than the uniform, so they crowd into the high-intensity regions.

A clean way to build one is **thinning**.
Start from a homogeneous process at the maximum rate $\lambda_{\max}=\sup_s\lambda(s)$, then keep each candidate point at $s$ independently with probability $p(s)=\lambda(s)/\lambda_{\max}$.
The survivors form an inhomogeneous Poisson process with exactly the intensity $\lambda(s)$, because independent thinning of a Poisson process by a probability $p(s)$ yields a Poisson process with intensity $p(s)\lambda(s)$.
Thinning is the workhorse for simulation and also the natural model for imperfect detection, where $p(s)$ is the probability an event that occurred at $s$ is actually observed.

> [!NOTE]
> Both Poisson models share **complete independence**: knowing where some points landed tells you nothing about where the others are.
> Any clustering an inhomogeneous Poisson process shows is entirely due to a varying $\lambda(s)$, not to interaction between points.

## Cox processes: when the intensity is itself random

Often we do not know $\lambda(s)$ — it depends on unobserved environmental drivers, and it is more honest to treat it as random.
A **Cox process** (a *doubly-stochastic Poisson process*) does exactly that: first draw a random intensity surface $\Lambda(s)$, then, conditional on it, generate an inhomogeneous Poisson process with that intensity.
Randomness now enters twice — once in the surface, once in the points given the surface — which is why the counts are more variable than Poisson.

By the [laws of total expectation and variance](expected-value.md), the count in a region satisfies $$\mathbb{E}[N(A)] = \mathbb{E}[\Lambda(A)], \qquad \operatorname{Var}(N(A)) = \underbrace{\mathbb{E}[\Lambda(A)]}_{\text{Poisson part}} + \underbrace{\operatorname{Var}(\Lambda(A))}_{\text{extra}}.$$ The variance strictly exceeds the mean whenever the intensity surface is genuinely random, so **every Cox process is overdispersed relative to Poisson**.
That extra variance shows up spatially as **clustering**: regions where the surface happened to be high receive bursts of points, and the pattern looks patchy even though, conditionally, the points never "interact."

### The log-Gaussian Cox process

To make $\Lambda(s)$ a flexible, positive, spatially smooth random surface, the most popular choice puts a [Gaussian process](gaussian-processes.md) on its logarithm.
A **log-Gaussian Cox process (LGCP)** takes $$\log\lambda(s) = \mu(s) + Z(s), \qquad Z(\cdot)\sim\mathrm{GP}\!\left(0,\;k(\cdot,\cdot)\right),$$ where $\mu(s)$ is a deterministic mean (often a regression on covariates) and $Z$ is a zero-mean Gaussian process whose [covariance function](covariance-functions.md) $k$ sets the correlation length of the clustering.
Exponentiating keeps the intensity positive, and the smoothness of the field is inherited from the [covariance kernel](covariance-functions.md), the same machinery used for [kriging](kriging.md) a continuous surface.
Because $\log\lambda(s)$ is Gaussian, the pointwise intensity is log-normal, so $\mathbb{E}[\lambda(s)] = \exp\!\big(\mu(s) + \tfrac{1}{2}\sigma^2\big)$ with $\sigma^2 = k(s,s)$, and a larger field variance $\sigma^2$ means both a higher mean intensity and heavier clustering.

> [!NOTE]
> **Neyman–Scott and Thomas processes** cluster differently: scatter unseen "parent" points as a Poisson process, then place a random number of "offspring" around each parent (Gaussian-displaced offspring give the **Thomas process**).
> These are also Cox processes, and like the LGCP they generate overdispersion — but the mechanism is explicit parent-offspring aggregation rather than a smooth latent field, which fits seeds near a plant or secondary cases near an index case.

## A worked example

**Homogeneous baseline.** Suppose bird nests occur at a constant intensity $\lambda = 5$ per km$^2$ across a $4$ km$^2$ reserve.
The nest count is $N\sim\mathrm{Poisson}(\lambda\lvert A\rvert)=\mathrm{Poisson}(20)$, so $\mathbb{E}[N]=20$ and $\operatorname{Var}(N)=20$, giving a standard deviation of $\sqrt{20}\approx 4.5$.
The chance of finding an empty reserve is $P(N=0)=e^{-20}\approx 2\times10^{-9}$ — effectively impossible under CSR.

**An intensity trend.** Now let the intensity rise toward better habitat, $\lambda(x,y) = \lambda_0\,e^{\,x}$ on the unit square $[0,1]^2$ with $\lambda_0 = 12$.
The expected count integrates the trend, $$\mathbb{E}[N] = \int_0^1\!\!\int_0^1 12\,e^{x}\,\mathrm{d}x\,\mathrm{d}y = 12\,(e-1)\approx 20.6,$$ close to the baseline but with the points shifted toward the $x=1$ edge.
To simulate it by thinning, note $\lambda_{\max}=12e\approx 32.6$, so we generate CSR at rate $32.6$ and keep each point at $(x,y)$ with probability $e^{x}/e = e^{\,x-1}$.

**Overdispersion from a random intensity.** Finally make the reserve-wide intensity random: $\Lambda = 20\,G$ with $G$ a positive multiplier satisfying $\mathbb{E}[G]=1$ and $\operatorname{Var}(G)=1/2$ (a Gamma surface).
Then $\mathbb{E}[N]=20$ as before, but $$\operatorname{Var}(N) = \mathbb{E}[\Lambda] + \operatorname{Var}(\Lambda) = 20 + 20^2\cdot\tfrac{1}{2} = 220,$$ a variance-to-mean ratio of $11$ instead of $1$.
This Gamma–Poisson mixture is exactly the negative binomial, the discrete signature of the clustering an LGCP produces continuously in space.

## In code

### R

```r
library(spatstat)

# Complete spatial randomness: intensity 100 on the unit square
csr <- rpoispp(lambda = 100)

# Inhomogeneous Poisson: intensity varies smoothly in space
inh <- rpoispp(lambda = function(x, y) 100 * exp(2 * x))

# Log-Gaussian Cox process: log-intensity is a Gaussian field (exponential covariance)
lgcp <- rLGCP(model = "exp", mu = 4, var = 1.3, scale = 0.05)

# Neyman-Scott / Thomas cluster process: parents + Gaussian-scattered offspring
thom <- rThomas(kappa = 15, scale = 0.03, mu = 8)

# Test an observed pattern against CSR (Ripley's K, envelope from simulations)
plot(envelope(csr, Kest, nsim = 99))
```

### Python

```python
import numpy as np

rng = np.random.default_rng(0)

# --- Homogeneous Poisson (CSR) on the unit square, intensity lam ---
lam = 50.0
N = rng.poisson(lam)                       # counts are Poisson(lam * |A|), |A| = 1
pts = rng.uniform(0, 1, size=(N, 2))       # points uniform given N
print("CSR: N =", N, "  E[N] =", lam)

# --- Inhomogeneous Poisson by thinning: lam(x, y) = lam * exp(2*(x - 1)) <= lam ---
x, y = pts[:, 0], pts[:, 1]
p = np.exp(2 * (x - 1))                     # acceptance probability in (0, 1]
kept = pts[rng.uniform(size=N) < p]
print("inhomogeneous: kept", len(kept), "of", N, "points")

# --- Cox process: intensity itself random -> overdispersion ---
# Lambda = lam * G, with G ~ Gamma(k, 1/k): E[G] = 1, Var[G] = 1/k  (Gamma-Poisson)
k = 2.0
G = rng.gamma(k, 1 / k, size=20000)
Ncox = rng.poisson(lam * G)
print("Cox mean ~", round(Ncox.mean(), 1), " (Poisson mean =", lam, ")")
print("Cox var  ~", round(Ncox.var(), 1),  " (Poisson var  =", lam, ")")
print("var/mean ~", round(Ncox.var() / Ncox.mean(), 2), "> 1  => overdispersed")
```

<!-- python-output:auto -->
```text
CSR: N = 53   E[N] = 50.0
inhomogeneous: kept 21 of 53 points
Cox mean ~ 50.2  (Poisson mean = 50.0 )
Cox var  ~ 1305.7  (Poisson var  = 50.0 )
var/mean ~ 26.02 > 1  => overdispersed
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Distributions
Random.seed!(0)

# Homogeneous Poisson (CSR) on the unit square, intensity lam
lam = 50.0
N = rand(Poisson(lam))                      # counts ~ Poisson(lam * |A|), |A| = 1
pts = rand(N, 2)                            # points uniform given N

# Inhomogeneous Poisson by thinning: lam(x, y) = lam * exp(2*(x - 1)) <= lam
p = @. exp(2 * (pts[:, 1] - 1))            # acceptance probability
kept = pts[rand(N) .< p, :]

# Cox process (Gamma-Poisson mixture): random intensity -> overdispersion
k = 2.0
G = rand(Gamma(k, 1 / k), 20_000)
Ncox = rand.(Poisson.(lam .* G))
println("var/mean ~ ", round(var(Ncox) / mean(Ncox), digits = 2), " > 1")

# (For LGCP / Thomas simulation and Ripley's K, see the PointProcesses.jl package.)
```

## Why it matters

Point-process thinking is the backbone of **spatial epidemiology** and disease mapping.
Modeling case locations as an inhomogeneous Poisson or log-Gaussian Cox process lets you estimate a smooth risk surface $\lambda(s)$, borrow strength across neighboring areas, and flag clusters while separating real aggregation from a merely varying population-at-risk.
The LGCP is especially natural here because its latent [Gaussian process](gaussian-processes.md) can absorb covariates (a regression mean) while its [covariance function](covariance-functions.md) captures residual spatial correlation from unmeasured drivers — the same fitted surface you would map by [kriging](kriging.md).
In ecology the same models describe the positions of nests, trees, or burrows: CSR is the null hypothesis, an inhomogeneous intensity encodes habitat preference, and a Cox or Thomas process captures the clustering left over from seed dispersal, social attraction, or contagion.

## Related

- [The Poisson Distribution](poisson-distribution.md)
- [Gaussian Processes](gaussian-processes.md)
- [Covariance Functions](covariance-functions.md)
- [Kriging](kriging.md)
- [Expected Value](expected-value.md)
- [Quantitative Methods](../math.md)
