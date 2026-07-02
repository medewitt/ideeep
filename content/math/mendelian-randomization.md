---
title: "Mendelian Randomization"
---

# Mendelian Randomization

Mendelian randomization (MR) uses genetic variants as [instrumental variables](instrumental-variables.md) to estimate the causal effect of a modifiable exposure on an outcome.
Because alleles are randomly assigned from parents to offspring at conception (Mendel's law of segregation), they are largely independent of the lifestyle and environmental [confounders](experimental-design.md) that plague observational studies — giving MR the flavor of "nature's randomized trial."

## Genes as instruments

MR is instrumental-variable analysis in which the instrument is one or more single-nucleotide polymorphisms (SNPs).
The three IV assumptions translate into genetic language:

1. **Relevance.** The SNP is robustly associated with the exposure (a genome-wide-significant SNP–exposure association).
2. **Independence.** The SNP is independent of confounders — threatened chiefly by **population stratification** (systematic ancestry differences correlated with both genotype and outcome).
3. **Exclusion restriction.** The SNP affects the outcome **only through** the exposure.
   The main violation is **horizontal pleiotropy**, where a variant influences the outcome via a separate pathway.

Because random assignment happens at conception, MR is also robust to **reverse causation** — the outcome cannot alter the genotype one was born with.

## The ratio (Wald) estimate

For a single variant $j$, let $\hat\gamma_j$ be the estimated SNP–exposure association (change in exposure per allele) and $\hat\Gamma_j$ the SNP–outcome association (change in outcome per allele).
The per-variant causal estimate is the ratio

\[
\hat\beta_j = \frac{\hat\Gamma_j}{\hat\gamma_j},
\]

the outcome-per-allele effect divided by the exposure-per-allele effect — exactly the Wald IV ratio applied to genetic summary statistics.

## Inverse-variance-weighted (IVW) estimate

With many independent variants, the individual ratios are combined by a fixed-effect meta-analysis that weights each by its precision.
Using weights $w_j = 1/\operatorname{se}(\hat\Gamma_j)^2$,

\[
\hat\beta_{\text{IVW}} = \frac{\sum_j \hat\gamma_j \hat\Gamma_j \, w_j}{\sum_j \hat\gamma_j^2 \, w_j}.
\]

This is **algebraically identical** to the slope of a weighted linear regression of the SNP–outcome estimates $\hat\Gamma_j$ on the SNP–exposure estimates $\hat\gamma_j$ **through the origin**, with weights $w_j$.
The zero intercept encodes the exclusion restriction: a variant with no effect on the exposure should have no effect on the outcome.

## Threats and sensitivity analyses

The IVW estimate is consistent only if **every** variant satisfies the exclusion restriction.
Because horizontal pleiotropy is common, MR studies report [sensitivity analyses](sensitivity-analysis.md) that relax this in different ways:

- **MR-Egger.** Regress $\hat\Gamma_j$ on $\hat\gamma_j$ **with** an intercept.
  A non-zero intercept flags average directional pleiotropy; the slope stays consistent under the weaker InSIDE assumption.
- **Weighted median.** Consistent if at least half of the weight comes from valid instruments — robust to a minority of pleiotropic variants.

Agreement across these methods strengthens a causal claim.

## Worked example

Five independent SNPs with summary statistics $(\hat\gamma_j, \hat\Gamma_j, \operatorname{se}(\hat\Gamma_j))$:

| SNP | $\hat\gamma_j$ | $\hat\Gamma_j$ | $\operatorname{se}(\hat\Gamma_j)$ | ratio $\hat\Gamma_j/\hat\gamma_j$ |
|-----|------|------|------|-------|
| 1 | 0.20 | 0.061 | 0.020 | 0.305 |
| 2 | 0.35 | 0.104 | 0.025 | 0.297 |
| 3 | 0.10 | 0.031 | 0.030 | 0.310 |
| 4 | 0.50 | 0.152 | 0.018 | 0.304 |
| 5 | 0.25 | 0.073 | 0.022 | 0.292 |

The per-SNP ratios cluster near $0.30$.
The IVW formula (weights $1/\operatorname{se}^2$) pools them to a precision-weighted causal estimate of about $\hat\beta_{\text{IVW}} \approx 0.303$.

### R

```r
gamma <- c(0.20, 0.35, 0.10, 0.50, 0.25)   # SNP-exposure
Gamma <- c(0.061, 0.104, 0.031, 0.152, 0.073)  # SNP-outcome
se    <- c(0.020, 0.025, 0.030, 0.018, 0.022)   # se of Gamma
w     <- 1 / se^2

# Per-SNP Wald ratios
Gamma / gamma                               # ~ 0.305 0.297 0.310 0.304 0.292

# Manual IVW = weighted regression through the origin
coef(lm(Gamma ~ gamma - 1, weights = w))    # ~ 0.303

# Closed form
sum(gamma * Gamma * w) / sum(gamma^2 * w)   # ~ 0.303

# Package: MendelianRandomization (also see TwoSampleMR)
# library(MendelianRandomization)
# obj <- mr_input(bx = gamma, bxse = rep(0.01, 5), by = Gamma, byse = se)
# mr_ivw(obj)                               # Estimate ~ 0.303
```

### Python

```python
import numpy as np

gamma = np.array([0.20, 0.35, 0.10, 0.50, 0.25])   # SNP-exposure
Gamma = np.array([0.061, 0.104, 0.031, 0.152, 0.073])  # SNP-outcome
se    = np.array([0.020, 0.025, 0.030, 0.018, 0.022])  # se of Gamma
w = 1.0 / se**2

# Per-SNP Wald ratios
Gamma / gamma                               # ~ [0.305 0.297 0.310 0.304 0.292]

# IVW: weighted regression through origin (closed form)
beta_ivw = np.sum(gamma * Gamma * w) / np.sum(gamma**2 * w)
beta_ivw                                    # ~ 0.303
```

### Julia

```julia
gamma = [0.20, 0.35, 0.10, 0.50, 0.25]        # SNP-exposure
Gamma = [0.061, 0.104, 0.031, 0.152, 0.073]   # SNP-outcome
se    = [0.020, 0.025, 0.030, 0.018, 0.022]   # se of Gamma
w = 1.0 ./ se.^2

# Per-SNP Wald ratios
Gamma ./ gamma                                # ~ 0.305 0.297 0.310 0.304 0.292

# IVW: weighted regression through the origin (closed form)
beta_ivw = sum(gamma .* Gamma .* w) / sum(gamma.^2 .* w)   # ~ 0.303
```

## Why it matters for statistics

Mendelian randomization brings the logic of instrumental variables to genetic epidemiology, letting researchers probe causal effects of exposures — LDL cholesterol, alcohol, body-mass index — that would be unethical or impractical to randomize.
It shows how a purely observational summary dataset can support causal inference when the instrument assumptions hold, and it makes sensitivity analysis (pleiotropy diagnostics) an essential part of the workflow rather than an afterthought.

## Related

- [Instrumental Variables](instrumental-variables.md)
- [Experimental Design](experimental-design.md)
- [Hypothesis Testing](hypothesis-testing.md)
- [Global Sensitivity Analysis](sensitivity-analysis.md)
- [Statistical Inference](statistical-inference.md)
- [Quantitative Methods](../math.md)
