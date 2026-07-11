---
title: "Rapid Antigen & Lateral-Flow Tests"
---

# Rapid Antigen & Lateral-Flow Tests

A rapid antigen test (RAT) is the paper strip that made at-home testing a household routine.
It detects a pathogen **protein** (antigen) directly from a swab or saliva, with no instrument, no power, and a result in about fifteen minutes.
The underlying format — the **lateral-flow immunoassay** — is the same one used by pregnancy tests, and its speed and simplicity come with a defining limitation: it is far less sensitive than a molecular test.

![Left: a rapid test needs a relatively high pathogen load to cross its detection threshold, so it turns positive only around peak load near symptom onset and misses the early and late infection that a lower-threshold PCR still catches. Right: the lateral-flow strip — sample wicks past a conjugate pad, a test line, and a control line, and the two-line, one-line, and no-control readouts mean positive, negative, and invalid.](../assets/figures/rapid-antigen-tests.svg "fig:rat")

## How the strip works

The specimen is mixed with a buffer and dripped onto a pad, and capillary action wicks it along a nitrocellulose strip past three zones.

1. A **conjugate pad** holds antibodies against the target antigen, tagged with colored gold nanoparticles or latex.
   If the antigen is present, it binds these labeled antibodies and is carried along.
2. The **test line** is coated with a second, immobilized antibody against the antigen.
   Antigen sandwiched between the mobile and fixed antibodies concentrates the colored label into a visible line.
3. The **control line** captures excess labeled antibody regardless of antigen, confirming the test ran correctly.

Two lines means positive; one line (control only) means negative; no control line means the test is invalid.

## Sensitivity tracks pathogen load

The single most important fact about rapid antigen tests is that their sensitivity depends on **how much antigen is present**, which depends on **when** in the infection you test.
A RAT needs a relatively high antigen concentration to cross its detection threshold, so it is most likely to be positive during the days of peak load — often around symptom onset — and misses early and late infection where a [PCR](qpcr.md) would still detect nucleic acid ([@fig:rat]).

The practical response is **serial testing**: repeating a rapid test every day or two dramatically raises the chance of catching the infection during its detectable window, partly compensating for the lower single-test sensitivity.

## Positive predictive value and prevalence

Rapid tests are usually built for **high specificity**, so a positive is generally trustworthy.
But the value of a positive still depends on how common the disease is.
The [positive predictive value](../math/diagnostic-testing.md),

$$\text{PPV} = \frac{\text{sens}\cdot p}{\text{sens}\cdot p + (1-\text{spec})(1-p)},$$

collapses when prevalence $p$ is very low — even a 99%-specific test throws mostly false positives when almost no one is infected — which is the core argument for **confirming** unexpected positives and for interpreting screening results in light of the tested population.

## Trade-offs & resource considerations

- **Sensitivity & specificity.** Low-to-moderate sensitivity (worst near the edges of the [diagnostic window](../diagnostics.md)), but high specificity.
  Sensitivity is best expressed *conditional on viral load*, not as a single headline number.
- **Cost.** Very low per test, no instrument — the least resource-intensive option available.
- **Training & infrastructure.** Essentially none; designed for lay users and the bedside, with no cold chain for many formats.
- **Turnaround.** ~15 minutes, at the point of care — its entire reason for existing.
- **Where it fits.** Rapid tests trade analytical sensitivity for **access and speed**.
  For controlling transmission, a same-minute answer that someone acts on can outperform a more sensitive result that arrives after they have already spread the pathogen.

## Why it matters

Rapid antigen tests reframed testing from a laboratory service into a personal, repeatable behavior.
Understanding *why* they miss early infection, *why* serial testing rescues much of that sensitivity, and *why* a positive's meaning depends on prevalence is essential to using them well — and to reading the surveillance signals they generate.

## Related

- [qPCR and RT-qPCR](qpcr.md)
- [ELISA](elisa.md)
- [Diagnostic Testing and Screening](../math/diagnostic-testing.md) — sensitivity, specificity, PPV
- [Diagnostics & Surveillance](../diagnostics.md)
