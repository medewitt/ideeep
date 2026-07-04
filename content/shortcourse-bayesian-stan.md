---
title: "Bayesian Modeling for Epidemiology with Stan"
description: "A one-week intensive, hands-on course in the applied Bayesian workflow with Stan, from priors to posterior predictive checks on a transmission model."
author: Michael DeWitt
date: 2026-07-04
---

This one-week course teaches the applied Bayesian workflow for epidemiologic
data using Stan.
It is aimed at people who need to fit hierarchical models to real data and want
a hands-on workflow rather than a theory course.
The course condenses the Bayesian half of the Statistical Modeling of
Infectious Disease Dynamics course and leans on the site's Stan pages.

> **Draft proposal.** This is an early sketch of a proposed short course. The
> course number, dates, fees, and daily schedule are placeholders and will be
> settled before the course is first offered.

---

# Overview

**IDE xxx (proposed)** is a non-credit, one-week intensive course in Bayesian
modeling with Stan.
Participants work through the full Bayesian workflow: setting priors, checking
them, writing and fitting a model, diagnosing the sampler, and checking the fit
against data.
Labs use cmdstanr in R or cmdstanpy in Python, and the week ends by applying the
workflow to a transmission model.

By the end of the course, participants will be able to:

- Follow the Bayesian workflow from prior to posterior check
- Set priors and run prior predictive checks
- Write and fit a model in Stan
- Read MCMC diagnostics and act on divergences
- Build hierarchical and partial-pooling models
- Run posterior predictive checks
- Apply the workflow to a simple transmission model

# Who should apply

The course is aimed at graduate students, postdocs, and researchers who fit
models to epidemiologic data.

**Prerequisites.** Working knowledge of R or Python is expected, along with a
basic grounding in regression. No prior Stan or Bayesian experience is assumed.

# Format and delivery

- **Duration.** 1 week (5 days), intensive.
- **Mode.** Hybrid. Attend in person or join online.
- **Daily hours.** A daily lecture followed by hands-on Stan labs, roughly a
  full working day.
- **Assessment.** No formal assessment.
- **Certificate.** Participants who attend receive a certificate of attendance.
- **Equipment.** Participants bring their own laptops with R (cmdstanr) or
  Python (cmdstanpy) and a working Stan toolchain. Setup instructions are sent
  before the course begins.

# Course content and topics

- The Bayesian workflow
- Priors and prior predictive checks
- Writing and fitting models in Stan
- MCMC diagnostics
- Hierarchical and partial-pooling models
- Posterior predictive checks
- Applying the workflow to a transmission model

# Reproducibility conventions

Labs follow the reproducibility habits used across IDEEEP work. Every stochastic
run is seeded (the course uses a shared seed so results match across machines),
and lab code passes the seed to Stan explicitly rather than relying on defaults.
When the sampler reports divergent transitions, the standard first step is to
raise `adapt_delta` (for example from the default of 0.8 toward 0.95 or higher)
and, where needed, to reparameterize the model. Participants record the seed,
`adapt_delta`, and other sampler settings alongside their results so runs can be
reproduced.

# Day-by-day timetable

| Day | Morning lecture | Afternoon lab (Stan) |
|-----|-----------------|-----------------------|
| 1 | The Bayesian workflow; priors | Prior predictive checks |
| 2 | Writing and fitting models in Stan | A first Stan model with cmdstanr / cmdstanpy |
| 3 | MCMC diagnostics | Reading diagnostics; setting `adapt_delta` |
| 4 | Hierarchical and partial-pooling models | Fitting a hierarchical model |
| 5 | Posterior predictive checks; transmission models | Fitting and checking a transmission model |

# Site resources

The course draws on material already published on this site. Participants can
read ahead or review afterward.

- [Bayesian inference](math/bayesian-inference.md)
- [MCMC](math/mcmc.md)
- [Markov chains](math/markov-chains.md)
- [Hierarchical models](math/hierarchical-models.md)
- [Model calibration](math/model-calibration.md)
- [Proper scoring rules](math/proper-scoring-rules.md)

Two further topics, prior predictive checks and posterior predictive checks,
are planned as site pages and will be linked here once published.

See [Programs](programs.md) for how this short course fits alongside the degree
tracks and other offerings.

# Fees and how to apply

**Fees.** @placeholder

**How to apply.** @placeholder

# AI and academic integrity

Large language models such as ChatGPT, Claude, and Gemini can support your
learning, and you are welcome to use them. If you do, cite the tools you used
and describe how you used them. These tools do not replace your own
understanding of the material, and you remain responsible for the accuracy of
your work and any citations. Using them without attribution is plagiarism.

# Proposal change notice

This is a draft proposal. Its content, structure, dates, and fees are subject to
change before the course is offered.
