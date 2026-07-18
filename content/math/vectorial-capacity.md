---
title: "Vectorial Capacity from Field Data"
description: "Estimating entomological indices — biting rate, sporozoite rate, EIR, and daily survival — from field data and combining them into vectorial capacity."
---

# Vectorial Capacity from Field Data

How much malaria transmission can a mosquito population sustain?
The [Ross–Macdonald](vector-borne.md) theory answers with **vectorial capacity** — the number of infectious bites that will eventually arise from all the mosquitoes biting a single infectious person on one day — but the theory is only as good as the **entomological indices** fed into it.
This page is about the measurement side: turning field collections (landing catches, dissections, ELISA plates) into biting rates, survival, and infection rates, and propagating their uncertainty into a capacity estimate.

![Vectorial capacity as a function of daily mosquito survival p. Because a mosquito must survive the whole extrinsic incubation period to transmit, capacity depends on p^n/(−ln p) and climbs steeply; the field estimate sits on the steep part, so a small drop in survival collapses transmission — the reason bed nets and indoor spraying work.](../assets/figures/vc-survival-sensitivity.svg "fig:vc-sens")

## The entomological indices

Field transmission is quantified through a handful of measurable quantities:

- **Human biting rate** $ma$ — bites per person per night, from **human landing catches** or calibrated traps.
  ($m$ is mosquitoes per person, $a$ the per-mosquito rate of biting humans.)
- **Sporozoite rate** $s$ — the fraction of mosquitoes carrying infectious sporozoites, from salivary-gland dissection or a circumsporozoite ELISA/PCR — a proportion with a binomial [confidence interval](confidence-intervals.md).
- **Entomological inoculation rate** $\text{EIR} = ma \cdot s$ — infectious bites per person per unit time, the standard **field measure of transmission intensity**, usually annualized.
- **Daily survival probability** $p$ — inferred from **parity** (the fraction of females that have laid eggs): with a gonotrophic cycle of $g$ days, $p = (\text{parous fraction})^{1/g}$, and mean adult lifespan is $-1/\ln p$.
- **Extrinsic incubation period** $n$ — days for the pathogen to become transmissible inside the mosquito.

## Vectorial capacity

Assembling these gives the classic expression

\[
V = \frac{m\,a^{2}\,p^{n}}{-\ln p}.
\label{eq:vc}
\]

Each piece has a meaning: $a^2$ because the mosquito must bite **twice** (once to acquire, once to transmit); $p^n$ is the probability of surviving the incubation period; $-1/\ln p$ is the expected remaining infectious lifespan.
Vectorial capacity is the entomological ceiling on the [basic reproduction number](reproduction-number-rt.md) — $R_0 = V\, bc / r$ once you fold in the transmission efficiencies $b,c$ and human recovery rate $r$.

## Survival is the dominant lever

Equation [@eq:vc] is far more sensitive to some inputs than others.
It scales with the **square** of the biting rate and, through $p^{n}/(-\ln p)$, **extremely steeply with survival**: because $n$ is around $10$–$12$ days, a mosquito that dies a day or two sooner is very unlikely to ever become infectious ([@fig:vc-sens]).
This is the quantitative reason adult-killing interventions — [insecticide-treated](insecticide-resistance-monitoring.md) nets, indoor residual spraying — outperform larval control: shaving a few points off daily survival cuts capacity far more than halving mosquito numbers.
It is also why [insecticide resistance](insecticide-resistance-monitoring.md), which *restores* survival, is so damaging: it pushes the population back up the steep part of the curve.

## A worked example

From a season of collections — landing catches, $120$ dissected for parity, $500$ tested for sporozoites — we estimate the indices, compute the EIR and vectorial capacity, and bootstrap the uncertainty ([@fig:vc-est]).

![Bootstrap distribution of the estimated vectorial capacity: the point estimate is about 2.5, but resampling the field data gives a wide 95% interval (roughly 1.1 to 5.6), because entomological quantities — especially survival — are hard to pin down.](../assets/figures/vc-estimate.svg "fig:vc-est")

```python
import numpy as np

rng = np.random.default_rng(11)
hlc = rng.poisson(6, size=80)              # bites/person/night over 80 person-nights
g, hbi, n_eip = 3.0, 0.9, 11               # gonotrophic cycle, human blood index, EIP
parous, n_dissect = 78, 120                # parity dissections
sporo_pos, n_sporo = 15, 500               # sporozoite ELISA

hbr = hlc.mean()                           # human biting rate ma
a = hbi / g                                # biting rate on humans per day
p = (parous / n_dissect) ** (1 / g)        # daily survival from parity
s = sporo_pos / n_sporo                    # sporozoite rate
eir = hbr * s * 365                         # annual entomological inoculation rate
V = hbr * a * p**n_eip / (-np.log(p))       # since m*a^2 = (ma)*a = hbr*a

# bootstrap the field sampling error into V
def one(): 
    hb = rng.choice(hlc, len(hlc), replace=True).mean()
    pf = rng.binomial(n_dissect, parous / n_dissect) / n_dissect
    return hb * a * (pf ** (1 / g)) ** n_eip / (-np.log(pf ** (1 / g)))
boot = np.array([one() for _ in range(4000)])

print(f"biting rate {hbr:.1f}/night, survival p={p:.3f}, sporozoite {s*100:.1f}%")
print(f"annual EIR = {eir:.0f} infectious bites/person/year")
print(f"vectorial capacity V = {V:.2f}  "
      f"(95% CI {np.percentile(boot,2.5):.1f}-{np.percentile(boot,97.5):.1f})")
```

<!-- python-output:auto -->
```text
biting rate 5.7/night, survival p=0.866, sporozoite 3.0%
annual EIR = 63 infectious bites/person/year
vectorial capacity V = 2.47  (95% CI 1.1-5.6)
```
<!-- /python-output:auto -->

The headline numbers — an EIR near $60$ and a vectorial capacity around $2.5$ — describe intense transmission, but the wide bootstrap interval is the honest part: field entomology is noisy, and a capacity "estimate" with no uncertainty is not one.

## In code

### R

```r
# entomological indices are simple arithmetic; the value is in propagating error
p <- (parous / n_dissect)^(1 / g)               # daily survival
V <- hbr * (hbi / g) * p^n_eip / (-log(p))
# boot::boot() over the landing-catch and dissection data for a CI on V and EIR
```

### Julia

```julia
p = (parous / n_dissect)^(1 / g)
V = hbr * (hbi / g) * p^n_eip / (-log(p))
# resample hlc and redraw parity/sporozoite counts to bootstrap the interval
```

## Why it matters

The entomological inoculation rate is the field gold standard for malaria transmission intensity — the number every control programme wants to drive toward zero — and vectorial capacity is the mechanistic quantity that says *which lever* moves it most.
Because capacity hinges on mosquito survival raised to a large power, it explains why the historically successful vector-control tools all shorten mosquito life, and why measuring [insecticide resistance](insecticide-resistance-monitoring.md) matters: an intervention only lowers capacity if it still actually kills.
Reporting these indices with their uncertainty, rather than as point values, is what keeps an entomological risk assessment honest.

## Related

- [Vector-Borne Disease Models](vector-borne.md)
- [Insecticide-Resistance Monitoring](insecticide-resistance-monitoring.md)
- [The Reproduction Number](reproduction-number-rt.md)
- [Poisson Distribution](poisson-distribution.md)
- [Confidence Intervals](confidence-intervals.md)
- [Species Distribution Models: Presence–Absence Data](species-distribution-presence-absence.md)
- [Quantitative Methods](../math.md)
