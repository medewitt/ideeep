---
title: "Genome-Wide Association Studies"
---

# Genome-Wide Association Studies

A genome-wide association study (GWAS) scans millions of genetic variants across the genome to find those statistically associated with a trait or disease.
It is the workhorse of modern genetic epidemiology, turning a table of genotypes and phenotypes into a map of the genome's contribution to human variation.

![Left: a Manhattan plot of −log₁₀ p across the genome, where null variants form a low noisy band and a tower of correlated SNPs on one chromosome rises above the genome-wide significance line at 5×10⁻⁸. Right: QQ plots comparing a well-controlled study (λ ≈ 1, points tracking the diagonal until a few true hits pull away) with a confounded one (λ ≫ 1, the whole cloud lifting off the diagonal early).](../assets/figures/gwas.svg "fig:gwas")

## The basic test

The unit of a GWAS is a single-nucleotide polymorphism (SNP): a position where individuals carry one of two alleles.
For each person we encode the genotype as an **allele dosage** $x_{ij} \in \{0, 1, 2\}$, the number of copies of the effect allele that individual $i$ carries at SNP $j$.
For each SNP we fit a regression of the phenotype on that dosage plus covariates.

For a **quantitative trait** $y$ (height, blood pressure, LDL cholesterol) we use linear regression:

\[
y_i = \alpha + \beta_j\, x_{ij} + \sum_k \delta_k c_{ik} + \varepsilon_i,
\]

where the $c_{ik}$ are covariates (age, sex, ancestry components).
For a **case/control** phenotype we use logistic regression, modeling the log-odds of being a case:

\[
\operatorname{logit}\Pr(y_i = 1) = \alpha + \beta_j\, x_{ij} + \sum_k \delta_k c_{ik}.
\]

The additive coding means $\beta_j$ is the per-allele effect: the expected change in the trait (or log-odds) for each extra copy of the effect allele.

## Effect estimates and p-values

Each SNP regression returns an estimate $\hat{\beta}_j$, its standard error $\operatorname{se}(\hat{\beta}_j)$, and a Wald test statistic

\[
z_j = \frac{\hat{\beta}_j}{\operatorname{se}(\hat{\beta}_j)},
\]

from which a [p-value](p-values.md) is computed by comparing to a normal (or chi-square) reference — a standard [hypothesis test](hypothesis-testing.md) run once per SNP.
Because a GWAS runs this test hundreds of thousands to millions of times, it is a massive [multiple-testing](multiple-testing.md) problem.

### The genome-wide significance threshold

Naively declaring "significant" at $\alpha = 0.05$ would produce tens of thousands of false positives.
The field instead uses a Bonferroni-style threshold that accounts for roughly one million effectively independent tests across the common variation of the human genome:

\[
\frac{0.05}{10^6} = 5 \times 10^{-8}.
\]

A SNP is declared genome-wide significant when its $p < 5 \times 10^{-8}$.
The count is "effective" rather than literal because nearby SNPs are correlated through [linkage disequilibrium](linkage-disequilibrium.md), so the millions of tested SNPs behave like about a million independent ones.

## Manhattan and QQ plots

Two plots summarize a GWAS ([@fig:gwas]).
The **Manhattan plot** shows $-\log_{10} p$ for every SNP against genomic position; real signals appear as skyscraper-like towers of correlated SNPs rising above the horizon line at $5 \times 10^{-8}$.
The **QQ plot** compares the observed distribution of $-\log_{10} p$ to the uniform distribution expected under the global null; points should track the diagonal until a few true hits pull away at the top-right tail.

### Genomic inflation factor

Systematic early departure of the whole QQ plot from the diagonal signals confounding.
It is quantified by the genomic inflation factor $\lambda$, the ratio of the observed median chi-square statistic to its null expectation:

\[
\lambda = \frac{\operatorname{median}(\chi^2_{\text{obs}})}{0.4549}.
\]

A well-controlled study has $\lambda \approx 1$; $\lambda \gg 1$ warns of inflation.

## Confounders

The two classic confounders are:

- **Population stratification.** If ancestry correlates with both allele frequency and the trait, SNPs that merely track ancestry look associated.
  The standard fix is to include the top principal components of the genotype matrix as covariates — see [population stratification](population-stratification.md).
- **Relatedness.** Cryptic relatives and family structure violate the independence assumption.
  Linear **mixed models** absorb this by adding a random effect with covariance given by a genetic relatedness matrix.

## Worked example

Suppose we regress a standardized quantitative phenotype on a single SNP's dosage in $n = 500$ people.
The fit returns $\hat{\beta} = 0.18$ with $\operatorname{se}(\hat{\beta}) = 0.045$.
The test statistic is $z = 0.18 / 0.045 = 4.0$, giving a two-sided $p = 2\,\Pr(Z \ge 4.0) \approx 6.3 \times 10^{-5}$.
This clears the nominal $0.05$ bar easily but falls short of genome-wide significance ($5 \times 10^{-8}$), so in a real scan it would not yet count as a discovery.

## In code

### R

```r
set.seed(1)
n <- 500; m <- 5                     # 500 people, 5 SNPs
G <- matrix(rbinom(n * m, 2, 0.3), n, m)   # dosages 0/1/2, MAF 0.3
y <- 0.4 * G[, 3] + rnorm(n)         # SNP 3 truly affects y

# Test every SNP with lm, collect effect + p-value
res <- t(apply(G, 2, function(g) {
  s <- summary(lm(y ~ g))$coefficients["g", ]
  c(beta = s[1], p = s[4])
}))
res
# SNP 3 has the largest |beta| and smallest p (~1e-30)

# For case/control use glm(status ~ g, family = binomial)
```

### Python

```python
import numpy as np, statsmodels.api as sm

rng = np.random.default_rng(1)
n, m = 500, 5
G = rng.binomial(2, 0.3, size=(n, m)).astype(float)   # dosages 0/1/2
y = 0.4 * G[:, 2] + rng.normal(size=n)                 # SNP index 2 real

for j in range(m):
    X = sm.add_constant(G[:, j])
    fit = sm.OLS(y, X).fit()
    print(j, round(fit.params[1], 3), f"{fit.pvalues[1]:.1e}")
# SNP 2 (0-indexed) shows the strongest effect and smallest p
# Logistic: sm.Logit(status, X).fit()
```

<!-- python-output:auto -->
```text
0 0.051 4.6e-01
1 0.044 5.0e-01
2 0.446 5.4e-11
3 0.039 5.6e-01
4 -0.029 6.7e-01
```
<!-- /python-output:auto -->

### Julia

```julia
using GLM, DataFrames, Random, Distributions
Random.seed!(1)
n, m = 500, 5
G = Float64.(rand(Binomial(2, 0.3), n, m))   # dosages 0/1/2
y = 0.4 .* G[:, 3] .+ randn(n)               # SNP 3 real

for j in 1:m
    df = DataFrame(g = G[:, j], y = y)
    fit = lm(@formula(y ~ g), df)
    println(j, "  β=", round(coef(fit)[2], digits=3),
            "  p=", coeftable(fit).cols[4][2])
end
# SNP 3 has the largest effect and smallest p
```

## Why it matters

GWAS has identified tens of thousands of robust trait-associated loci, seeding drug targets, biological hypotheses, and downstream tools.
Its outputs feed directly into [polygenic scores](polygenic-scores.md) that sum many small effects for prediction, into [heritability](heritability.md) estimates from genome-wide data, and into Mendelian randomization for causal inference.
The study design is also a lesson in disciplined statistics: honest multiple-testing control and careful confounder adjustment are what separate real biology from artifacts.

## Related

- [p-Values](p-values.md)
- [Hypothesis testing](hypothesis-testing.md)
- [Multiple Testing and False Discovery Rate](multiple-testing.md)
- [Population Stratification and PCA Control](population-stratification.md)
- [Linkage Disequilibrium](linkage-disequilibrium.md)
- [Polygenic Scores](polygenic-scores.md)
- [Heritability and Variance Components](heritability.md)
- [Quantitative Methods](../math.md)
