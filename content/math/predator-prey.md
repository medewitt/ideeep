---
title: "Lotka–Volterra Predator–Prey Dynamics"
---

# Lotka–Volterra Predator–Prey Dynamics

Predators and their prey are locked in a coupled feedback loop: more prey feeds more predators, and more predators eat down the prey.
The [Lotka–Volterra model](https://en.wikipedia.org/wiki/Lotka–Volterra_equations) is the simplest mathematical picture of this dance, and it explains why so many natural populations oscillate rather than settle down.

![Lotka–Volterra dynamics: predator and prey oscillate out of phase (left) and trace closed cycles in the phase plane (right).](../assets/figures/predator-prey.svg)

## The basic model

We track prey density $N$ and predator density $P$ through time.
Prey grow exponentially in the absence of predators and are removed by predation; predators reproduce in proportion to the prey they consume and die at a constant rate.

\[
\begin{aligned}
\frac{dN}{dt} &= rN - aNP \\
\frac{dP}{dt} &= b\,aNP - mP
\end{aligned}
\]

Here $r$ is the intrinsic prey growth rate, $a$ is the attack (predation) rate, $b$ is the conversion efficiency of eaten prey into new predators, and $m$ is the predator mortality rate.
The product $aNP$ is a mass-action term: encounters between predators and prey occur in proportion to the density of each.

Unlike [logistic growth](logistic-growth.md), the prey here have no carrying capacity of their own — the only thing holding them back is the predator.

## Interior equilibrium

An equilibrium is a state where both populations stop changing, so we set both derivatives to zero.
Ignoring the trivial extinction point $(0,0)$, we look for the interior (coexistence) equilibrium where $N>0$ and $P>0$.

Setting $\frac{dP}{dt}=0$ with $P>0$ gives $b\,aN = m$, so

\[
N^* = \frac{m}{ba}.
\]

Setting $\frac{dN}{dt}=0$ with $N>0$ gives $r = aP$, so

\[
P^* = \frac{r}{a}.
\]

Notice the counterintuitive structure: the equilibrium prey density depends only on predator parameters, and the equilibrium predator density depends only on prey parameters.
Enriching the prey (raising $r$) does not raise equilibrium prey — it raises predators.

## Neutral cycles and structural instability

Linearizing about $(N^*, P^*)$ gives a [Jacobian](jacobians.md) whose [eigenvalues](eigenvalues-and-eigenvectors.md) are purely imaginary, $\lambda = \pm i\sqrt{rm}$.
Purely imaginary eigenvalues mean the equilibrium is a **center**: trajectories neither spiral in nor out but trace closed loops.
The system conserves the quantity $V = b\,aN - m\ln N + aP - r\ln P$, so each initial condition sits on its own fixed orbit.

This makes the basic model **structurally unstable**: the cycles are neutral, and the smallest change to the equations — adding prey self-limitation, a saturating functional response, or noise — destroys the delicate closed orbits.
Real predator–prey cycles are therefore better described by modified models.

## Functional responses

The term $aN$ is the **functional response**: the per-predator prey consumption rate as a function of prey density.
Holling classified three shapes.

- **Type I** — linear, $f(N) = aN$; consumption rises without bound (the basic model above).
- **Type II** — saturating, $f(N) = \dfrac{aN}{1 + ahN}$, where $h$ is the handling time per prey; a predator that must spend time subduing and digesting prey eventually saturates.
- **Type III** — sigmoid, $f(N) = \dfrac{aN^2}{1 + ahN^2}$; low predation on rare prey (from switching or prey refuges) gives an S-shaped curve.

Replacing the linear term with a type II response changes the stability of the interior equilibrium.
Because a saturating predator becomes less effective as prey become abundant, enriching the system (raising prey carrying capacity) can destabilize the equilibrium and drive ever-larger cycles toward extinction — the **paradox of enrichment**.

## Worked example

Let $r = 1.0$, $a = 0.02$, $b = 0.1$, and $m = 0.4$.

Interior prey equilibrium:

\[
N^* = \frac{m}{ba} = \frac{0.4}{0.1 \times 0.02} = \frac{0.4}{0.002} = 200.
\]

Interior predator equilibrium:

\[
P^* = \frac{r}{a} = \frac{1.0}{0.02} = 50.
\]

So the populations balance at $(N^*, P^*) = (200, 50)$.
The cycle period near this center is approximately $T = \dfrac{2\pi}{\sqrt{rm}} = \dfrac{2\pi}{\sqrt{1.0 \times 0.4}} \approx 9.93$ time units.

## In code

We integrate the ODEs and plot the population cycles and a phase-plane orbit.

### R

```r
library(deSolve)

lv <- function(t, y, p) {
  with(as.list(c(y, p)), {
    dN <- r * N - a * N * P
    dP <- b * a * N * P - m * P
    list(c(dN, dP))
  })
}

p  <- c(r = 1.0, a = 0.02, b = 0.1, m = 0.4)
y0 <- c(N = 300, P = 40)
t  <- seq(0, 60, by = 0.05)
out <- ode(y = y0, times = t, func = lv, parms = p)

# Interior equilibrium: N* = m/(b a) = 200, P* = r/a = 50
matplot(out[, "time"], out[, c("N", "P")], type = "l",
        xlab = "time", ylab = "density")
plot(out[, "N"], out[, "P"], type = "l",
     xlab = "prey N", ylab = "predator P")  # closed orbit
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

r, a, b, m = 1.0, 0.02, 0.1, 0.4

def lv(t, y):
    N, P = y
    return [r*N - a*N*P, b*a*N*P - m*P]

sol = solve_ivp(lv, (0, 60), [300, 40], t_eval=np.linspace(0, 60, 1200))
N, P = sol.y

# Interior equilibrium: N* = m/(b*a) = 200.0, P* = r/a = 50.0
print(m/(b*a), r/a)          # -> 200.0 50.0

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(sol.t, N, sol.t, P)          # cycles vs time
ax2.plot(N, P)                        # closed phase-plane orbit
plt.show()
```

<!-- python-output:auto -->
```text
200.0 50.0
```
<!-- /python-output:auto -->

### Julia

```julia
using DifferentialEquations, Plots

function lv!(du, u, p, t)
    N, P = u
    r, a, b, m = p
    du[1] = r*N - a*N*P
    du[2] = b*a*N*P - m*P
end

p   = (1.0, 0.02, 0.1, 0.4)
prob = ODEProblem(lv!, [300.0, 40.0], (0.0, 60.0), p)
sol  = solve(prob, Tsit5(); saveat = 0.05)

# Interior equilibrium: N* = m/(b*a) = 200, P* = r/a = 50
plot(sol)                              # cycles vs time
plot(sol[1, :], sol[2, :])             # closed orbit
```

## Why it matters

Predator–prey theory underpins how ecologists interpret coupled oscillations in the wild, from lynx and hare pelts to plankton blooms and the dynamics of hosts and their parasites, a structure shared with epidemic models such as the [SIR model](sir.md).
It shows that regular cycles can arise from deterministic interactions alone, and that the *stability* of those cycles is fragile — a lesson that shapes biological control, conservation of exploited populations, and warnings like the paradox of enrichment.

## Related

- [Competition and Coexistence](competition-coexistence.md)
- [The Community Matrix and Stability](community-matrix.md)
- [Equilibria and Stability](equilibria-and-stability.md)
- [Jacobians](jacobians.md)
- [Logistic Growth](logistic-growth.md)
- [Compartmental Models (SIR)](sir.md)
- [Quantitative Methods](../math.md)
