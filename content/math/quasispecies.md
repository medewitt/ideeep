---
title: "Quasispecies and the Error Threshold"
description: "Eigen's quasispecies model: why a fast-mutating pathogen is a cloud of related genotypes selected as a unit, and how too much mutation triggers an error catastrophe."
---

# Quasispecies and the Error Threshold

An RNA virus does not replicate as a single genome that occasionally throws off a mutant.
Its polymerase is so error-prone — of order one mistake per genome per copy for many RNA viruses — that every infected host carries a *swarm* of closely related sequences, a mutant cloud centred on the fittest variant.
Eigen's **quasispecies** theory treats that whole cloud, not any one sequence, as the thing selection acts on, and it predicts a sharp limit: push the mutation rate past a critical **error threshold** and the cloud loses its centre entirely, an **error catastrophe** that erases the genetic information the population was built around.
This is the theory behind [lethal mutagenesis](resistance-evolution.md) as an antiviral strategy and the reason RNA viruses seem to sit precariously close to the edge of viability.

![Equilibrium frequency of the master sequence collapses to zero as the per-genome mutation rate crosses the error threshold at ln(sigma).](../assets/figures/quasispecies.svg)

## Mutation and selection as one operator

Label the possible genotypes $i = 1, \dots, n$ and let $x_i$ be the fraction of the population carrying genotype $i$, with $\sum_i x_i = 1$.
Genotype $j$ replicates with fitness $f_j$, but replication is imperfect: a copy of $j$ comes out as $i$ with probability $Q_{ij}$, the entries of a mutation matrix whose columns sum to one.
The two forces combine into a single reproduction operator $W_{ij} = f_j Q_{ij}$, and the quasispecies dynamics are the replicator equation \[ \dot x_i = \sum_j W_{ij}\, x_j - \phi\, x_i, \qquad \phi = \sum_{k} f_k x_k, \] where the outflow term $\phi$ is the mean fitness and simply keeps the frequencies normalised.
In discrete generations the same model is the map \[ x_i' = \frac{\sum_j f_j\, Q_{ij}\, x_j}{\bar f}, \qquad \bar f = \sum_j f_j x_j . \] Set $Q = I$ (perfect copying) and this collapses to ordinary [selection](selection-popgen.md): the fittest genotype fixes.
The mutation term is what couples the genotypes together, so the equilibrium is not a single winner but a stationary *distribution* — the quasispecies — and it is the leading eigenvector of $W$.

## The master sequence and its cloud

On a **single-peak landscape** one sequence, the *master*, replicates $\sigma$ times faster than every mutant: $f_0 = \sigma > 1$ and $f_i = 1$ for $i \neq 0$.
The equilibrium is a mutant cloud whose height falls off with Hamming distance (the number of differing sites) from the master.
Selection concentrates weight on the peak; mutation smears it outward; the balance sets the shape.
The subtle, important part is that selection does not maximise the fitness of the *most common* sequence — it maximises the mean fitness of the *whole cloud*.
A slightly lower peak surrounded by fit neighbours (a flat part of the landscape) can outcompete a taller peak surrounded by lethal mutants — the "survival of the flattest" effect that has no analogue in mutation-free selection.

## The error threshold

Whether the cloud even has a centre depends on how fast mutation erodes the master.
Let each of the $L$ sites copy correctly with fidelity $q$, so an error-free genome copy has probability \[ Q_{00} = q^{L} \equiv Q \approx e^{-L(1-q)} = e^{-U}, \qquad U = L\mu, \] writing $\mu = 1 - q$ for the per-site mutation rate and $U$ for the expected number of mutations per genome per replication.
Neglecting the rare back-mutations that land exactly on the master, the master sequence is maintained at equilibrium only while its fitness advantage survives the fidelity loss, \[ \sigma\, Q > 1, \] and its equilibrium frequency is \[ x_0 = \frac{\sigma Q - 1}{\sigma - 1} \quad\text{when } \sigma Q > 1, \qquad x_0 = 0 \text{ otherwise.} \] The inequality $\sigma Q > 1$ rearranges, via $Q \approx e^{-U}$, into a threshold on the genomic mutation rate: \[ U_c = \ln \sigma, \qquad\text{equivalently}\qquad L_{\max} \approx \frac{\ln \sigma}{\mu}. \] Below $U_c$ the cloud stays localised around the master; above it the master's frequency drops to zero, the distribution spreads uniformly over sequence space, and heredity fails — this delocalisation is the **error catastrophe**.
The threshold cuts both ways.
Read as $L_{\max} = \ln\sigma / \mu$, it caps how long a genome can be at a given fidelity, which is why the most error-prone replicators are also the shortest, and why no known RNA virus carries a genome much beyond $\sim\!30$ kb without evolving proofreading.

## Worked example

Take a genome of $L = 20$ sites and a master that replicates $\sigma = 4$ times faster than its mutants.
The threshold sits at $U_c = \ln 4 \approx 1.386$ mutations per genome, i.e. a per-site rate $\mu_c = U_c / L \approx 0.069$.
At a comfortable $\mu = 0.03$ the genome fidelity is $Q = 0.97^{20} \approx 0.544$, so $\sigma Q \approx 2.18 > 1$ and the master holds an equilibrium share \[ x_0 = \frac{2.18 - 1}{4 - 1} \approx 0.39. \] Push the polymerase to $\mu = 0.12$ and $Q = 0.88^{20} \approx 0.078$, giving $\sigma Q \approx 0.31 < 1$: the master is gone, $x_0 = 0$, and the population has fallen over the error threshold.

## Simulation

The closed form above ignores back-mutation.
To see the real cloud, iterate the exact mutation–selection map over Hamming *error classes*: group all sequences by their number of mismatches $k = 0,\dots,L$ from the master, give class $0$ fitness $\sigma$ and the rest fitness $1$, and move probability between classes with the binary mutation kernel (each of the $k$ wrong sites can revert, each of the $L-k$ right sites can mutate).
Iterating to equilibrium recovers the localised cloud below threshold and its collapse above.

### Python

```python
import numpy as np
from math import comb

def mutation_kernel(L, mu):
    # T[i, j] = P(class j -> class i) under independent per-site flips.
    T = np.zeros((L + 1, L + 1))
    for j in range(L + 1):          # start with j wrong sites
        for a in range(j + 1):      # a of them revert to the master
            for b in range(L - j + 1):  # b of the right sites mutate
                i = j - a + b
                T[i, j] += (comb(j, a) * mu**a * (1 - mu)**(j - a) *
                            comb(L - j, b) * mu**b * (1 - mu)**(L - j - b))
    return T

def equilibrium_master(L, mu, sigma, iters=2000):
    f = np.ones(L + 1); f[0] = sigma          # single-peak landscape
    T = mutation_kernel(L, mu)
    x = np.ones(L + 1) / (L + 1)              # start uniform
    for _ in range(iters):
        w = T @ (f * x)                        # select, then mutate
        x = w / w.sum()                        # renormalise
    return x[0]

L, sigma = 20, 4.0
for mu in (0.03, 0.069, 0.12):                # below, near, above U_c/L
    print(f"mu={mu:.3f}  U={L*mu:.2f}  x0={equilibrium_master(L, mu, sigma):.3f}")
print(f"error threshold U_c = ln(sigma) = {np.log(sigma):.3f}")
```

<!-- python-output:auto -->
```text
mu=0.030  U=0.60  x0=0.396
mu=0.069  U=1.38  x0=0.000
mu=0.120  U=2.40  x0=0.000
error threshold U_c = ln(sigma) = 1.386
```
<!-- /python-output:auto -->

### R

```r
mutation_kernel <- function(L, mu) {
  T <- matrix(0, L + 1, L + 1)
  for (j in 0:L) for (a in 0:j) for (b in 0:(L - j)) {
    i <- j - a + b
    T[i + 1, j + 1] <- T[i + 1, j + 1] +
      choose(j, a) * mu^a * (1 - mu)^(j - a) *
      choose(L - j, b) * mu^b * (1 - mu)^(L - j - b)
  }
  T
}

equilibrium_master <- function(L, mu, sigma, iters = 2000) {
  f <- rep(1, L + 1); f[1] <- sigma
  T <- mutation_kernel(L, mu)
  x <- rep(1 / (L + 1), L + 1)
  for (i in seq_len(iters)) { w <- T %*% (f * x); x <- w / sum(w) }
  x[1]
}

for (mu in c(0.03, 0.069, 0.12))
  cat(sprintf("mu=%.3f  x0=%.3f\n", mu, equilibrium_master(20, mu, 4)))
```

### Julia

```julia
function mutation_kernel(L, mu)
    T = zeros(L + 1, L + 1)
    for j in 0:L, a in 0:j, b in 0:(L - j)
        i = j - a + b
        T[i + 1, j + 1] += binomial(j, a) * mu^a * (1 - mu)^(j - a) *
                           binomial(L - j, b) * mu^b * (1 - mu)^(L - j - b)
    end
    T
end

function equilibrium_master(L, mu, sigma; iters = 2000)
    f = ones(L + 1); f[1] = sigma
    T = mutation_kernel(L, mu)
    x = fill(1 / (L + 1), L + 1)
    for _ in 1:iters
        w = T * (f .* x); x = w ./ sum(w)
    end
    x[1]
end

for mu in (0.03, 0.069, 0.12)
    println("mu=$mu  x0=", round(equilibrium_master(20, mu, 4.0), digits = 3))
end
```

## Why it matters

Quasispecies thinking reframes a fast-evolving pathogen as a distribution rather than a sequence, which changes what you measure and what you can do about it.
The mutant cloud is a reservoir of pre-existing [drug-resistance](resistance-evolution.md) and immune-escape variants, so therapy and immunity select from standing diversity rather than waiting for new mutations — one reason monotherapy fails so fast against HIV and hepatitis C. The error threshold turns the virus's own mutation rate into a target: antivirals such as favipiravir and molnupiravir work by nudging replication *over* the threshold, driving the population to the error catastrophe instead of trying to stop it.
And the survival-of-the-flattest effect means the fittest cloud is not always the one with the fittest peak, a warning against reading pathogen evolution off a single consensus genome.

## Related

- [Selection and Mutation–Selection Balance](selection-popgen.md)
- [Genetic Drift and the Wright–Fisher Model](genetic-drift.md)
- [The Evolution of Resistance](resistance-evolution.md)
- [Adaptive Dynamics and the Evolution of Virulence](evolution-of-virulence.md)
- [Within-Host Dynamics and the Immune Response](within-host-dynamics.md)
- [Quantitative Methods](../math.md)
