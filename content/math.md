---
title: "Quantitative Methods"
toc: true
description: "Bite-sized references on the calculus, linear algebra, probability, and statistics behind infectious disease modeling, each with worked examples and R, Python, and Julia code."
---

<img src="assets/winston_hall_slider.jpg" style="width:100%;display:block;" alt="Winston Hall slider image">

# Quantitative Methods

A growing collection of bite-sized references covering the calculus, linear
algebra, probability, and statistics that underpin quantitative work in
infectious disease ecology, evolution, and epidemiology. Each page pairs the
core idea and notation with a worked example and runnable code in **R**,
**Python**, and **Julia** for simulation and intuition.

## Foundations & notation

- [The Language of Mathematics](math/language-of-mathematics.md) — number systems, symbols, and how to read an equation
- [Mathematical Notation](math/mathematical-notation.md) — symbols, sums, products, and LaTeX
- [Functions and Graphs](math/functions-and-graphs.md) — common functions and how to plot them
- [Exponentials and Logarithms](math/exponentials-and-logarithms.md) — rules, the number $e$, and log identities

## Working with data

- [Manipulating Data Frames](math/manipulating-data.md) — dplyr, data.table, pandas, Polars, and DataFrames.jl
- [Graphing Data](math/graphing-data.md) — matching charts to questions and the grammar of graphics

## Sequences, series & limits

- [Sequences](math/sequences.md) — notation, monotonicity, and boundedness
- [Limits](math/limits.md) — convergence, properties, and L'Hôpital's rule
- [Series](math/series.md) — arithmetic, geometric, and power series
- [Taylor and Maclaurin Series](math/taylor-series.md) — polynomial approximation

## Differentiation

- [Derivatives](math/derivatives.md) — the instantaneous rate of change
- [Common Derivatives](math/common-derivatives.md) — a reference table
- [Product Rule](math/product-rule.md)
- [Quotient Rule](math/quotient-rule.md)
- [Chain Rule](math/chain-rule.md)
- [Partial Derivatives](math/partial-derivatives.md)
- [The Gradient](math/gradient.md)

## Integration

- [Integrals](math/integrals.md) — area under a curve and the Fundamental Theorem
- [Common Integrals](math/common-integrals.md) — a reference table
- [u-Substitution](math/u-substitution.md)
- [Integration by Parts](math/integration-by-parts.md)

## Optimization

- [Optimization and Critical Points](math/optimization.md) — maxima, minima, and convexity

## Convexity & inequalities

- [Jensen's Inequality and Nonlinear Averaging](math/jensens-inequality.md)
- [The Legendre Transform](math/legendre-transform.md) — convex conjugates

## Linear algebra

- [Matrix and Vector Notation](math/matrix-notation.md)
- [Matrix Operations](math/matrix-operations.md)
- [Inverse, Determinant, and Rank](math/matrix-inverse-and-determinant.md)
- [Eigenvalues and Eigenvectors](math/eigenvalues-and-eigenvectors.md)
- [Jacobians](math/jacobians.md)

## Probability & statistics

- [Statistical Inference](math/statistical-inference.md) — population, parameter, sample, estimate
- [Probability Basics](math/probability-basics.md)
- [Random Variables](math/random-variables.md) — pmf, pdf, and the CDF
- [Common Distributions: An Overview](math/distributions-overview.md)
  - [Normal](math/normal-distribution.md) ·
    [Binomial](math/binomial-distribution.md) ·
    [Poisson](math/poisson-distribution.md) ·
    [Exponential](math/exponential-distribution.md) ·
    [t](math/t-distribution.md)
- [Expected Value](math/expected-value.md)
- [Moment Generating Functions](math/moment-generating-functions.md)
- [Measures of Center](math/measures-of-center.md) — mean, median, quantiles
- [Measures of Variability](math/measures-of-variability.md) — variance, SD, standard error
- [Sampling Distributions](math/sampling-distributions.md)
- [The Law of Large Numbers](math/law-of-large-numbers.md)
- [The Central Limit Theorem](math/central-limit-theorem.md)
- [Markov Chains](math/markov-chains.md) — transition matrices and stationary distributions
- [Branching Processes](math/branching-processes.md) — Galton–Watson, extinction, and outbreaks
- [Random Walks and Brownian Motion](math/random-walk-brownian-motion.md) — diffusive scaling and the Wiener process
- [Copulas](math/copulas.md) — separating dependence from the marginals via Sklar's theorem
- [Maximum Likelihood Estimation](math/maximum-likelihood.md)
- [Moment Matching](math/moment-matching.md) — method of moments and distributional approximation
- [Monotonic Transformations](math/monotonic-transformations.md)
- [Hypothesis Testing](math/hypothesis-testing.md)
- [p-Values](math/p-values.md)
- [Confidence Intervals](math/confidence-intervals.md)
- [Permutation Tests](math/permutation-tests.md)
- [Diagnostic Testing and Screening](math/diagnostic-testing.md) — sensitivity, specificity, PPV, and ROC
- [Proper Scoring Rules](math/proper-scoring-rules.md) — Brier, log score, CRPS, and forecast calibration

## Regression & generalized linear models

- [Linear Regression](math/linear-regression.md)
- [Logistic Regression](math/logistic-regression.md)
- [Generalized Linear Models](math/generalized-linear-models.md) — GLMs and Poisson regression
- [Hierarchical (Multilevel) Models](math/hierarchical-models.md) — partial pooling and shrinkage

## Bayesian inference

- [Bayesian Inference](math/bayesian-inference.md) — priors, likelihood, and the posterior
- [Markov Chain Monte Carlo](math/mcmc.md)
- [Prior Predictive Checks](math/prior-predictive-checks.md) — simulate from the prior to sanity-check it before fitting
- [Posterior Predictive Checks](math/posterior-predictive-checks.md) — compare replicated data to the observed to test the model
- [Identifiability](math/identifiability.md) — when the data cannot separate parameters

## Gaussian processes & spatial statistics

*Gaussian processes:*

- [Gaussian Processes](math/gaussian-processes.md) — distributions over functions and GP regression
- [Covariance Functions and the Matérn Family](math/covariance-functions.md) — kernels, smoothness, and lengthscale
- [Hilbert-Space Approximations for Gaussian Processes](math/hilbert-space-gp.md) — fast basis-function GPs

*Geostatistics & areal models:*

- [Kriging and Geostatistics](math/kriging.md) — variograms and best linear unbiased prediction
- [Spatial Point Processes](math/spatial-point-processes.md) — Poisson, Cox, and log-Gaussian Cox processes
- [Areal Models: CAR, ICAR, and BYM](math/areal-models-car.md) — disease mapping on a neighborhood graph
- [Bayesian Spatial Models with INLA](math/inla.md) — fast latent-Gaussian inference and the SPDE approach
- [Distances on a Sphere: Haversine and Beyond](math/distance-measures.md) — great-circle vs Euclidean distance
- [Spatial Cluster Detection](math/spatial-cluster-detection.md) — Moran's I, LISA, and the spatial scan statistic
- [Spatiotemporal Models](math/spatiotemporal-models.md) — separable and nonseparable space–time covariance

## Survival analysis

- [Survival Analysis](math/survival-analysis.md) — Kaplan–Meier, hazards, censoring
- [Cox Proportional Hazards Regression](math/cox-regression.md)

## Experimental & study design

- [Experimental Design](math/experimental-design.md) — experimental vs observational, sources of bias
- [Factorial Designs](math/factorial-designs.md) — main effects and interactions
- [Fractional Factorial Designs](math/fractional-factorial-designs.md) — partial designs, aliasing, resolution
- [Optimal Experimental Design](math/optimal-design.md) — D-, A-, and I-optimality
- [Response Surface Methodology](math/response-surface.md) — optimizing over continuous factors
- [Latin Hypercube Sampling](math/latin-hypercube.md) — space-filling designs for computer experiments
- [Global Sensitivity Analysis](math/sensitivity-analysis.md) — Sobol indices and Morris screening
- [Survey Sampling](math/survey-sampling.md) — SRS, stratified, cluster, and weighting

## Causal inference

- [Causal Inference](math/causal-inference.md) — confounding, counterfactuals, and Simpson's paradox
- [Instrumental Variables](math/instrumental-variables.md) — estimating causal effects under confounding
- [Mendelian Randomization](math/mendelian-randomization.md) — genetic variants as instruments

## Statistical & population genetics

*Population-genetics foundations:*

- [Hardy–Weinberg Equilibrium](math/hardy-weinberg.md) — genotype frequencies and the χ² test
- [Linkage Disequilibrium](math/linkage-disequilibrium.md) — $D$, $D'$, and $r^2$
- [Genetic Drift and the Wright–Fisher Model](math/genetic-drift.md)
- [Selection and Mutation–Selection Balance](math/selection-popgen.md)
- [Population Structure and F_ST](math/population-structure.md)
- [The Coalescent](math/coalescent-theory.md) — genealogies backward in time
- [Phylodynamics](math/phylodynamics.md) — reading epidemic dynamics from pathogen phylogenies

*Association & complex traits:*

- [Genome-Wide Association Studies](math/gwas.md)
- [Multiple Testing and False Discovery Rate](math/multiple-testing.md)
- [Population Stratification and PCA Control](math/population-stratification.md)
- [Heritability and Variance Components](math/heritability.md)
- [Quantitative Genetics and the Breeder's Equation](math/quantitative-genetics.md)
- [Polygenic Scores](math/polygenic-scores.md)

*Molecular evolution:*

- [Detecting Selection with dN/dS](math/dn-ds.md)
- [The Molecular Clock and Phylodynamics](math/molecular-clock.md)

## Evolutionary dynamics

- [Evolutionary Game Theory](math/evolutionary-game-theory.md) — ESS and replicator dynamics
- [The Evolution of Cooperation](math/evolution-of-cooperation.md) — the Prisoner's Dilemma and Nowak's five rules
- [Adaptive Dynamics and the Evolution of Virulence](math/evolution-of-virulence.md)
- [The Price Equation and Evolutionary Epidemiology](math/price-equation.md) — selection, transmission, and within-host change as an exact identity
- [Adaptive Dynamics](math/adaptive-dynamics.md) — invasion fitness, singular strategies, and evolutionary branching
- [The Evolution of Resistance](math/resistance-evolution.md) — selection under drug pressure and the cost of resistance

## Population & community ecology

*Single-species dynamics:*

- [Exponential and Logistic Growth](math/logistic-growth.md)
- [Discrete-Time Models and the Logistic Map](math/discrete-population-models.md)
- [Structured Population Models](math/structured-populations.md) — Leslie matrices
- [Metapopulations and the Levins Model](math/metapopulations.md)
- [Asynchrony and the Inflationary Effect](math/metapopulation-asynchrony.md) — how spatiotemporal variation and dispersal inflate abundance and persistence

*Species interactions & stability:*

- [Lotka–Volterra Predator–Prey Dynamics](math/predator-prey.md)
- [Competition and Coexistence](math/competition-coexistence.md)
- [The Community Matrix and Stability](math/community-matrix.md)

*Biodiversity & community structure:*

- [Diversity Indices](math/diversity-indices.md) — Shannon, Simpson, Hill numbers
- [Species-Abundance Distributions and Neutral Theory](math/species-abundance.md)

*Dynamical-systems & epidemic-dynamics toolkit:*

- [Equilibria and Linear Stability](math/equilibria-and-stability.md) — nullclines and phase planes
- [Bifurcations](math/bifurcations.md) — thresholds and tipping points
- [The Next-Generation Matrix and R₀](math/next-generation-matrix.md)

*Spatial dynamics & pattern formation:*

- [Spatial Diffusion and the Heat Equation](math/spatial-diffusion.md) — random movement and $\sqrt{t}$ spreading
- [Reaction–Diffusion and Spatial Spread](math/reaction-diffusion.md) — the Fisher–KPP wave
- [Turing Patterns](math/turing-patterns.md) — diffusion-driven pattern formation
- [Spatial Moment Equations](math/spatial-moment-equations.md) — mean density and spatial covariance from a stochastic individual-based model

## Networks

- [Networks and Graphs](math/networks.md) — adjacency matrices, degree, and structure
- [Centrality and Node Importance](math/centrality.md) — degree, betweenness, eigenvector centrality
- [Random-Graph Models](math/network-models.md) — Erdős–Rényi, scale-free, small-world
- [Networks in Ecology and Epidemiology](math/ecological-networks.md) — food webs and transmission networks

## Pharmacokinetics & pharmacodynamics

- [Pharmacokinetics: Compartment Models](math/pharmacokinetics.md) — ADME, clearance, half-life, AUC
- [Pharmacodynamics: Dose–Response](math/pharmacodynamics.md) — the Emax/Hill model
- [Antimicrobial PK/PD](math/antimicrobial-pkpd.md) — MIC and the PK/PD indices
- [PK/PD Target Attainment](math/pkpd-target-attainment.md) — probability of target attainment and dose selection

## Epidemic modeling

- [Compartmental Models](math/sir.md) — the SIR model and $R_0$
- [Density-Dependent and Frequency-Dependent Transmission](math/transmission-modes.md) — how the contact rate scales with host density, and the critical density threshold
- [SEIR and Compartmental Extensions](math/seir-models.md) — latent classes, waning, demography
- [Vector-Borne Disease Models](math/vector-borne.md) — the Ross–Macdonald framework
- [Reservoir Ecology](math/reservoir-ecology.md) — maintenance hosts, spillover, and multi-host persistence
- [Stochastic Epidemics and the Gillespie Algorithm](math/stochastic-epidemics.md)
- [The Effective Reproduction Number and Forecasting](math/reproduction-number-rt.md)
- [The Renewal Equation](math/renewal-equation.md) — linking incidence, the generation interval, and $R_t$
- [Population Dynamics of Resistance](math/resistance-dynamics.md) — two-strain competition and the treatment threshold
- [Fitting Dynamic Models to Data](math/model-calibration.md) — calibration and identifiability
