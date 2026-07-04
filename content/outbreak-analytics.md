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
- [Mathematical Biology](bio301-math-bio.md)

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
