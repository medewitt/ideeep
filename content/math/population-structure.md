---
title: "Population Structure and F_ST"
---

# Population Structure and F_ST

Population structure means a sample is not one randomly mating population but a mixture of subpopulations with different allele frequencies.
Ignoring it is dangerous: it deflates heterozygosity, mimics inbreeding, and — most importantly for epidemiology — creates spurious genotype–disease associations when ancestry happens to correlate with exposure or risk.

## The Wahlund effect

Suppose a total population is subdivided into subpopulations that each mate randomly internally but rarely exchange migrants.
Within each subpopulation, genotype frequencies follow [Hardy–Weinberg equilibrium](hardy-weinberg.md), but when you pool the subpopulations and compute genotype frequencies as if they were one unit, you find fewer heterozygotes than $2\bar p\bar q$ would predict.
This deficit of heterozygotes caused purely by lumping together subpopulations with different allele frequencies is the Wahlund effect.
It arises because the variance in allele frequency among subpopulations subtracts directly from the pooled heterozygosity.

## Defining F_ST

Wright's fixation index $F_{ST}$ quantifies how much of the genetic variation is due to differences among subpopulations.
Write the expected heterozygosity of a population with allele frequency $p$ as $H = 2p(1-p)$.
Define:

- $H_S$: the mean expected heterozygosity within subpopulations, averaged over subpopulations, $H_S = \overline{2 p_i (1 - p_i)}$.
- $H_T$: the expected heterozygosity of the pooled population, computed from the mean allele frequency $\bar p$, so $H_T = 2\bar p (1 - \bar p)$.

Then \[ F_{ST} = \frac{H_T - H_S}{H_T} . \] Because subpopulation differentiation always makes $H_S \le H_T$, $F_{ST}$ lies between $0$ and $1$: it is the fraction of total heterozygosity "lost" to structure.
The quantity $H_T - H_S$ is exactly the [variance](measures-of-variability.md) in allele frequency among subpopulations (the Wahlund variance), which is why $F_{ST}$ can be read as a standardized among-group variance.

### Interpreting the magnitude

As a rough guide (following Wright), $F_{ST}$ below $0.05$ indicates little differentiation, $0.05$–$0.15$ moderate, $0.15$–$0.25$ great, and above $0.25$ very great differentiation.
Human continental groups sit around $0.10$–$0.15$; strongly isolated demes or bottlenecked pathogen populations can be far higher.

## Worked example

Take two subpopulations of equal size with allele frequencies $p_1 = 0.7$ and $p_2 = 0.3$ at a biallelic locus.

Within-subpopulation heterozygosities: \[ H_1 = 2(0.7)(0.3) = 0.42, \qquad H_2 = 2(0.3)(0.7) = 0.42, \] so $H_S = \tfrac{1}{2}(0.42 + 0.42) = 0.42$.
The mean allele frequency is $\bar p = \tfrac{1}{2}(0.7 + 0.3) = 0.5$, giving \[ H_T = 2(0.5)(0.5) = 0.5 . \] Therefore \[ F_{ST} = \frac{0.5 - 0.42}{0.5} = \frac{0.08}{0.5} = 0.16 . \] An $F_{ST}$ of $0.16$ signals substantial differentiation: $16\%$ of the total heterozygosity is accounted for by the frequency difference between the two groups.

## Why it matters for association studies

Structure is a leading source of confounding in genetic epidemiology.

- If disease prevalence and allele frequency both vary across ancestral groups, pooling them produces a spurious correlation — the mechanism behind [population stratification](population-stratification.md) in a [GWAS](gwas.md).
- Methods that estimate and adjust for ancestry (principal components computed from genome-wide markers, mixed models) work precisely by controlling the structure that $F_{ST}$ measures; the leading axes are the [eigenvectors](eigenvalues-and-eigenvectors.md) of the genotype covariance matrix.
- Beyond confounding, $F_{ST}$ across the genome reflects demographic history: migration homogenizes ($F_{ST}\to 0$), while isolation and drift differentiate.

## In code

### R

```r
p <- c(0.7, 0.3)             # allele freqs in two equal-sized subpops
het <- function(p) 2 * p * (1 - p)
HS <- mean(het(p))           # 0.42
pbar <- mean(p)              # 0.5
HT <- het(pbar)              # 0.5
FST <- (HT - HS) / HT        # 0.16
c(HS = HS, HT = HT, FST = FST)
```

### Python

```python
import numpy as np
p = np.array([0.7, 0.3])          # two equal-sized subpopulations
het = lambda p: 2 * p * (1 - p)
HS = het(p).mean()                # 0.42
pbar = p.mean()                   # 0.5
HT = 2 * pbar * (1 - pbar)        # 0.5
FST = (HT - HS) / HT              # 0.16
print(HS, HT, FST)
```

<!-- python-output:auto -->
```text
0.42000000000000004 0.5 0.15999999999999992
```
<!-- /python-output:auto -->

### Julia

```julia
p = [0.7, 0.3]                    # two equal-sized subpopulations
het(p) = 2 .* p .* (1 .- p)
HS = mean(het(p))                 # 0.42
pbar = mean(p)                    # 0.5
HT = 2 * pbar * (1 - pbar)        # 0.5
FST = (HT - HS) / HT              # 0.16
println((HS, HT, FST))
```

## Why it matters

$F_{ST}$ turns a qualitative worry — "are my samples really one population?" — into a single number linking heterozygosity, among-group variance, and demographic history.
That number is both a lens on migration and isolation and a red flag for confounding, which is why quantifying and adjusting for structure is a non-negotiable step before trusting any genotype–phenotype association.

## Related

- [Hardy–Weinberg Equilibrium](hardy-weinberg.md)
- [Genetic Drift and the Wright–Fisher Model](genetic-drift.md)
- [Population Stratification](population-stratification.md)
- [GWAS](gwas.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Measures of Variability](measures-of-variability.md)
- [Quantitative Methods](../math.md)
