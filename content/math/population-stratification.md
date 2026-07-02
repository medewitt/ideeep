---
title: "Population Stratification and PCA Control"
---

# Population Stratification and PCA Control

The most notorious confounder in association studies is ancestry: if the groups being compared differ in genetic background, the genome lights up with associations that have nothing to do with the trait.
Detecting and correcting this "population stratification" is what makes a [GWAS](gwas.md) trustworthy.

## The confounding mechanism

Population stratification arises when three things line up: the sample contains subpopulations, those subpopulations differ in allele frequency, and they also differ in the trait for reasons unrelated to that allele.
Then any SNP whose frequency tracks ancestry becomes correlated with the trait, producing a **spurious association**.
The classic illustration is a "chopsticks gene": in a sample mixing two ancestries, any variant more common in one group appears associated with chopstick use, purely through ancestry as the confounder.
This is exactly the confounding structure that good [experimental design](experimental-design.md) tries to break by balancing groups.

## Detecting inflation

If stratification is inflating associations, test statistics across the whole genome are systematically too large.
This shows up as an early, uniform lift of the QQ plot off its diagonal, quantified by the genomic inflation factor

\[
\lambda = \frac{\operatorname{median}(\chi^2_{\text{obs}})}{0.4549},
\]

the ratio of the observed median chi-square statistic to the null median expected for one degree of freedom.
A clean study has $\lambda \approx 1$; values well above $1$ (say $\lambda > 1.1$ at moderate sample sizes) flag confounding that must be corrected before trusting any hit.

## Correcting with principal components

The standard correction is to include the top principal components of the genotype matrix as covariates in every SNP regression.
Stack the standardized genotypes into an $n \times m$ matrix $Z$ (people by SNPs, each column centered and scaled).
The principal components are the leading [eigenvectors](eigenvalues-and-eigenvectors.md) of the genotype covariance $\tfrac{1}{n} Z^\top Z$ (equivalently the top singular vectors of $Z$):

\[
\tfrac{1}{n} Z^\top Z\, v_k = \lambda_k\, v_k .
\]

Because ancestry is the largest source of correlated allele-frequency variation, the leading eigenvectors are precisely the **axes of ancestry**, and each person's scores on them place them along those axes.
Adding the top few PCs as covariates lets the regression absorb ancestry, leaving $\hat{\beta}_j$ to reflect within-ancestry association only.
This is why stratification correction is, at heart, an eigenvalue/eigenvector computation on the genotype matrix — the same [population structure](population-structure.md) that PCA reveals is what it removes.

## Simulated example

Simulate two subpopulations of 300 people each.
A causal-looking SNP has effect-allele frequency $0.7$ in population A and $0.2$ in population B, and the trait mean is higher in A for reasons unrelated to genotype.
Regressing the trait on this SNP alone yields a strongly "significant" but entirely spurious association; adding the first principal component of the genome-wide genotypes as a covariate collapses it back toward null.

### R

```r
set.seed(42)
n <- 600; pop <- rep(c("A", "B"), each = 300)
# Genome-wide SNPs with ancestry-differentiated frequencies
freq <- ifelse(pop == "A", 0.7, 0.2)
G <- sapply(1:200, function(j) rbinom(n, 2, ifelse(pop=="A",
        runif(1,.5,.8), runif(1,.1,.4))))
snp <- rbinom(n, 2, freq)                 # candidate SNP, no true effect
y <- ifelse(pop == "A", 1, 0) + rnorm(n)  # trait differs by pop only

summary(lm(y ~ snp))$coefficients["snp", 4]     # tiny p: SPURIOUS

pcs <- prcomp(scale(G))$x[, 1:2]                 # top 2 PCs = ancestry
summary(lm(y ~ snp + pcs))$coefficients["snp", 4]  # p ~ non-significant
```

### Python

```python
import numpy as np, statsmodels.api as sm
from sklearn.decomposition import PCA

rng = np.random.default_rng(42)
n = 600; pop = np.array([0]*300 + [1]*300)          # 0=A, 1=B
G = np.column_stack([rng.binomial(2, np.where(pop==0,
        rng.uniform(.5,.8), rng.uniform(.1,.4))) for _ in range(200)]).astype(float)
snp = rng.binomial(2, np.where(pop==0, 0.7, 0.2)).astype(float)  # no true effect
y = (pop == 0).astype(float) + rng.normal(size=n)   # trait differs by pop

Zs = (G - G.mean(0)) / G.std(0)
print(sm.OLS(y, sm.add_constant(snp)).fit().pvalues[1])            # tiny: spurious
pcs = PCA(n_components=2).fit_transform(Zs)
X = sm.add_constant(np.column_stack([snp, pcs]))
print(sm.OLS(y, X).fit().pvalues[1])                              # non-significant
```

### Julia

```julia
using Statistics, GLM, DataFrames, LinearAlgebra, Random, Distributions
Random.seed!(42)
n = 600; pop = vcat(fill(0, 300), fill(1, 300))
G = Float64.(hcat([rand.(Binomial.(2, ifelse.(pop.==0, 0.65, 0.25))) for _ in 1:200]...))
snp = Float64.(rand.(Binomial.(2, ifelse.(pop.==0, 0.7, 0.2))))   # no true effect
y = Float64.(pop .== 0) .+ randn(n)

df = DataFrame(y=y, snp=snp)
println(coeftable(lm(@formula(y ~ snp), df)).cols[4][2])   # tiny p: spurious

Z = (G .- mean(G, dims=1)) ./ std(G, dims=1)
pcs = eigen(Symmetric(cov(Z))).vectors[:, end:-1:end-1]    # top 2 eigenvectors
scores = Z * pcs
df2 = DataFrame(y=y, snp=snp, pc1=scores[:,1], pc2=scores[:,2])
println(coeftable(lm(@formula(y ~ snp + pc1 + pc2), df2)).cols[4][2])  # non-sig
```

## Why it matters

Uncontrolled stratification produced a generation of unreplicable candidate-gene claims; PCA-based correction is the standard that helped GWAS become highly reproducible.
The idea generalizes: whenever a high-dimensional dataset hides latent group structure, projecting out the leading eigenvectors is a principled way to adjust for it.
Reporting $\lambda$ and PC-adjusted results is now a basic expectation of credible genetic analysis.

## Related

- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Population Structure](population-structure.md)
- [Genome-Wide Association Studies](gwas.md)
- [Experimental Design](experimental-design.md)
- [Quantitative Methods](../math.md)
