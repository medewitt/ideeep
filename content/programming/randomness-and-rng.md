---
title: "Randomness & Random Number Generation"
---

# Randomness & Random Number Generation

Stochastic simulation is the beating heart of mathematical biology — epidemic models, bootstraps, permutation tests, coalescent genealogies, MCMC.
All of it rests on the computer's ability to produce "random" numbers.
But a computer is a deterministic machine, so the numbers are not truly random at all: they are **pseudo-random**, produced by a formula that generates a stream of numbers with the *statistical properties* of randomness.

Understanding that one fact — the randomness is a reproducible illusion — is what lets you make your stochastic work both **correct** and **reproducible**.

## Pseudo-Random, and Why That's Good

A **pseudo-random number generator (PRNG)** starts from a **seed** and deterministically produces a long stream of numbers that look random.
Same seed, same stream — every time, on every machine.
Far from a limitation, this is exactly what you want: it makes a stochastic analysis **reproducible**.

**Always set a seed** at the top of any script that uses randomness.

```r
set.seed(2026)          # R
```

```julia
using Random; Random.seed!(2026)      # Julia
```

```python
import numpy as np
rng = np.random.default_rng(2026)     # Python: make a seeded generator
```

With the seed fixed, two runs produce identical draws — the foundation of a [reproducible](reproducibility.md) result:

```python
a = np.random.default_rng(42)
b = np.random.default_rng(42)
print(a.integers(0, 100, 6))
print(b.integers(0, 100, 6))    # identical stream
```

<!-- python-output:auto -->
```text
[ 8 77 65 43 43 85]
[ 8 77 65 43 43 85]
```
<!-- /python-output:auto -->

## Use a Modern Generator

Not all generators are equally good, and the defaults have improved.
A few practical rules:

- **In Python, use the modern `Generator` API** (`np.random.default_rng(seed)`), *not* the legacy global `np.random.seed()` / `np.random.rand()`.
  The new one uses a better algorithm (PCG64) and avoids a hidden global state that makes bugs hard to trace.
- **In R and Julia the built-in defaults are solid** (`set.seed` and `Random.seed!`); just set them explicitly.
- **Create a generator object and pass it around** rather than relying on hidden global state — it makes which code touches the random stream explicit.
- **Never build your own generator** (e.g. `x = (a*x + c) mod m`) for real work; homemade PRNGs have subtle correlations that silently bias results.

## Drawing From Any Distribution

Your generator gives you **uniform** numbers on $[0, 1]$.
Everything else is built from those.
The most fundamental construction is **inverse-CDF (inverse-transform) sampling**: if $U \sim \text{Uniform}(0,1)$, then $F^{-1}(U)$ has the distribution with CDF $F$.
For an $\text{Exponential}(\lambda)$ the inverse CDF is $x = -\ln(U)/\lambda$, so a stream of uniforms becomes a stream of exponential waiting times:

![Inverse-CDF sampling: uniform draws on the left, passed through x = -ln(U)/lambda, come out exponentially distributed on the right, matching the true exponential pdf.](../assets/figures/rng-inverse-cdf.svg)

```python
rng = np.random.default_rng(0)
u = rng.random(50_000)
x = -np.log(u) / 1.5                 # Exponential(rate = 1.5) by inverse-CDF
print(f"sample mean: {x.mean():.4f}    theory 1/rate: {1/1.5:.4f}")
```

<!-- python-output:auto -->
```text
sample mean: 0.6660    theory 1/rate: 0.6667
```
<!-- /python-output:auto -->

In practice you call the library's named sampler (`rexp`, `randexp`, `rng.exponential`), which uses inverse-CDF or a faster method internally.
When there is no tidy inverse CDF, **rejection sampling** is the general fallback: propose from an easy distribution and accept a fraction of draws so the survivors follow the target — the same principle underlying [MCMC](../math/mcmc.md).

```r
# R: named samplers, seeded
set.seed(0)
waits <- rexp(50000, rate = 1.5)     # exponential waiting times
counts <- rpois(50000, lambda = 3)   # Poisson event counts
```

```julia
# Julia
using Random, Distributions
rng = MersenneTwister(0)
waits = rand(rng, Exponential(1 / 1.5), 50_000)
```

## The Parallel-RNG Trap

This is the mistake that quietly corrupts big simulation studies — and mathematical biologists run big simulation studies.
When you spread replicates across cores or [cluster](hpc-clusters-slurm.md) jobs, it is tempting to seed each worker with the *same* seed, or with `seed = worker_id`.
Both are wrong: identical seeds make every worker produce the **same** "random" numbers (so your 1,000 replicates are really one replicate copied 1,000 times), and naively adjacent seeds can produce **overlapping or correlated** streams.

The right way is to derive **independent sub-streams** from one parent seed:

```python
# Python: spawn independent child generators from one seed
parent = np.random.SeedSequence(2026)
children = parent.spawn(1000)                 # one per replicate / worker
rngs = [np.random.default_rng(c) for c in children]
# worker i uses rngs[i] -- guaranteed independent, and fully reproducible
```

```r
# R: L'Ecuyer-CMRG streams are designed for parallel independence
RNGkind("L'Ecuyer-CMRG")
set.seed(2026)
# furrr / future automatically hand each worker an independent stream
```

```julia
# Julia: derive independent per-worker generators from one master seed
using Random
master = Xoshiro(2026)
rngs = [Xoshiro(rand(master, UInt64)) for _ in 1:1000]   # one per replicate
```

Do give every parallel worker an **independent, reproducible** stream from a single master seed.
Don't reuse one seed everywhere, and don't let workers share one global generator.

## Where Randomness Drives the Biology

- **Stochastic epidemic models** — Gillespie's algorithm draws the next event's time (inverse-CDF exponential) and type at every step; small populations need the stochasticity that ODEs smooth away — see the [stochastic epidemic](../math/stochastic-epidemics.md) and [branching process](../math/branching-processes.md) pages.
- **Bootstrap and permutation tests** — resampling the data to get confidence intervals and null distributions is pure random sampling.
- **Population genetics** — the [coalescent](../math/coalescent-theory.md) and [genetic drift](../math/genetic-drift.md) are simulated by random genealogies and allele sampling.
- **Bayesian inference** — [MCMC](../math/mcmc.md) explores the posterior through random proposals; reproducibility hinges on the seed.
- **Monte Carlo experiments** — estimating power, coverage, or extinction probability by averaging over many random runs (the [law of large numbers](../math/law-of-large-numbers.md) at work).

## Related

- [A Simulation Toolkit](simulation-toolkit.md) — structuring the simulation studies this feeds
- [Reproducibility](reproducibility.md) — seeds as a first-class part of a reproducible result
- [Running Jobs on an HPC Cluster (SLURM)](hpc-clusters-slurm.md) — parallel replicates and independent streams
- [MCMC](../math/mcmc.md) and [Stochastic Epidemic Models](../math/stochastic-epidemics.md) — randomness put to work
- [Programming & Computing](../programming.md)
