---
title: "Epidemiology"
---

# Epidemiology

The concepts that turn a stream of case reports into an understanding of how a pathogen moves through a population.
This collection starts with the **time intervals** that structure transmission — the delays between infection, symptoms, and onward spread — and the modern methods for estimating them from imperfect surveillance data.
Each page pairs the biology and notation with worked examples and runnable code in **R**, **Python**, and **Julia**.

## Epidemiological delays and intervals

- [Epidemiological Intervals and Delays](epidemiology/epidemiological-intervals.md) — incubation, latent, and infectious periods; the serial and generation intervals; and how they shape $R_t$
- [Fitting Delay Distributions: Truncation and Censoring](epidemiology/delay-distributions-censoring.md) — estimating delays from real-time data with interval censoring and right truncation

## Related quantitative methods

These pages in the [Quantitative Methods](math.md) collection develop the machinery the epidemiology pages build on.

- [Compartmental Models (SIR)](math/sir.md) — the SIR model and $R_0$
- [The Effective Reproduction Number and Forecasting](math/reproduction-number-rt.md)
- [Survival Analysis](math/survival-analysis.md) — hazards and censoring
- [Maximum Likelihood Estimation](math/maximum-likelihood.md)
- [Fitting Dynamic Models to Data](math/model-calibration.md)
