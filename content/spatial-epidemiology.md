---
title: "Spatial Epidemiology and Disease Mapping"
description: "A graduate methods course on spatial point patterns, areal disease-mapping models, Gaussian processes, and kriging for infectious disease risk."
author: Michael DeWitt
date: 2026-07-04
---

This course sequences the spatial statistics used in infectious disease
epidemiology into a taught methods course. Students learn to model spatial
point patterns of cases, fit areal disease-mapping models, and predict
continuous risk surfaces with Gaussian processes and kriging. The material
turns the site's spatial reference cluster into an ordered path from point
patterns to smoothed risk maps.

The course syllabus is shown below.

> **Draft syllabus.** This is a scaffold for the concentration. Dates, meeting
> times, and specific assignments will be finalized before the semester begins.

---

# Course title and instructors

**Title:** Spatial Epidemiology and Disease Mapping  
**Course Number:** BIO 6xx (proposed; with an undergraduate cross-list where
noted)  
**Semester:** TBD  
**Credit Hours:** 3  
**Meeting Time:** TBD  
**Prerequisites:** [Statistical Modeling of Infectious Disease
Dynamics](statistical-modeling-id.md) or equivalent Bayesian methods

**Course Director:** Michael E. DeWitt, MS  
**Email:** medewitt@wakehealth.edu or dewime23@wfu.edu  

# Course description

Where cases occur carries information about how disease spreads. This course
teaches the standard spatial methods used in graduate infectious disease
epidemiology. Students learn to model spatial point patterns and test for
clustering, fit areal disease-mapping models with neighborhood structure
(CAR, ICAR, BYM, and BYM2) and interpret smoothed relative-risk surfaces, and
use Gaussian processes and their Hilbert-space approximations for continuous
spatial risk. We cover covariance functions, kriging for prediction at
unobserved locations, integrated nested Laplace approximation (INLA) for fast
inference, and the practical questions of distance metrics and map
projections. Throughout, the emphasis is on quantifying spatial uncertainty
rather than reporting point maps alone. The course connects to open site work
on the spatial statistics cluster.

# Learning outcomes

Upon successful completion of this course, students will be able to:

- Model spatial point patterns of cases and test for clustering
- Fit areal disease-mapping models (CAR, ICAR, BYM, and BYM2) and interpret
  smoothed risk surfaces
- Use Gaussian processes and their approximations for continuous spatial risk
- Predict at unobserved locations with kriging and quantify spatial uncertainty
- Choose appropriate distance metrics and map projections for a given problem
- Fit spatial models efficiently with INLA and evaluate the approximation

# Textbook and other resources

There is no single required textbook. Recommended references and readings
include:

- Banerjee S, Carlin BP, Gelfand AE. *Hierarchical Modeling and Analysis for
  Spatial Data*, 2nd ed. CRC Press, 2014.
- Cressie N. *Statistics for Spatial Data*, rev. ed. Wiley, 1993.
- Blangiardo M, Cameletti M. *Spatial and Spatio-temporal Bayesian Models with
  R-INLA*. Wiley, 2015.
- Diggle PJ. *Statistical Analysis of Spatial and Spatio-Temporal Point
  Patterns*, 3rd ed. CRC Press, 2013.

Additional primary literature will be assigned throughout the semester.

## Site resources

This course draws on the following IDEEE reference pages:

- [Distance measures](math/distance-measures.md)
- [Spatial point processes](math/spatial-point-processes.md)
- [Areal models (CAR)](math/areal-models-car.md)
- [Covariance functions](math/covariance-functions.md)
- [Gaussian processes](math/gaussian-processes.md)
- [Hilbert-space GP](math/hilbert-space-gp.md)
- [Kriging](math/kriging.md)
- [INLA](math/inla.md)
- [Spatial diffusion](math/spatial-diffusion.md)
- [Spatial moment equations](math/spatial-moment-equations.md)

Planned reference pages on spatial cluster detection (scan statistics) and
spatiotemporal models will be added and assigned as they come online.

# Course structure and schedule

This course meets over 15 weeks and combines lecture with applied spatial
analysis. The schedule below is a draft outline of topics.

| Week | Topic |
|------|-------|
| 1 | Introduction to spatial epidemiology |
| 2 | Distance metrics, coordinates, and map projections |
| 3 | Spatial point patterns and intensity |
| 4 | Testing for clustering and spatial cluster detection |
| 5 | Areal data and neighborhood structure |
| 6 | CAR and ICAR models |
| 7 | BYM and BYM2 disease-mapping models |
| 8 | Interpreting smoothed relative-risk surfaces |
| 9 | Covariance functions and stationarity |
| 10 | Gaussian processes for continuous risk |
| 11 | Hilbert-space GP approximations |
| 12 | Kriging and spatial prediction |
| 13 | INLA for fast spatial inference |
| 14 | Spatiotemporal models |
| 15 | Student project presentations and wrap-up |

Note: Specific dates will be provided at the beginning of the semester. Topics
may be adjusted based on class progress and student interests.

# Grades and assignments

| Activity | Weight |
|----------|--------|
| Participation and discussion | 15% |
| Applied problem sets | 35% |
| Midterm mapping exercise | 20% |
| Final project | 30% |

**Final project:** Students will build a disease map for a real data set,
choosing an appropriate spatial model, reporting a smoothed risk surface, and
quantifying spatial uncertainty in a written report and presentation.

# Course policies

**Attendance:** Regular attendance is expected, particularly for discussion
sessions. Please alert the instructor if you are unable to attend for any
reason.

**Late/Makeup work:** Assignments are due on the dates provided. We recognize
that extenuating circumstances arise, and assignments may be submitted up to 2
days late without penalty. If you need an extension, contact the instructor as
soon as possible and **before the due date**.

**Artificial intelligence:** Artificial intelligence tools and large language
models such as ChatGPT, Claude, and Gemini are now part of the academic and
professional landscape and we encourage you to find ways to use them to enhance
your learning. However, if you use these tools, you must cite your sources and
provide a detailed description of the tools you used to complete the assignment.
In no way can these tools take the place of your own work and understanding of
the material. They should be used to supplement your learning, not replace it.
You are ultimately responsible for your work including content and the use of
valid citations and references. Using these tools without proper attribution is
plagiarism and will be treated as such.

# Department/School/University policies

**Academic Integrity:** Wake Forest University is committed to a culture of
academic integrity. As a part of this community, you share the responsibility
for creating a place of honesty, intellectual curiosity, and individual
accountability. As you committed to with your honor pledge signature, you agree
"not to deceive any member of the community; not to steal, cheat, or plagiarize
on academic work; and not to engage in any other form of academic misconduct."
If you have questions about documenting your work, working with external
sources, or working with peers on assigned work, consult with me as soon as
possible. Instances of academic dishonesty will be referred to the Honor and
Ethics Council.

**Accessibility:** Wake Forest University provides reasonable accommodations to
students with disabilities. If you are in need of an accommodation, please
contact me privately as early in the term as possible. Retroactive
accommodations will not be provided. Students requiring accommodations must also
consult the Center for Learning, Access, and Student Success (118 Reynolda Hall,
336-758-5929, class.wfu.edu).

**Accommodations for Religious or Spiritual Practices:** Wake Forest University
benefits from the multitude of faiths and spiritual identities held by members
of our learning community. Should you need accommodations this semester, email
me as soon as possible to ensure we have time to develop equitable
alternatives.

**Class recordings:** In case any class recordings are provided, they are
reserved only for students in this class for educational purposes and are
protected under FERPA. The recordings should not be shared outside the class in
any form.

# Syllabus change notice

This syllabus and the dates herein are subject to change.
