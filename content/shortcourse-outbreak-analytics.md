---
title: "Outbreak Analytics Bootcamp"
description: "A one-week intensive, hands-on course in the real-time analytics used during an outbreak response, from epidemic curves to short-term forecasts."
author: Michael DeWitt
date: 2026-07-04
---

This one-week bootcamp gives practitioners the analytic skills that matter during
a response: reading an epidemic curve, estimating the time-varying reproduction
number, and producing a short forecast.
It is the applied, condensed sibling of the Outbreak Analytics and Modeling
course and is built around hands-on R labs.
Participants leave able to run a basic real-time analysis on their own data.

> **Draft proposal.** This is an early sketch of a proposed short course. The
> course number, dates, fees, and daily schedule are placeholders and will be
> settled before the course is first offered.

---

# Overview

**IDE xxx (proposed)** is a non-credit, one-week intensive course in outbreak
analytics.
Each day pairs a short lecture with an extended R lab so participants practice
the full path from raw line list to a scored forecast.
The emphasis is on methods that hold up under the time pressure and incomplete
data of a live response.

By the end of the course, participants will be able to:

- Build and read an epidemic curve, accounting for reporting delay
- Estimate the time-varying reproduction number from case data
- Reason about superspreading using branching processes
- Fit a simple compartmental model to observed cases
- Produce a nowcast that corrects for right-truncation
- Make and score a short-term forecast

# Who should apply

The course is aimed at public-health analysts, response staff, graduate
students, and clinicians who take part in outbreak analysis.

**Prerequisites.** Working knowledge of R is expected: participants should be
able to read data, write simple functions, and make basic plots. No prior
modeling experience is assumed.

# Format and delivery

- **Duration.** 1 week (5 days), intensive.
- **Mode.** Hybrid. Attend in person or join online.
- **Daily hours.** A daily lecture followed by hands-on R labs, roughly a full
  working day.
- **Assessment.** No formal assessment.
- **Certificate.** Participants who attend receive a certificate of attendance.
- **Equipment.** Participants bring their own laptops with R and RStudio
  installed. Setup instructions are sent before the course begins.

# Course content and topics

- Epidemic curves and reporting delay
- The renewal equation and time-varying reproduction number estimation
- Branching processes and superspreading
- Fitting a simple compartmental model
- Nowcasting and right-truncation
- Short-term forecasting and forecast scoring

# Day-by-day timetable

| Day | Morning lecture | Afternoon lab (R) |
|-----|-----------------|--------------------|
| 1 | Epidemic curves and reporting delay | Building and cleaning an epidemic curve |
| 2 | The renewal equation and estimating $R_t$ | Estimating $R_t$ from case data |
| 3 | Branching processes and superspreading | Simulating and fitting a branching process |
| 4 | Fitting a simple compartmental model; nowcasting | Fitting an SIR model; a first nowcast |
| 5 | Short-term forecasting and forecast scoring | Producing and scoring a forecast |

# Site resources

The course draws on material already published on this site. Participants can
read ahead or review afterward.

- [The reproduction number and $R_t$](math/reproduction-number-rt.md)
- [The SIR model](math/sir.md)
- [Stochastic epidemics](math/stochastic-epidemics.md)
- [Branching processes](math/branching-processes.md)
- [Proper scoring rules](math/proper-scoring-rules.md)
- [Delay distributions and censoring](epidemiology/delay-distributions-censoring.md)

Three further topics, nowcasting, epidemic forecasting, and the renewal
equation, are planned as site pages and will be linked here once published.

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
