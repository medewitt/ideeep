---
title: "Programming & Computing"
toc: true
description: "Practical guides to reproducible scientific computing and good programming practice, with runnable examples in R, Python, and Julia."
---

<img src="assets/cards/programming.svg" style="width:100%;display:block;" alt="An abstract plaintext-and-grid motif in the site palette representing programming and computing.">

# Programming & Computing

One of the most powerful transitions to rigorous work is the use of a plaintext approach.
This ranges from using Markdown or $\LaTeX$ to write prose and writing scripts to run your analysis.
Furthermore, the use of literature programming practices (again using resources like Quarto or even just plain markdown) allow you to take more control of your work
Plus these tools often unlock the ability to leverage similar powerful tools together, like using scripts to write outputs that you can translate directly to your finished products.

Understanding these approaches along with borrowing key concepts from computer science and more generally programming are a must for those working in quantitative fields.

## Topics

Below are some brief topics ranging from good programming practice and the everyday tools of reproducible scientific computing, with examples in R, Python, and Julia.

- [Good Programming Practices](programming/good-programming-practices.md) — naming, small functions, and clean code
- [Project Workflow](programming/project-workflow.md) — organizing an analytic project
- [Software Design & Packaging](programming/software-design-and-packaging.md) — modularity, interfaces, and turning analysis into a package
- [Reproducibility](programming/reproducibility.md) — seeds, environments, and literate code
- [Debugging and Troubleshooting](programming/debugging-and-troubleshooting.md) — a calm process and the reprex
- [A Simulation Toolkit](programming/simulation-toolkit.md) — building fake data and simulation studies
- [Randomness & Random Number Generation](programming/randomness-and-rng.md) — seeds, sampling, and the parallel-RNG trap
- [Big-O Notation & Computational Complexity](programming/big-o-and-complexity.md) — how work grows with data, and the `O(n²)` trap
- [Data Structures & Choosing the Right Container](programming/data-structures.md) — arrays, hash maps, and sets, and the list→set fix
- [Data Representation & File Formats](programming/data-representation-and-formats.md) — encodings, CSV pitfalls, tidy/relational data, SQL, and FASTA/VCF
- [Tidy and Relational Data](programming/tidy-and-relational-data.md) — tidy layout, wide vs long, and relational joins
- [Principles of Data Visualization](programming/data-visualization-principles.md) — matching chart to question, honest axes, and colorblind-safe palettes
- [Plain Text and File Systems](programming/plain-text-and-filesystems.md) — durable plain-text workflows, paths, and project layout
- [Regular Expressions & Finite-State Machines](programming/regular-expressions.md) — parsing sequences, logs, and messy field data
- [Data Ingestion & APIs](programming/data-ingestion-and-apis.md) — pulling from GenBank, GBIF, and GISAID programmatically
- [Recursion & Dynamic Programming](programming/recursion-and-dynamic-programming.md) — memoization, sequence alignment, HMMs, and tree likelihoods
- [Graph & Network Algorithms](programming/graph-algorithms.md) — BFS/DFS, shortest paths, and connected components on biological networks
- [Floating-Point Arithmetic & Numerical Stability](programming/floating-point-and-numerical-stability.md) — log space, the log-sum-exp trick, and why likelihoods hit zero
- [Numerical Methods for Dynamical Systems](programming/numerical-methods-for-dynamical-systems.md) — integrating ODEs, Euler vs RK4, stiffness, and solvers
- [Testing & Verification for Scientific Code](programming/testing-scientific-code.md) — unit tests, invariants, and testing stochastic code
- [Vectorization, Memory & Profiling](programming/vectorization-and-performance.md) — constant-factor speed, the memory hierarchy, and profiling
- [Parallelism & Concurrency](programming/parallelism-and-concurrency.md) — cores vs threads, race conditions, and thread oversubscription
- [Manipulating Data Frames](math/manipulating-data.md) — dplyr, data.table, pandas, Polars, DataFrames.jl
- [Computer Basics for Scientists](programming/computer-basics.md) — files, paths, and the command line
- [Running Jobs on an HPC Cluster (SLURM)](programming/hpc-clusters-slurm.md) — the DEAC & DEMON clusters, modules, SSH, and job submission
- [Handling Secrets and API Keys](programming/handling-secrets.md) — keys, environment variables, and `.gitignore`
- [Research and Data Ethics, Governance, and Responsible Sharing](programming/research-data-ethics-and-governance.md) — IRB and consent, FAIR data, re-identification risk, and equitable data sharing
- [Version Control with Git & GitHub](programming/version-control-git.md)
- [Building a Personal Website](programming/personal-website.md)
- [LaTeX and Technical Documents](programming/latex-and-documents.md)
- [Note-Taking with Org Mode](programming/org-mode.md)

## Resources

### Integrated Development Environments
These are programs that help you write plain text documents, code, generate things.

- [VSCode](https://code.visualstudio.com)
- [RStudio/ Posit](https://posit.co/products/open-source/rstudio)
- [NeoVim](https://neovim.io)
- Emacs (often available on MacOS and Linux, with [Doom](https://github.com/doomemacs/core) configurations)

### Computing Environments

Below are some common open-source tools used for scientific computing.

- R
- Julia
- Python

There are other tools that are often available for purchase (e.g., SAS, MATLAB) or have closed-source platforms (e.g., Mathematica).


## Guides

- [Happy Git with R](https://happygitwithr.com)
- [Plain Text Guide to Social Science](https://plain-text.co/index.html#introduction)
- [The Semester of Your CS Education](https://missing.csail.mit.edu)