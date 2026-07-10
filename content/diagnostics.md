---
title: "Diagnostics & Surveillance"
toc: true
description: "The workhorse laboratory methods of infectious-disease diagnostics and surveillance — qPCR, ELISA, LAMP, culture, MALDI-TOF and more — and the trade-offs that decide which to use."
image: assets/photos/parasite-microscopy-card.jpg
image_alt: "A parasite viewed under the microscope during laboratory diagnostics."
---

<img src="assets/photos/parasite-microscopy.jpg" style="width:100%;display:block;" alt="A parasite viewed under the microscope during laboratory diagnostics.">

# Diagnostics & Surveillance

Every case count, every prevalence estimate, and every genomic tree starts with a **laboratory test** that says "this sample contains this pathogen."
The methods differ in what they detect, how fast, how cheaply, and with what infrastructure — and no single assay wins on every axis.
This collection walks through the workhorse techniques of infectious-disease diagnostics and the trade-offs that decide which one belongs in a reference lab, a clinic, or a field tent.

![What each assay class detects across the course of an infection: nucleic acid and antigen appear early and transiently, while IgM and then IgG antibodies rise later and persist.](assets/figures/diagnostic-window.svg)

## What each method detects

A diagnostic can target any layer of the pathogen or the host's response to it, and the target sets both the timing of detection and the meaning of a positive.

- **Nucleic acid** (the pathogen's RNA/DNA) — [qPCR](diagnostics/qpcr.md), [LAMP](diagnostics/lamp.md). Most sensitive and specific; positive early, during active infection.
- **Antigen** (pathogen proteins) — [rapid antigen tests](diagnostics/rapid-antigen-tests.md), antigen-capture [ELISA](diagnostics/elisa.md). Fast and cheap; positive only when pathogen load is high.
- **Antibody** (the host's immune response) — [ELISA](diagnostics/elisa.md), [Western blot](diagnostics/sds-page-western-blot.md). Positive *after* seroconversion; the basis of serosurveillance and evidence of past exposure.
- **Whole organism** — [culture and Gram stain](diagnostics/culture-and-gram-stain.md), [microscopy](diagnostics/microscopy.md). Direct growth or visualization; still the reference standard for many bacteria and parasites.
- **Molecular fingerprint** — [MALDI-TOF mass spectrometry](diagnostics/maldi-tof.md), [electron microscopy](diagnostics/electron-microscopy.md). Identifies an organism from its protein spectrum or its ultrastructure.

## The diagnostic window

The figure above is the single most useful idea in the field: **timing determines which test is positive.**
Nucleic acid and antigen appear first, tracking active infection, then fade.
Antibodies (IgM, then IgG) appear only after the immune system responds, so a serological test taken too early is falsely negative, while a PCR taken weeks after recovery can be falsely negative even though the person was truly infected.
This is why case definitions often pair a **molecular** confirmatory test for acute infection with **serology** for past exposure.

## Trade-offs: no assay wins on every axis

Choosing a diagnostic is an exercise in constrained optimization across sensitivity, specificity, speed, cost, and the infrastructure and training a method demands.

![Diagnostic methods plotted by time-to-result against analytical sensitivity, with bubble size showing cost and complexity: rapid tests are fast but insensitive, PCR is sensitive but slower and costlier, and culture and microscopy occupy their own niches.](assets/figures/diagnostics-tradeoffs.svg)

| Method | Detects | Sensitivity | Specificity | Turnaround | Cost / complexity | Key resource constraint |
| --- | --- | --- | --- | --- | --- | --- |
| [qPCR](diagnostics/qpcr.md) | nucleic acid | very high | very high | hours | high (thermocycler, cold chain) | reagents, trained staff, power |
| [LAMP](diagnostics/lamp.md) | nucleic acid | high | high | ~30–60 min | low–moderate | primer design; contamination control |
| [ELISA](diagnostics/elisa.md) | antigen / antibody | moderate–high | high | hours | moderate (plate reader) | antibody reagents, batch controls |
| [Rapid antigen test](diagnostics/rapid-antigen-tests.md) | antigen | low–moderate | high | ~15 min | very low | none — point-of-care |
| [Culture & Gram stain](diagnostics/culture-and-gram-stain.md) | live organism | high | high | 1–5 days | moderate | viable sample, biosafety, skilled tech |
| [Microscopy](diagnostics/microscopy.md) | organism / cells | variable | moderate–high | minutes | low | expert microscopist |
| [SDS-PAGE / Western](diagnostics/sds-page-western-blot.md) | specific protein | moderate | very high | hours–1 day | moderate | antibodies, technical skill |
| [MALDI-TOF](diagnostics/maldi-tof.md) | protein fingerprint | high | high | minutes (post-culture) | high capital, low per-test | ~US$150–250k instrument; a culture first |
| [Electron microscopy](diagnostics/electron-microscopy.md) | ultrastructure | low | moderate | hours | very high | ~US$0.5–2M instrument, expert operator |

Two lessons recur across the pages that follow.

- **Sensitivity and specificity are not fixed properties of an assay** — they depend on the sampling timing (the diagnostic window), the specimen quality, and the prevalence in the tested population, which drives the [positive predictive value](math/diagnostic-testing.md).
- **The best test on paper is often the wrong test in practice.** A PCR assay with 99% sensitivity is useless without cold chain, stable power, reagent supply, and trained technologists; a rapid test with 60% sensitivity that returns a result in fifteen minutes at the bedside may avert far more transmission.

## From diagnosis to surveillance

Individual tests aggregate into **surveillance** — the systematic monitoring that tells us where and how fast a pathogen is spreading.

- **Screening vs confirmatory testing** — cheap, fast, sensitive tests screen broadly; specific tests confirm positives, a two-tier strategy that manages the [false-positive burden at low prevalence](math/diagnostic-testing.md).
- **Pooled testing** — combining specimens multiplies throughput when prevalence is low, at some cost in sensitivity.
- **Wastewater surveillance** — [qPCR](diagnostics/qpcr.md) or sequencing of sewage tracks community transmission without testing individuals.
- **Genomic surveillance** — sequencing positives reveals variants and reconstructs transmission (see [the molecular clock](math/molecular-clock.md) and [phylodynamics](math/molecular-clock.md)).

## Methods

- [qPCR and RT-qPCR](diagnostics/qpcr.md) — amplification, Ct values, standard curves, and efficiency
- [LAMP: Isothermal Amplification](diagnostics/lamp.md) — point-of-care molecular testing without a thermocycler
- [ELISA](diagnostics/elisa.md) — plate immunoassays and the four-parameter logistic curve
- [Rapid Antigen & Lateral-Flow Tests](diagnostics/rapid-antigen-tests.md) — bedside antigen detection and its prevalence dependence
- [Culture and the Gram Stain](diagnostics/culture-and-gram-stain.md) — growing and classifying bacteria, and susceptibility testing
- [Diagnostic Microscopy and Parasitology](diagnostics/microscopy.md) — blood films, stains, and crystal analysis
- [SDS-PAGE and Western Blotting](diagnostics/sds-page-western-blot.md) — separating proteins and confirmatory serology
- [MALDI-TOF Mass Spectrometry](diagnostics/maldi-tof.md) — identifying microbes by their protein fingerprint
- [Electron Microscopy](diagnostics/electron-microscopy.md) — visualizing virions and ultrastructure

## Related

- [Detection Probability: Viral Kinetics and Assay Thresholds](epidemiology/detection-probability.md) — the quantitative link between viral load, the limit of detection, and time-varying sensitivity
- [Diagnostic Testing and Screening](math/diagnostic-testing.md) — sensitivity, specificity, PPV, and ROC
- [Data Ingestion & APIs](programming/data-ingestion-and-apis.md) — pulling sequence data from GenBank and GISAID
- [The Molecular Clock and Phylodynamics](math/molecular-clock.md)
- [Epidemiology](epidemiology.md)
