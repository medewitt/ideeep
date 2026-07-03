---
title: "Metapopulations and the Levins Model"
---

# Metapopulations and the Levins Model

Real landscapes are patchy: a species survives not as one continuous population but as a scatter of local populations that wink out and are recolonized.
The Levins model captures this "population of populations" with a single equation, and it turns out to be mathematically identical to a simple epidemic — patches play the role of hosts, and occupancy plays the role of infection.

## The metapopulation idea

A **metapopulation** is a set of local populations occupying discrete habitat patches, linked by dispersal.
Individual patches may go extinct, but colonization from occupied patches can rescue the whole system, so the metapopulation persists even as its parts blink on and off.
Rather than track numbers within each patch, the classic Levins model tracks only the **fraction of patches occupied**, $p(t)\in[0,1]$.

## The Levins model

Occupancy changes through two opposing processes.
Empty patches (a fraction $1-p$) are colonized by propagules from occupied patches (a fraction $p$) at rate $c$, while occupied patches go extinct at rate $e$: $$\frac{dp}{dt}=c\,p(1-p)-e\,p.$$ The colonization term $c\,p(1-p)$ has exactly the shape of [logistic growth](logistic-growth.md) — it needs occupied patches to send colonists and empty patches to receive them — while $-e\,p$ removes occupied patches at a constant per-patch rate.

### Equilibrium occupancy

Setting $dp/dt=0$ and factoring gives $p\bigl(c(1-p)-e\bigr)=0$, so there are two [equilibria](equilibria-and-stability.md).
The trivial one, $p^*=0$ (regional extinction), and the interior one $$p^*=1-\frac{e}{c}.$$ This is positive — the metapopulation persists — only if $$c>e,$$ i.e. colonization must outpace extinction.
Linearizing shows that when $c>e$ the extinction state $p^*=0$ is unstable and the interior equilibrium $1-e/c$ is stable; when $c<e$ the only nonnegative equilibrium is $p^*=0$, and the metapopulation is doomed.

## Habitat destruction and the extinction threshold

Suppose a fraction $D$ of patches is permanently destroyed, so they can never be occupied.
Only a fraction $1-D$ of patches remain available for colonization, and the equilibrium occupancy drops to $$p^*=1-D-\frac{e}{c}.$$ Persistence now requires $1-D>e/c$, giving an **extinction threshold**: the metapopulation collapses once $$D>1-\frac{e}{c}.$$ Strikingly, the amount of habitat that can be destroyed before collapse equals the pre-destruction occupancy $1-e/c$ — species that already occupy few patches are the most vulnerable to habitat loss.

## Parallel to an SIS epidemic

The Levins equation is structurally the same as a simple [SIS](sir.md) epidemic model.
Reinterpret occupied patches as **infected** hosts and empty patches as **susceptible** hosts: colonization is transmission (rate $c$, requiring contact between infected and susceptible) and patch extinction is recovery (rate $e$).
The persistence condition $c>e$ is precisely the epidemic threshold $R_0=c/e>1$, and equilibrium occupancy $1-e/c$ is the endemic prevalence $1-1/R_0$.
Habitat destruction that raises the extinction threshold is the direct analogue of vaccinating a fraction of the population to push $R_0$ below one.

## A worked example

Let $c=0.4$ and $e=0.1$ per unit time.
The colonization–extinction ratio is $c/e=4$ (the analogue of $R_0=4$), so the metapopulation persists.
Equilibrium occupancy is $p^*=1-e/c=1-0.25=0.75$: three-quarters of patches are occupied at steady state.
Now destroy $D=0.5$ of the patches: occupancy falls to $p^*=1-0.5-0.25=0.25$.
The system tips to extinction once $D>1-e/c=0.75$ — destroying more than three-quarters of the habitat wipes the species out even though colonists still exist.

## In code

We solve the Levins ODE and compare the numerical steady state to the formula $1-e/c$.

### R

```r
library(deSolve)

levins <- function(t, p, par) list(par$c * p * (1 - p) - par$e * p)
par <- list(c = 0.4, e = 0.1)
out <- ode(y = c(p = 0.05), times = seq(0, 100, 1), func = levins, parms = par)

tail(out[, "p"], 1)   # ~0.75
1 - par$e / par$c     # 0.75  (analytic equilibrium)
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

c, e = 0.4, 0.1
f = lambda t, p: c * p * (1 - p) - e * p
sol = solve_ivp(f, (0, 100), [0.05], t_eval=[100], rtol=1e-8)

print(sol.y[0, -1])   # ~0.75
print(1 - e / c)      # 0.75

D = 0.5               # habitat destruction
print(1 - D - e / c)  # 0.25 occupancy after destroying half the patches
```

<!-- python-output:auto -->
```text
0.7499997354809338
0.75
0.25
```
<!-- /python-output:auto -->

### Julia

```julia
using DifferentialEquations

c, e = 0.4, 0.1
f(p, par, t) = c * p * (1 - p) - e * p
prob = ODEProblem(f, 0.05, (0.0, 100.0))
sol = solve(prob, Tsit5())

sol.u[end]        # ~0.75
1 - e / c         # 0.75 analytic equilibrium
```

## Why it matters

The Levins model shows that a species can persist regionally while every local population is doomed, reframing conservation around colonization, extinction, and the connectivity of patches rather than any single site.
Its extinction threshold quantifies how much habitat loss a metapopulation can absorb, and its exact parallel to the SIS epidemic threshold means the same mathematics predicts both when a species survives a fragmenting landscape and when a pathogen invades a host population.

## Related

- [Exponential and Logistic Growth](logistic-growth.md)
- [Equilibria and Stability](equilibria-and-stability.md)
- [Compartmental Models (SIR)](sir.md)
- [Quantitative Methods](../math.md)
