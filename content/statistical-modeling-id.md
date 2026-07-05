---
title: "Statistical Modeling of Infectious Disease Dynamics"
description: "A graduate course on the statistical machinery of disease modeling: likelihood, Bayesian workflow, hierarchical structure, and fitting mechanistic transmission models to data."
author: Michael DeWitt
date: 2026-07-04
---

This course teaches the statistical machinery behind infectious disease
modeling: likelihood, the Bayesian workflow, hierarchical structure, and
fitting mechanistic transmission models to data. Graduate students doing IDEEE
research in Biology or Molecular Medicine will learn to write a transmission
model as a statistical model and fit it in Stan. The course formalizes the
workflow that many of the site's reference pages already assume.

The course syllabus is shown below.

> **Draft syllabus.** This is a scaffold for the concentration. Dates, meeting
> times, and specific assignments will be finalized before the semester begins.

---

# Course title and instructors

**Title:** Statistical Modeling of Infectious Disease Dynamics  
**Course Number:** BIO 6xx (proposed; with an undergraduate cross-list where
noted)  
**Semester:** TBD  
**Credit Hours:** 3  
**Meeting Time:** TBD  
**Prerequisites:** [Mathematical Biology](bio301-math-bio.md), Biostatistics
(BIO 380), and programming experience

**Course Director:** Michael E. DeWitt, MS  
**Email:** medewitt@wakehealth.edu or dewime23@wfu.edu  

# Course description

Fitting a transmission model to data is a statistical problem. This course
treats mechanistic models of infectious disease as statistical models built
from an observation process and a latent transmission process. Students learn
likelihood and maximum likelihood estimation, Bayesian inference and Markov
chain Monte Carlo, and hierarchical (partial-pooling) models for multi-site or
multi-strain data. We work through the full Bayesian workflow end to end: prior
predictive checks, fitting in Stan, convergence diagnostics, and posterior
predictive checks. We also cover model calibration, identifiability, sensitivity
analysis, and scoring for model comparison. Students estimate key quantities
such as the basic reproduction number and the generation interval using the
next-generation approach and propagate the resulting uncertainty.

# Learning outcomes

Upon successful completion of this course, students will be able to:

- Write down and fit a mechanistic transmission model as a statistical model
  with an observation component and a process component
- Carry out a full Bayesian workflow: prior predictive checks, fitting in Stan,
  convergence diagnostics, and posterior predictive checks
- Build hierarchical and partial-pooling models for multi-site or multi-strain
  data
- Estimate key quantities such as the basic reproduction number and the
  generation interval using the next-generation approach and propagate
  uncertainty
- Assess identifiability and calibrate models against observed data
- Compare models using proper scoring rules and sensitivity analysis

# Textbook and other resources

There is no single required textbook. Recommended references and readings
include:

- Gelman A, et al. *Bayesian Data Analysis*, 3rd ed. CRC Press, 2013.
- McElreath R. *Statistical Rethinking*, 2nd ed. CRC Press, 2020.
- Stan Development Team. *Stan User's Guide*. https://mc-stan.org/docs/
- Bjørnstad ON. *Epidemics: Models and Data in R*. Springer, 2018.

Additional primary literature will be assigned throughout the semester.

## Site resources

This course draws on the following IDEEE reference pages:

- [Maximum likelihood](math/maximum-likelihood.md)
- [Bayesian inference](math/bayesian-inference.md)
- [Markov chains](math/markov-chains.md)
- [MCMC](math/mcmc.md)
- [Hierarchical models](math/hierarchical-models.md)
- [Model calibration](math/model-calibration.md)
- [Sensitivity analysis](math/sensitivity-analysis.md)
- [Proper scoring rules](math/proper-scoring-rules.md)
- [The next-generation matrix](math/next-generation-matrix.md)
- [The reproduction number and Rt](math/reproduction-number-rt.md)
- [SEIR models](math/seir-models.md)
- [Epidemiological intervals](epidemiology/epidemiological-intervals.md)
- [Delay distributions and censoring](epidemiology/delay-distributions-censoring.md)
- [The Euler–Lotka equation and the r–R₀
  relationship](epidemiology/euler-lotka.md) — estimating R₀ from a growth rate
  and the generation interval
- [Multi-scale (nested) models](epidemiology/nested-models.md) — linking
  within-host and between-host processes in a fitted model
- [Critical transitions and early-warning
  signals](math/critical-transitions.md) — detecting approaching thresholds from
  fluctuations in time series

Planned reference pages on prior predictive checks, posterior predictive
checks, and identifiability will be added and assigned as they come online.

# Course structure and schedule

This course meets over 15 weeks and combines lecture with hands-on model
fitting in Stan. The schedule below is a draft outline of topics.

| Week | Topic |
|------|-------|
| 1 | Transmission models as statistical models |
| 2 | Likelihood and maximum likelihood estimation |
| 3 | The observation process and count data |
| 4 | Bayesian inference and prior specification |
| 5 | Markov chains and MCMC |
| 6 | Fitting models in Stan and convergence diagnostics |
| 7 | Prior predictive checks |
| 8 | Posterior predictive checks and model criticism |
| 9 | Hierarchical and partial-pooling models |
| 10 | Multi-site and multi-strain data |
| 11 | Model calibration and identifiability |
| 12 | Estimating R0 and the generation interval |
| 13 | Sensitivity analysis and uncertainty propagation |
| 14 | Model comparison and proper scoring rules |
| 15 | Student project presentations and wrap-up |

Note: Specific dates will be provided at the beginning of the semester. Topics
may be adjusted based on class progress and student interests.

# Grades and assignments

| Activity | Weight |
|----------|--------|
| Participation and discussion | 15% |
| Problem sets (Stan-based) | 35% |
| Midterm modeling exercise | 20% |
| Final project | 30% |

**Final project:** Students will fit a mechanistic transmission model to a real
data set, carrying out the full Bayesian workflow and reporting estimates with
uncertainty in a written report and presentation.

:::{course-policies.md}:::

:::{university-policies.md}:::

:::{syllabus-change-notice.md}:::
