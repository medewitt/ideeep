---
title: "Quantitative Methods"
toc: true
description: "Bite-sized references on the calculus, linear algebra, probability, and statistics behind infectious disease modeling, each with worked examples and R, Python, and Julia code."
---

<img src="assets/winston_hall_slider.jpg" style="width:100%;display:block;" alt="Winston Hall on the Wake Forest University campus.">

# Quantitative Methods

Quantitative methods are essential for those working in mathematical biology, doing epidemiology, and designing experiments (from basic bench experiments to large field experiments) -- especially as part of the modern practice of these fields.
The best way to learn these skills is through constant exposure and solving practical problems.

Here we collate a collection of bite-sized references covering the calculus, linear algebra, probability, and statistics that underpin quantitative work in infectious disease ecology, evolution, and epidemiology.
Each page pairs the core idea and notation with a worked example and runnable code in [**R**](https://cran.r-project.org), [**Python**](https://www.python.org), and [**Julia**](https://julialang.org) for simulation and mostly importantly, intuition.
Note that many of these came from years of notes, but some are created with the assistance of LLMs.
Let us know if you spot any errors.
Furthermore, many of the posts taken on strong opinions regarding the use of particular methods.
These are tools and as such there are often many different ways of applying tools to problems (e.g., two carpenters with the same tools may approach building a cabinet in very different ways using different sets of tools).

Math is hard.
It requires practice and repetition.

## Foundations & notation

- [The Language of Mathematics](math/language-of-mathematics.md) — number systems, symbols, and how to read an equation
- [Mathematical Notation](math/mathematical-notation.md) — symbols, sums, products, and LaTeX
- [Functions and Graphs](math/functions-and-graphs.md) — common functions and how to plot them
- [Exponentials and Logarithms](math/exponentials-and-logarithms.md) — rules, the number $e$, and log identities

## Working with data

- [Manipulating Data Frames](math/manipulating-data.md) — dplyr, data.table, pandas, Polars, and DataFrames.jl
- [Graphing Data](math/graphing-data.md) — matching charts and designing figures to questions and the grammar of graphics

## Sequences, series & limits

- [Sequences](math/sequences.md) — notation, monotonicity, and boundedness
- [Limits](math/limits.md) — convergence, properties, and L'Hôpital's rule
- [Series](math/series.md) — arithmetic, geometric, and power series
- [Taylor and Maclaurin Series](math/taylor-series.md) — polynomial approximation to functions

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
- [Lebesgue Integration](math/lebesgue-integration.md) — slicing the range, integrating against any measure, and a mixed continuous-plus-atomic force of infection

## Optimization

- [Optimization and Critical Points](math/optimization.md) — maxima, minima, and convexity

## Convexity & inequalities

- [Jensen's Inequality and Nonlinear Averaging](math/jensens-inequality.md) -- how you have to make sure you know what you are averaging
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
  - [Normal](math/normal-distribution.md) · [Binomial](math/binomial-distribution.md) · [Poisson](math/poisson-distribution.md) · [Exponential](math/exponential-distribution.md) · [t](math/t-distribution.md)
- [Expected Value](math/expected-value.md)
- [Moment Generating Functions](math/moment-generating-functions.md)
- [Measures of Center](math/measures-of-center.md) — mean, median, quantiles
- [Measures of Variability](math/measures-of-variability.md) — variance, SD, standard error
- [Sampling Distributions](math/sampling-distributions.md)
- [The Law of Large Numbers](math/law-of-large-numbers.md)
- [The Central Limit Theorem](math/central-limit-theorem.md)
- [Markov Chains](math/markov-chains.md) — transition matrices and stationary distributions
- [Branching Processes](math/branching-processes.md) — Galton–Watson, extinction, and outbreaks
- [Superspreading and Transmission Heterogeneity](math/superspreading.md) — the offspring distribution, the dispersion $k$, and the 20/80 rule
- [Chain-Binomial Models and the Household Secondary Attack Rate](math/chain-binomial-reed-frost.md) — Reed-Frost transmission and household final size
- [Random Walks and Brownian Motion](math/random-walk-brownian-motion.md) — diffusive scaling and the Wiener process
- [Quasi-Stationary Distributions](math/quasi-stationary-distributions.md) — the endemic level before fade-out, and persistence as an eigenvalue
- [Fourier and Spectral Analysis](math/fourier-spectral-analysis.md) — decomposing a signal into frequencies and finding periodicity with the periodogram
- [Wavelet Analysis](math/wavelet-analysis.md) — time-resolved periodicity for non-stationary signals, the scalogram, and wavelet coherence
- [Copulas](math/copulas.md) — separating dependence from the marginals via Sklar's theorem
- [Maximum Likelihood Estimation](math/maximum-likelihood.md)
- [Kullback–Leibler Divergence](math/kl-divergence.md) — relative entropy, cross-entropy, and forward vs reverse KL
- [Moment Matching](math/moment-matching.md) — method of moments and distributional approximation
- [Monotonic Transformations](math/monotonic-transformations.md)
- [Hypothesis Testing](math/hypothesis-testing.md)
- [p-values](math/p-values.md)
- [Type M and Type S Errors](math/type-m-s-errors.md) — design analysis beyond power: the exaggeration ratio and sign-error rate of significant estimates
- [Confidence Intervals](math/confidence-intervals.md)
- [Permutation Tests](math/permutation-tests.md)
- [Diagnostic Testing and Screening](math/diagnostic-testing.md) — sensitivity, specificity, PPV, and ROC
- [Bland–Altman Agreement](math/bland-altman.md) — comparing two measurement methods by bias and limits of agreement, not correlation
- [Dilutions, Titers, and Standard Curves](math/dilutions-and-titers.md) — turning an assay readout into a concentration: serial-dilution titers and standard-curve interpolation
- [Proper Scoring Rules](math/proper-scoring-rules.md) — Brier, log score, CRPS, and forecast calibration

## Regression & generalized linear models

- [Linear Regression](math/linear-regression.md)
- [Logistic Regression](math/logistic-regression.md)
- [Proportional Odds Models](math/proportional-odds.md) — ordinal outcomes, and how they relate to logistic and survival regression
- [Generalized Linear Models](math/generalized-linear-models.md) — GLMs and Poisson regression
- [Splines and Penalized Regression](math/splines.md) — B-splines, restricted cubic splines, penalized/thin-plate smooths (Wood, Harrell)
- [Contrasts and Average Marginal Effects](math/average-marginal-effects.md) — turning link-scale coefficients into risk differences and effects on the outcome scale
- [Age, Period, and Cohort Effects](math/age-period-cohort.md) — separating birth-cohort effects from age and calendar-time trends in risk models
- [Hierarchical (Multilevel) Models](math/hierarchical-models.md) — partial pooling and shrinkage
- [Multilevel Regression and Poststratification](math/multilevel-regression-poststratification.md) — small-area estimation from non-representative surveys

## Bayesian inference

- [Bayesian Inference](math/bayesian-inference.md) — priors, likelihood, and the posterior
- [Markov Chain Monte Carlo](math/mcmc.md)
- [The Kalman Filter](math/kalman-filter.md) — the linear-Gaussian predict/update recursion, time-varying transmission, and fusing wastewater with case reports
- [State-Space Models and Particle Filtering](math/state-space-particle-filter.md) — partially observed Markov processes and the bootstrap particle filter
- [POMP Models and Plug-and-Play Inference](math/partially-observed-markov-processes.md) — iterated filtering, particle MCMC, and synthetic likelihood behind the `pomp` package
- [Hidden Markov Models](math/hidden-markov-models.md) — discrete latent regimes via the forward, Viterbi, and Baum-Welch algorithms
- [Approximate Bayesian Computation](math/approximate-bayesian-computation.md) — likelihood-free inference by simulation, for models you can run but not write down
- [Prior Predictive Checks](math/prior-predictive-checks.md) — simulate from the prior to sanity-check it before fitting
- [Posterior Predictive Checks](math/posterior-predictive-checks.md) — compare replicated data to the observed to test the model
- [Identifiability](math/identifiability.md) — when data cannot separate parameters

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
- [Competing Risks](math/competing-risks.md) — cause-specific vs subdistribution hazards, cumulative incidence, and the 1−KM trap

## Experimental & study design

- [Experimental Design](math/experimental-design.md) — experimental vs observational, sources of bias
- [Factorial Designs](math/factorial-designs.md) — main effects and interactions
- [Fractional Factorial Designs](math/fractional-factorial-designs.md) — partial designs, aliasing, resolution
- [Optimal Experimental Design](math/optimal-design.md) — D-, A-, and I-optimality
- [Response Surface Methodology](math/response-surface.md) — optimizing over continuous factors
- [Latin Hypercube Sampling](math/latin-hypercube.md) — space-filling designs for computer experiments
- [Analysis of Variance](math/anova.md) — partitioning variation into between- and within-group parts, the F-test
- [Split-Plot Designs](math/split-plot-designs.md) — whole-plot and sub-plot factors, two error strata
- [Repeated Measures Designs](math/repeated-measures.md) — same subjects over conditions, within-subject correlation
- [Crossover Designs](math/crossover-designs.md) — every subject gets every treatment; washout and carryover
- [Stepped-Wedge Designs](math/stepped-wedge-designs.md) — staggered cluster rollout, separating effect from time trend
- [Balanced Incomplete Block Designs](math/balanced-incomplete-block-designs.md) — when a block cannot hold every treatment, keeping pairs balanced
- [Latin Square Designs](math/latin-square-designs.md) — controlling two blocking factors at once in a t×t layout
- [Meta-Analysis](math/meta-analysis.md) — pooling effects and prevalence across studies, heterogeneity and a Bayesian I²
- [Meta-Regression](math/meta-regression.md) — explaining between-study heterogeneity with study-level covariates
- [Publication Bias and Small-Study Effects](math/publication-bias.md) — funnel plots, Egger's test, and trim-and-fill
- [Diagnostic Test Accuracy Meta-Analysis](math/diagnostic-accuracy-meta-analysis.md) — pooling sensitivity and specificity with the bivariate/HSROC model
- [Global Sensitivity Analysis](math/sensitivity-analysis.md) — Sobol indices and Morris screening
- [Survey Sampling](math/survey-sampling.md) — SRS, stratified, cluster, and weighting
- [Bayesian Bandits for Adaptive Sampling and Trial Design](math/bayesian-bandits.md) — Thompson sampling to shift a testing budget toward the positive sites, and response-adaptive clinical trials
- [Capture-Recapture and Multiplier Methods](math/capture-recapture.md) — estimating a population's true size from overlapping incomplete lists

## Causal inference

- [Causal Inference](math/causal-inference.md) — confounding, counterfactuals, and Simpson's paradox
- [Propensity Scores](math/propensity-scores.md) — the balancing score, and matching, stratification, and weighting on it
- [Inverse Probability Weighting](math/inverse-probability-weighting.md) — reweighting to a pseudo-population, stabilized weights, and marginal structural models
- [G-Estimation](math/g-estimation.md) — structural nested models and the g-methods for time-varying confounding
- [Matching Methods](math/matching-methods.md) — exact, propensity-score, and coarsened exact matching, with balance diagnostics
- [E-Values and Unmeasured Confounding](math/e-values.md) — how strong a hidden confounder would need to be to explain away a result
- [Instrumental Variables](math/instrumental-variables.md) — estimating causal effects under confounding
- [Mendelian Randomization](math/mendelian-randomization.md) — genetic variants as instruments

## Statistical & population genetics

*Population-genetics foundations:*

- [Hardy–Weinberg Equilibrium](math/hardy-weinberg.md) — genotype frequencies and the χ² test
- [Linkage Disequilibrium](math/linkage-disequilibrium.md) — $D$, $D'$, and $r^2$
- [Genetic Drift and the Wright–Fisher Model](math/genetic-drift.md)
- [Selection and Mutation–Selection Balance](math/selection-popgen.md)
- [Population Structure and F_ST](math/population-structure.md)
- [Phylogenetic Inference: Substitution Models and Tree Building](math/phylogenetic-inference.md) — from sequences to a tree, with IQ-TREE and BEAST
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
- [Quasispecies and the Error Threshold](math/quasispecies.md) — the mutant cloud, error catastrophe, and lethal mutagenesis

## Evolutionary dynamics

- [Evolutionary Game Theory](math/evolutionary-game-theory.md) — ESS and replicator dynamics
- [The Evolution of Cooperation](math/evolution-of-cooperation.md) — the Prisoner's Dilemma and Nowak's five rules
- [Kin Selection and Inclusive Fitness](math/kin-selection.md) — Hamilton's rule derived from the Price equation
- [Adaptive Dynamics and the Evolution of Virulence](math/evolution-of-virulence.md)
- [The Price Equation and Evolutionary Epidemiology](math/price-equation.md) — selection, transmission, and within-host change as an exact identity
- [Adaptive Dynamics](math/adaptive-dynamics.md) — invasion fitness, singular strategies, and evolutionary branching
- [The Evolution of Resistance](math/resistance-evolution.md) — selection under drug pressure and the cost of resistance
- [Life-History Theory](math/life-history-theory.md) — trade-offs, age at maturity, and evolutionary demography

## Population & community ecology

*Single-species dynamics:*

- [Exponential and Logistic Growth](math/logistic-growth.md)
- [Discrete-Time Models and the Logistic Map](math/discrete-population-models.md)
- [Structured Population Models](math/structured-populations.md) — Leslie matrices
- [Reproductive Value and Demographic Sensitivity](math/reproductive-value.md) — the left eigenvector and where interventions move growth most
- [Metapopulations and the Levins Model](math/metapopulations.md) -- models considering more than patch or population and their interactions
- [Asynchrony and the Inflationary Effect](math/metapopulation-asynchrony.md) — how spatiotemporal variation and dispersal inflate abundance, persistence, and can increase infection
- [Source–Sink Dynamics](math/source-sink-dynamics.md) — BIDE bookkeeping and why abundance misleads
- [Spatial Synchrony and the Moran Effect](math/spatial-synchrony.md) — dispersal, correlated noise, and traveling waves

*Species interactions & stability:*

- [Lotka–Volterra Predator–Prey Dynamics](math/predator-prey.md) - the basis of many models in ecology and infectious diseases
- [Functional Responses and the Paradox of Enrichment](math/functional-responses.md) — Holling types and enrichment-driven cycles
- [Competition and Coexistence](math/competition-coexistence.md)
- [Modern Coexistence Theory and the Storage Effect](math/coexistence-theory.md) — stabilizing niche vs fitness differences
- [The Community Matrix and Stability](math/community-matrix.md)

*Species distributions & niche modeling:*

- [Species Distribution Models: Presence-Only Data](math/species-distribution-presence-only.md) — background points and the Maxent / Poisson point-process view
- [Species Distribution Models: Presence–Absence Data](math/species-distribution-presence-absence.md) — logistic occurrence models, AUC, and the detection/occupancy caveat

*Biodiversity & community structure:*

- [Diversity Indices](math/diversity-indices.md) — Shannon, Simpson, Hill numbers
- [Species-Abundance Distributions and Neutral Theory](math/species-abundance.md)

*Dynamical-systems & epidemic-dynamics toolkit:*

- [Equilibria and Linear Stability](math/equilibria-and-stability.md) — nullclines and phase planes
- [Floquet Theory and the Stability of Periodic Systems](math/floquet-theory.md) — the monodromy matrix, Floquet multipliers, and stability of periodic orbits and forced equilibria
- [Bifurcations](math/bifurcations.md) — thresholds and tipping points
- [Critical Transitions and Early-Warning Signals](math/critical-transitions.md) — rising variance and autocorrelation before a tipping point
- [The Next-Generation Matrix and R₀](math/next-generation-matrix.md)

*Spatial dynamics & pattern formation:*

- [Spatial Diffusion and the Heat Equation](math/spatial-diffusion.md) — random movement and $\sqrt{t}$ spreading
- [Reaction–Diffusion and Spatial Spread](math/reaction-diffusion.md) — the Fisher–KPP wave
- [Metapopulation Networks and the Invasion Threshold](math/metapopulation-networks.md) — mobility, degree heterogeneity, and global invasion
- [Turing Patterns](math/turing-patterns.md) — diffusion-driven pattern formation
- [Spatial Moment Equations](math/spatial-moment-equations.md) — mean density and spatial covariance from a stochastic individual-based model

## Networks

- [Networks and Graphs](math/networks.md) — adjacency matrices, degree, and structure
- [Centrality and Node Importance](math/centrality.md) — degree, betweenness, eigenvector centrality
- [Random-Graph Models](math/network-models.md) — Erdős–Rényi, scale-free, small-world
- [Networks in Ecology and Epidemiology](math/ecological-networks.md) — food webs and transmission networks
- [Graph Neural Networks](math/graph-neural-networks.md) — learning on contact and mobility graphs by message passing

## Machine learning & AI

*Foundations & core architectures:*

- [Overfitting, Regularization, and Cross-Validation](math/overfitting-regularization.md) — the bias–variance tradeoff, validation, k-fold CV, and L1/L2 penalties
- [Tree Ensembles: Random Forests and Gradient Boosting](math/tree-ensembles.md) — the workhorse models for tabular prediction, and feature importance
- [Neural Networks and the Multilayer Perceptron](math/neural-networks.md) — neurons, activations, backpropagation, and the curved boundaries depth buys
- [Recurrent Networks and LSTMs](math/recurrent-networks-lstm.md) — hidden state, why plain RNNs forget, gated memory, and case-count forecasting
- [Convolutional Networks and Image Identification](math/convolutional-networks-image.md) — learned filters, feature maps, transfer learning, and skin-lesion classification
- [Graph Neural Networks](math/graph-neural-networks.md) — message passing on contact and mobility graphs, and the GCN layer
- [Transformers and Attention](math/transformers-attention.md) — self-attention, multi-head attention, and the architecture behind foundation models

*Unsupervised learning:*

- [Dimensionality Reduction and Embeddings](math/dimensionality-reduction.md) — PCA, t-SNE, and UMAP for visualizing and compressing high-dimensional data
- [Clustering and Unsupervised Learning](math/clustering.md) — k-means, Gaussian mixtures, hierarchical, and density-based clustering

*Generative models & Bayesian deep learning:*

- [Variational Autoencoders](math/variational-autoencoders.md) — encoder/decoder, the ELBO, the reparameterization trick, and surveillance anomaly detection
- [Encoding Spatial Priors with VAEs (PriorVAE)](math/prior-encoding-vae.md) — amortizing a slow spatial prior into a decoder for fast Bayesian disease mapping
- [Deep Learning, Foundation Models, and Agentic AI](math/deep-learning-agentic-models.md) — the architecture family, attention and transformers, and language-model agents in outbreak analytics

*Trust, uncertainty & interpretability:*

- [Model Interpretability and SHAP](math/interpretability-shap.md) — explaining predictions with Shapley values, permutation importance, and partial dependence
- [Uncertainty, Calibration, and Conformal Prediction](math/uncertainty-calibration-conformal.md) — aleatoric vs epistemic uncertainty, reliability diagrams, and distribution-free prediction sets

*Applications:*

- [Scientific Machine Learning: Neural ODEs and Physics-Informed Networks](math/scientific-machine-learning.md) — differentiable simulation, learning unknown dynamics, and embedding known ODEs as constraints
- [Remote Sensing, Object Counting, and Outbreak Detection](math/remote-sensing-outbreak-detection.md) — counting cars in a hospital parking deck as a proxy signal, and the assumptions that make or break it

## Pharmacokinetics & pharmacodynamics

- [Pharmacokinetics: Compartment Models](math/pharmacokinetics.md) — ADME, clearance, half-life, AUC
- [Pharmacodynamics: Dose–Response](math/pharmacodynamics.md) — the Emax/Hill model
- [Antimicrobial PK/PD](math/antimicrobial-pkpd.md) — minimum inhibatory concentration (MIC) and the PK/PD indices
- [PK/PD Target Attainment](math/pkpd-target-attainment.md) — probability of target attainment and dose selection

## Epidemic modeling

- [Compartmental Models](math/sir.md) — the SIR model and $R_0$
- [Final Size, Herd Immunity, and Overshoot](math/final-size-and-herd-immunity.md) — the final size relation, the herd immunity threshold, and epidemic overshoot
- [Density-Dependent and Frequency-Dependent Transmission](math/transmission-modes.md) — how the contact rate scales with host density, and the critical density threshold
- [SEIR and Compartmental Extensions](math/seir-models.md) — latent classes, waning, demography
- [Social Contact Matrices and Age-Structured Mixing](math/contact-matrices.md) — who-meets-whom by age, from contact surveys to $R_0$
- [Serocatalytic Models](math/serocatalytic-models.md) — estimating the force of infection from age–seroprevalence surveys
- [Within-Host Dynamics and the Immune Response](math/within-host-dynamics.md) — virus, infected cells, and B-cell/T-cell immunity
- [Burst Size, Latent Period, and Mutation at the Cellular Scale](math/viral-burst-size.md) — the cell-level viral life history: $R_0 = B\rho$, continuous-vs-burst extinction, the optimal lysis time, and the mutational output $B\mu$
- [Vector-Borne Disease Models](math/vector-borne.md) — the Ross–Macdonald framework
- [Vectorial Capacity from Field Data](math/vectorial-capacity.md) — estimating biting rate, survival, EIR, and vectorial capacity from entomological collections
- [Insecticide-Resistance Monitoring](math/insecticide-resistance-monitoring.md) — diagnostic-dose classification, LC50/LC90, and the resistance ratio
- [Reservoir Ecology](math/reservoir-ecology.md) — maintenance hosts, spillover, and multi-host persistence
- [Stochastic Epidemics and the Gillespie Algorithm](math/stochastic-epidemics.md)
- [Quasi-Stationary Distributions](math/quasi-stationary-distributions.md) — endemic persistence, fade-out, and the mean time to extinction
- [Queueing Theory and ICU Colonization](math/queueing-theory.md) — patients through beds as a queue, a birth-death model of hospital colonization, and pricing out infection-prevention practices
- [The Effective Reproduction Number and Forecasting](math/reproduction-number-rt.md)
- [The Renewal Equation](math/renewal-equation.md) — linking incidence, the generation interval, and $R_t$
- [Population Dynamics of Resistance](math/resistance-dynamics.md) — two-strain competition and the treatment threshold
- [Antimicrobial Resistance Across Scales](math/amr-across-scales.md) — the individual-versus-population tension, competitive release, and a nested malaria model joining within- and between-host dynamics
- [Behavior–Disease Coupled Models](math/behavior-disease-coupled-models.md) — prevalence-dependent behavior and the feedback between action and transmission
- [Climate Forcing in Transmission Models](math/climate-forcing-in-transmission-models.md) — seasonal forcing, temperature-dependent parameters, and resonance
- [Fitting Dynamic Models to Data](math/model-calibration.md) — calibration and identifiability

## Health economics & decision analysis

- [Cost-Effectiveness Analysis](math/cost-effectiveness-analysis.md) — costs, QALYs and DALYs, the ICER, and the willingness-to-pay threshold
