---
title: "Antimicrobial PK/PD"
---

# Antimicrobial PK/PD

Antimicrobial PK/PD combines what the body does to the drug with what the drug does to the pathogen, in order to pick a dose and schedule that maximizes killing while suppressing resistance.
It joins the concentration–time curve from [pharmacokinetics](pharmacokinetics.md) to the concentration–effect curve from [pharmacodynamics](pharmacodynamics.md) through a single benchmark: the MIC.

![Left: the worked IV-bolus profile C(t) = 40·e^(−0.35t) against MIC = 2 shows all three indices at once — the peak (Cmax/MIC = 20), the shaded exposure (AUC/MIC), and the time the free concentration stays above the MIC (%T>MIC = 100% here). Right: delivering the same daily dose as a short bolus, an extended infusion, or a continuous infusion keeps the concentration above the MIC for very different fractions of the interval, so the best dosing shape depends on which index governs the drug.](../assets/figures/antimicrobial-pkpd.svg "fig:pkpd")

## The MIC and free drug

The **minimum inhibitory concentration** (MIC) is the lowest drug concentration that prevents visible growth of an organism in vitro.
It is a fixed number for a given drug–bug pair, so the concentration–time profile can be scored against it.
Only unbound (free) drug is microbiologically active, so the indices below use the free concentration $f\,C(t)$, where $f$ is the unbound fraction.

## The three PK/PD indices

Which feature of the profile predicts efficacy depends on the drug's kill pattern, giving three indices ([@fig:pkpd]).

### Percent time above MIC

For **time-dependent** agents such as β-lactams, killing depends on how long the free concentration stays above the MIC, not how high it climbs:

\[
\%fT_{>MIC} = \frac{1}{\tau}\int_0^\tau \mathbf{1}\!\left[f\,C(t) > MIC\right]\,dt \times 100\%
\]

Typical bacteriostatic-to-maximal targets fall around $T_{>MIC} \approx 40\text{–}70\%$ of the dosing interval $\tau$.

### AUC over MIC

For agents whose total exposure matters — fluoroquinolones, and vancomycin — the index is the 24-hour free AUC divided by the MIC:

\[
\frac{fAUC_{24}}{MIC}
\]

A widely used vancomycin target is $AUC/MIC \approx 400$.

### Peak over MIC

For **concentration-dependent** agents such as aminoglycosides, a high peak drives rapid killing:

\[
\frac{fC_{max}}{MIC} \approx 8\text{–}10
\]

## Dosing strategies

Each index implies a dosing shape.
Because β-lactams are governed by time above MIC, extended or continuous infusions keep the concentration over the MIC for more of the interval than a short bolus of the same total dose.
Because aminoglycosides are governed by the peak, once-daily dosing gives a tall peak (large $C_{max}/MIC$) while allowing a drug-free trough that limits toxicity and exploits the post-antibiotic effect.

### Suppressing resistance

Above the MIC but below the concentration that blocks resistant mutants (the mutant prevention concentration) lies the **mutant selection window**, where susceptible cells are killed but pre-existing resistant mutants are selectively amplified.
Regimens that push exposure through this window quickly — higher peaks or sustained time above MIC — reduce the chance of selecting resistance.

## Worked example

Take a one-compartment IV bolus with $C_0 = 40\ \mathrm{mg/L}$ and elimination rate $k = 0.35\ \mathrm{h^{-1}}$ (half-life 2 h), dosed every $\tau = 8\ \mathrm{h}$, against an organism with $MIC = 2\ \mathrm{mg/L}$.
Assume the drug is fully unbound ($f = 1$) for simplicity, so $C(t) = 40\,e^{-0.35 t}$.

The concentration falls to the MIC when $40\,e^{-0.35 t} = 2$, i.e.

\[
t_{>MIC} = \frac{\ln(C_0/MIC)}{k} = \frac{\ln(40/2)}{0.35} = \frac{\ln 20}{0.35} = \frac{2.996}{0.35} = 8.56\ \mathrm{h}
\]

Since $8.56\ \mathrm{h}$ exceeds the 8 h interval, the free concentration stays above the MIC for the entire interval, so $\%T_{>MIC} = 100\%$.

At steady state the AUC over one dosing interval equals the single-dose AUC from $0$ to $\infty$, namely $C_0/k$, so the exposure over 24 h (three doses of $\tau = 8\ \mathrm{h}$) is $AUC_{24} = 3 \times C_0/k$:

\[
AUC_{24} = 3 \times \frac{40}{0.35} = 3 \times 114.3 = 342.9\ \mathrm{mg\cdot h/L}
\]

\[
\frac{AUC_{24}}{MIC} = \frac{342.9}{2} = 171
\]

The peak-to-MIC ratio is $C_{max}/MIC = 40/2 = 20$.
So this regimen easily satisfies a time-dependent target but would fall short of a vancomycin-style $AUC/MIC \approx 400$ goal — a concrete illustration of how the target index changes the verdict on the same profile.

## In code

We simulate one dose of $C(t)$, find the time above MIC by root-finding, integrate the single-dose AUC by the trapezoid rule, and use the steady-state identity $AUC_{24} = n_{doses}\times AUC_{0\text{-}\infty}$ to report all three indices.

### R

```r
library(pracma)

C0 <- 40; k <- 0.35; tau <- 8; MIC <- 2; n <- 3   # 3 doses/day
Cf <- function(t) C0 * exp(-k * t)

# time above MIC (root of Cf(t) = MIC), capped at tau
tcross <- log(C0 / MIC) / k
tabove <- min(tcross, tau)
pct_T  <- 100 * tabove / tau            # 100% here

t <- seq(0, 48, by = 0.01)              # ~infinite horizon for one dose
auc_single <- trapz(t, Cf(t))           # ~114.3 = C0/k
auc24 <- n * auc_single                 # 342.9 mg*h/L
c(pctT = pct_T, AUC_MIC = auc24 / MIC, Cmax_MIC = C0 / MIC)
# ~ pctT 100, AUC/MIC 171, Cmax/MIC 20
```

### Python

```python
import numpy as np
from scipy.optimize import brentq

C0, k, tau, MIC, n = 40.0, 0.35, 8.0, 2.0, 3   # 3 doses/day
Cf = lambda t: C0 * np.exp(-k * t)

tcross = brentq(lambda t: Cf(t) - MIC, 0, tau) if Cf(tau) < MIC else tau
tabove = min(tcross, tau)
pct_T = 100 * tabove / tau               # 100.0

t = np.linspace(0, 48, 4801)             # ~infinite horizon for one dose
auc_single = np.trapz(Cf(t), t)          # ~114.3 = C0/k
auc24 = n * auc_single                    # 342.9
print(pct_T, auc24 / MIC, C0 / MIC)      # ~ 100, 171, 20
```

### Julia

```julia
using Roots

C0, k, tau, MIC, n = 40.0, 0.35, 8.0, 2.0, 3   # 3 doses/day
Cf(t) = C0 * exp(-k * t)

tcross = Cf(tau) < MIC ? find_zero(t -> Cf(t) - MIC, (0, tau)) : tau
tabove = min(tcross, tau)
pct_T  = 100 * tabove / tau              # 100.0

t = 0:0.01:48                            # ~infinite horizon for one dose
Cvals = Cf.(t)
auc_single = sum(diff(t) .* (Cvals[1:end-1] .+ Cvals[2:end]) ./ 2)  # ~114.3
auc24 = n * auc_single                   # 342.9
(pct_T, auc24 / MIC, C0 / MIC)           # ~ (100, 171, 20)
```

## Why it matters

PK/PD indices turn a pile of pharmacology into three actionable numbers that tell you whether a regimen will work and how to reshape it if it will not — infuse longer, dose higher, or extend the interval.
Getting these targets right at the population level is also what keeps the [transmission](sir.md) of resistant organisms in check, linking bedside dosing to the epidemiology of resistance.

## Related

- [Pharmacokinetics: Compartment Models](pharmacokinetics.md)
- [Pharmacodynamics: Dose–Response](pharmacodynamics.md)
- [Compartmental Models](sir.md) — transmission of resistant strains
- [Quantitative Methods](../math.md)
