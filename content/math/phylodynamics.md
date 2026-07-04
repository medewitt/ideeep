---
title: "Phylodynamics"
description: "Reading epidemic and evolutionary dynamics off the shape of a time-resolved pathogen phylogeny."
---

# Phylodynamics

Pathogen genomes carry a record of the epidemic that produced them.
As a virus or bacterium spreads it also mutates, so the branching pattern and timing of a phylogeny built from sampled sequences encode how the pathogen population grew, shrank, and moved.
Phylodynamics reads epidemiological quantities — prevalence, growth rate, the reproduction number — directly off the shape of a time-scaled tree.

![A time-scaled coalescent genealogy of five samples beside a skyline estimate of the effective population size N_e(t), which rises during epidemic growth and plateaus.](../assets/figures/phylodynamics.svg)

## How a tree encodes dynamics

A time-resolved phylogeny places every internal node — each common ancestor — at a calendar date.
The spacing of those nodes is the signal.
When the infected population is large and growing, lineages rarely share a recent ancestor, so coalescences are spread far apart near the tips.
When the population is small, lineages find common ancestors quickly and the tree is bushy and shallow.
Two modeling traditions turn this intuition into inference: the coalescent, which conditions on the tree and links node spacing to population size, and birth-death models, which treat transmission and sampling as explicit events.

## The coalescent and effective size

The [coalescent](coalescent-theory.md) runs the genealogy backward in time.
With $k$ ancestral lineages in a population of effective size $N_e$, each of the $\binom{k}{2}$ pairs merges at rate $1/N_e$, so the waiting time to the next coalescence is exponential with rate $\binom{k}{2}/N_e$:

\[
T_k \sim \text{Exponential}\!\left(\frac{\binom{k}{2}}{N_e}\right),
\qquad \mathbb{E}[T_k] = \frac{2 N_e}{k(k-1)} .
\]

Coalescence rate scales inversely with $N_e$, so a genealogy with widely spaced nodes implies a large effective size and one with tightly packed nodes implies a small one.
For a pathogen, $N_e$ tracks the number of infections through which the lineage is transmitted, so it moves with prevalence over the course of an epidemic.
Allowing $N_e = N_e(t)$ to vary and estimating it in pieces gives the **skyline plot**, a nonparametric reconstruction of population size through time from the observed coalescence times.

## Birth-death models and $R_0$

An alternative describes the tree forward in time with a **birth-death-sampling process**: infected lineages transmit (branch) at rate $\lambda$, become uninfectious (die) at rate $\mu$, and are sampled at rate $\psi$.
Under this generative model the basic reproduction number is

\[
R_0 = \frac{\lambda}{\mu + \psi},
\]

so fitting a birth-death model to a dated tree estimates $R_0$ and the sampling fraction directly, a natural companion to the renewal-equation view of [$R_t$](reproduction-number-rt.md).
Because each transmission event is an explicit birth, the birth-death family connects phylodynamics to the theory of [branching processes](branching-processes.md), where the same $R_0$ threshold separates outbreaks that fade from those that grow.

## The molecular clock sets the timescale

Neither view works until the tree is measured in calendar time rather than in substitutions.
The [molecular clock](molecular-clock.md) supplies the conversion: if substitutions accumulate at an approximately constant rate $r$ per site per year, then genetic distance is proportional to elapsed time, and dating the tips by their sampling dates lets us date every internal node and the time to the most recent common ancestor.
A time-scaled tree is the shared input to both the coalescent and birth-death analyses above.

## A worked example

Suppose a constant-$N_e$ coalescent produced a genealogy of $n = 5$ sampled sequences with the coalescence waiting times

\[
T_5 = 40,\quad T_4 = 55,\quad T_3 = 130,\quad T_2 = 380 \text{ years.}
\]

Each epoch with $k$ lineages waits at expected rate $\binom{k}{2}/N_e$, so the maximum-likelihood estimate pools the epochs by their coalescence pressure $\binom{k}{2}$:

\[
\hat{N}_e = \frac{\sum_{k=2}^{n} \binom{k}{2}\, T_k}{n - 1}.
\]

The weights are $\binom{5}{2}=10,\ \binom{4}{2}=6,\ \binom{3}{2}=3,\ \binom{2}{2}=1$, giving

\[
\hat{N}_e = \frac{10(40) + 6(55) + 3(130) + 1(380)}{4}
= \frac{400 + 330 + 390 + 380}{4} = 375 .
\]

The lone two-lineage epoch waits far longer than the crowded five-lineage epoch, yet each contributes comparable information once weighted by $\binom{k}{2}$.

## In code

### R

```r
# Estimate constant Ne from coalescence waiting times.
Tk <- c(40, 55, 130, 380)      # epochs k = 5,4,3,2
k  <- 5:2
w  <- choose(k, 2)             # C(k,2) coalescence pressure
Ne_hat <- sum(w * Tk) / (length(Tk))
Ne_hat                          # 375
```

### Python

```python
import numpy as np
rng = np.random.default_rng(1834)


def coalescent_times(n, Ne, rng):
    """Simulate epoch waiting times and their C(k,2) weights."""
    times, weights = [], []
    for k in range(n, 1, -1):
        c = k * (k - 1) / 2
        times.append(rng.exponential(Ne / c))  # rate c/Ne -> scale Ne/c
        weights.append(c)
    return np.array(times), np.array(weights)


Ne_true, n, reps = 1000.0, 10, 300
num, den = 0.0, 0
for _ in range(reps):
    t, w = coalescent_times(n, Ne_true, rng)
    num += np.sum(w * t)     # pooled numerator sum C(k,2) T_k
    den += len(t)            # pooled coalescence count reps*(n-1)
Ne_hat = num / den           # maximum-likelihood estimate

print(f"true Ne      = {Ne_true:.0f}")
print(f"estimated Ne = {Ne_hat:.1f}")
```

<!-- python-output:auto -->
```text
true Ne      = 1000
estimated Ne = 1010.5
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Distributions
Random.seed!(1834)

function coalescent_times(n, Ne)
    times = Float64[]; weights = Float64[]
    for k in n:-1:2
        c = k * (k - 1) / 2
        push!(times, rand(Exponential(Ne / c)))  # rate c/Ne -> scale Ne/c
        push!(weights, c)
    end
    times, weights
end

Ne_true, n, reps = 1000.0, 10, 300
num, den = 0.0, 0
for _ in 1:reps
    t, w = coalescent_times(n, Ne_true)
    num += sum(w .* t); den += length(t)
end
println("estimated Ne = ", round(num / den, digits = 1))
```

## Why it matters

Phylodynamics turns a pathogen's genome sequences into an independent readout of epidemic dynamics, complementing case counts that are often incomplete or lagged.
Skyline reconstructions of $N_e(t)$ have traced the hidden early growth of HIV, hepatitis C, and Ebola, while birth-death estimates of $R_0$ from dated trees supported real-time situational awareness during SARS-CoV-2 spread.
Because the inference rests only on sampled sequences and their dates, it recovers transmission history even where surveillance is sparse.

## Related

- [The Coalescent](coalescent-theory.md)
- [The Molecular Clock](molecular-clock.md)
- [Branching Processes](branching-processes.md)
- [The Effective Reproduction Number and Forecasting](reproduction-number-rt.md)
- [Adaptive Dynamics](adaptive-dynamics.md)
- [Quantitative Methods](../math.md)
