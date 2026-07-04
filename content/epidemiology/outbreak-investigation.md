---
title: "Outbreak Investigation"
description: "The standard field steps for investigating an outbreak, from case definition and line list to the epidemic curve, hypothesis testing, and control."
---

# Outbreak Investigation

An outbreak investigation is a structured piece of detective work carried out against the clock.
The goal is to find out what is making people sick, who is at risk, and how to stop it, using a sequence of steps that turns scattered reports into a testable explanation.
The steps are conventional and roughly ordered, but in a live investigation they overlap and loop back as new cases and new data arrive.

![Two epidemic curves side by side: a point-source outbreak with a single tight peak roughly one incubation period wide, and a propagated outbreak with successive peaks about one serial interval apart.](../assets/figures/outbreak-investigation.svg)

## The standard steps

Field investigations follow a well-worn checklist, associated with the training of Epidemic Intelligence Service officers.
The order below is a guide, not a straitjacket; control measures in particular should start as soon as there is enough evidence to act.

1. **Verify the diagnosis and confirm an outbreak exists.** Check that the reported cases are real and correctly diagnosed, then compare the observed count against what is normally expected for this place and season.
   An outbreak is an excess over that baseline; two cases of a rare disease can be an outbreak, while a seasonal rise in a common one may not be.
2. **Establish a case definition.** Write down explicit criteria for who counts as a case, usually graded into **confirmed** (laboratory-verified), **probable** (typical illness with an epidemiologic link), and **suspected** (compatible symptoms only).
   A good case definition combines clinical features with restrictions on person, place, and time.
3. **Find cases and build a line list.** Search actively for cases beyond those first reported, and record each one as a row in a **line list** with columns for identifiers, symptoms, onset date, and exposures.
4. **Describe the outbreak by person, place, and time.** This descriptive epidemiology summarizes who is affected, where, and when, and it is where the epidemic curve is drawn.
5. **Generate hypotheses.** The descriptive picture suggests candidate exposures or sources worth testing.
6. **Test the hypotheses with an analytic study.** Compare exposure between the sick and the well (see below).
7. **Implement control measures and communicate.** Remove the source, interrupt transmission, and protect those at risk, then write up and share what was found.

## The case definition and the line list

The case definition is the spine of the investigation because every later count depends on it.
Make it too narrow and real cases are missed; make it too broad and unrelated illness dilutes any signal.
Grading cases into confirmed, probable, and suspected lets the investigation move before laboratory results are complete while keeping the categories auditable.

The line list is simply a table with one row per case.
It is the raw material for every summary that follows: tally the onset-date column and you have an epidemic curve; cross-tabulate exposure against illness and you have the beginnings of an analytic study.

## Reading the epidemic curve

An **epidemic curve** (epi curve) is a histogram of case counts by time of onset.
Its shape carries information about how the outbreak is being driven.

- A **point-source** outbreak comes from a single, brief common exposure — a contaminated meal at one event.
  Cases rise and fall in one tight wave whose width reflects the spread of the **incubation period**, so the whole curve spans roughly the range of incubation times.
- A **continuous common-source** outbreak comes from an exposure that persists — a water supply contaminated for weeks.
  Cases stay elevated in a plateau for as long as the source is active, then fall once it is removed.
- A **propagated** (person-to-person) outbreak spreads from case to case.
  It shows successive peaks spaced about one **serial interval** apart, each larger than the last while susceptible people remain, until the supply of susceptibles runs down.

The figure contrasts the tight single peak of a point source with the rolling generations of a propagated outbreak.
Reading these shapes is a first pass at the mechanism before any analytic study is run.

## From the curve back to the exposure

For a point-source outbreak the epi curve doubles as a clock pointing back to the exposure.
Onset happens one incubation period after infection, so the peak of the curve sits about one **median incubation period** after the moment of common exposure:

$$\hat{t}_{\text{exposure}} \approx t_{\text{peak onset}} - \text{median incubation period}.$$

Working backward from the earliest and latest onsets with the shortest and longest plausible incubation periods brackets a likely **exposure window**, which narrows the search for the source.
The incubation period is the disease clock covered in [Epidemiological intervals](epidemiological-intervals.md); the reporting delays that blur the right-hand tail of the curve are covered in [Delay distributions and censoring](delay-distributions-censoring.md).

## Testing hypotheses: cohort or case-control

Descriptive epidemiology suggests a source; an analytic study tests it by comparing exposure between the ill and the well.
The choice of design depends on the setting.

- A **retrospective cohort study** fits a closed, enumerable population — everyone at a wedding.
  You interview all attendees, split them by each exposure, and compare attack rates to get a **relative risk**.
- A **case-control study** fits an open or large population where the denominator is unknown — cases scattered across a city.
  You compare the exposure history of cases against a sample of well controls and estimate an **odds ratio**.

Whichever design is used, the exposure with the strongest, most consistent association and a plausible biological story becomes the working explanation, which then guides control.

## A worked example

A small gathering produces seven cases with the following onset days, measured from the day of the event (day 0):

| Case | Onset day |
| --- | --- |
| 1 | 2 |
| 2 | 3 |
| 3 | 3 |
| 4 | 4 |
| 5 | 4 |
| 6 | 4 |
| 7 | 5 |

Tallying the onset column gives the epidemic curve: 1 case on day 2, 2 on day 3, 3 on day 4, and 1 on day 5.
The curve is a single tight peak on day 4, the classic point-source shape.
If the pathogen has a median incubation period of 3 days, the peak of onsets on day 4 points back to a common exposure around day 1, consistent with the gathering itself.

## In code

We build the epidemic curve from a line list and estimate the exposure day.

### R

```r
line_list <- data.frame(
  case = 1:7,
  onset_day = c(2, 3, 3, 4, 4, 4, 5)
)

epi_curve <- as.data.frame(table(onset_day = line_list$onset_day))
peak_day <- as.integer(
  as.character(epi_curve$onset_day[which.max(epi_curve$Freq)])
)

median_incubation <- 3
exposure_day <- peak_day - median_incubation

print(epi_curve)
cat("peak onset day:", peak_day,
    "estimated exposure day:", exposure_day, "\n")
```

### Python

We use [Polars](https://pola.rs) to tally onsets into an epidemic curve.

```python
import polars as pl

line_list = pl.DataFrame(
    {"case": [1, 2, 3, 4, 5, 6, 7],
     "onset_day": [2, 3, 3, 4, 4, 4, 5]}
)

epi_curve = (
    line_list.group_by("onset_day")
    .agg(pl.len().alias("cases"))
    .sort("onset_day")
)

peak_day = epi_curve.filter(
    pl.col("cases") == pl.col("cases").max()
)["onset_day"][0]
median_incubation = 3
exposure_day = peak_day - median_incubation

print(epi_curve)
print(f"peak onset day: {peak_day}")
print(f"estimated exposure day: {exposure_day}")
```

<!-- python-output:auto -->
```text
shape: (4, 2)
┌───────────┬───────┐
│ onset_day ┆ cases │
│ ---       ┆ ---   │
│ i64       ┆ u32   │
╞═══════════╪═══════╡
│ 2         ┆ 1     │
│ 3         ┆ 2     │
│ 4         ┆ 3     │
│ 5         ┆ 1     │
└───────────┴───────┘
peak onset day: 4
estimated exposure day: 1
```
<!-- /python-output:auto -->

### Julia

```julia
using DataFrames, StatsBase

line_list = DataFrame(case = 1:7, onset_day = [2, 3, 3, 4, 4, 4, 5])

counts = countmap(line_list.onset_day)
epi_curve = sort(DataFrame(onset_day = collect(keys(counts)),
                           cases = collect(values(counts))), :onset_day)

peak_day = epi_curve.onset_day[argmax(epi_curve.cases)]
median_incubation = 3
exposure_day = peak_day - median_incubation

println(epi_curve)
println("peak onset day: $peak_day, exposure day: $exposure_day")
```

## Why it matters

Outbreak investigation is where epidemiological theory meets a room full of sick people and a deadline.
The case definition decides what gets counted, the line list holds the evidence, and the epidemic curve turns a column of onset dates into a statement about mechanism and timing.
The same intervals that govern transmission dynamics — incubation and serial intervals — are the tools that let an investigator read an outbreak's shape and point back to its source, which is what makes control possible.
The companion concept page on surveillance systems covers how the cases that seed an investigation are detected in the first place.

## Related

- [Epidemiological intervals](epidemiological-intervals.md)
- [Delay distributions and censoring](delay-distributions-censoring.md)
- [The SIR Model](../math/sir.md)
- [The Effective Reproduction Number and Forecasting](../math/reproduction-number-rt.md)
- [Epidemiology](../epidemiology.md)
