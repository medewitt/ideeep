---
title: "Surveillance Systems"
description: "How public-health surveillance detects disease, why only a fraction of infections are ever counted, and how reporting delays distort the most recent data."
---

# Surveillance Systems

Public-health surveillance is the ongoing, systematic collection, analysis, and interpretation of health data, tied to action.
It is the sensory apparatus of public health: without it, an outbreak is invisible until it is large, and a control program cannot tell whether it is working.
Every case count you read comes out of a surveillance system, and understanding that system's design tells you what the count can and cannot mean.

![The surveillance pyramid: a wide base of all infections narrows through symptomatic illness, care-seeking, testing, and reporting, so the reported cases at the tip are a small fraction of the infections underneath.](../assets/figures/surveillance-systems.svg)

## What surveillance is for

Surveillance serves several ends at once: detecting outbreaks early, tracking trends over time, estimating the burden of disease, identifying who is at risk, and evaluating whether interventions work.
The unifying idea is that the data are collected in order to be acted on, not archived.
A system that reports beautifully but too late, or that no one uses to make decisions, has failed regardless of its data quality.

## Passive versus active surveillance

The core distinction is who does the work of reporting.

- **Passive surveillance** waits for clinicians, laboratories, and hospitals to report cases as part of routine practice, usually for a list of notifiable conditions.
  It is cheap and covers a wide area, which makes it the backbone of most national systems, but it under-reports because it depends on others remembering to report.
- **Active surveillance** has public-health staff reach out to reporting sites to solicit cases, checking records and prompting for reports.
  It is more complete and timely but costly, so it is reserved for limited periods or high-stakes settings — during an outbreak, or to confirm elimination.

## Sentinel and syndromic systems

Two designs trade completeness for speed or feasibility.

- **Sentinel surveillance** monitors a chosen subset of reporting sites — a network of clinics that report every case of influenza-like illness — rather than trying to capture every case everywhere.
  A well-chosen sentinel network gives a reliable read on trends at a fraction of the cost of universal reporting.
- **Syndromic surveillance** tracks pre-diagnostic signals such as symptom patterns, emergency-department chief complaints, or over-the-counter medication sales.
  It trades diagnostic certainty for timeliness, flagging an unusual rise days before laboratory confirmation would.

## The case definition as the ruler

As in an outbreak investigation, the **case definition** sets what the system counts.
It is the ruler against which every trend is measured, so a mid-stream change to the definition can create an apparent jump or drop in cases that reflects the ruler, not the disease.
A sensitive definition catches most true cases at the cost of false positives; a specific one is surer but misses milder or atypical illness.
Consistency over time matters as much as the choice itself, because surveillance is about detecting change.

## System attributes

The CDC evaluation guidelines judge a surveillance system on several attributes, which usually trade off against one another.

- **Sensitivity** is the proportion of true cases the system detects.
- **Specificity** and **positive predictive value** concern false positives: specificity is the proportion of non-cases correctly not flagged, while the positive predictive value is the proportion of reported cases that are genuine.
- **Timeliness** is the delay between an event and its availability for action.
- **Representativeness** is whether the cases captured reflect the true distribution across people, place, and time.
- **Simplicity**, **flexibility**, and **acceptability** govern whether the system can be run, adapted, and sustained by the people who feed it.

No system maximizes all of these; a fast syndromic system sacrifices specificity, while a confirmed-case system sacrifices timeliness.

## The surveillance pyramid and under-ascertainment

Only a fraction of infections ever become reported cases, and the **surveillance pyramid** shows why.
Start from all infections at the wide base, then narrow at each step: only some infections become symptomatic, only some of the symptomatic seek care, only some of those are tested, and only some positive tests are reported.
Each step multiplies by a fraction less than one, so the reported count at the tip is a small and biased sample of the infections underneath.

This attrition, called **under-ascertainment**, means a reported count must be multiplied back up to approximate true infections.
If the fraction surviving each step is $p_1, p_2, \dots, p_k$, then

$$\text{reported} = \text{infections} \times \prod_{i=1}^{k} p_i,
\qquad
\widehat{\text{infections}} = \frac{\text{reported}}{\prod_{i=1}^{k} p_i}.$$

The reciprocal $1 / \prod_i p_i$ is the **multiplier** that scales reported cases up to infections.
Because the fractions themselves are uncertain and change with testing policy and health-seeking behavior, the multiplier is a moving target — which is why case counts are hard to compare across places and time.
Serological surveys, which sample antibodies directly, are one way to estimate the base of the pyramid independently.

## Reporting delays and the most recent data

The right-hand edge of any surveillance time series is a trap.
Because each case takes time to move from onset through testing to the reporting database, the most recent days always look artificially low: cases that have already occurred simply have not been reported yet.
Interpreting that dip as a real decline is a classic error.
Correcting for the delay to reconstruct what recent counts will become is **nowcasting**, covered in [Delay distributions and censoring](delay-distributions-censoring.md); the intervals that set these delays are covered in [Epidemiological intervals](epidemiological-intervals.md).

## A worked example

Suppose that for a given pathogen 60% of infections become symptomatic, 60% of the symptomatic seek care, 60% of care-seekers are tested, and 60% of positive tests are reported.
The fraction of infections that reach the top of the pyramid is $0.6^4 \approx 0.13$, so only about 13% of infections are ever counted.
Given 1,000 reported cases, the estimated true infection count is $1000 / 0.13 \approx 7{,}716$, a multiplier of about 7.7.
Small per-step fractions compound quickly: four steps at 60% each leave under a seventh of infections visible.

## In code

We multiply through the pyramid to get the multiplier and the implied infections.

### R

```r
fractions <- c(symptomatic = 0.60, seek_care = 0.60,
               tested = 0.60, reported = 0.60)

detected_fraction <- prod(fractions)
multiplier <- 1 / detected_fraction

reported <- 1000
estimated_infections <- reported * multiplier

cat("detected fraction:", round(detected_fraction, 4), "\n")
cat("multiplier:", round(multiplier, 2), "\n")
cat("estimated infections:", round(estimated_infections), "\n")
```

### Python

We use [Polars](https://pola.rs) to hold the pyramid and take the running product.

```python
import polars as pl

pyramid = pl.DataFrame(
    {"level": ["symptomatic", "seek_care", "tested", "reported"],
     "fraction": [0.60, 0.60, 0.60, 0.60]}
)

detected_fraction = pyramid["fraction"].product()
multiplier = 1 / detected_fraction

reported = 1000
estimated_infections = reported * multiplier

print(pyramid)
print(f"detected fraction: {detected_fraction:.4f}")
print(f"multiplier: {multiplier:.2f}")
print(f"estimated infections: {round(estimated_infections)}")
```

<!-- python-output:auto -->
```text
shape: (4, 2)
┌─────────────┬──────────┐
│ level       ┆ fraction │
│ ---         ┆ ---      │
│ str         ┆ f64      │
╞═════════════╪══════════╡
│ symptomatic ┆ 0.6      │
│ seek_care   ┆ 0.6      │
│ tested      ┆ 0.6      │
│ reported    ┆ 0.6      │
└─────────────┴──────────┘
detected fraction: 0.1296
multiplier: 7.72
estimated infections: 7716
```
<!-- /python-output:auto -->

### Julia

```julia
fractions = (symptomatic = 0.60, seek_care = 0.60,
             tested = 0.60, reported = 0.60)

detected_fraction = prod(values(fractions))
multiplier = 1 / detected_fraction

reported = 1000
estimated_infections = reported * multiplier

println("detected fraction: ", round(detected_fraction, digits = 4))
println("multiplier: ", round(multiplier, digits = 2))
println("estimated infections: ", round(estimated_infections))
```

## Why it matters

Surveillance decides what counts as a case, how quickly it is seen, and how much of the true picture is captured, and every one of those choices shapes the numbers that drive policy.
The pyramid is a standing reminder that a reported count is the visible tip of a much larger, partly hidden burden, and that the multiplier turning one into the other is uncertain and shifting.
Reading a surveillance curve well means knowing which infections it misses and remembering that its most recent points are always incomplete.
The cases a system detects are also what seed the outbreak investigations that a companion concept page describes.

## Related

- [Diagnostic Testing and Screening](../math/diagnostic-testing.md)
- [Delay distributions and censoring](delay-distributions-censoring.md)
- [Epidemiological intervals](epidemiological-intervals.md)
- [Diagnostics & Surveillance](../diagnostics.md)
- [Epidemiology](../epidemiology.md)
