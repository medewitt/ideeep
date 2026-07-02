---
title: "Heritability and Variance Components"
---

# Heritability and Variance Components

Heritability answers a deceptively simple question: how much of the variation in a trait across a population is due to genetic differences rather than environment?
It is a variance ratio, not a statement about any individual, and it anchors the study of disease genetics, breeding, and [polygenic scores](polygenic-scores.md).

## Decomposing phenotypic variance

For a trait measured across a population, the total or **phenotypic variance** splits into genetic and environmental parts:

\[
V_P = V_G + V_E,
\]

where $V_G$ is the [variance](measures-of-variability.md) attributable to genotype differences and $V_E$ to environment (this simple form assumes genotype and environment are uncorrelated and non-interacting).
The genetic variance itself decomposes further:

\[
V_G = V_A + V_D + V_I,
\]

into **additive** effects $V_A$ (the average per-allele contributions that parents pass on), **dominance** $V_D$ (interactions between alleles at one locus), and **epistatic** $V_I$ (interactions across loci).

## Two heritabilities

**Broad-sense heritability** is the fraction of phenotypic variance explained by all genetic differences:

\[
H^2 = \frac{V_G}{V_P}.
\]

**Narrow-sense heritability** uses only the additive part:

\[
h^2 = \frac{V_A}{V_P}.
\]

The narrow-sense $h^2$ is the more useful quantity in most of quantitative genetics because additive effects are what respond to selection and what a linear predictor built from allele dosages can capture.
Both are ratios between $0$ and $1$, and both are properties of a *population in an environment*, not fixed constants of a trait.

## Estimating heritability

### Twin studies and Falconer's formula

Identical (monozygotic, MZ) twins share essentially all their DNA; fraternal (dizygotic, DZ) twins share on average half their segregating variants.
If MZ pairs are more similar than DZ pairs, genetics is contributing.
Comparing the trait correlation within MZ pairs, $r_{MZ}$, to that within DZ pairs, $r_{DZ}$, **Falconer's formula** estimates

\[
h^2 \approx 2\,(r_{MZ} - r_{DZ}).
\]

The factor of two reflects that DZ twins share half the additive variance, so doubling the gap in correlations recovers the additive fraction.
Broad-sense $H^2$ can be approximated as $2(r_{MZ}-r_{DZ})$ as well under simple assumptions, and $c^2 = 2 r_{DZ} - r_{MZ}$ estimates the shared-environment share.

### SNP-heritability from genome-wide data

Modern estimates use unrelated individuals and measured genotypes directly.
Methods such as **GREML** fit a linear mixed model in which the phenotype has a random genetic effect whose covariance between individuals is their **genetic relatedness matrix** (GRM), computed from genome-wide SNPs:

\[
\operatorname{Var}(y) = V_g\, A + V_e\, I,
\]

with $A$ the GRM.
The estimated $V_g / (V_g + V_e)$ is **SNP-heritability**, the additive variance tagged by common SNPs.
It is typically lower than twin-based $h^2$, and the gap ("missing heritability") reflects rare variants and imperfect tagging.

## Worked example

A twin study of a quantitative trait reports $r_{MZ} = 0.80$ and $r_{DZ} = 0.50$.
Falconer's formula gives

\[
h^2 \approx 2\,(0.80 - 0.50) = 0.60,
\]

so about 60% of the trait variance is additively genetic.
The shared-environment estimate is $c^2 = 2(0.50) - 0.80 = 0.20$, and the remaining $1 - 0.80 = 0.20$ is unique environment plus measurement error.

## In code

### R

```r
r_mz <- 0.80; r_dz <- 0.50
h2 <- 2 * (r_mz - r_dz)      # 0.60  narrow-sense heritability
c2 <- 2 * r_dz - r_mz        # 0.20  shared environment
e2 <- 1 - r_mz               # 0.20  unique environment

# Variance-component view: V_P = V_G + V_E
V_G <- 6; V_E <- 4; V_P <- V_G + V_E
H2  <- V_G / V_P             # 0.60  broad-sense
# SNP-heritability in practice: lme4/GCTA-style mixed model with a GRM
```

### Python

```python
r_mz, r_dz = 0.80, 0.50
h2 = 2 * (r_mz - r_dz)       # 0.60
c2 = 2 * r_dz - r_mz         # 0.20
e2 = 1 - r_mz                # 0.20

V_G, V_E = 6.0, 4.0
V_P = V_G + V_E
H2 = V_G / V_P               # 0.60  broad-sense
# SNP-heritability: statsmodels MixedLM / GREML-style GRM model
```

### Julia

```julia
r_mz, r_dz = 0.80, 0.50
h2 = 2 * (r_mz - r_dz)       # 0.60
c2 = 2 * r_dz - r_mz         # 0.20
e2 = 1 - r_mz                # 0.20

V_G, V_E = 6.0, 4.0
V_P = V_G + V_E
H2 = V_G / V_P               # 0.60  broad-sense
# SNP-heritability: MixedModels.jl with a genetic relatedness matrix
```

## Why it matters

Heritability sets a ceiling on how well genetics can ever predict a trait, framing expectations for [GWAS](gwas.md) discovery and polygenic-score accuracy.
It is also one of the most misunderstood numbers in science: a high $h^2$ does not mean a trait is unchangeable, nor does it explain differences *between* groups or *within* an individual — it describes the sources of variance in one population under its particular range of environments.

## Related

- [Measures of Variability](measures-of-variability.md)
- [Genome-Wide Association Studies](gwas.md)
- [Polygenic Scores](polygenic-scores.md)
- [Quantitative Methods](../math.md)
