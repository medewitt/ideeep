---
title: "ELISA"
---

# ELISA

The enzyme-linked immunosorbent assay (ELISA) uses the exquisite specificity of an **antibody–antigen bond** to detect and quantify a target, reading it out as a color change driven by an enzyme.
Run in 96-well plates, it is the workhorse of **serosurveillance** (measuring who has antibodies to a pathogen) and of antigen detection, cheap and scalable enough to process thousands of samples a day.

![An ELISA standard curve fit with the four-parameter logistic model: optical density rises sigmoidally with analyte concentration, with the inflection at the EC50.](../assets/figures/elisa-4pl.svg)

## The core idea and the main formats

Every ELISA immobilizes something on the plate, washes away everything that does not stick, and detects what remains with an **enzyme-conjugated antibody** that converts a colorless substrate into a colored product.
The **optical density (OD)** measured by a plate reader is proportional to how much target was captured.

- **Direct** — antigen on the plate, detected by a single enzyme-labeled antibody.
- **Indirect** — antigen on the plate, detected by a patient antibody, then an enzyme-labeled anti-species secondary antibody.
  This is the standard format for **antibody/serology** testing.
- **Sandwich** — a capture antibody on the plate grabs the antigen, and a second labeled antibody detects it.
  Highly specific for **antigen** detection.
- **Competitive** — sample analyte competes with a labeled reference; here **more signal means less analyte**, useful for small molecules.

## Turning optical density into concentration

OD does not rise linearly with concentration — it saturates.
The standard model for an ELISA calibration curve is the **four-parameter logistic (4PL)**:

$$\text{OD}(x) = d + \frac{a - d}{1 + (x/c)^{b}},$$

where $a$ is the bottom (blank) signal, $d$ is the top (saturation), $c$ is the **EC50** (the concentration at the inflection point), and $b$ is the Hill slope.
You fit the 4PL to a dilution series of known standards, then invert it to read unknown concentrations off their ODs.
Reliable quantification is only possible within the curve's dynamic range — samples above saturation must be diluted and re-run.

## Cutoffs for qualitative serology

For yes/no serosurveys the readout is dichotomized with a **cutoff**, often set from a panel of known negatives (e.g. mean + 3 SD of the negative controls).
Every cutoff trades [sensitivity against specificity](../math/diagnostic-testing.md), and because seroprevalence surveys often run at **low true prevalence**, even a small false-positive rate can dominate the positives — which is why raw seroprevalence is usually adjusted for assay performance.

## A worked example

We fit a 4PL curve to a seven-point standard series and back-calculate the concentration of an unknown from its OD.

## In code

### R

```r
fourpl <- function(x, a, d, c, b) d + (a - d) / (1 + (x / c)^b)
conc <- c(1, 3, 10, 30, 100, 300, 1000)
od   <- c(0.06, 0.12, 0.34, 0.98, 1.9, 2.7, 3.1)

fit <- nls(od ~ fourpl(conc, a, d, c, b),
           start = list(a = 0.05, d = 3.2, c = 30, b = 1))
coef(fit)   # bottom, top, EC50, Hill slope
```

### Python

```python
import numpy as np
from scipy.optimize import curve_fit

def fourpl(x, a, d, c, b):
    return d + (a - d) / (1 + (x / c) ** b)

conc = np.array([1, 3, 10, 30, 100, 300, 1000.0])
od   = np.array([0.06, 0.12, 0.34, 0.98, 1.9, 2.7, 3.1])

(a, d, c, b), _ = curve_fit(fourpl, conc, od, p0=[0.05, 3.2, 30.0, 1.0], maxfev=10000)
print(f"bottom={a:.2f}  top={d:.2f}  EC50={c:.1f} ng/mL  hill={b:.2f}")

# invert the curve to read an unknown OD back to a concentration
od_unknown = 1.2
conc_unknown = c * ((a - d) / (od_unknown - d) - 1) ** (1 / b)
print(f"OD {od_unknown} -> {conc_unknown:.1f} ng/mL")
```

<!-- python-output:auto -->
```text
bottom=0.01  top=3.30  EC50=73.0 ng/mL  hill=1.04
OD 1.2 -> 42.4 ng/mL
```
<!-- /python-output:auto -->

### Julia

```julia
using LsqFit
fourpl(x, p) = p[2] .+ (p[1] .- p[2]) ./ (1 .+ (x ./ p[3]) .^ p[4])
conc = [1, 3, 10, 30, 100, 300, 1000.0]
od   = [0.06, 0.12, 0.34, 0.98, 1.9, 2.7, 3.1]

fit = curve_fit(fourpl, conc, od, [0.05, 3.2, 30.0, 1.0])
fit.param   # bottom, top, EC50, Hill slope
```

## Trade-offs & resource considerations

- **Sensitivity & specificity.** Good, and tunable through the cutoff, but bounded by the quality of the antibody reagents and by cross-reactivity — antibodies raised against one pathogen may bind a related one, inflating false positives.
- **Cost.** Moderate: a plate reader (a few thousand dollars), plates, and antibody/conjugate reagents.
  Per-sample cost is low once the platform is in place, which is why ELISA scales for large serosurveys.
- **Training & infrastructure.** A standard immunology-lab technique — pipetting accuracy, wash steps, and **plate-to-plate controls** matter, and results drift without careful standardization across batches and operators.
- **Turnaround.** Hours per plate, in batches.
- **Quantitative discipline.** Every plate needs its own standard curve and controls; comparing raw ODs across plates without recalibration is a common and serious error.

## Why it matters

ELISA is how we measure population immunity.
Serosurveys built on ELISA tell us what fraction of a population has been infected or vaccinated — the [susceptible pool](../math/sir.md) that drives whether transmission can be sustained — and antigen-capture ELISAs detect active infection where a rapid test is not sensitive enough.

## Related

- [Rapid Antigen & Lateral-Flow Tests](rapid-antigen-tests.md)
- [SDS-PAGE and Western Blotting](sds-page-western-blot.md)
- [Diagnostic Testing and Screening](../math/diagnostic-testing.md)
- [Pharmacodynamics: Dose–Response](../math/pharmacodynamics.md) — the same logistic/Hill curve
- [Diagnostics & Surveillance](../diagnostics.md)
