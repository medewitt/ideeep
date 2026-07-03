---
title: "Polygenic Scores"
---

# Polygenic Scores

Most common traits and diseases are not driven by one gene but by thousands of variants each nudging risk a little.
A polygenic score collapses all those tiny effects into a single number per person, turning the output of a [GWAS](gwas.md) into an individual-level predictor of disease risk or trait value.

## Definition

A polygenic (risk) score for person $i$ is a weighted sum of their trait-increasing alleles, with weights taken from GWAS effect estimates:

\[
\text{PGS}_i = \sum_{j} \hat{\beta}_j\, x_{ij},
\]

where $x_{ij} \in \{0, 1, 2\}$ is the dosage of the effect allele of SNP $j$ in person $i$ and $\hat{\beta}_j$ is that SNP's estimated per-allele effect (a log-odds ratio for disease, a slope for a quantitative trait).
Each person's score is just a dot product between their genotype vector and the vector of weights.
Because the score is additive across independent small effects, its distribution across a population is approximately Gaussian by the central limit theorem, and it is usually standardized to mean $0$, variance $1$ for interpretation.

## Construction

The weights $\hat{\beta}_j$ come from a large "training" GWAS, but two problems must be handled.
First, nearby SNPs are correlated through [linkage disequilibrium](linkage-disequilibrium.md), so raw summation would double-count the same signal.
Second, most SNPs carry no real effect, and including their noise degrades prediction.

Two families of methods address this:

- **Clumping + thresholding (C+T).** "Clump" correlated SNPs to keep one representative per LD region, then keep only SNPs passing a p-value threshold $p < p_T$.
  The threshold is tuned in a validation set.
- **Bayesian shrinkage.** Methods like LDpred and PRS-CS model all SNPs jointly, using a prior on effect sizes and an LD reference to shrink noisy weights toward zero rather than hard-thresholding.
  These usually predict better than C+T.

## Evaluation

A score is only as good as its out-of-sample prediction, assessed in an independent test set.
For a **quantitative trait**, report the variance explained,

\[
R^2 = \operatorname{cor}(\text{PGS}, y)^2,
\]

ideally the *incremental* $R^2$ beyond covariates like age, sex, and ancestry components.
For a **binary disease**, report the area under the ROC curve (AUC) or the odds ratio per standard deviation of the score.
These accuracies are bounded above by the trait's [heritability](heritability.md): a score can never explain more variance than genetics contributes.

### The transferability caveat

A crucial limitation: a score trained in one ancestry predicts substantially worse in others.
LD patterns, allele frequencies, and effect sizes differ across populations, so weights and the tag SNPs they ride on do not carry over.
Because most large GWAS have been conducted in European-ancestry samples, polygenic scores are markedly less accurate in African, East Asian, and other ancestries — an equity problem the field is actively working to fix.

## Worked example

Three independent SNPs have GWAS weights $\hat{\beta} = (0.3,\ -0.1,\ 0.5)$.
A person carries dosages $x = (2,\ 1,\ 0)$.
Their score is

\[
\text{PGS} = 0.3 \times 2 + (-0.1) \times 1 + 0.5 \times 0 = 0.6 - 0.1 + 0 = 0.5.
\]

Repeating this dot product for everyone in a sample yields a score per person, which we then correlate with the observed phenotype to gauge predictive accuracy.

## In code

### R

```r
set.seed(3)
beta <- c(0.3, -0.1, 0.5)                    # GWAS weights, 3 SNPs
n <- 400
G <- sapply(c(0.3, 0.5, 0.2), function(f) rbinom(n, 2, f))  # genotypes
pgs <- as.vector(G %*% beta)                 # one score per person
y <- pgs + rnorm(n, sd = 1)                  # phenotype (score + noise)

# Single person: dosages (2,1,0) -> score 0.5
sum(c(2, 1, 0) * beta)                        # 0.5

cor(pgs, y)^2                                 # R^2 ~ 0.35 (variance explained)
```

### Python

```python
import numpy as np
rng = np.random.default_rng(3)
beta = np.array([0.3, -0.1, 0.5])            # GWAS weights
n = 400
G = np.column_stack([rng.binomial(2, f, n) for f in (0.3, 0.5, 0.2)]).astype(float)
pgs = G @ beta                               # score per person
y = pgs + rng.normal(size=n)                 # phenotype

print(np.dot([2, 1, 0], beta))               # 0.5  (single individual)
print(np.corrcoef(pgs, y)[0, 1] ** 2)        # R^2 ~ 0.35
```

<!-- python-output:auto -->
```text
0.5
0.0901190504815184
```
<!-- /python-output:auto -->

### Julia

```julia
using Statistics, Random, Distributions
Random.seed!(3)
beta = [0.3, -0.1, 0.5]                       # GWAS weights
n = 400
G = Float64.(hcat([rand(Binomial(2, f), n) for f in (0.3, 0.5, 0.2)]...))
pgs = G * beta                                # score per person
y = pgs .+ randn(n)                           # phenotype

println(dot([2, 1, 0], beta))                 # 0.5  (single individual)
println(cor(pgs, y)^2)                        # R^2 ~ 0.35
```

## Why it matters

Polygenic scores are moving from research tool toward clinical use — flagging people at high genetic risk for heart disease, breast cancer, or diabetes for earlier screening.
They connect several ideas on this site: GWAS supplies the weights, heritability caps their accuracy, and their genetic construction lets them serve as instruments in [Mendelian randomization](mendelian-randomization.md).
Their poor cross-ancestry transfer is also a stark reminder that a statistical tool inherits the biases of the data it was trained on.

## Related

- [Genome-Wide Association Studies](gwas.md)
- [Heritability and Variance Components](heritability.md)
- [Mendelian Randomization](mendelian-randomization.md)
- [Measures of Variability](measures-of-variability.md)
- [Quantitative Methods](../math.md)
