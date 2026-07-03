---
title: "Reaction–Diffusion and Spatial Spread"
---

# Reaction–Diffusion and Spatial Spread

An invading species, a spreading epidemic, and an advantageous gene all share the same problem: something grows locally while also moving through space.
Reaction–diffusion equations couple these two ingredients — local dynamics and random movement — and their signature result is a front that advances at a predictable speed.

## The general form

A reaction–diffusion model tracks a density $u(x,t)$ that changes for two reasons.
Locally it grows or decays according to a **reaction** term $f(u)$, and it spreads out by **diffusion**, the tendency of random movement to flatten gradients.
Combining them gives $$\partial_t u = D\,\nabla^2 u + f(u),$$ where $D$ is the **diffusion coefficient** (units of area per time) and $\nabla^2$ is the Laplacian.
The [partial derivative](partial-derivatives.md) $\partial_t u$ is the rate of change in time at a fixed point in space, while $\nabla^2 u = \partial_{xx}u$ (in one dimension) measures the local curvature of the density.
Where $u$ dips below its neighbors the curvature is positive and diffusion fills the dip in; where $u$ peaks the curvature is negative and diffusion erodes the peak.

The diffusion term alone, $\partial_t u = D\,\partial_{xx}u$, is the heat equation: it smooths any initial profile toward uniformity.
The reaction term alone, $\partial_t u = f(u)$, is an ordinary differential equation describing growth at a single location.
Their combination is what lets a locally growing population push outward into empty territory.

## The Fisher–KPP equation

The most famous choice takes $f(u)$ to be [logistic growth](logistic-growth.md), giving the Fisher–KPP equation $$\partial_t u = D\,\partial_{xx}u + r\,u(1-u).$$ Here $u$ is scaled so the carrying capacity is $1$, $r$ is the intrinsic growth rate, and $D$ is the diffusion coefficient.
R. A. Fisher introduced it in 1937 to model the spread of an advantageous gene through a population distributed along a line, and Kolmogorov, Petrovsky, and Piskunov analyzed it the same year.

The equation has two spatially uniform [equilibria](equilibria-and-stability.md): the empty state $u=0$ and the invaded state $u=1$.
Treating the reaction term as a local ODE, $f'(u) = r(1-2u)$, so $f'(0)=r>0$ makes the empty state unstable while $f'(1)=-r<0$ makes the invaded state stable.
Any small seed of population therefore grows, and diffusion carries the growth outward.

### The traveling wave

The key result is that the solution settles into a **traveling wave**: a fixed front profile that connects $u=1$ behind it to $u=0$ ahead of it and moves at constant speed without changing shape.
Writing $u(x,t)=U(x-ct)$ for a front moving right at speed $c$, the asymptotic speed selected from a compact (localized) initial condition is $$c = 2\sqrt{rD}.$$ This minimal speed comes from linearizing at the leading edge, where $u$ is tiny and the equation reduces to $\partial_t u \approx D\,\partial_{xx}u + r\,u$; requiring a non-oscillating (non-negative) front picks out $c=2\sqrt{rD}$.
Faster growth or faster movement both speed the invasion, but only through their geometric mean under the square root, so quadrupling $r$ or $D$ merely doubles the speed.

## A worked example

Suppose a beetle invades with growth rate $r = 0.4\ \text{yr}^{-1}$ and diffusion coefficient $D = 25\ \text{km}^2\,\text{yr}^{-1}$.
The asymptotic front speed is $$c = 2\sqrt{rD} = 2\sqrt{0.4 \times 25} = 2\sqrt{10} \approx 6.32\ \text{km/yr}.$$ Over a decade the invasion front therefore advances roughly $63$ km.
If a management program halves the effective growth rate to $r=0.2\ \text{yr}^{-1}$, the new speed is $2\sqrt{0.2\times 25}=2\sqrt{5}\approx 4.47\ \text{km/yr}$ — a reduction by a factor of $\sqrt{2}$, not a factor of two, because the speed depends on $\sqrt{r}$.

## Simulation

We integrate the 1D Fisher–KPP equation by the method of lines: discretize space on a grid, approximate $\partial_{xx}u$ by the second difference $(u_{i+1}-2u_i+u_{i-1})/\Delta x^2$, and step forward with explicit Euler.
Starting from a small patch at the left, the front should advance at speed $\approx 2\sqrt{rD}$.
For stability the time step must satisfy $D\,\Delta t/\Delta x^2 \le 1/2$.

### R

```r
r <- 0.4; D <- 0.25
dx <- 0.5; dt <- 0.1              # D*dt/dx^2 = 0.1 <= 0.5, stable
L <- 200; n <- L / dx + 1
x <- seq(0, L, by = dx)
u <- as.numeric(x < 5)           # invaded patch on the left
steps <- 2000                    # t = 200

for (s in 1:steps) {
  lap <- c(0, diff(diff(u)), 0) / dx^2   # Neumann (zero-flux) ends
  u <- u + dt * (D * lap + r * u * (1 - u))
}

front <- max(x[u > 0.5])         # position of u = 0.5 level set
front / (steps * dt)             # ~0.63  vs  2*sqrt(r*D) = 0.632
```

### Python

```python
import numpy as np

r, D = 0.4, 0.25
dx, dt = 0.5, 0.1                 # D*dt/dx^2 = 0.1 <= 0.5, stable
L = 200.0
x = np.arange(0, L + dx, dx)
u = (x < 5).astype(float)         # invaded patch on the left
steps = 2000                      # t = 200

for _ in range(steps):
    lap = np.zeros_like(u)
    lap[1:-1] = (u[2:] - 2 * u[1:-1] + u[:-2]) / dx**2
    u = u + dt * (D * lap + r * u * (1 - u))

front = x[u > 0.5].max()          # position of u = 0.5 level set
print(front / (steps * dt))       # ~0.63  vs  2*sqrt(r*D) = 0.632
```

### Julia

```julia
r, D = 0.4, 0.25
dx, dt = 0.5, 0.1                 # D*dt/dx^2 = 0.1 <= 0.5, stable
L = 200.0
x = collect(0:dx:L)
u = Float64.(x .< 5)             # invaded patch on the left
steps = 2000                     # t = 200
lap = zeros(length(u))

for _ in 1:steps
    @views lap[2:end-1] .= (u[3:end] .- 2 .* u[2:end-1] .+ u[1:end-2]) ./ dx^2
    u .+= dt .* (D .* lap .+ r .* u .* (1 .- u))
end

front = maximum(x[u .> 0.5])     # position of u = 0.5 level set
println(front / (steps * dt))    # ~0.63  vs  2*sqrt(r*D) = 0.632
```

## Why it matters

Reaction–diffusion is the workhorse model for anything that spreads while it grows.
Skellam used it to explain the spread of muskrats across Europe from a handful of escapees, and the same $c=2\sqrt{rD}$ law predicts how fast an invasive species colonizes new range.
In epidemiology, adding diffusion to an [SIR](sir.md) model turns a well-mixed outbreak into a traveling wave of infection sweeping across a landscape.
When space is patchy rather than continuous, [metapopulation](metapopulations.md) models play the analogous role, and when the reaction couples two interacting species the same framework produces the stationary [Turing patterns](turing-patterns.md) rather than moving fronts.

## Related

- [Exponential and Logistic Growth](logistic-growth.md)
- [Partial Derivatives](partial-derivatives.md)
- [Equilibria and Stability](equilibria-and-stability.md)
- [Turing Patterns](turing-patterns.md)
- [The SIR Model](sir.md)
- [Metapopulations](metapopulations.md)
- [Quantitative Methods](../math.md)
