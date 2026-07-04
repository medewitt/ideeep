---
title: "Population Dynamics of Resistance"
description: "How treatment pressure, the fitness cost of resistance, and transmission set the equilibrium fraction of drug-resistant infections in a host population."
---

# Population Dynamics of Resistance

Antimicrobial resistance plays out on two scales.
Within a single infection, mutation and selection change the makeup of a bacterial population, which is the story told in [The Evolution of Resistance](resistance-evolution.md).
Across a host population, drug-sensitive and drug-resistant strains circulate as competing transmission chains, and treatment tilts the competition toward whichever strain the drug cannot clear.
This page is about that second, epidemiological scale, following the two-strain transmission models of Lipsitch, Bonhoeffer, and colleagues.

![Equilibrium fraction of infections carried by the resistant strain rising with the treatment rate, with the competitive-exclusion threshold marked.](../assets/figures/resistance-dynamics.svg)

## Two strains competing for hosts

Picture a population of hosts, each either susceptible or infected by one of two strains.
The **sensitive** strain transmits at rate $\beta$ and is cleared both naturally and by treatment.
The **resistant** strain transmits at rate $\beta(1-c)$, where $c$ is the *fitness cost* of resistance, and treatment does nothing to it.
Writing $S$, $I_s$, and $I_r$ for the fractions of hosts in each state, an SIS model with treatment rate $\tau$ reads

\[
\begin{aligned}
\frac{dI_s}{dt} &= \beta S I_s - \gamma I_s - \tau I_s \\
\frac{dI_r}{dt} &= \beta(1-c)\, S I_r - \gamma I_r \\
\frac{dS}{dt} &= \gamma(I_s + I_r) + \tau I_s - \beta S I_s - \beta(1-c)\, S I_r
\end{aligned}
\]

Here $\gamma$ is the natural clearance rate and cleared hosts return to $S$, so this is an SIS rather than an SIR system.
The two strains share the same susceptible pool, so they are in direct competition for hosts to infect.

## Treatment is selection at the population scale

Each strain has an effective reproduction number, the average number of new infections one case produces given the current clearance pressure.
For the sensitive strain treatment adds to clearance, while the resistant strain is untouched:

\[
R_s = \frac{\beta S}{\gamma + \tau}, \qquad R_r = \frac{\beta(1-c)\, S}{\gamma}
\]

Whichever strain has the larger reproduction number at a shared susceptible level $S$ outcompetes the other.
Treatment is the selection pressure: raising $\tau$ shrinks $R_s$ but leaves $R_r$ alone.

## The fitness cost sets the tipping point

The two strains are equally fit when $R_s = R_r$, which happens at a threshold treatment rate

\[
\tau^\ast = \frac{\gamma c}{1 - c}
\]

Below $\tau^\ast$ the sensitive strain wins because it transmits faster and treatment is too rare to matter.
Above $\tau^\ast$ the drug clears sensitive infections quickly enough that the slower resistant strain, immune to the drug, takes over.
A larger fitness cost $c$ pushes $\tau^\ast$ higher, so a costly resistance mutation is held in check until drug use climbs.
This is why the cost of resistance is the quantity clinicians and modelers most want to measure.

## Coexistence and slow reversal

In the bare model the switch at $\tau^\ast$ is abrupt, an instance of competitive exclusion.
Two features soften it into the S-curve in the figure.
Real populations continually generate resistance de novo when treatment converts a sensitive infection into a resistant one, which seeds a low resistant fraction even below $\tau^\ast$.
Host heterogeneity, where some people are treated far more than others, lets each strain dominate its own niche so the strains coexist over a range of treatment rates rather than at a single knife-edge.

The same competition explains why resistance is slow to reverse.
Once the resistant strain is established and the susceptible pool has shifted, cutting drug use back below $\tau^\ast$ does not immediately restore the sensitive strain, because reversal is limited by the small fitness cost $c$ acting over many transmission generations.
If the cost is near zero, resistance can persist almost indefinitely after the selective pressure is gone.

## A worked example

Take $\beta = 0.30\ \mathrm{day^{-1}}$, natural clearance $\gamma = 0.10\ \mathrm{day^{-1}}$ (a ten-day infection), and a fitness cost $c = 0.30$.
The threshold treatment rate is

\[
\tau^\ast = \frac{\gamma c}{1 - c} = \frac{0.10 \times 0.30}{0.70} = 0.043\ \mathrm{day^{-1}}
\]

At a low treatment rate $\tau = 0.02\ \mathrm{day^{-1}}$ we have $R_s \propto \beta/(\gamma+\tau) = 0.30/0.12 = 2.5$ against $R_r \propto \beta(1-c)/\gamma = 0.21/0.10 = 2.1$, so the sensitive strain dominates.
Doubling treatment to $\tau = 0.06\ \mathrm{day^{-1}}$ makes $R_s \propto 0.30/0.16 = 1.9 < 2.1$, and the resistant strain wins.
Adding a small de novo resistance rate during treatment turns the abrupt switch into the smooth rise plotted above, so the equilibrium resistant fraction climbs steadily with $\tau$.

## In code

We integrate the two-strain SIS model to steady state, adding a small rate $\rho$ at which treated sensitive infections become resistant, and read off the resistant fraction $I_r/(I_s+I_r)$ for a few treatment rates.

### R

```r
library(deSolve)

beta <- 0.30; gamma <- 0.10; cost <- 0.30; rho <- 0.01

rhs <- function(t, y, p) {
  S <- y[1]; Is <- y[2]; Ir <- y[3]; tau <- p$tau
  new_s <- beta * S * Is
  new_r <- beta * (1 - cost) * S * Ir
  dIs <- new_s - gamma * Is - tau * Is
  dIr <- new_r - gamma * Ir + rho * tau * Is
  dS  <- gamma * Is + gamma * Ir + (1 - rho) * tau * Is - new_s - new_r
  list(c(dS, dIs, dIr))
}

frac <- function(tau) {
  out <- ode(c(0.98, 0.01, 0.01), seq(0, 5000, 10), rhs, list(tau = tau))
  last <- out[nrow(out), ]
  last["3"] / (last["2"] + last["3"])       # Ir / (Is + Ir)
}
sapply(c(0.02, 0.04, 0.06), frac)            # ~ 0.01, 0.17, 1.00
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

beta, gamma, cost, rho = 0.30, 0.10, 0.30, 0.01


def rhs(t, y, tau):
    S, Is, Ir = y
    new_s = beta * S * Is
    new_r = beta * (1 - cost) * S * Ir
    dIs = new_s - gamma * Is - tau * Is
    dIr = new_r - gamma * Ir + rho * tau * Is
    dS = gamma * Is + gamma * Ir + (1 - rho) * tau * Is - new_s - new_r
    return [dS, dIs, dIr]


def resistant_fraction(tau):
    sol = solve_ivp(rhs, [0, 5000], [0.98, 0.01, 0.01],
                    args=(tau,), rtol=1e-9, atol=1e-11)
    S, Is, Ir = sol.y[:, -1]
    return Ir / (Is + Ir)


for tau in (0.02, 0.04, 0.06):
    print(f"tau={tau:.2f}/day  resistant fraction={resistant_fraction(tau):.3f}")
```

<!-- python-output:auto -->
```text
tau=0.02/day  resistant fraction=0.012
tau=0.04/day  resistant fraction=0.167
tau=0.06/day  resistant fraction=1.000
```
<!-- /python-output:auto -->

### Julia

```julia
using DifferentialEquations

beta, gamma, cost, rho = 0.30, 0.10, 0.30, 0.01

function rhs!(du, u, tau, t)
    S, Is, Ir = u
    new_s = beta * S * Is
    new_r = beta * (1 - cost) * S * Ir
    du[1] = gamma*Is + gamma*Ir + (1-rho)*tau*Is - new_s - new_r
    du[2] = new_s - gamma*Is - tau*Is
    du[3] = new_r - gamma*Ir + rho*tau*Is
end

function frac(tau)
    prob = ODEProblem(rhs!, [0.98, 0.01, 0.01], (0.0, 5000.0), tau)
    u = solve(prob, Tsit5(); reltol = 1e-9).u[end]
    u[3] / (u[2] + u[3])
end
frac.((0.02, 0.04, 0.06))                    # ~ (0.01, 0.17, 1.00)
```

## Why it matters

The population dynamics of resistance say that how much a drug is used, not just how it is used in one patient, determines how common resistance becomes.
That reframes stewardship as managing a shared resource: the community-wide treatment rate sets the selection pressure, and the fitness cost sets how hard resistance is to reverse once it spreads.
The same transmission machinery that gives an epidemic its [basic reproduction number](next-generation-matrix.md) governs which strain circulates, so slowing resistance is as much an epidemiological problem as a pharmacological one.

## Related

- [Compartmental Models](sir.md) — the SIS and SIR transmission machinery
- [The Evolution of Resistance](resistance-evolution.md) — the within-host selection scale
- [Antimicrobial PK/PD](antimicrobial-pkpd.md) — dosing that suppresses resistance in the individual
- [The Next-Generation Matrix and R₀](next-generation-matrix.md) — reproduction numbers for competing strains
- [PK/PD Target Attainment](pkpd-target-attainment.md) — the sibling dosing view
- [Quantitative Methods](../math.md)
