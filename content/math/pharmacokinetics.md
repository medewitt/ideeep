---
title: "Pharmacokinetics: Compartment Models"
---

# Pharmacokinetics: Compartment Models

Pharmacokinetics (PK) is what the body does to a drug — its absorption, distribution, metabolism, and excretion (ADME).
Remarkably, these processes are described with the same mass-balance ordinary differential equations that power [compartmental epidemic models](sir.md), so the drug concentration in a "compartment" rises and falls by the same first-order kinetics that move individuals between $S$, $I$, and $R$.

## The one-compartment IV bolus

The simplest model imagines the body as a single well-mixed compartment of volume $V_d$ from which the drug is eliminated at a rate proportional to its concentration.
For an intravenous bolus dose $D$ given at $t=0$, mass balance gives

\[
V_d \frac{dC}{dt} = -CL \cdot C, \qquad C(0) = C_0 = \frac{D}{V_d}
\]

whose solution is a simple [exponential decay](exponentials-and-logarithms.md):

\[
C(t) = \frac{D}{V_d}\, e^{-kt}
\]

Here $k = CL/V_d$ is the first-order elimination rate constant.

### The core parameters

The **volume of distribution** relates the dose to the initial concentration:

\[
V_d = \frac{D}{C_0}
\]

It is an apparent volume — a proportionality constant, not a physical space — and can exceed total body water for drugs that partition into tissue.

**Clearance** is the volume of plasma cleared of drug per unit time and links the rate constant to the volume:

\[
CL = k\, V_d
\]

The **half-life** is the time for the concentration to fall by half, found by solving $e^{-k t_{1/2}} = \tfrac12$:

\[
t_{1/2} = \frac{\ln 2}{k}
\]

The **area under the curve** is the total exposure, obtained by integrating $C(t)$ from $0$ to $\infty$ (see [integrals](integrals.md)):

\[
\mathrm{AUC} = \int_0^\infty C(t)\,dt = \frac{C_0}{k} = \frac{D}{CL}
\]

## First-order oral absorption

Oral dosing adds an absorption compartment (the gut) that feeds the central compartment at first-order rate $k_a$, with bioavailable fraction $F$.
The concentration follows the Bateman equation:

\[
C(t) = \frac{F D k_a}{V_d\,(k_a - k)}\left(e^{-kt} - e^{-k_a t}\right)
\]

This rises from zero, reaches a peak $C_{max}$, and then declines.
Setting the [derivative](derivatives.md) $dC/dt=0$ gives the time of the peak:

\[
t_{max} = \frac{\ln(k_a/k)}{k_a - k}
\]

## Two-compartment model

When drug distributes into a peripheral tissue compartment before reaching equilibrium, the decline after an IV bolus is biexponential — a fast distribution phase followed by a slower elimination phase:

\[
C(t) = A\, e^{-\alpha t} + B\, e^{-\beta t}, \qquad \alpha > \beta
\]

The macro-constants $A$, $B$, $\alpha$, and $\beta$ are combinations of the intercompartmental micro-rate constants, and $\beta$ governs the terminal half-life.

## Repeated dosing and steady state

Give a maintenance dose $D$ every interval $\tau$ and the drug accumulates until input balances elimination.
The average concentration at steady state depends only on the rate of bioavailable input and clearance:

\[
C_{ss,avg} = \frac{F D}{CL\,\tau}
\]

This equation drives clinical dosing: to hit a target average concentration, choose $D/\tau$ to match $CL \cdot C_{ss,avg}/F$.

## Worked example

A 500 mg IV bolus produces an initial plasma concentration of $C_0 = 20\ \mathrm{mg/L}$, and a second sample at $t=4\ \mathrm{h}$ reads $10\ \mathrm{mg/L}$.

Volume of distribution:

\[
V_d = \frac{D}{C_0} = \frac{500\ \mathrm{mg}}{20\ \mathrm{mg/L}} = 25\ \mathrm{L}
\]

The concentration halved in 4 h, so $t_{1/2} = 4\ \mathrm{h}$ and

\[
k = \frac{\ln 2}{t_{1/2}} = \frac{0.693}{4\ \mathrm{h}} = 0.173\ \mathrm{h^{-1}}
\]

Clearance:

\[
CL = k\, V_d = 0.173\ \mathrm{h^{-1}} \times 25\ \mathrm{L} = 4.33\ \mathrm{L/h}
\]

Total exposure:

\[
\mathrm{AUC} = \frac{C_0}{k} = \frac{20\ \mathrm{mg/L}}{0.173\ \mathrm{h^{-1}}} = 115.5\ \mathrm{mg\cdot h/L} = \frac{D}{CL} = \frac{500}{4.33}
\]

Both routes to the AUC agree, a useful consistency check.

## In code

We compute the IV-bolus profile in closed form, confirm it against a numerical ODE solve, and estimate the AUC by the trapezoid rule.

### R

```r
library(deSolve)
library(pracma)

D <- 500; V <- 25; k <- 0.173         # dose, volume, rate constant
C0 <- D / V                            # 20 mg/L
t  <- seq(0, 24, by = 0.1)
Cexact <- C0 * exp(-k * t)

# numerical ODE for the same one-compartment system
f <- function(t, C, p) list(-p$k * C)
out <- ode(y = c(C = C0), times = t, func = f, parms = list(k = k))
max(abs(out[, "C"] - Cexact))          # ~1e-6: ODE matches closed form

trapz(t, Cexact)                        # ~113.6 mg*h/L (finite window)
C0 / k                                  # 115.6 mg*h/L (0 to infinity)
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

D, V, k = 500.0, 25.0, 0.173
C0 = D / V                              # 20 mg/L
t = np.linspace(0, 24, 241)
Cexact = C0 * np.exp(-k * t)

sol = solve_ivp(lambda t, C: -k * C, (0, 24), [C0], t_eval=t, rtol=1e-9)
print(np.max(np.abs(sol.y[0] - Cexact)))   # ~1e-7: agree

print(np.trapz(Cexact, t))                 # ~113.6 mg*h/L
print(C0 / k)                              # 115.6 mg*h/L (analytic AUC)
```

### Julia

```julia
using DifferentialEquations

D, V, k = 500.0, 25.0, 0.173
C0 = D / V                              # 20 mg/L
prob = ODEProblem((C, p, t) -> -k * C, C0, (0.0, 24.0))
sol = solve(prob, Tsit5(); saveat = 0.1)

t = sol.t
Cexact = @. C0 * exp(-k * t)
maximum(abs.(sol.u .- Cexact))          # tiny: numerical matches analytic

auc = sum(diff(t) .* (Cexact[1:end-1] .+ Cexact[2:end]) ./ 2)  # ~113.6
C0 / k                                   # 115.6 analytic AUC
```

## Why it matters

Every antibiotic dose is chosen by solving these equations: clearance and volume set the dose and interval, and the resulting concentration–time curve is the input to the drug's effect.
Linking that curve to [pharmacodynamics](pharmacodynamics.md) — what the drug does to the pathogen — is exactly how the [PK/PD indices](antimicrobial-pkpd.md) for antimicrobial dosing are built.

## Related

- [Pharmacodynamics: Dose–Response](pharmacodynamics.md)
- [Antimicrobial PK/PD](antimicrobial-pkpd.md)
- [Compartmental Models](sir.md) — the same mass-balance ODEs
- [Exponentials and Logarithms](exponentials-and-logarithms.md) — first-order decay
- [Integrals](integrals.md) — computing the AUC
- [Derivatives](derivatives.md) — finding the peak concentration
- [Quantitative Methods](../math.md)
