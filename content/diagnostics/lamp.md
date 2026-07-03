---
title: "LAMP: Isothermal Amplification"
---

# LAMP: Isothermal Amplification

Loop-mediated isothermal amplification (LAMP) does what [qPCR](qpcr.md) does — copy a target nucleic acid until it is detectable — but **without thermal cycling**.
The whole reaction runs at a single, constant temperature (around 60–65 °C), which means it needs nothing more than a heat block or even body heat, no expensive thermocycler.
That single fact makes LAMP one of the most important tools for **point-of-care and field molecular diagnostics**.

## How it works

LAMP uses a strand-displacing DNA polymerase and a set of **four to six primers** that recognize six to eight distinct regions of the target.
The primers are designed so that the growing strands fold back on themselves to form loops, creating new priming sites continuously.
The result is a self-sustaining cascade that produces a large amount of product very fast — a positive can appear in as little as 15–30 minutes.

Because amplification does not need the sample to be cycled, LAMP is also more **tolerant of inhibitors** found in crude specimens, so it often works on minimally processed samples (a limited swab eluate, sometimes raw saliva) where PCR would need clean, extracted nucleic acid.

For RNA targets, adding a reverse-transcription step gives **RT-LAMP**, which is the basis of many rapid tests for SARS-CoV-2 and other RNA viruses.

## Reading the result

LAMP produces so much product that the readout can be gloriously simple:

- **Colorimetric** — a pH-sensitive dye changes color (e.g. pink to yellow) as the reaction releases protons; readable by eye.
- **Turbidity** — precipitating magnesium pyrophosphate makes the tube visibly cloudy.
- **Fluorescence** — an intercalating dye allows real-time, quantitative readout on an instrument.

The eyeball-readable versions are what let LAMP run outside a laboratory entirely.

## Trade-offs & resource considerations

- **Sensitivity & specificity.** High, approaching PCR for many targets, and the multi-primer design gives good specificity.
  It is generally a little less sensitive than a well-optimized qPCR near the limit of detection.
- **Cost.** Low: no thermocycler, minimal equipment, and cheap lyophilized ("dried-down") reagent formats that survive without a cold chain — a decisive advantage in low-resource settings.
- **Training & infrastructure.** Minimal to run, which is the whole point.
  The hard part is **up front**: designing and validating the four-to-six-primer set is considerably more demanding than designing PCR primers, so assay development is specialist work even though deployment is not.
- **Turnaround.** Very fast — results in under an hour, often in 30 minutes.
- **The main hazard is contamination.** LAMP generates enormous amounts of amplicon, so a single opened positive tube can aerosolize product and cause false positives across a workspace; closed-tube readouts and strict workflow separation are essential.

## Why it matters

LAMP is the technology that moves molecular-grade sensitivity out of the reference lab and toward the patient.
For diseases where the barrier to control is **access to fast testing** — malaria and tuberculosis in low-resource settings, outbreak triage in the field — an isothermal assay that a community health worker can run on a heat block changes what surveillance is possible.

## Related

- [qPCR and RT-qPCR](qpcr.md)
- [Rapid Antigen & Lateral-Flow Tests](rapid-antigen-tests.md)
- [Diagnostic Testing and Screening](../math/diagnostic-testing.md)
- [Diagnostics & Surveillance](../diagnostics.md)
