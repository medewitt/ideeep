---
title: "MALDI-TOF Mass Spectrometry"
---

# MALDI-TOF Mass Spectrometry

MALDI-TOF mass spectrometry identifies a microbe by reading its **protein fingerprint**.
From a single colony it produces, in minutes, a spectrum of the organism's most abundant proteins that is characteristic enough to name the species — replacing panels of biochemical tests that used to take a day or more.
Over the past fifteen years it has become the default identification method in clinical microbiology laboratories.

![A MALDI-TOF mass spectrum: peaks at characteristic mass-to-charge ratios form a species-specific fingerprint of abundant cellular proteins.](../assets/figures/maldi-tof-spectrum.svg)

## How it works

The acronym unpacks the method.

- **MALDI** — Matrix-Assisted Laser Desorption/Ionization.
  A speck of the organism is mixed with a chemical **matrix** on a target plate.
  A laser pulse vaporizes and **ionizes** the mixture, lofting intact protein ions into the instrument without shattering them.
- **TOF** — Time-Of-Flight.
  The ions are accelerated by an electric field and fly down a tube to a detector.
  Lighter ions arrive sooner, so **flight time encodes mass-to-charge ratio (m/z)**.

The result is a spectrum of peaks across roughly 2,000–20,000 daltons, dominated by abundant, conserved proteins (largely ribosomal).
Because those proteins differ subtly between species, the **pattern of peaks is a fingerprint**.

## Identification and reference libraries

Identification is pattern-matching, not sequencing.
The measured spectrum is compared against a **reference library** of spectra from known organisms, and the best match — with a confidence score — is reported.
This makes MALDI-TOF only as good as its database: common bacteria and yeasts are identified superbly, while organisms poorly represented in the library (some rare or newly described species) may fail to match.

Beyond species ID, the same technology is expanding into **antimicrobial-resistance** detection (spotting resistance-associated peaks or measuring whether an organism degrades a drug) and strain typing, and the broader field of **clinical proteomics** applies mass spectrometry to host proteins as biomarkers.

## Trade-offs & resource considerations

- **Sensitivity & specificity.** Excellent species-level accuracy for organisms in the reference library, from a tiny amount of material.
  Its main blind spots are closely related species with near-identical spectra and organisms absent from the database.
- **Cost.** The defining trade-off: a **high capital cost** (an instrument runs roughly US$150,000–250,000) but an extremely **low per-test cost** — often cents in matrix and consumables.
  This economics rewards **high-volume** central laboratories and is hard to justify for low-throughput or field settings.
- **Training & infrastructure.** Needs a stable lab environment and trained staff for spotting and maintenance, plus, in most workflows, a **pure culture first** — so it inherits [culture](culture-and-gram-stain.md)'s turnaround and its inability to identify unculturable organisms.
- **Turnaround.** Minutes **once a colony is available** — dramatically faster than the biochemical panels it replaced, but gated by the upstream growth step.

## Why it matters

MALDI-TOF collapsed microbial identification from a day of biochemical tests to a few minutes of mass spectrometry, changing the tempo of clinical microbiology and, with it, how quickly patients get the right antibiotic.
For surveillance it enables rapid, cheap, high-throughput speciation of large isolate collections — the raw material for tracking which organisms, and increasingly which resistant strains, are circulating.

## Related

- [Culture and the Gram Stain](culture-and-gram-stain.md) — the upstream isolate MALDI-TOF identifies
- [SDS-PAGE and Western Blotting](sds-page-western-blot.md) — another protein-based method
- [Electron Microscopy](electron-microscopy.md)
- [Diagnostics & Surveillance](../diagnostics.md)
