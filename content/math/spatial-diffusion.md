---
title: "Spatial Diffusion and the Heat Equation"
description: "How something spreads through space by random movement alone — the diffusion (heat) equation, the underlying random walk, and the Gaussian spreading of a point release."
---

# Spatial Diffusion and the Heat Equation

Drop a bit of dye into still water, release a puff of spores into calm air, or track an animal wandering without a destination, and the same thing happens: the material spreads out, smoothing from a sharp concentration into an ever-broader blur.
Diffusion is that spreading — the macroscopic consequence of countless particles each moving at random, with no growth, no source, and no preferred direction.
This page is about pure spreading; when local growth is added on top, the dynamics change qualitatively into the constant-speed fronts of [reaction–diffusion](reaction-diffusion.md).

![The Gaussian heat kernel broadening over several times from a point release, and the characteristic spread growing like the square root of time.](../assets/figures/spatial-diffusion.svg)

## The diffusion (heat) equation

Let $u(x,t)$ be the concentration of some substance at position $x$ and time $t$.
Pure diffusion obeys the **diffusion equation**, also called the **heat equation**, $$\partial_t u = D\,\nabla^2 u,$$ where $D$ is the **diffusion coefficient** (units of area per time) and $\nabla^2$ is the Laplacian.
In one dimension $\nabla^2 u = \partial_{xx} u$ is just the curvature of the concentration profile, so the equation reads $\partial_t u = D\,\partial_{xx} u$.
The [partial derivative](partial-derivatives.md) $\partial_t u$ is the rate of change at a fixed point in space, and its sign is set entirely by the local curvature.
Where the profile dips below its neighbors the curvature is positive and $u$ rises to fill the dip; where the profile peaks the curvature is negative and the peak erodes.
Diffusion therefore does nothing but flatten gradients: it conserves the total amount of substance while relentlessly smoothing it toward uniformity.

### Fick's law: the constitutive assumption

The equation follows from one physical idea, **Fick's law**, which says that the flux of substance points down the concentration gradient and is proportional to its steepness, $$J = -D\,\nabla u.$$ Particles do not "want" to move anywhere, but because there are more of them on the high side of a gradient than the low side, random motion carries a net flow from high to low concentration.
Combining Fick's law with conservation of mass — the continuity statement $\partial_t u = -\nabla\cdot J$, that concentration changes only as flux accumulates — gives $\partial_t u = \nabla\cdot(D\,\nabla u) = D\,\nabla^2 u$ when $D$ is constant.
The minus sign is the whole story: flux runs *against* the gradient, which is why diffusion always erases differences rather than amplifying them.

## The microscopic picture: a random walk

Underneath the smooth equation is a jittering particle.
Consider a walker on a line that every time step $\tau$ takes a step of size $\pm\ell$, each direction equally likely, independent of the past — a **random walk**, the discrete cousin of **Brownian motion**.
After $n$ steps its position is a sum of independent $\pm\ell$ increments, so its mean displacement is zero (the walk drifts nowhere) but its variance grows: each step adds $\ell^2$ to the variance, giving $\operatorname{Var}(x_n) = n\,\ell^2$.
Writing $t = n\tau$ and $D = \ell^2/(2\tau)$, the **mean-squared displacement** is $$\mathbb{E}[x^2] = 2Dt \quad\text{in one dimension,}$$ and $\mathbb{E}[\|x\|^2] = 2dDt$ in $d$ dimensions, since each of the $d$ independent coordinates contributes $2Dt$.
The characteristic distance the walker has wandered is the square root of this, $$\sqrt{\mathbb{E}[x^2]} = \sqrt{2Dt} \propto \sqrt{t}.$$ This $\sqrt{t}$ scaling is the signature of diffusion, and it makes diffusion **slow**: to spread twice as far takes four times as long, and to spread ten times as far takes a hundred times as long.
A directed process covers distance $\propto t$; a diffusing one covers distance $\propto \sqrt{t}$, and the gap between them only widens with time.

## The fundamental solution: a spreading Gaussian

What does a point release actually look like as it spreads?
Start with all the substance concentrated at the origin — a spike, formally a Dirac delta — and let it diffuse.
The solution is the **fundamental solution**, or **heat kernel**, $$u(x,t) = \frac{1}{\sqrt{4\pi D t}}\,\exp\!\left(-\frac{x^2}{4 D t}\right).$$ This is a [normal distribution](normal-distribution.md) with mean $0$ and variance $\sigma^2 = 2Dt$, and it is no coincidence: the [central limit theorem](central-limit-theorem.md) guarantees that a sum of many small independent random steps is Gaussian, so the spatial profile of many diffusing walkers is a bell curve whose width $\sigma = \sqrt{2Dt}$ grows like $\sqrt{t}$.
As $t$ increases the Gaussian gets shorter and wider while the area under it stays fixed at $1$, exactly as the figure shows.
Because the diffusion equation is linear, the spreading of *any* initial profile is obtained by convolving it with this kernel — every release is a superposition of point releases, each blurring into its own broadening Gaussian.

## Boundary conditions

On a finite domain the equation needs conditions at the edges, and two kinds cover most cases.
A **Dirichlet** condition fixes the concentration at a boundary, $u = u_0$ — appropriate for an absorbing edge held at a reservoir value, such as a lake shore that instantly dilutes any arriving pollutant.
A **Neumann** condition fixes the flux, $\partial_x u = 0$ for a reflecting or **zero-flux** boundary, appropriate for an impermeable wall that nothing crosses, so the substance piles up rather than leaking out.
The choice matters: absorbing (Dirichlet) boundaries drain substance and drive the interior toward zero, while zero-flux (Neumann) boundaries conserve it and let diffusion settle to a flat, uniform steady state.

## How diffusion differs from advection and from reaction–diffusion

It is worth separating three transport mechanisms that are easy to conflate.
**Advection** is directed transport: a substance carried by a current or wind obeys $\partial_t u = -v\,\partial_x u$, and its center of mass moves at speed $v$, covering distance $\propto t$ without spreading.
**Diffusion** is undirected: the center of mass stays put and the substance spreads symmetrically, with width $\propto \sqrt{t}$.
Real plumes usually combine the two — the advection–diffusion equation $\partial_t u = -v\,\partial_x u + D\,\partial_{xx} u$ describes a Gaussian blob that drifts downstream at speed $v$ while broadening like $\sqrt{t}$.
[Reaction–diffusion](reaction-diffusion.md) is different again: adding a growth term $f(u)$ lets a locally multiplying population continually resupply its leading edge, and the result is a **traveling wave** that advances at a *constant* speed $c = 2\sqrt{rD}$ — distance $\propto t$, not $\sqrt{t}$.
The contrast is the key lesson: random movement alone spreads a fixed amount of material ever more thinly and slowly, whereas movement plus growth invades new territory at a steady pace.

## A worked example

Suppose a pollutant is released at a point in groundwater with diffusion coefficient $D = 10^{-3}\ \text{m}^2\,\text{s}^{-1}$.

**Spread after a given time.** After one day, $t = 86{,}400\ \text{s}$, the characteristic spread is $$\sigma = \sqrt{2Dt} = \sqrt{2 \times 10^{-3} \times 86{,}400} \approx \sqrt{172.8} \approx 13.1\ \text{m}.$$ So a day of pure diffusion smears the release over roughly ten metres — modest, because diffusion is slow.

**Time to diffuse a given distance.** To spread a characteristic distance $L = 100\ \text{m}$ we invert $L = \sqrt{2Dt}$ to get $$t = \frac{L^2}{2D} = \frac{100^2}{2 \times 10^{-3}} = 5\times 10^{6}\ \text{s} \approx 58\ \text{days}.$$ Reaching $1\ \text{km}$ by diffusion alone would take $100$ times as long — about $16$ years — because the time scales with the *square* of the distance.
This quadratic cost is why diffusion dominates only over short ranges (across a cell membrane, through a few metres of soil) and why long-range dispersal almost always relies on advection or active movement instead.

## In code

We simulate many independent one-dimensional random walkers and confirm that their mean-squared displacement grows linearly in time as $\mathbb{E}[x^2] = 2Dt$.

### R

```r
set.seed(1)
n_walkers <- 20000
n_steps   <- 400
ell <- 1; tau <- 1                 # step size and step time
D <- ell^2 / (2 * tau)             # diffusion coefficient = 0.5

steps <- matrix(sample(c(-ell, ell), n_walkers * n_steps, replace = TRUE),
                nrow = n_walkers)
pos <- t(apply(steps, 1, cumsum))  # position of each walker over time

for (t in c(100, 200, 400)) {
  msd <- mean(pos[, t]^2)
  cat(sprintf("t=%3d  MSD=%7.1f  2Dt=%7.1f\n", t, msd, 2 * D * t))
}
```

### Python

```python
import numpy as np

rng = np.random.default_rng(1)
n_walkers, n_steps = 20000, 400
ell, tau = 1.0, 1.0                     # step size and step time
D = ell**2 / (2 * tau)                  # diffusion coefficient = 0.5

steps = rng.choice([-ell, ell], size=(n_walkers, n_steps))
pos = np.cumsum(steps, axis=1)          # position of each walker over time

for t in (100, 200, 400):
    msd = np.mean(pos[:, t - 1] ** 2)   # mean-squared displacement
    print(f"t={t:3d}  MSD={msd:7.1f}  2Dt={2 * D * t:7.1f}")
```

<!-- python-output:auto -->
```text
t=100  MSD=   99.8  2Dt=  100.0
t=200  MSD=  200.9  2Dt=  200.0
t=400  MSD=  402.1  2Dt=  400.0
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics
Random.seed!(1)
n_walkers, n_steps = 20000, 400
ell, tau = 1.0, 1.0                     # step size and step time
D = ell^2 / (2 * tau)                   # diffusion coefficient = 0.5

steps = rand((-ell, ell), n_walkers, n_steps)
pos = cumsum(steps, dims = 2)           # position of each walker over time

for t in (100, 200, 400)
    msd = mean(pos[:, t] .^ 2)          # mean-squared displacement
    println("t=$t  MSD=$(round(msd, digits=1))  2Dt=$(2 * D * t)")
end
```

The measured mean-squared displacement tracks $2Dt$ closely, confirming the linear-in-time growth that underlies the $\sqrt{t}$ spread.

## Why it matters

Diffusion is the null model for spread: it is what happens when things move but nothing grows, and its slow $\sqrt{t}$ crawl is the baseline against which faster mechanisms are measured.
It sets the scale for how far pathogen particles, spores, or airborne droplets drift from a source, how a pollutant plume broadens as it seeps through soil or groundwater, and how far an individual animal wanders when foraging without a goal.
The same mathematics explains why molecular signalling works only across microns — a signalling molecule takes milliseconds to cross a cell but centuries to cross a room — so life relies on diffusion for the short haul and bulk flow for the long haul.
Crucially, pure diffusion does *not* by itself produce the sharp, constant-speed epidemic fronts seen when disease sweeps across a landscape; those require the growth term of [reaction–diffusion](reaction-diffusion.md), and comparing the two makes precise why an outbreak advances like a wall of fire ($\propto t$) rather than a spreading stain ($\propto \sqrt{t}$).

## Related

- [Reaction–Diffusion and Spatial Spread](reaction-diffusion.md)
- [Random Walks and Brownian Motion](random-walk-brownian-motion.md)
- [Partial Derivatives](partial-derivatives.md)
- [The Normal Distribution](normal-distribution.md)
- [Quantitative Methods](../math.md)
