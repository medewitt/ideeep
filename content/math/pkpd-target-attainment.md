---
title: "PK/PD Target Attainment"
description: "Using pharmacodynamic targets and Monte Carlo over patient variability to compute the probability of target attainment and choose antimicrobial doses and breakpoints."
---

# PK/PD Target Attainment

A dose that works in the average patient can still fail in many individuals, because clearance, volume, and MIC all vary.
Target attainment turns that variability into a probability: given a dose and an organism, what fraction of patients reach the pharmacodynamic target that predicts a good outcome?
The calculation joins the concentration-time curve from [pharmacokinetics](pharmacokinetics.md) to the [PK/PD indices](antimicrobial-pkpd.md) through a Monte Carlo simulation over between-patient differences.

![Probability of target attainment falling as the MIC rises, shown for two doses, with the 90% attainment target marked.](../assets/figures/pkpd-target-attainment.svg)

## Pharmacodynamic targets

The feature of the concentration-time profile that predicts killing depends on the drug class, giving three targets measured against the MIC.

For **beta-lactams** killing is time-dependent, so the target is the fraction of the dosing interval that free drug spends above the MIC:

\[
fT_{>MIC} = \frac{1}{\tau}\int_0^\tau \mathbf{1}\!\left[fC(t) > MIC\right] dt
\]

with goals typically around $40$ to $70\%$ of the interval.
For **fluoroquinolones and vancomycin** total exposure matters, so the target is the free 24-hour area under the curve over the MIC, $fAUC_{24}/MIC$.
For **aminoglycosides** a tall peak drives killing, so the target is the peak over the MIC, $fC_{max}/MIC$.
Each target is a single number that a simulated profile either clears or misses.

## Probability of target attainment

A patient's pharmacokinetics are not known in advance, so the target is met only with some probability.
Let $\theta$ collect the patient-varying parameters (clearance, volume), drawn from a population distribution $p(\theta)$ fit to a pharmacokinetic study.
The **probability of target attainment** at a given dose and MIC is the chance a random patient clears the target:

\[
\mathrm{PTA}(\text{dose}, MIC) = \Pr\!\left[\, T(\theta) \ge T^\ast \mid \text{dose}, MIC \,\right]
= \int \mathbf{1}\!\left[T(\theta) \ge T^\ast\right] p(\theta)\, d\theta
\]

where $T(\theta)$ is the achieved index for that patient and $T^\ast$ is the target value.
The integral rarely has a closed form, so it is estimated by Monte Carlo: draw many virtual patients, compute each one's index, and take the fraction that succeed.
A regimen is usually judged acceptable when $\mathrm{PTA} \ge 90\%$.

## From PTA to the cumulative fraction of response

PTA is computed at a single MIC, but a real pathogen population presents a *distribution* of MICs.
Weighting the PTA by how often each MIC occurs gives the **cumulative fraction of response**, the expected attainment across the organism population:

\[
\mathrm{CFR} = \sum_{i} \mathrm{PTA}(MIC_i)\, \Pr(MIC = MIC_i)
\]

CFR answers the empirical-therapy question, where the MIC is unknown at the time of dosing, whereas PTA answers the targeted question once the MIC is measured.

## Choosing doses and breakpoints

The PTA-versus-MIC curve is the tool for both decisions.
Reading down from the $90\%$ line gives the highest MIC a dose reliably covers, which is the pharmacodynamic **breakpoint** separating susceptible from resistant.
Reading across shows how a larger dose or a longer infusion shifts the whole curve rightward, extending coverage to less susceptible organisms.
Regulators and committees use exactly these curves to set dosing and susceptibility breakpoints.

## A worked example

Take a beta-lactam given as a $1\ \mathrm{g}$ intravenous bolus every $\tau = 8\ \mathrm{h}$ into a volume $V = 15\ \mathrm{L}$, with the target $fT_{>MIC} \ge 50\%$ against an organism with $MIC = 8\ \mathrm{mg/L}$.
Clearance varies across patients lognormally with median $6\ \mathrm{L/h}$ and a coefficient of variation of $40\%$, so each patient has elimination rate $k = CL/V$ and a steady-state peak

\[
C_{max,ss} = \frac{D/V}{1 - e^{-k\tau}}
\]

The concentration decays as $C_{max,ss}\, e^{-kt}$ over the interval, so it stays above the MIC for a time $\ln(C_{max,ss}/MIC)/k$, and the fraction above MIC is that time divided by $\tau$ (capped at one, or zero if the peak never reaches the MIC).
Simulating many patients and counting those with $fT_{>MIC} \ge 50\%$ gives a PTA near $78\%$ for the $1\ \mathrm{g}$ dose, short of the $90\%$ goal.
Doubling to $2\ \mathrm{g}$ lifts the whole profile and pushes PTA above $90\%$ at the same MIC, which is exactly how a dose is selected.

## In code

We draw lognormal clearances, form each patient's steady-state profile in closed form, compute $fT_{>MIC}$, and report the attainment probability for two doses at a fixed MIC.

### R

```r
set.seed(1834)
V <- 15; tau <- 8; target <- 0.50; mic <- 8
cl_med <- 6; cl_cv <- 0.40; n <- 5000

sigma <- sqrt(log(1 + cl_cv^2))
cl <- cl_med * exp(rnorm(n, 0, sigma))       # lognormal clearance
k  <- cl / V

ft_above <- function(dose) {
  cmax <- (dose / V) / (1 - exp(-k * tau))    # steady-state peak
  tcross <- ifelse(cmax > mic, log(cmax / mic) / k, 0)
  pmin(tcross, tau) / tau
}
c(g1 = mean(ft_above(1000) >= target),        # ~0.78
  g2 = mean(ft_above(2000) >= target))        # ~0.93
```

### Python

```python
import numpy as np

rng = np.random.default_rng(1834)
V, tau, target, mic = 15.0, 8.0, 0.50, 8.0
cl_med, cl_cv, n = 6.0, 0.40, 5000

sigma = np.sqrt(np.log(1 + cl_cv**2))
cl = cl_med * np.exp(rng.normal(0.0, sigma, n))   # lognormal clearance
k = cl / V


def ft_above_mic(dose):
    cmax = (dose / V) / (1 - np.exp(-k * tau))     # steady-state peak
    t_cross = np.where(cmax > mic, np.log(cmax / mic) / k, 0.0)
    return np.minimum(t_cross, tau) / tau


for dose in (1000.0, 2000.0):
    pta = np.mean(ft_above_mic(dose) >= target)
    print(f"dose={dose/1000:.0f} g   PTA at MIC={mic:g} = {pta:.3f}")
```

<!-- python-output:auto -->
```text
dose=1 g   PTA at MIC=8 = 0.776
dose=2 g   PTA at MIC=8 = 0.930
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics
Random.seed!(1834)
V, tau, target, mic = 15.0, 8.0, 0.50, 8.0
cl_med, cl_cv, n = 6.0, 0.40, 5000

sigma = sqrt(log(1 + cl_cv^2))
cl = cl_med .* exp.(sigma .* randn(n))          # lognormal clearance
k = cl ./ V

function ft_above(dose)
    cmax = (dose / V) ./ (1 .- exp.(-k .* tau))
    tcross = ifelse.(cmax .> mic, log.(cmax ./ mic) ./ k, 0.0)
    min.(tcross, tau) ./ tau
end
(mean(ft_above(1000.0) .>= target),            # ~0.78
 mean(ft_above(2000.0) .>= target))            # ~0.93
```

## Why it matters

Target attainment is how dosing decisions carry their uncertainty honestly, reporting the probability a regimen works rather than a single point estimate that hides the patients it fails.
The same PTA curves that pick a dose also set the susceptibility breakpoints laboratories use to call an organism resistant, linking bedside pharmacology to surveillance.
Keeping attainment high at the individual scale is also what suppresses the [population spread of resistance](resistance-dynamics.md), since regimens that clear infections reliably give resistant strains fewer openings.

## Related

- [Pharmacokinetics: Compartment Models](pharmacokinetics.md) — the concentration-time curve behind each patient
- [Pharmacodynamics: Dose–Response](pharmacodynamics.md) — where the targets come from
- [Antimicrobial PK/PD](antimicrobial-pkpd.md) — the indices scored against the MIC
- [Population Dynamics of Resistance](resistance-dynamics.md) — the sibling population view
- [Quantitative Methods](../math.md)
