---
title: "Competition and Coexistence"
---

# Competition and Coexistence

When two species use the same limiting resources, each depresses the other's growth — yet countless species manage to coexist.
The Lotka–Volterra competition model and modern coexistence theory explain when a competitor wins, when both persist, and when the winner depends on who arrives first.

## The competition model

We extend [logistic growth](logistic-growth.md) to two species that compete.
Each species limits itself, and also feels its competitor through a conversion coefficient.

\[
\begin{aligned}
\frac{dN_1}{dt} &= r_1 N_1\!\left(1 - \frac{N_1 + \alpha_{12} N_2}{K_1}\right) \\
\frac{dN_2}{dt} &= r_2 N_2\!\left(1 - \frac{N_2 + \alpha_{21} N_1}{K_2}\right)
\end{aligned}
\]

Here $r_i$ is the intrinsic growth rate of species $i$, $K_i$ is its carrying capacity, and $\alpha_{ij}$ is the per-capita competitive effect of species $j$ on species $i$.
If $\alpha_{12} = 1$, an individual of species 2 counts exactly like an individual of species 1 in crowding species 1; $\alpha_{12} < 1$ means interspecific competition is weaker than intraspecific.

## Zero-growth isoclines

A **zero-growth isocline** for a species is the set of $(N_1, N_2)$ where that species neither grows nor declines.
Setting $\frac{dN_1}{dt}=0$ gives the line $N_1 = K_1 - \alpha_{12} N_2$, and setting $\frac{dN_2}{dt}=0$ gives $N_2 = K_2 - \alpha_{21} N_1$.

The way these two lines sit in the $N_1$–$N_2$ plane determines the outcome, giving four cases.

- **Species 1 wins** — species 1's isocline lies entirely outside species 2's; species 2 is driven to extinction from any starting point.
- **Species 2 wins** — the mirror image; species 1 is excluded.
- **Priority effects (bistable, founder control)** — the isoclines cross, but the interior equilibrium is unstable; whichever species establishes first excludes the other.
- **Stable coexistence** — the isoclines cross with a stable interior equilibrium; both species persist.

The interior equilibrium exists at the intersection, but only in the coexistence case is it a stable node that trajectories approach.

## The coexistence condition

Stable coexistence requires that **each species can invade when rare** — the mutual invasibility criterion.
Species 2 can invade a resident species 1 (sitting at $N_1 = K_1$) when its per-capita growth rate is positive there, which reduces to $K_2 > \alpha_{21} K_1$.
By symmetry species 1 invades species 2's equilibrium when $K_1 > \alpha_{12} K_2$.

Combining, coexistence is stable when

\[
\alpha_{12} < \frac{K_1}{K_2} \quad\text{and}\quad \alpha_{21} < \frac{K_2}{K_1},
\]

which implies $\alpha_{12}\,\alpha_{21} < 1$: interspecific competition must be weaker than intraspecific for both species.
When instead $\alpha_{12}\alpha_{21} > 1$ (each isocline crossing so interspecific competition dominates), we get priority effects.

The **competitive exclusion principle** is the boundary case: two species competing for a single limiting resource in exactly the same way cannot coexist indefinitely — one excludes the other.

## Modern coexistence terms

Contemporary theory reframes these conditions as a balance of two forces.
**Stabilizing niche differences** describe how strongly each species limits itself relative to its competitor; they push toward coexistence by making rare species grow faster (self-limitation exceeding cross-limitation, i.e. $\alpha_{12}\alpha_{21} < 1$).
**Fitness differences** describe the overall competitive advantage of one species over the other; they push toward exclusion.
Species coexist when stabilizing niche differences are large enough to overcome their fitness difference — a useful lens for anything from plant communities to competing pathogen strains.

## Worked example

Let $K_1 = 1000$, $K_2 = 800$, $\alpha_{12} = 0.6$, and $\alpha_{21} = 0.7$.

Check the two invasion conditions:

\[
\frac{K_1}{K_2} = \frac{1000}{800} = 1.25 > 0.6 = \alpha_{12}, \qquad
\frac{K_2}{K_1} = \frac{800}{1000} = 0.80 > 0.7 = \alpha_{21}.
\]

Both hold (equivalently $\alpha_{12}\alpha_{21} = 0.42 < 1$), so the species **stably coexist**.
The interior equilibrium is

\[
N_1^* = \frac{K_1 - \alpha_{12} K_2}{1 - \alpha_{12}\alpha_{21}}
= \frac{1000 - 0.6\cdot 800}{1 - 0.42} = \frac{520}{0.58} \approx 897,
\]
\[
N_2^* = \frac{K_2 - \alpha_{21} K_1}{1 - \alpha_{12}\alpha_{21}}
= \frac{800 - 0.7\cdot 1000}{0.58} = \frac{100}{0.58} \approx 172.
\]

## In code

We draw the isoclines and overlay a few trajectories.

### R

```r
library(deSolve)

comp <- function(t, y, p) {
  with(as.list(c(y, p)), {
    dN1 <- r1 * N1 * (1 - (N1 + a12 * N2) / K1)
    dN2 <- r2 * N2 * (1 - (N2 + a21 * N1) / K2)
    list(c(dN1, dN2))
  })
}

p <- c(r1 = 0.5, r2 = 0.5, K1 = 1000, K2 = 800, a12 = 0.6, a21 = 0.7)
t <- seq(0, 100, by = 0.2)

for (y0 in list(c(N1 = 50, N2 = 700), c(N1 = 900, N2 = 50))) {
  out <- ode(y = y0, times = t, func = comp, parms = p)
  cat(tail(out[, "N1"], 1), tail(out[, "N2"], 1), "\n")
}
# Both start points converge near (897, 172): stable coexistence
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

r1, r2, K1, K2, a12, a21 = 0.5, 0.5, 1000, 800, 0.6, 0.7

def comp(t, y):
    N1, N2 = y
    return [r1*N1*(1 - (N1 + a12*N2)/K1),
            r2*N2*(1 - (N2 + a21*N1)/K2)]

for y0 in ([50, 700], [900, 50]):
    sol = solve_ivp(comp, (0, 200), y0, t_eval=[200])
    print(sol.y[:, -1])       # both -> [~897, ~172]: coexistence
```

<!-- python-output:auto -->
```text
[896.34570986 172.37913759]
[896.31173928 172.36258286]
```
<!-- /python-output:auto -->

### Julia

```julia
using DifferentialEquations

function comp!(du, u, p, t)
    N1, N2 = u
    r1, r2, K1, K2, a12, a21 = p
    du[1] = r1*N1*(1 - (N1 + a12*N2)/K1)
    du[2] = r2*N2*(1 - (N2 + a21*N1)/K2)
end

p = (0.5, 0.5, 1000.0, 800.0, 0.6, 0.7)
for u0 in ([50.0, 700.0], [900.0, 50.0])
    sol = solve(ODEProblem(comp!, u0, (0.0, 200.0), p), Tsit5())
    println(sol.u[end])       # both -> [~897, ~172]: coexistence
end
```

## Why it matters

Competition theory is the backbone of community ecology: it predicts which species assemble together, why invaders sometimes take over and sometimes fail, and how biodiversity is maintained.
The invasion criterion and the niche-versus-fitness framing guide restoration, invasion risk assessment, and the study of coexisting strains of parasites and pathogens.

## Related

- [Lotka–Volterra Predator–Prey Dynamics](predator-prey.md)
- [The Community Matrix and Stability](community-matrix.md)
- [Equilibria and Stability](equilibria-and-stability.md)
- [Logistic Growth](logistic-growth.md)
- [Quantitative Methods](../math.md)
