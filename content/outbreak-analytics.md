---
title: "Outbreak Analytics and Modeling"
description: "A hands-on analytics sequence for real-time epidemic analysis: epidemic curves, reproduction number estimation, compartmental and branching-process models, nowcasting, and forecasting."
author: Michael DeWitt
date: 2026-07-04
---

This course assembles the tools of real-time epidemic analysis into a single
sequence: reconstructing epidemic curves, estimating the reproduction number,
fitting compartmental and branching-process models, nowcasting reporting
delays, and producing and scoring short-term forecasts. It turns the site's
modeling pages into hands-on analytics work in R, with Python and Julia
parallels.

The course syllabus is shown below.

> **Draft syllabus.** This is a scaffold for the concentration. Course number,
> credit hours, dates, and specific assignments are placeholders and will be
> finalized before the course is offered.

---

# Course title and instructors

**Title:** Outbreak Analytics and Modeling  
**Course Number:** BIO 3xx (proposed; confirm with the Department of Biology)  
**Semester:** TBD  
**Credit Hours:** 3  
**Meeting Time:** TBD

**Course Director:** Michael E. DeWitt, MS  
**Email:** medewitt@wakehealth.edu or dewime23@wfu.edu  

# Course description

When an outbreak is underway, decisions depend on a set of analyses that must be
run quickly and honestly: what does the epidemic curve show once we correct for
reporting delay, is transmission growing or shrinking, and what will the next
few weeks look like. This course builds that analytic sequence. Students
reconstruct epidemic curves from line-list and aggregated data, estimate the
time-varying reproduction number and communicate its uncertainty, fit
deterministic and stochastic compartmental and branching-process models to
outbreak data, and produce short-term forecasts scored with proper scoring
rules. The course leans on the modeling material the site already teaches and
turns it into applied practice. The course is cross-listable to graduate
students.

# Learning outcomes

Upon successful completion of this course, students will be able to:

- Reconstruct and interpret an epidemic curve from line-list or aggregated
  data, correcting for reporting delay and right-truncation
- Estimate the time-varying reproduction number and communicate its uncertainty
- Fit and simulate compartmental and branching-process models to outbreak data
- Produce and score a short-term forecast using proper scoring rules
- Explain superspreading and its effect on outbreak dynamics through
  branching-process reasoning
- Apply nowcasting to correct for censoring in recent case counts
- Coordinate the analytic workflow within a response team, clarifying roles and
  translating results into clear recommendations for decision-makers

# Textbook and other resources

There is no single required textbook. Recommended references include:

- Vynnycky E, White RG. *An Introduction to Infectious Disease Modelling*.
  Oxford University Press.
- Bjørnstad ON. *Epidemics: Models and Data Using R*. Springer.
- Selected primary literature on reproduction number estimation and forecasting

Additional readings will be assigned throughout the course.

## Site resources

This course draws on IDEEEP content pages as assigned readings and lab
material:

- [The reproduction number and Rt](math/reproduction-number-rt.md)
- [The SIR model](math/sir.md)
- [SEIR models](math/seir-models.md)
- [Stochastic epidemics](math/stochastic-epidemics.md)
- [Branching processes](math/branching-processes.md)
- [The next-generation matrix](math/next-generation-matrix.md)
- [Model calibration](math/model-calibration.md)
- [Proper scoring rules](math/proper-scoring-rules.md)
- [Delay distributions and censoring](epidemiology/delay-distributions-censoring.md)
- [Risk communication and community engagement](epidemiology/risk-communication-and-rcce.md)
- [Systems thinking and systems mapping](epidemiology/systems-thinking-and-systems-mapping.md)
- [The Euler–Lotka equation and the r–R₀
  relationship](epidemiology/euler-lotka.md) — turning a growth rate into a
  reproduction number through the generation interval
- [The speed and strength of epidemic
  control](epidemiology/epidemic-control.md) — how fast versus how hard an
  intervention must act
- [Critical community size and epidemic
  fade-out](epidemiology/critical-community-size.md) — when stochastic
  extinction ends a chain of transmission
- [Metapopulation networks and the invasion
  threshold](math/metapopulation-networks.md) — spread across coupled
  populations and the network invasion condition
- [Mathematical Biology](bio301-math-bio.md)

A live response is also a coordination problem: analytics feed decisions only
when roles are clear and results are communicated well, so the course threads in
the collaboration and communication skills from [systems thinking and systems
mapping](epidemiology/systems-thinking-and-systems-mapping.md) and [risk
communication](epidemiology/risk-communication-and-rcce.md).

New concept pages on nowcasting, epidemic forecasting, and the renewal equation
are planned and will be linked here as they are published.

# Course structure and schedule

This course meets over 15 weeks and combines lecture with computer labs on real
outbreak data. The schedule below is a draft outline of topics.

| Week | Topic |
|------|-------|
| 1 | Introduction to outbreak analytics and the data pipeline |
| 2 | Epidemic curves from line-list and aggregated data |
| 3 | Delay distributions, censoring, and right-truncation |
| 4 | The renewal equation |
| 5 | Estimating R0 and the time-varying Rt |
| 6 | Communicating uncertainty in Rt |
| 7 | Branching processes and superspreading |
| 8 | Deterministic compartmental models |
| 9 | Stochastic compartmental models |
| 10 | The next-generation matrix and thresholds |
| 11 | Fitting models to data: calibration |
| 12 | Nowcasting recent case counts |
| 13 | Short-term forecasting |
| 14 | Forecast evaluation and proper scoring rules |
| 15 | Project presentations and wrap-up |

Note: Specific dates will be provided at the beginning of the semester. Topics
may be adjusted based on class progress and student interests.

# Grades and assignments

| Activity | Weight |
|----------|--------|
| Participation and lab discussion | 20% |
| Computer labs and assignments | 30% |
| Exam(s) | 20% |
| Final project | 30% |

**Final project:** Students will carry out a real-time analysis of an outbreak
dataset, reconstructing the epidemic curve, estimating the reproduction number,
and producing a scored short-term forecast, with all code reproducible.

:::{course-policies.md}:::

:::{university-policies.md}:::

:::{syllabus-change-notice.md}:::
