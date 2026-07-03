---
title: "qPCR and RT-qPCR"
---

# qPCR and RT-qPCR

Quantitative PCR is the reference standard for detecting a pathogen's nucleic acid.
It copies a target DNA sequence through repeated cycles of heating and cooling, and — crucially — measures the amount of product **as it accumulates**, in real time, using a fluorescent reporter.
For RNA viruses a reverse-transcription step (**RT-qPCR**) first turns RNA into DNA; this is the chemistry behind most molecular tests for SARS-CoV-2, influenza, and HIV viral load.

![A qPCR standard curve: quantification cycle (Ct) plotted against log10 template copies, with the slope giving the amplification efficiency.](../assets/figures/qpcr-standard-curve.svg)

## How amplification is read out

Each cycle roughly doubles the amount of target, so product grows **exponentially** until reagents deplete.
Fluorescence rises in step with product.
The **quantification cycle** (Ct, also called Cq) is the cycle number at which fluorescence crosses a fixed threshold above background.

More starting template means the threshold is crossed sooner, so **Ct is inversely related to the amount of target**: a low Ct (say 18) means a lot of template, a high Ct (say 35) means very little.
This is why Ct is sometimes used as a rough proxy for viral load, though it is sensitive to sampling and assay details and should be interpreted cautiously.

## The standard curve, efficiency, and quantification

To turn Ct into an absolute quantity you run a **dilution series** of known concentration and fit a line:

$$\text{Ct} = a + b \cdot \log_{10}(\text{copies}).$$

The slope $b$ measures **amplification efficiency**:

$$E = 10^{-1/b} - 1.$$

A slope of $-3.32$ corresponds to perfect doubling every cycle, $E = 100\%$; acceptable assays fall roughly between $-3.6$ and $-3.1$ (90–110%).
The intercept sets the assay's sensitivity, and the lowest concentration reliably detected is the **limit of detection (LOD)**.

**Digital PCR (dPCR)** sidesteps the standard curve entirely by partitioning the sample into thousands of tiny reactions and counting how many are positive, giving an absolute count without a calibrator — at higher cost.

## Controls

A trustworthy qPCR run carries controls: a **no-template control** (catches contamination), a **positive control** (confirms the assay works), and, for RT-qPCR, an **internal/extraction control** (a host gene or spike-in that confirms the specimen was adequate and not inhibited).

## A worked example

We fit a standard curve to a ten-fold dilution series and read the efficiency off the slope, then quantify an unknown from its Ct.

## In code

### R

```r
log10_copies <- 1:7
ct <- c(36.8, 33.5, 30.1, 26.9, 23.5, 20.2, 16.9)
fit <- lm(ct ~ log10_copies)

slope <- coef(fit)[2]
efficiency <- 10^(-1 / slope) - 1
unknown_ct <- 28.0
unknown_log10 <- (unknown_ct - coef(fit)[1]) / slope

c(efficiency = efficiency, r2 = summary(fit)$r.squared,
  unknown_copies = 10^unknown_log10)
```

### Python

```python
import numpy as np

log10_copies = np.arange(1, 8)
ct = np.array([36.8, 33.5, 30.1, 26.9, 23.5, 20.2, 16.9])

slope, intercept = np.polyfit(log10_copies, ct, 1)
efficiency = 10 ** (-1 / slope) - 1

# R^2 of the linear fit
pred = intercept + slope * log10_copies
r2 = 1 - np.sum((ct - pred) ** 2) / np.sum((ct - ct.mean()) ** 2)

# quantify an unknown from its Ct
unknown_ct = 28.0
unknown_copies = 10 ** ((unknown_ct - intercept) / slope)

print(f"efficiency = {efficiency*100:.1f}%   R^2 = {r2:.4f}")
print(f"Ct {unknown_ct} -> {unknown_copies:,.0f} copies")
```

<!-- python-output:auto -->
```text
efficiency = 100.2%   R^2 = 1.0000
Ct 28.0 -> 4,480 copies
```
<!-- /python-output:auto -->

### Julia

```julia
log10_copies = 1:7
ct = [36.8, 33.5, 30.1, 26.9, 23.5, 20.2, 16.9]

X = hcat(ones(length(ct)), collect(log10_copies))
intercept, slope = X \ ct
efficiency = 10^(-1 / slope) - 1
unknown_copies = 10^((28.0 - intercept) / slope)

(efficiency = efficiency, unknown_copies = unknown_copies)
```

## Trade-offs & resource considerations

- **Sensitivity & specificity.** qPCR is the benchmark: analytical sensitivity down to a handful of copies and near-perfect specificity when primers and probes are well designed.
  Its clinical sensitivity is still bounded by **sampling** — a swab that misses the site of replication, or a test run outside the [diagnostic window](../diagnostics.md), yields a false negative despite a flawless assay.
- **Cost.** Moderate-to-high per test, plus a thermocycler (thousands to tens of thousands of dollars), extraction reagents, and probes; reagent supply chains are a real vulnerability during surges.
- **Training & infrastructure.** Needs a molecular lab with separated pre- and post-amplification areas to prevent contamination, reliable power, a **cold chain** for reagents, and technologists trained in extraction and assay setup.
- **Turnaround.** Hours per run, longer once transport and batching are counted — the main reason point-of-care alternatives like [LAMP](lamp.md) and [rapid antigen tests](rapid-antigen-tests.md) exist.
- **Interpretation.** A positive means nucleic acid is present, not that viable, transmissible pathogen is — PCR can stay positive long after infectiousness ends.

## Why it matters

RT-qPCR is the molecular backbone of outbreak response: it defines confirmed cases, drives [wastewater surveillance](../diagnostics.md), and supplies the positive samples that feed [genomic surveillance](../math/molecular-clock.md).
Understanding Ct, efficiency, and the standard curve is what separates "the test was positive" from a defensible, quantitative result.

## Related

- [LAMP: Isothermal Amplification](lamp.md)
- [Rapid Antigen & Lateral-Flow Tests](rapid-antigen-tests.md)
- [Diagnostic Testing and Screening](../math/diagnostic-testing.md)
- [Linear Regression](../math/linear-regression.md)
- [Diagnostics & Surveillance](../diagnostics.md)
