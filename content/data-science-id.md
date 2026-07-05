---
title: "Data Science for Infectious Disease"
description: "Applied data science for infectious disease: ingesting and validating messy surveillance data, structuring reproducible projects, and communicating results honestly."
author: Michael DeWitt
date: 2026-07-04
---

This course extends reproducible research craft into applied data science for
infectious disease: ingesting messy surveillance data, wrangling and validating
it, and communicating results with honest visualizations. It sequences the
site's Programming and Computing library around real infectious-disease
datasets.

The course syllabus is shown below.

> **Draft syllabus.** This is a scaffold for the concentration. Course number,
> credit hours, dates, and specific assignments are placeholders and will be
> finalized before the course is offered.

---

# Course title and instructors

**Title:** Data Science for Infectious Disease  
**Course Number:** BIO 3xx (proposed; confirm with the Department of Biology)  
**Semester:** TBD  
**Credit Hours:** 3  
**Meeting Time:** TBD

**Course Director:** Michael E. DeWitt, MS  
**Email:** medewitt@wakehealth.edu or dewime23@wfu.edu  

# Course description

Working with real infectious-disease data means dealing with files in awkward
formats, records that are missing or duplicated, and results that must be
communicated without overstating what the data support. This course teaches the
applied data-handling side of the work. Students ingest and validate data from
files and APIs, handle formats, missingness, and secrets safely, structure a
reproducible project under version control with tested and documented code,
build clear and honest visualizations that show uncertainty, and reason about
performance and numerical stability as analyses scale. The material comes from
the site's Programming and Computing library, sequenced around real datasets.

This course overlaps with Research Tools and Methods, which covers reproducible
research craft. The intended split is clean: Research Tools and Methods teaches
the craft and reproducibility habits, while this course focuses on applied data
handling and visualization with infectious-disease data. Where a course renumber
or absorption is proposed, the overlap should be resolved so the two courses do
not duplicate content.

# Learning outcomes

Upon successful completion of this course, students will be able to:

- Ingest and validate infectious-disease data from files and APIs, handling
  formats, missingness, and secrets safely
- Structure a reproducible project with version control and tested, documented
  code
- Build clear, honest visualizations of epidemiologic data with uncertainty
- Reason about performance and numerical stability when analyses scale
- Move data between formats and reshape it into an analysis-ready structure

# Textbook and other resources

There is no single required textbook. Recommended references include:

- Wickham H, Çetinkaya-Rundel M, Grolemund G. *R for Data Science*. O'Reilly.
- Wilke CO. *Fundamentals of Data Visualization*. O'Reilly.
- Selected primary literature and public surveillance datasets

Additional readings will be assigned throughout the course.

## Site resources

This course draws on IDEEEP content pages as assigned readings and lab
material:

- [Programming and Computing](programming.md)
- [Data representation and formats](programming/data-representation-and-formats.md)
- [Data ingestion and APIs](programming/data-ingestion-and-apis.md)
- [Project workflow](programming/project-workflow.md)
- [Version control with Git](programming/version-control-git.md)
- [Testing scientific code](programming/testing-scientific-code.md)
- [Debugging and troubleshooting](programming/debugging-and-troubleshooting.md)
- [Reproducibility](programming/reproducibility.md)
- [Graphing data](math/graphing-data.md)
- [Manipulating data](math/manipulating-data.md)
- [HPC clusters and Slurm](programming/hpc-clusters-slurm.md)
- [Research Tools and Methods](bio390-research-tools.md)

New concept pages on data-visualization principles and on tidy and relational
data are planned and will be linked here once published.

# Course structure and schedule

This course meets over 15 weeks and combines lecture with computer labs on real
infectious-disease datasets. The schedule below is a draft outline of topics.

| Week | Topic |
|------|-------|
| 1 | Introduction: the infectious-disease data pipeline |
| 2 | Data representation and formats |
| 3 | Tidy and relational data |
| 4 | Data ingestion from files |
| 5 | Ingestion from APIs and handling secrets safely |
| 6 | Validation and missingness |
| 7 | Reshaping and manipulating data |
| 8 | Project workflow and structure |
| 9 | Version control with Git |
| 10 | Testing and debugging scientific code |
| 11 | Reproducibility |
| 12 | Principles of honest data visualization |
| 13 | Visualizing uncertainty |
| 14 | Performance, numerical stability, and scaling to HPC |
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

**Final project:** Students will build a reproducible analysis of a real
infectious-disease dataset from ingestion through validation to visualization,
with tested code under version control and honest communication of uncertainty.

:::{course-policies.md}:::

:::{university-policies.md}:::

:::{syllabus-change-notice.md}:::
