---
title: "Quantitative Genetics and the Breeder's Equation"
---

# Quantitative Genetics and the Breeder's Equation

Most traits that matter — height, body mass, pathogen virulence, drug resistance — vary continuously because they are shaped by many genes of small effect acting together with the environment.
Quantitative genetics is the framework for such traits: it partitions their variation into heritable and non-heritable parts and predicts how a population responds when we select on them.

## Partitioning phenotypic variance

For a continuous trait, the phenotype $P$ of an individual is modelled as a genetic value plus an environmental deviation, $P = G + E$.
The genetic value itself splits into an additive part $A$ (the sum of average effects of the alleles carried) and non-additive parts from dominance and epistasis.
Assuming these components are uncorrelated, the total [phenotypic variance](measures-of-variability.md) decomposes as \[ V_P = V_A + V_D + V_E, \] where $V_A$ is the additive genetic variance, $V_D$ the dominance variance, and $V_E$ the environmental variance.
Only $V_A$ reflects effects that are transmitted predictably from parent to offspring, because offspring inherit alleles, not genotypes — the specific pairing that creates dominance is reshuffled each generation.

## Narrow-sense heritability

The fraction of phenotypic variance that is additive is the narrow-sense [heritability](heritability.md), \[ h^2 = \frac{V_A}{V_P}. \] It ranges from $0$ to $1$ and measures how faithfully phenotype predicts breeding value, so it is exactly the quantity that governs the response to selection.
It is a property of a particular population in a particular environment, not a fixed constant of the trait.

## The breeder's equation

Truncation or differential selection lets only some individuals reproduce.
The selection differential $S$ is the difference between the mean phenotype of the selected parents and the mean of the whole population before selection.
The response $R$ is the shift in the mean phenotype of the offspring generation relative to the parental population.
The breeder's equation links them through heritability: \[ R = h^2 S. \] The intuition is that selection acts on phenotypes but only the additive component is inherited, so the population moves a fraction $h^2$ of the way that the selected parents were displaced.
Standardizing the selection differential by the phenotypic standard deviation $\sigma_P$ defines the selection intensity $i = S/\sigma_P$, giving the equivalent form \[ R = h^2\, i\, \sigma_P. \] High heritability means selection is effective; when $h^2 \approx 0$ even strong selection produces almost no response, because the trait differences among parents are environmental and not passed on.

## Worked example

A population of plants has stem height with phenotypic mean $50$ cm and narrow-sense heritability $h^2 = 0.5$.
We select as parents only the tallest individuals, whose mean height is $60$ cm.
The selection differential is \[ S = 60 - 50 = 10 \text{ cm}. \] The predicted response is \[ R = h^2 S = 0.5 \times 10 = 5 \text{ cm}, \] so the offspring generation is expected to average $55$ cm.
If the heritability were only $h^2 = 0.1$, the same selection would yield $R = 1$ cm — the same effort, one-fifth of the gain.

## Simulation

Build additive breeding values for parents, impose selection, generate offspring whose breeding value is the mid-parent value plus fresh Mendelian and environmental noise, and check that the realized response matches $h^2 S$.

### R

```r
set.seed(1)
n  <- 100000
VA <- 0.5; VE <- 0.5          # so VP = 1, h2 = 0.5
h2 <- VA / (VA + VE)

A <- rnorm(n, 0, sqrt(VA))    # additive breeding values
P <- A + rnorm(n, 0, sqrt(VE))

# select top 20% as parents
thr  <- quantile(P, 0.80)
sel  <- P >= thr
S    <- mean(P[sel]) - mean(P) # selection differential

# offspring: mid-parent breeding value + Mendelian sampling + environment
pa <- sample(which(sel)); ma <- sample(which(sel))
Aoff <- (A[pa] + A[ma]) / 2 + rnorm(length(pa), 0, sqrt(VA / 2))
Poff <- Aoff + rnorm(length(pa), 0, sqrt(VE))
R <- mean(Poff) - mean(P)

c(S = S, predicted = h2 * S, observed = R)  # observed ~ h2 * S
```

### Python

```python
import numpy as np
rng = np.random.default_rng(1)

n = 100_000
VA, VE = 0.5, 0.5             # VP = 1, h2 = 0.5
h2 = VA / (VA + VE)

A = rng.normal(0, np.sqrt(VA), n)
P = A + rng.normal(0, np.sqrt(VE), n)

thr = np.quantile(P, 0.80)    # top 20% become parents
sel = np.where(P >= thr)[0]
S = P[sel].mean() - P.mean()

pa = rng.permutation(sel); ma = rng.permutation(sel)
Aoff = (A[pa] + A[ma]) / 2 + rng.normal(0, np.sqrt(VA / 2), len(pa))
Poff = Aoff + rng.normal(0, np.sqrt(VE), len(pa))
R = Poff.mean() - P.mean()

print(S, h2 * S, R)           # R ~ h2 * S
```

### Julia

```julia
using Statistics, Random
Random.seed!(1)

n = 100_000
VA, VE = 0.5, 0.5             # VP = 1, h2 = 0.5
h2 = VA / (VA + VE)

A = randn(n) .* sqrt(VA)
P = A .+ randn(n) .* sqrt(VE)

thr = quantile(P, 0.80)       # top 20%
sel = findall(P .>= thr)
S = mean(P[sel]) - mean(P)

pa = shuffle(sel); ma = shuffle(sel)
Aoff = (A[pa] .+ A[ma]) ./ 2 .+ randn(length(pa)) .* sqrt(VA / 2)
Poff = Aoff .+ randn(length(pa)) .* sqrt(VE)
R = mean(Poff) - mean(P)

(S, h2 * S, R)                # R ~ h2 * S
```

## Why it matters

The breeder's equation is the quantitative backbone of artificial selection in agriculture and of predicting evolution in the wild.
It tells a plant breeder how fast a yield trait can be improved, warns an epidemiologist how quickly a pathogen population may evolve resistance, and — because the same additive-variance logic underlies the regression of offspring on parents — connects directly to how heritability is estimated from field and pedigree data.

## Related

- [Heritability](heritability.md)
- [Selection and Mutation–Selection Balance](selection-popgen.md)
- [Measures of Variability](measures-of-variability.md)
- [Linear Regression](linear-regression.md)
- [Normal Distribution](normal-distribution.md)
- [Quantitative Methods](../math.md)
