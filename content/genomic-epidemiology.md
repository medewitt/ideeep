---
title: "Applied Genomic and Phylodynamic Epidemiology"
description: "Linking pathogen genomes to epidemiologic metadata end to end: sequencing, phylogenetics, phylodynamics, transmission-cluster detection, and genomic surveillance, with data governance throughout."
author: Michael DeWitt
date: 2026-07-05
---

This course develops pathogen genomic epidemiology end to end: from sequencing
and phylogenetics through phylodynamic inference to transmission-cluster
detection and genomic surveillance. It is deliberately applied and
surveillance-oriented, going beyond generic bioinformatics to connect genomes to
the epidemiologic questions they can answer.

The course syllabus is shown below.

> **Draft syllabus.** This is a scaffold for the concentration. Course number,
> credit hours, dates, and specific assignments are placeholders and will be
> finalized before the course is offered.

---

# Course title and instructors

**Title:** Applied Genomic and Phylodynamic Epidemiology  
**Course Number:** BIO 6xx (proposed; cross-listed undergraduate, confirm with the Department of Biology)  
**Semester:** TBD  
**Credit Hours:** 3  
**Meeting Time:** TBD

**Course Director:** Michael E. DeWitt, MS  
**Email:** medewitt@wakehealth.edu or dewime23@wfu.edu  

# Course description

Pathogen genome sequences, linked to metadata such as date, place, and host, have
become a routine part of outbreak response and disease surveillance. Turning that
data into epidemiologic insight requires a specific chain of skills that a general
bioinformatics course does not assemble in one place. This course follows the
pathogen-genomics workflow from sample to decision: sequencing technologies and
their trade-offs, quality control and consensus calling, alignment and
phylogenetics, molecular-clock and coalescent reasoning, phylodynamic inference of
transmission and epidemiologic parameters, and the detection of transmission
clusters from genetic distance. Students situate these methods inside real
surveillance systems, learn to predict antimicrobial resistance from genotype, and
work throughout with the metadata standards, data governance, and equitable
data-sharing practices that make genomic surveillance trustworthy. The intended
contrast with the existing genomics and bioinformatics electives is deliberate:
this course is about pathogen surveillance and epidemiology, not generic sequence
analysis.

# Learning outcomes

Upon successful completion of this course, students will be able to:

- Describe the end-to-end genomic-surveillance workflow from sample to actionable
  output
- Choose appropriately among sequencing platforms and quality-control steps
- Build and interpret phylogenies and reason about molecular-clock and coalescent
  models
- Apply phylodynamic thinking to reconstruct transmission and estimate
  epidemiologic parameters
- Detect transmission clusters from genetic distance and integrate genomes with
  epidemiologic metadata
- Apply metadata standards, data governance, and equitable data-sharing practices
  to genomic surveillance

# Textbook and other resources

There is no single required textbook. Recommended references include:

- Hill V, et al. Progress and challenges in virus genomic epidemiology. *Trends
  Parasitol* 2021. https://doi.org/10.1016/j.pt.2021.08.007
- Selected primary literature on phylodynamics, genomic surveillance, and
  pathogen bioinformatics
- Public tooling and documentation (e.g. Nextstrain, PulseNet, GenomeTrakr) as
  assigned

Additional readings will be assigned throughout the course.

## Site resources

This course draws on IDEEEP content pages as assigned readings:

- [Genomic surveillance](epidemiology/genomic-surveillance.md)
- [Phylodynamics](math/phylodynamics.md)
- [The molecular clock](math/molecular-clock.md)
- [Coalescent theory](math/coalescent-theory.md)
- [dN/dS and selection on sequences](math/dn-ds.md)
- [Quasispecies](math/quasispecies.md)
- [Research and data ethics, governance, and responsible sharing](programming/research-data-ethics-and-governance.md)
- [HPC clusters and Slurm](programming/hpc-clusters-slurm.md)
- [Diagnostics and surveillance](diagnostics.md)

# Course structure and schedule

This course meets over 15 weeks and combines lecture with computer labs on real
pathogen-genomic datasets. The schedule below is a draft outline of topics.

| Week | Topic |
|------|-------|
| 1 | Why genomic epidemiology: from retrospective genomics to actionable surveillance |
| 2 | Sequencing technologies and their trade-offs |
| 3 | Quality control, assembly, and consensus calling |
| 4 | Alignment and building phylogenies |
| 5 | Reading trees: what a phylogeny does and does not show |
| 6 | The molecular clock and time-scaled trees |
| 7 | Coalescent theory and effective population size |
| 8 | Phylodynamics I: linking trees to epidemic dynamics |
| 9 | Phylodynamics II: estimating transmission and parameters |
| 10 | Transmission clusters and genetic-distance thresholds |
| 11 | Genotype-to-phenotype: antimicrobial resistance |
| 12 | Genomic surveillance systems and tooling |
| 13 | Metadata standards and integration with epidemiologic data |
| 14 | Data governance, equity, and responsible sharing |
| 15 | Project presentations and wrap-up |

Note: Specific dates will be provided at the beginning of the semester. Topics
may be adjusted based on class progress and student interests.

# Grades and assignments

| Activity | Weight |
|----------|--------|
| Participation and literature discussion | 20% |
| Computer labs and assignments | 30% |
| Exam(s) | 20% |
| Final project | 30% |

**Final project:** Students will analyze a real or realistic pathogen-genomic
dataset, reconstruct transmission or estimate an epidemiologic quantity, and
present the result with attention to metadata quality and data-sharing practice.

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
