---
title: "Spatial Moment Equations"
description: "How Bolker and Pacala reduce an individual-based, spatially explicit stochastic population to coupled equations for its mean density and spatial covariance, and why discreteness alone drives clustering."
---

# Spatial Moment Equations

Individual-based spatial models capture two things a mean-field model throws away: individuals are discrete, and they interact with their neighbors rather than with the population average.
Both features generate spatial pattern, clumping or over-dispersion, and that pattern feeds back on the dynamics.
[Bolker & Pacala (1997)](https://doi.org/10.1006/tpbi.1997.1331) make the pattern analytically tractable by writing deterministic equations for the first two spatial moments of the population: its mean density and its spatial covariance.

![Integrating the moment equations for a locally dispersing plant. Left: the mean density settles below the mean-field carrying capacity as average covariance builds up. Right: the equilibrium spatial covariance is positive, the signature of clustering.](../assets/figures/spatial-moment-equations.svg)

## The stochastic process

The motivating system is a population of plants in continuous space.
Each plant reproduces at a constant rate $f$, and its seed disperses a random distance drawn from a **dispersal kernel** $D(z)$, a probability density over displacements.
Each plant dies at a rate that rises with local crowding, $$M(x,t) = \mu + \alpha\,d(x,t), \qquad d(x,t) = \int U(y-x)\,n(y,t)\,dy,$$ where $\mu$ is density-independent mortality, $\alpha$ scales competition, and the **competition kernel** $U$ weights neighbors by distance.
The density $n(x,t)$ is a sum of Dirac spikes, one per plant, so the model keeps both the discreteness of individuals and the finite range of their interactions.

Its mean-field shadow is [logistic growth](logistic-growth.md) with intrinsic rate $r=f-\mu$ and carrying capacity $K=(f-\mu)/\alpha$.
The mean field is what you get when dispersal and competition act at infinite range, so every plant feels the global density.
Local dispersal and local competition are what break that limit and generate pattern.
Simulating the full process is easy, using the same [Gillespie-style](stochastic-epidemics.md) event updates as any spatial stochastic model, but a single realization tells you little about the ensemble.

## From individuals to moments

Instead of tracking every plant, take expectations across the ensemble of realizations.
The **first moment** is the mean density $n(t)$, a single number under spatial stationarity.
The **second moment** is the spatial autocovariance at lag $r$, $$c(r) = \big\langle\,(n(x)-\bar n)\,(n(x+r)-\bar n)\,\big\rangle,$$ which measures how the presence of a plant at one point changes the expected density a distance $r$ away.
Positive $c(r)$ at short lags means clustering; negative $c(r)$ means regular spacing.
This is a different object from the [moment-generating function](moment-generating-functions.md) of a single random variable: here the moments are spatial, taken over the arrangement of points in space.

Taking expectations produces a hierarchy.
The equation for the mean depends on the covariance, because a plant's death rate depends on its neighbors.
The equation for the covariance depends on a **third spatial moment**, the three-way arrangement of a plant, its neighbor, and their competitor.
Every level leans on the one above, an infinite chain.
The one approximation in the method is **moment closure**: assume the third central moment is negligible and cut the chain at second order.
The truncation works well whenever neighborhoods hold more than a handful of plants, and it fails for very short-range kernels where a plant has only one or two neighbors.

## The mean-density equation

Closing at second order gives a closed equation for the mean, $$\frac{dn}{dt} = n\big(f-\mu-\alpha n\big) \;-\; \alpha\,U(0)\,n \;-\; \alpha\!\int U(r)\,c(r)\,dr.$$ The first group is ordinary mean-field logistic growth.
The second term, $-\alpha\,U(0)\,n$, is a correction for discreteness that survives even when plants are randomly (Poisson) arranged, so it can be folded into an effective mortality $\mu' = \mu + \alpha\,U(0)$.
The third term is the one that couples the mean to spatial pattern: it is $-\alpha\bar c$, where $$\bar c = \int U(r)\,c(r)\,dr$$ is the competition-weighted average covariance, a crowding index.

The sign of $\bar c$ decides everything.
When plants cluster ($\bar c>0$) they sit in denser-than-average neighborhoods, compete more than the mean field assumes, and the equilibrium mean is pushed below the carrying capacity $K$.
When plants are regularly spaced ($\bar c<0$) each one competes with fewer neighbors than average, and the mean sits above $K$.
For the locally dispersing plant in the figure the depression is on the order of $10\text{–}30\%$, a spatial effect that no mean-field bookkeeping can recover.

## The covariance equation

The second moment obeys an integro-differential equation, more involved than the mean but readable term by term, $$\frac{\partial c(r)}{\partial t} = 2\Big[\,{-\mu' c(r)} + f\big\{(D * c)(r) + n\,D(r)\big\} - \alpha n\big\{(U * c)(r) + n\,U(r) + c(r)\big\} - \alpha\,U(r)\,c(r)\,\Big],$$ where $*$ is convolution, $(a*b)(r)=\int a(s)\,b(r-s)\,ds$.
Density-independent mortality, the $-\mu' c(r)$ term, erodes any pattern back toward randomness.
Reproduction with local dispersal, the $f\{\cdots\}$ terms, builds positive covariance by dropping offspring near their parents.
Density-dependent mortality, the $-\alpha n\{\cdots\}$ terms, builds negative covariance by thinning crowded patches.
Clustering versus spacing is the balance struck between these forces.

## Pattern from discreteness

The terms carrying a bare $n$ rather than a $c$, namely $n\,D(r)$ and $n\,U(r)$, are the engine of the whole story.
They come from the certainty of finding a plant at its own location, a Dirac spike at zero lag, which is a purely discrete effect.
Start the population from a Poisson distribution, so $c(r)=0$ everywhere, and these terms are nonzero: covariance grows away from zero on its own, and the population organizes into a pattern with no external forcing.

This is what "stochastically driven" means, and it separates the method from [reaction–diffusion](reaction-diffusion.md) pattern formation.
A [Turing pattern](turing-patterns.md) needs a deterministic instability, a uniform state that amplifies perturbations at some wavelength.
The deterministic analogue of these moment equations has a uniform state that is stable at every wavelength for ordinary kernels, so it never patterns on its own.
The pattern here is seeded by the discreteness of individuals, then shaped by dispersal and competition, and it is exactly what the extra $n$-terms encode.

## Simulation

Rather than run the individual-based process, integrate the closed moment equations directly.
Discretize the lag $r$ on a grid, represent the kernels and the covariance as arrays, evaluate the convolutions on that grid, and step the mean and covariance forward together from a near-Poisson start.
The equilibrium mean falls below the mean-field $K=20$, and the variance-to-mean ratio $\sigma^2/\bar n = \bar c/\bar n + 1$ climbs above one, the two headline signatures of clustering.

### R

```r
f <- 0.8; mu <- 0.4; alpha <- 0.02; lam <- 3.0
K <- (f - mu) / alpha                     # mean-field carrying capacity

L <- 6.0; dr <- 0.06; dt <- 0.01; Tmax <- 250.0
r <- seq(-L, L, by = dr)
U <- 0.5 * lam * exp(-lam * abs(r)); U <- U / (sum(U) * dr)   # competition
D <- 0.5 * lam * exp(-lam * abs(r)); D <- D / (sum(D) * dr)   # dispersal
U0 <- 0.5 * lam                           # self-competition U(0)
mu_p <- mu + alpha * U0

conv <- function(a, k) {                  # centered convolution, k symmetric
  m <- (length(k) - 1L) / 2L
  full <- convolve(a, rev(k), type = "open")
  dr * full[(m + 1L):(m + length(a))]
}

n <- 2.0; cc <- numeric(length(r))        # start near-Poisson (c = 0)
for (s in seq_len(as.integer(Tmax / dt))) {
  cbar <- dr * sum(U * cc)
  n <- n + dt * (n * (f - mu - alpha * n) - alpha * U0 * n - alpha * cbar)
  cc <- cc + dt * 2 * (-mu_p * cc + f * (conv(cc, D) + n * D) -
                       alpha * n * (conv(cc, U) + n * U + cc) - alpha * U * cc)
}
c(K = K, n_star = n, var_to_mean = dr * sum(U * cc) / n + 1)
```

### Python

```python
import numpy as np

# Individual-based plant model reduced to moment equations (Bolker-Pacala):
# fecundity f, background death mu, competition alpha, and Laplacian kernels
# with inverse scale lam for both dispersal D and competition U.
f, mu, alpha, lam = 0.8, 0.4, 0.02, 3.0
K = (f - mu) / alpha                       # mean-field carrying capacity

L, dr, dt, T = 6.0, 0.06, 0.01, 250.0
r = np.arange(-L, L + dr / 2, dr)
U = 0.5 * lam * np.exp(-lam * np.abs(r)); U /= U.sum() * dr
D = 0.5 * lam * np.exp(-lam * np.abs(r)); D /= D.sum() * dr
U0 = 0.5 * lam                             # self-competition U(0)
mu_p = mu + alpha * U0                      # mortality with self-competition


def conv(a, k):                            # discrete convolution on the lag grid
    return dr * np.convolve(a, k, mode="same")


n, c = 2.0, np.zeros_like(r)               # start near-Poisson (c = 0)
for _ in range(int(T / dt)):
    cbar = dr * np.sum(U * c)              # competition-weighted covariance
    n += dt * (n * (f - mu - alpha * n) - alpha * U0 * n - alpha * cbar)
    c += dt * 2 * (-mu_p * c + f * (conv(c, D) + n * D)
                   - alpha * n * (conv(c, U) + n * U + c) - alpha * U * c)

cbar = dr * np.sum(U * c)
print(f"mean-field K     = {K:.1f}")
print(f"spatial n*       = {n:.2f}")
print(f"depression       = {100 * (K - n) / K:.0f}%")
print(f"variance-to-mean = {cbar / n + 1:.2f}")
```

<!-- python-output:auto -->
```text
mean-field K     = 20.0
spatial n*       = 17.75
depression       = 11%
variance-to-mean = 1.75
```
<!-- /python-output:auto -->

### Julia

```julia
using DSP

f, mu, alpha, lam = 0.8, 0.4, 0.02, 3.0
K = (f - mu) / alpha                       # mean-field carrying capacity

L, dr, dt, T = 6.0, 0.06, 0.01, 250.0
r = collect(-L:dr:L)
U = 0.5lam .* exp.(-lam .* abs.(r)); U ./= sum(U) * dr   # competition
D = 0.5lam .* exp.(-lam .* abs.(r)); D ./= sum(D) * dr   # dispersal
U0 = 0.5lam                                # self-competition U(0)
mu_p = mu + alpha * U0

function conv_same(a, k)                   # centered convolution, k symmetric
    m = (length(k) - 1) ÷ 2
    full = conv(a, k)                      # length = length(a) + length(k) - 1
    dr .* full[(m + 1):(m + length(a))]
end

n = 2.0; c = zeros(length(r))              # start near-Poisson (c = 0)
for _ in 1:round(Int, T / dt)
    cbar = dr * sum(U .* c)
    global n += dt * (n * (f - mu - alpha * n) - alpha * U0 * n - alpha * cbar)
    global c += dt * 2 .* (-mu_p .* c .+ f .* (conv_same(c, D) .+ n .* D) .-
                 alpha * n .* (conv_same(c, U) .+ n .* U .+ c) .- alpha .* U .* c)
end
(K = K, n_star = n, var_to_mean = dr * sum(U .* c) / n + 1)
```

## Why it matters

The recipe is general.
Any spatial process built from pairwise interactions, take expectations, and you get evolution equations for the mean densities and the spatial covariances of everything involved, closed by dropping the third moment.
[Bolker & Pacala (1997)](https://doi.org/10.1006/tpbi.1997.1331) work through single-species plant competition, but the same construction handles predator–prey systems and host–parasite or [epidemic](sir.md) models, where the covariance between susceptibles and infecteds governs how fast transmission spreads through a clustered population.
The payoff is a middle path between two unsatisfying extremes: individual-based simulations that reproduce reality but resist analysis, and mean-field models that are analytically clean but blind to the discreteness and local structure that shape real populations.
Moment equations keep both space and stochasticity while staying close enough to a set of ordinary equations that you can read the ecology off the terms.

## Related

- [Reaction–Diffusion and Spatial Spread](reaction-diffusion.md)
- [Turing Patterns](turing-patterns.md)
- [Metapopulations and the Levins Model](metapopulations.md)
- [Asynchrony and the Inflationary Effect](metapopulation-asynchrony.md)
- [Stochastic Epidemics and the Gillespie Algorithm](stochastic-epidemics.md)
- [Moment Generating Functions](moment-generating-functions.md)
- [Exponential and Logistic Growth](logistic-growth.md)
- [Quantitative Methods](../math.md)
