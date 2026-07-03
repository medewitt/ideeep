---
title: "SDS-PAGE and Western Blotting"
---

# SDS-PAGE and Western Blotting

SDS-PAGE separates proteins by **size**, and the Western blot then asks whether a **specific** protein is present using an antibody probe.
Together they answer a question no amplification or growth-based method can: *is this exact protein — this antigen, this antibody — here?* In diagnostics that makes the Western blot a **confirmatory** test, brought in to adjudicate the positives from more sensitive but less specific screens.

## SDS-PAGE: separating proteins by size

**PAGE** is polyacrylamide gel electrophoresis: proteins are driven through a gel mesh by an electric field, and smaller proteins move faster.
On its own, protein charge and shape would confound the separation, so **SDS** (sodium dodecyl sulfate), a detergent, is added.
SDS unfolds proteins and coats them with uniform negative charge, so that migration depends on **size alone**.

Run alongside a ladder of known molecular weights, a sample resolves into bands, each band a protein of a particular size.
Staining the gel (e.g. Coomassie) reveals the whole protein complement; but to identify a *specific* protein among the hundreds present, you need the blot.

## Western blotting: probing for a specific protein

1. **Transfer** — the separated proteins are moved out of the gel onto a membrane, preserving their positions.
2. **Block** — the membrane is flooded with irrelevant protein so antibodies bind only their true target.
3. **Probe** — a **primary antibody** binds the protein of interest; an enzyme- or fluorophore-labeled **secondary antibody** then binds the primary and generates a signal.
4. **Detect** — a band appears at the target protein's molecular weight.

Because the readout is a band *at a specific size* recognized by a *specific antibody*, the Western blot is extremely specific — two independent constraints (size and antibody recognition) must agree.

## Confirmatory serology

That specificity is why Western blots became classic **confirmatory** serological tests.

- **HIV (historically).** A sensitive ELISA screened for anti-HIV antibodies; reactive samples were confirmed by a Western blot showing bands against several distinct viral proteins, guarding against ELISA false positives.
  (Modern algorithms have largely replaced this with antigen/antibody combination assays and molecular confirmation, but the logic is the same.)
- **Lyme disease.** The recommended approach has long been a **two-tier** strategy: a sensitive ELISA first, confirmed by a Western blot (or a second EIA) scored for specific bands.

## Trade-offs & resource considerations

- **Sensitivity & specificity.** Modest sensitivity but **very high specificity** — its entire role is to confirm, not to screen.
  Interpreting which and how many bands count as positive requires validated criteria, and subjective band-reading is a recognized source of error.
- **Cost.** Moderate: gels, transfer apparatus, and antibodies, with meaningful reagent costs per run.
- **Training & infrastructure.** Technically demanding and multi-step; results depend on careful transfer, blocking, and antibody handling, so it is a **skilled-technologist** method, not a point-of-care one.
- **Turnaround.** Hours to a day, in batches.
- **Where it fits.** As the specific back-end of a two-tier algorithm, paired with a sensitive [ELISA](elisa.md) front-end — the classic screen-then-confirm design that controls false positives at low prevalence.

## Why it matters

The screen-then-confirm pattern that Western blots anchor is a template that runs throughout diagnostics and surveillance: pair a **sensitive** first test to catch everything with a **specific** second test to weed out false positives.
Understanding SDS-PAGE and blotting also underpins much of the molecular biology behind vaccine and therapeutic development, where confirming that a protein is expressed at the right size is a daily task.

## Related

- [ELISA](elisa.md) — the sensitive screen a Western blot confirms
- [MALDI-TOF Mass Spectrometry](maldi-tof.md) — a faster protein-based identification
- [Diagnostic Testing and Screening](../math/diagnostic-testing.md) — screening vs confirmatory strategies
- [Diagnostics & Surveillance](../diagnostics.md)
