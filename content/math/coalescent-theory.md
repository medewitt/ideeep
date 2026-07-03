---
title: "The Coalescent"
---

# The Coalescent

The coalescent looks at a population's genealogy backward in time: starting from a sample of sequences today, ancestral lineages merge — coalesce — until they reach a single common ancestor.
This backward view is the engine of modern pathogen phylodynamics, letting us read effective population sizes, epidemic growth, and divergence times straight off a phylogenetic tree.

## Coalescence of two lineages

Consider two sampled gene copies in a Wright–Fisher population with effective size $N_e$ (diploid, $2N_e$ gene copies; here we use the haploid convention with $N_e$ copies for cleaner formulas).
Going back one generation, the two lineages share a parent with [probability](probability-basics.md) $1/N_e$.
The number of generations until they coalesce is therefore geometric with success probability $1/N_e$, and for large $N_e$ it is well approximated by an [exponential distribution](exponential-distribution.md): \[ T_2 \sim \text{Exponential}(\text{rate} = 1/N_e), \qquad \mathbb{E}[T_2] = N_e \text{ generations.} \] So two random lineages typically trace back to a common ancestor about $N_e$ generations ago.

## Many lineages

With $k$ ancestral lineages, any of the $\binom{k}{2}$ pairs could be the next to coalesce.
Each pair coalesces at rate $1/N_e$, so the total rate of coalescence is $\binom{k}{2}/N_e$, and the waiting time until the number of lineages drops from $k$ to $k-1$ is exponential: \[ T_k \sim \text{Exponential}\!\left(\text{rate} = \frac{\binom{k}{2}}{N_e}\right), \qquad \mathbb{E}[T_k] = \frac{N_e}{\binom{k}{2}} = \frac{2 N_e}{k(k-1)} . \] Because $\binom{k}{2}$ is large when many lineages remain, early coalescences (many lineages) happen fast and the last one — the merge from two lineages to one — takes by far the longest.
The waiting times are independent, a direct use of the memoryless [exponential](exponential-distribution.md) property.

### Time to the most recent common ancestor

The time to the most recent common ancestor (TMRCA) of a sample of $n$ is the sum of the independent waiting times as the lineage count falls from $n$ down to $1$: \[ T_{\text{MRCA}} = \sum_{k=2}^{n} T_k, \qquad \mathbb{E}[T_{\text{MRCA}}] = \sum_{k=2}^{n} \frac{2 N_e}{k(k-1)} = 2 N_e \left(1 - \frac{1}{n}\right). \] Notice the striking result: even for very large samples the expected TMRCA approaches $2N_e$, never much more, because the final two-lineage epoch dominates.

### Total tree length

The total branch length of the genealogy sums, over each epoch with $k$ lineages, that epoch's duration times the $k$ lineages present: \[ \mathbb{E}[T_{\text{total}}] = \sum_{k=2}^{n} k \cdot \mathbb{E}[T_k] = \sum_{k=2}^{n} k \cdot \frac{2N_e}{k(k-1)} = 2 N_e \sum_{i=1}^{n-1} \frac{1}{i} . \] The harmonic sum $\sum_{i=1}^{n-1} 1/i$ grows only logarithmically, so total tree length — and hence the expected number of neutral mutations, and thus genetic diversity — increases slowly with sample size.

## Worked example

Take $N_e = 1000$ and a sample of $n = 4$ lineages.
The expected waiting times per epoch are \[ \mathbb{E}[T_4] = \frac{2(1000)}{4\cdot 3} = 166.7,\quad \mathbb{E}[T_3] = \frac{2(1000)}{3\cdot 2} = 333.3,\quad \mathbb{E}[T_2] = \frac{2(1000)}{2\cdot 1} = 1000 . \] Summing gives the expected TMRCA: \[ \mathbb{E}[T_{\text{MRCA}}] = 166.7 + 333.3 + 1000 = 1500 \text{ generations}, \] which matches $2N_e(1 - 1/n) = 2000(1 - 1/4) = 1500$.
The expected total tree length is \[ \mathbb{E}[T_{\text{total}}] = 2(1000)\left(1 + \tfrac12 + \tfrac13\right) = 2000 \cdot 1.8333 = 3666.7 \text{ generations}, \] and note how the two-lineage epoch alone ($1000$ generations) accounts for two-thirds of the TMRCA.

## Simulation

### R

```r
set.seed(42)
sim_tmrca <- function(n, Ne) {
  total <- 0
  for (k in n:2) {
    rate <- choose(k, 2) / Ne
    total <- total + rexp(1, rate)   # waiting time in the k-lineage epoch
  }
  total
}
tmrca <- replicate(10000, sim_tmrca(4, 1000))
mean(tmrca)   # ~ 1500, matching 2*Ne*(1 - 1/n)
```

### Python

```python
import numpy as np
rng = np.random.default_rng(42)

def sim_tmrca(n, Ne):
    total = 0.0
    for k in range(n, 1, -1):
        rate = (k * (k - 1) / 2) / Ne     # C(k,2)/Ne
        total += rng.exponential(1 / rate)  # numpy uses scale = 1/rate
    return total

tmrca = np.array([sim_tmrca(4, 1000) for _ in range(10000)])
print(tmrca.mean())   # ~ 1500, matching 2*Ne*(1 - 1/n)
```

<!-- python-output:auto -->
```text
1487.0811141773204
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Distributions
Random.seed!(42)

function sim_tmrca(n, Ne)
    total = 0.0
    for k in n:-1:2
        rate = (k * (k - 1) / 2) / Ne     # C(k,2)/Ne
        total += rand(Exponential(1 / rate))  # Exponential takes the scale
    end
    total
end

tmrca = [sim_tmrca(4, 1000) for _ in 1:10_000]
println(mean(tmrca))   # ~ 1500, matching 2*Ne*(1 - 1/n)
```

## Why it matters

The coalescent is the probabilistic backbone linking sampled sequences to the demographic history that produced them.
Because coalescence rates scale inversely with $N_e$, a genealogy inferred from pathogen genomes encodes the effective population size and its changes over an epidemic, and the same tree — read forward with a mutation rate — underlies the [molecular clock](molecular-clock.md) dating of divergence events.

## Related

- [Genetic Drift and the Wright–Fisher Model](genetic-drift.md)
- [Molecular Clock](molecular-clock.md)
- [Exponential Distribution](exponential-distribution.md)
- [Probability Basics](probability-basics.md)
- [Expected Value](expected-value.md)
- [Simulation Toolkit](../programming/simulation-toolkit.md)
- [Quantitative Methods](../math.md)
