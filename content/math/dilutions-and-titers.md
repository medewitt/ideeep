---
title: "Dilutions, Titers, and Standard Curves"
description: "Turning an assay readout into a concentration: serial-dilution titers and endpoints, and reading an unknown off an ELISA standard curve."
---

# Dilutions, Titers, and Standard Curves

An assay never hands you a concentration directly.
It gives a **readout** — a count of plaques, the last dilution that still shows an effect, an optical density — and the quantitative work is turning that readout back into "how much was in the sample."
This page collects the two everyday calculations that do it: the **serial-dilution titer** used throughout serology and virology, and the **standard-curve interpolation** used for continuous readouts like an ELISA optical density.

![Left: a two-fold serial dilution chain — each tube holds half the concentration of the one before, so the reciprocal dilution doubles down the row. Right: a serum's percent-neutralization dose-response; the 50% neutralization titer (NT50) is read where the curve crosses 50%, interpolated between the bracketing dilutions to about 1:196.](../assets/figures/serial-dilution.svg "fig:dilution")

## Serial dilutions and the dilution factor

A **serial dilution** repeatedly dilutes a sample by a fixed factor — two-fold and ten-fold are the usual choices — so the concentration in tube $k$ falls geometrically:

\[
C_k = \frac{C_0}{\text{DF}^{\,k}},
\]

where $\text{DF}$ is the dilution factor.
Ten-fold steps span orders of magnitude quickly (for counting colonies or plaques); two-fold steps give the finer resolution wanted for a titer ([@fig:dilution]).

To recover the **original concentration from a countable dilution**, undo the dilution and the plated volume.
If a plate seeded with a $10^{-4}$ dilution and $0.1\ \text{mL}$ inoculum grows $32$ plaques, the stock titer is

\[
\text{titer} = \frac{N}{d \cdot V} = \frac{32}{10^{-4} \times 0.1} = 3.2\times 10^{6}\ \text{PFU/mL},
\]

with $N$ the count, $d$ the dilution fraction, and $V$ the plated volume.
The same arithmetic gives CFU/mL for bacteria or copies/mL for a spiked qPCR standard.

## Endpoint and 50% titers

For a graded readout — neutralization, hemagglutination inhibition, agglutination — the result is reported as a **titer**: the reciprocal of a dilution.
The simplest is the **endpoint titer**, the reciprocal of the *highest* dilution still scoring positive against a cutoff.
It is crude, because it can only land on the discrete dilutions actually tested.

A **50% titer** is far more stable: the dilution at which the response is half-maximal — NT50 for neutralization, TCID50 or ID50 for infectivity.
Because responses are roughly linear in the *log* of the dilution, you interpolate on the log scale between the two dilutions that bracket 50%:

\[
\log_2(\text{titer}) = x_1 + \frac{y_1 - 50}{y_1 - y_2}\,(x_2 - x_1),
\]

where $(x_1,y_1)$ and $(x_2,y_2)$ are the log-dilutions and responses on either side of 50%.
For strictly all-or-none readouts (each replicate positive or negative), the **Spearman–Kärber** estimator does the same job for the 50% infectious dose, summing the response proportions across the dilution series.

## A worked example: neutralization titer

A serum is tested in two-fold dilutions and the percent neutralization recorded at each.
We recover the plaque titer of the virus stock and the serum's NT50 by log-linear interpolation.

```python
import numpy as np

# virus stock titer from a plaque count
plaques, dilution, volume = 32, 1e-4, 0.1          # count, dilution, mL plated
titer = plaques / (dilution * volume)
print(f"stock titer = {titer:.2e} PFU/mL")

# serum neutralization: reciprocal dilution and percent neutralized
recip = np.array([10, 20, 40, 80, 160, 320, 640, 1280.0])
pct = np.array([98, 95, 88, 72, 55, 38, 20, 8.0])

lx = np.log2(recip)
i = np.where(pct >= 50)[0][-1]                      # last dilution >= 50%
xstar = lx[i] + (pct[i] - 50) / (pct[i] - pct[i + 1]) * (lx[i + 1] - lx[i])
nt50 = 2**xstar
endpoint = recip[i]                                 # crude endpoint titer
print(f"endpoint titer 1:{endpoint:.0f}   interpolated NT50 1:{nt50:.0f}")
```

<!-- python-output:auto -->
```text
stock titer = 3.20e+06 PFU/mL
endpoint titer 1:160   interpolated NT50 1:196
```
<!-- /python-output:auto -->

The interpolated NT50 (about $1{:}196$) sits between the tested dilutions, where the crude endpoint could only report $1{:}160$ — a real gain in precision for the same plate.

## Standard curves: continuous readouts

When the readout is a continuous signal — an ELISA optical density, a fluorescence — you calibrate against **standards** of known concentration and read unknowns off the fitted curve.
Optical density saturates, so the standard model is the **four-parameter logistic (4PL)** introduced on the [ELISA page](../diagnostics/elisa.md):

\[
\text{OD}(x) = d + \frac{a - d}{1 + (x/c)^{b}},
\]

with bottom $a$, top $d$, EC50 $c$, and Hill slope $b$.
Fit it to the standards, then **invert** it to turn an unknown OD back into a concentration:

\[
x = c\left(\frac{a - d}{\text{OD} - d} - 1\right)^{1/b}.
\]

Two practical rules travel with every standard curve ([@fig:curve]):

- **Stay inside the dynamic range.** Interpolation is only trustworthy between the lowest and highest standards; a sample above saturation must be **diluted and re-run**.
- **Multiply back by the dilution factor.** A sample pre-diluted $1{:}100$ to bring it on-scale reads a concentration $100\times$ smaller than the truth — the interpolated value must be scaled back up.

![An ELISA standard curve fit with a four-parameter logistic model; an unknown sample's optical density is projected onto the curve to recover its concentration, then multiplied by the 1:100 pre-dilution to report the original concentration.](../assets/figures/standard-curve-readback.svg "fig:curve")

## A worked example: ELISA optical density

A serum is pre-diluted $1{:}100$ to land within the assay's range and read at OD $1.10$.
We fit the 4PL to the standards, invert it, and correct for the dilution.

```python
from scipy.optimize import curve_fit

def fourpl(x, a, d, c, b):
    return d + (a - d) / (1 + (x / c) ** b)

conc = np.array([0.5, 1.5, 5, 15, 50, 150, 500.0])         # standards (units/mL)
od = np.array([0.05, 0.11, 0.30, 0.85, 1.8, 2.6, 3.0])
(a, d, c, b), _ = curve_fit(fourpl, conc, od, p0=[0.03, 3.1, 20, 1.0],
                            maxfev=20000)

od_unknown, dil_factor = 1.10, 100
x = c * ((a - d) / (od_unknown - d) - 1) ** (1 / b)         # invert the 4PL
print(f"EC50 = {c:.1f} units/mL   Hill slope = {b:.2f}")
print(f"OD {od_unknown} -> {x:.1f} units/mL  x{dil_factor} = {x*dil_factor:.0f} units/mL")
```

<!-- python-output:auto -->
```text
EC50 = 39.3 units/mL   Hill slope = 1.10
OD 1.1 -> 21.6 units/mL  x100 = 2163 units/mL
```
<!-- /python-output:auto -->

The raw interpolation gives about $22$ units/mL; multiplied by the $1{:}100$ pre-dilution, the reported concentration is roughly $2200$ units/mL — the number that would be wrong by a hundred-fold if the dilution step were forgotten.

## In code

### R

```r
fourpl <- function(x, a, d, c, b) d + (a - d) / (1 + (x / c)^b)
conc <- c(0.5, 1.5, 5, 15, 50, 150, 500)
od   <- c(0.05, 0.11, 0.30, 0.85, 1.8, 2.6, 3.0)
fit  <- nls(od ~ fourpl(conc, a, d, c, b),
            start = list(a = 0.03, d = 3.1, c = 20, b = 1))
p <- coef(fit)
x <- p["c"] * ((p["a"] - p["d"]) / (1.10 - p["d"]) - 1)^(1 / p["b"])
x * 100          # apply the 1:100 dilution factor
```

### Julia

```julia
using LsqFit
fourpl(x, p) = p[2] .+ (p[1] .- p[2]) ./ (1 .+ (x ./ p[3]) .^ p[4])
conc = [0.5, 1.5, 5, 15, 50, 150, 500.0]
od   = [0.05, 0.11, 0.30, 0.85, 1.8, 2.6, 3.0]
fit = curve_fit(fourpl, conc, od, [0.03, 3.1, 20.0, 1.0])
a, d, c, b = fit.param
x = c * ((a - d) / (1.10 - d) - 1)^(1 / b) * 100     # invert and un-dilute
```

## Why it matters

These two calculations sit under a huge amount of infectious-disease measurement.
Neutralization and hemagglutination-inhibition **titers** are the standard readouts of vaccine immunogenicity and serosurveillance; plaque and TCID50 assays quantify how much virus a sample carries; ELISA **standard curves** convert plate readings into the antibody concentrations that feed [seroprevalence](../epidemiology/severity-cfr-ifr.md) estimates.
Getting the dilution bookkeeping right — the factor, the plated volume, the pre-dilution — is mundane and completely consequential: a dropped factor of ten or a titer read off the wrong end of the curve turns a careful assay into a wrong number.

## Related

- [ELISA](../diagnostics/elisa.md)
- [qPCR and RT-qPCR](../diagnostics/qpcr.md)
- [Detection Probability: Viral Kinetics and Assay Thresholds](../epidemiology/detection-probability.md)
- [Pharmacodynamics: Dose–Response](pharmacodynamics.md)
- [Bland–Altman Agreement](bland-altman.md)
- [Diagnostic Testing and Screening](diagnostic-testing.md)
- [Quantitative Methods](../math.md)
