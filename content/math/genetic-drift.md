---
title: "Genetic Drift and the Wright–Fisher Model"
---

# Genetic Drift and the Wright–Fisher Model

Genetic drift is the random change in allele frequency that happens simply because a finite population is a finite sample of gametes each generation.
It matters wherever population sizes are small — bottlenecked pathogen lineages, isolated host demes, founder events after a colonization — because there chance, not selection, can drive an allele all the way to fixation or loss.

## The Wright–Fisher model

The Wright–Fisher model is the simplest idealization of drift.
A population of $N$ diploid individuals carries $2N$ gene copies at a locus; each generation is formed by drawing $2N$ alleles with replacement from the current pool.
If the current frequency of allele $A$ is $p$, the number of copies in the next generation is a binomial draw: \[ X' \sim \text{Binomial}(2N, p), \qquad p' = \frac{X'}{2N}. \] This is exactly the [binomial distribution](binomial-distribution.md) applied to allele sampling, and it makes the behavior of drift easy to characterize.

### Mean and variance

Because the sampling is unbiased, the expected next-generation frequency equals the current one: \[ \mathbb{E}[p'] = \frac{2N p}{2N} = p . \] So drift has no preferred direction — on average nothing changes.
What changes is the spread.
The [variance](measures-of-variability.md) of the new frequency is \[ \operatorname{Var}(p') = \frac{p(1-p)}{2N} . \] The $2N$ in the denominator is the whole story: in a large population the variance is tiny and frequencies barely move, while in a small population the same formula produces large random jumps.
Here $p$ is treated as a [random variable](random-variables.md) whose expectation is preserved but whose uncertainty accumulates.

## Consequences of drift

Run the process long enough and three robust facts emerge.

- Absorption: with no mutation, every allele eventually reaches fixation ($p = 1$) or loss ($p = 0$); these are the only stable states because $\operatorname{Var}(p')=0$ there.
- Fixation probability: because $\mathbb{E}[p']=p$ every generation, the probability that allele $A$ is the one ultimately fixed equals its current frequency, $\Pr(\text{fixation}) = p$.
- Loss of heterozygosity: the expected heterozygosity $H = 2p(1-p)$ decays geometrically, losing a fraction $\tfrac{1}{2N}$ per generation:
\[
\mathbb{E}[H_{t+1}] = \left(1 - \frac{1}{2N}\right)\mathbb{E}[H_t] .
\]
So genetic variation erodes at a rate set entirely by population size.

### Effective population size

Real populations violate the Wright–Fisher assumptions — unequal sex ratios, variable offspring number, overlapping generations, fluctuating size.
The effective population size $N_e$ is the size of an ideal Wright–Fisher population that would drift (lose heterozygosity) at the same rate as the real one.
It is almost always smaller than the census size, and it is $N_e$, not the head count, that governs the formulas above and the [coalescent](coalescent-theory.md) timescale.

## Worked example

Start an allele at frequency $p = 0.5$ in a population of $N = 25$ diploids, so $2N = 50$ gene copies.
The next generation's frequency has expectation $0.5$ and variance \[ \operatorname{Var}(p') = \frac{0.5 \cdot 0.5}{50} = 0.005, \] a standard deviation of about $\sqrt{0.005} \approx 0.071$.
So a single generation typically shifts the frequency by roughly $7$ percentage points either way.
The probability that this allele is eventually fixed is just its current frequency, $0.5$, and the expected heterozygosity decays by a factor $1 - 1/50 = 0.98$ per generation — about a $2\%$ loss of variation each generation in this small population.

## Simulation

### R

```r
set.seed(1)
drift <- function(N, p0, gens) {
  p <- numeric(gens + 1); p[1] <- p0
  for (t in 1:gens) p[t + 1] <- rbinom(1, 2 * N, p[t]) / (2 * N)
  p
}
reps <- replicate(1000, drift(N = 25, p0 = 0.5, gens = 100)[101])
mean(reps == 1)  # ~ 0.5 : fraction fixed matches starting frequency
mean(reps == 0)  # ~ 0.5 : fraction lost
```

### Python

```python
import numpy as np
rng = np.random.default_rng(1)

def drift(N, p0, gens):
    p = p0
    for _ in range(gens):
        p = rng.binomial(2 * N, p) / (2 * N)
    return p

reps = np.array([drift(25, 0.5, 100) for _ in range(1000)])
print((reps == 1).mean())  # ~ 0.5 : fraction fixed ~ starting frequency
print((reps == 0).mean())  # ~ 0.5 : fraction lost
```

### Julia

```julia
using Random, Distributions
Random.seed!(1)

function drift(N, p0, gens)
    p = p0
    for _ in 1:gens
        p = rand(Binomial(2N, p)) / (2N)
    end
    return p
end

reps = [drift(25, 0.5, 100) for _ in 1:1000]
println(mean(reps .== 1))  # ~ 0.5 : fraction fixed
println(mean(reps .== 0))  # ~ 0.5 : fraction lost
```

## Why it matters

Genetic drift is the neutral null against which selection is judged: any explanation invoking adaptation must beat what chance sampling alone would produce.
Because its strength scales as $1/(2N_e)$, drift dominates in the small, fluctuating populations typical of pathogens and founder events, shaping standing variation, the fate of new mutations, and the genealogies that phylodynamic inference reads backward in time.

## Related

- [Hardy–Weinberg Equilibrium](hardy-weinberg.md)
- [Coalescent Theory](coalescent-theory.md)
- [Population Structure and F_ST](population-structure.md)
- [Binomial Distribution](binomial-distribution.md)
- [Expected Value](expected-value.md)
- [Measures of Variability](measures-of-variability.md)
- [Simulation Toolkit](../programming/simulation-toolkit.md)
- [Quantitative Methods](../math.md)
