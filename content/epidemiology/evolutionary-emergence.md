---
title: "The Evolutionary Emergence of Pathogens"
description: "Emergence as a race between adaptation and extinction: how a subcritical spillover with R0 below one can evolve to R0 above one before demographic stochasticity wipes it out."
---

# The Evolutionary Emergence of Pathogens

Most pathogens that spill into humans are poorly adapted to the new host and start subcritical, with $R_0 < 1$, so each introduction is a stuttering chain destined to die out.
Emergence is the rare event where an adaptive mutation lifts $R_0$ above one *before* the chain goes extinct.
It is a race between adaptation and extinction, and the same [branching-process](../math/branching-processes.md) machinery that governs whether a [spillover](zoonotic-spillover.md) takes off also governs whether it can evolve its way to a pandemic ([Antia et al. 2003](https://doi.org/10.1038/nature02104)).

![Three panels: a stuttering wild-type transmission chain rescued when a mutation crosses the R0 = 1 threshold, the probability of emergence rising steeply as the initial R0 approaches one for several mutation supplies, and an evolutionary-rescue trajectory where a declining wild type is overtaken by a rising adapted type.](../assets/figures/evolutionary-emergence.svg)

## Emergence as evolutionary rescue

A subcritical introduction forms a [branching process](../math/branching-processes.md) whose mean offspring number is the wild-type reproduction number $R_w < 1$.
On its own that chain is doomed: extinction is certain.
But at each transmission the pathogen can mutate to an adapted type with $R_m > 1$, which then has a positive chance of establishing.
Emergence is evolutionary rescue in a transmission chain: a declining lineage saved by a variant that arises and spreads before the wild type burns out ([Antia et al. 2003](https://doi.org/10.1038/nature02104)).

## Probability of emergence

Two branching-process facts combine into the emergence probability.
A single adapted case establishes with probability $\pi = 1 - q_m$, where $q_m$ is the extinction probability of the adapted process, the smallest root of $q = G_m(q)$ for the mutant offspring generating function.
A subcritical wild-type chain seeded by one case produces, in expectation, $R_w/(1 - R_w)$ transmissions in total, the geometric sum of $R_w^k$.
If each transmission throws off an adapted mutant with probability $\mu$, treating rare mutant lineages as independent gives

\[
P_{\text{emerge}} \approx 1 - \exp\!\left(-\,\mu\,\frac{R_w}{1 - R_w}\,\pi\right).
\]

The whole story sits in the factor $R_w/(1 - R_w)$.
As $R_w \to 1^-$ it diverges, so a spillover that *almost* spreads lingers for many generations and gives adaptation many attempts.
A strain with $R_0$ just below one is therefore far more dangerous than its subcritical label suggests, and the dependence on initial $R_0$ is steep rather than gentle.

## What limits emergence

The simple formula assumes a single mutation suffices, but real adaptation is more constrained ([Gandon, Hochberg, Holt & Day 2013](https://doi.org/10.1098/rstb.2012.0086)).
When the jump to $R_0 > 1$ needs several mutations in sequence, each intermediate is itself subcritical and usually lost, so the path narrows sharply.
Emergence also depends on the *supply* of chains: a larger, longer-lived reservoir of spillover events means more independent attempts, and standing genetic variation in the reservoir can pre-load the adapted type instead of waiting for it to arise de novo.
These factors set how often the race is even run, not just whether a given chain wins it.

## The life history of emergence

Which adapted strains emerge is shaped by the disease's life history and its epidemiological feedbacks ([André & Day 2005](https://doi.org/10.1098/rspb.2005.3170)).
Because emergence selects among variants during the brief subcritical window, the strains that win are those that raise $R_0$ fastest, which is not always the eventual [evolutionarily optimal virulence](../math/evolution-of-virulence.md).
A variant that transmits early and hard can emerge even if it would later be outcompeted, so the trait distribution among emerging pathogens is biased by the emergence process itself, not just by long-run selection.

## A worked example

Take an adapted type with $n = 10$ contacts and per-contact transmission $p_m = 0.16$, so $R_m = 1.6$.
Solving $q = (1 - p_m + p_m q)^{10}$ gives an establishment probability $\pi \approx 0.6$.
With mutation probability $\mu = 2\times 10^{-3}$ per transmission, a wild type at $R_w = 0.8$ throws off $R_w/(1-R_w) = 4$ transmissions on average, so $P_{\text{emerge}} \approx 1 - e^{-2\times 10^{-3}\cdot 4\cdot 0.6} \approx 0.005$.
Push the wild type to $R_w = 0.95$ and it throws off $19$ transmissions, roughly quadrupling the emergence probability from the same mutation rate: the steep dependence on how close the spillover starts to threshold.

## In code

The executed block simulates the two-type branching process directly, seeding many subcritical chains that can mutate at each transmission, and estimates the emergence probability for two initial $R_0$ values.

### Python

```python
import numpy as np

rng = np.random.default_rng(1834)
n, pm, mu = 10, 0.16, 2e-3          # mutant contacts, per-contact risk, mutation prob
Rm = n * pm                          # adapted-type R0 = 1.6

def mutant_establishes():            # does one adapted lineage escape extinction?
    z = 1
    for _ in range(300):
        z = rng.binomial(n, pm, size=z).sum()
        if z == 0:
            return False
        if z > 500:                  # runaway growth counts as established
            return True
    return True

def emerges(Rw):                     # one subcritical spillover, adaptation allowed
    pw = Rw / n
    z = 1
    for _ in range(500):
        if z == 0:
            return False             # wild-type chain died before adapting
        kids = int(rng.binomial(n, pw, size=z).sum())
        n_mut = rng.binomial(kids, mu)
        for _ in range(n_mut):
            if mutant_establishes():
                return True
        z = kids - n_mut
    return False

n_sim = 30000
for Rw in (0.8, 0.95):
    p = np.mean([emerges(Rw) for _ in range(n_sim)])
    print(f"initial R0 = {Rw}:  P(emergence) ~ {p:.4f}")
```

<!-- python-output:auto -->
```text
initial R0 = 0.8:  P(emergence) ~ 0.0052
initial R0 = 0.95:  P(emergence) ~ 0.0218
```
<!-- /python-output:auto -->

### R

```r
set.seed(1834)
n <- 10; pm <- 0.16; mu <- 2e-3

mutant_establishes <- function() {
  z <- 1
  for (g in 1:300) {
    z <- sum(rbinom(z, n, pm))
    if (z == 0) return(FALSE)
    if (z > 500) return(TRUE)
  }
  TRUE
}

emerges <- function(Rw) {
  pw <- Rw / n; z <- 1
  for (g in 1:500) {
    if (z == 0) return(FALSE)
    kids <- sum(rbinom(z, n, pw))
    n_mut <- rbinom(1, kids, mu)
    if (n_mut > 0 && any(replicate(n_mut, mutant_establishes()))) return(TRUE)
    z <- kids - n_mut
  }
  FALSE
}

for (Rw in c(0.8, 0.95))
  cat(Rw, mean(replicate(30000, emerges(Rw))), "\n")
```

### Julia

```julia
using Random, Distributions, Statistics
Random.seed!(1834)
n, pm, mu = 10, 0.16, 2e-3

function mutant_establishes()
    z = 1
    for _ in 1:300
        z = sum(rand(Binomial(n, pm), z))
        z == 0 && return false
        z > 500 && return true
    end
    true
end

function emerges(Rw)
    pw = Rw / n; z = 1
    for _ in 1:500
        z == 0 && return false
        kids = sum(rand(Binomial(n, pw), z))
        n_mut = rand(Binomial(kids, mu))
        for _ in 1:n_mut
            mutant_establishes() && return true
        end
        z = kids - n_mut
    end
    false
end

for Rw in (0.8, 0.95)
    println(Rw, " ", mean(emerges(Rw) for _ in 1:30000))
end
```

## Why it matters

Evolutionary emergence is the quantitative core of pandemic-risk reasoning.
It explains why surveillance should worry most about spillovers that are *nearly* transmissible, since a pathogen at $R_0 = 0.95$ can be an order of magnitude more likely to emerge than one at $R_0 = 0.5$, and why cutting the mutation supply, by reducing the number and duration of spillover chains, lowers risk even when no single introduction looks threatening.
It ties [zoonotic spillover](zoonotic-spillover.md) to the [branching-process](../math/branching-processes.md) theory of extinction and to the [evolution of virulence](../math/evolution-of-virulence.md), making emergence a race whose odds we can estimate rather than a black swan we can only fear.

## Related

- [Zoonotic Spillover](zoonotic-spillover.md)
- [Branching Processes](../math/branching-processes.md)
- [Adaptive Dynamics and the Evolution of Virulence](../math/evolution-of-virulence.md)
- [The Next-Generation Matrix and R₀](../math/next-generation-matrix.md)
- [Epidemiology](../epidemiology.md)
