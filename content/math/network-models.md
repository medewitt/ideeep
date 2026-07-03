---
title: "Random-Graph Models"
---

# Random-Graph Models

Real contact networks and food webs are messy, so we need generative models that explain how their structure could arise and that serve as null models — the baseline you compare data against to decide what is surprising.
The choice of model shapes everything downstream, because degree heterogeneity governs whether a pathogen fizzles or explodes.

![Degree distributions: Erdős–Rényi is Poisson-like (left) while a scale-free network has a heavy power-law tail (right).](../assets/figures/network-models.svg)

## The Erdős–Rényi random graph

The simplest model is the **Erdős–Rényi** random graph $G(N,p)$: start with $N$ [nodes](networks.md) and connect each of the $\binom{N}{2}$ possible pairs independently with probability $p$.
Because every node has $N-1$ potential partners each realised with probability $p$, the degree of a node is a sum of independent Bernoulli trials, so it follows a [binomial distribution](binomial-distribution.md) with mean \[ \langle k\rangle = (N-1)\,p. \] For large $N$ and small $p$ with $\langle k\rangle$ fixed, this binomial converges to a [Poisson distribution](poisson-distribution.md), \[ P(k) \approx e^{-\langle k\rangle}\frac{\langle k\rangle^{\,k}}{k!}, \] which is sharply peaked about its mean: the network is **homogeneous**, with almost every node having a similar number of contacts and hubs essentially absent.

A defining feature of $G(N,p)$ is a **sharp giant-component threshold**.
When the mean degree crosses $\langle k\rangle = 1$, the largest connected component abruptly jumps from tiny ($O(\log N)$ nodes) to giant (a finite fraction of the whole network).
For an epidemic, this phase transition is the difference between a few isolated cases and a population-wide outbreak.

## Configuration model and scale-free networks

The Erdős–Rényi model produces one specific degree distribution, but often we want to fix the degrees and randomise everything else.
The **configuration model** does exactly this: it takes a prescribed **degree sequence**, gives each node that many half-edges ("stubs"), and then wires the stubs together in random pairs.
It is the standard null model for asking whether a network property is explained by its degree distribution alone or requires something more.

Many real networks are far from homogeneous: their degree distribution is a **power law**, \[ P(k) \propto k^{-\gamma}, \] typically with exponent $2 < \gamma < 3$.
Such **scale-free** networks have a **heavy tail** — a small number of enormously connected **hubs** coexist with many low-degree nodes.
One mechanism that generates them is **Barabási–Albert preferential attachment**: nodes are added one at a time and preferentially link to nodes that are already well connected, a "rich get richer" rule that concentrates edges onto early, popular nodes.
A hallmark of the heavy tail is that the second moment $\langle k^2\rangle$ can be very large — even diverging as $N\to\infty$ when $\gamma \le 3$ — even though the mean $\langle k\rangle$ stays finite.

## Small-world networks

A third stylised fact is that many networks are **small-world**: they have high local clustering (like a regular lattice) yet short average path lengths (like a random graph).
The **Watts–Strogatz** model reproduces this by starting from a ring lattice and randomly rewiring a small fraction of edges; those few long-range shortcuts collapse path lengths dramatically while leaving most of the local triangles intact.

## Why degree heterogeneity matters

The contrast between a Poisson network and a scale-free one is not academic.
Hubs act as **super-spreaders**: in an epidemic on a scale-free contact network, the epidemic threshold is pushed down (and, in the idealised limit $\langle k^2\rangle \to \infty$, can vanish entirely), so diseases invade at transmission rates that a homogeneous network would suppress.
The same heterogeneity governs **robustness**: scale-free networks tolerate random node failures gracefully but collapse quickly when their hubs are removed — which is exactly why targeting highly connected individuals (high [centrality](centrality.md)) for vaccination or removal is so effective.

## Simulation: comparing degree distributions

We generate an Erdős–Rényi graph and a Barabási–Albert graph with the same size and compare their degree distributions: the first is tightly peaked, the second is heavy-tailed with clear hubs.

### R

```r
library(igraph)
set.seed(1)

er <- sample_gnp(n = 1000, p = 4 / 999)   # <k> ~ 4, Poisson-like
ba <- sample_pa(n = 1000, m = 2, directed = FALSE)  # power law

mean(degree(er)); max(degree(er))   # ~4    ;  ~11  (thin tail)
mean(degree(ba)); max(degree(ba))   # ~4    ;  ~90+ (a few hubs)
```

### Python

```python
import networkx as nx
import numpy as np
rng = np.random.default_rng(1)

er = nx.gnp_random_graph(1000, 4 / 999, seed=1)
ba = nx.barabasi_albert_graph(1000, 2, seed=1)

er_deg = [d for _, d in er.degree()]
ba_deg = [d for _, d in ba.degree()]
print(np.mean(er_deg), max(er_deg))  # ~4,  ~12   (Poisson: thin tail)
print(np.mean(ba_deg), max(ba_deg))  # ~4,  ~90+  (scale-free: hubs)
```

<!-- python-output:auto -->
```text
3.984 11
3.992 87
```
<!-- /python-output:auto -->

### Julia

```julia
using Graphs, Statistics, Random
Random.seed!(1)

er = erdos_renyi(1000, 4 / 999)
ba = barabasi_albert(1000, 2)

println((mean(degree(er)), maximum(degree(er))))  # (~4, ~12)  thin tail
println((mean(degree(ba)), maximum(degree(ba))))  # (~4, ~90+) hubs
```

Both graphs share a mean degree near $4$, but the Barabási–Albert graph's maximum degree is many times larger — the visible signature of hubs and a heavy tail.

## Why it matters

Random-graph models supply the null hypotheses of network science: to claim a food web is unusually clustered or a contact network unusually hub-dominated, you compare it against Erdős–Rényi or configuration-model ensembles with matched size and degrees.
They also make the mechanistic point that microscopic wiring rules — independent edges, preferential attachment, or local rewiring — produce macroscopically different worlds for spreading and stability.
Above all, they show why degree heterogeneity is decisive: the same average number of contacts can hide super-spreading hubs that shift epidemic thresholds and reshape which interventions work on an [ecological network](ecological-networks.md) or a population.

## Related

- [Networks and Graphs](networks.md)
- [Centrality](centrality.md)
- [Ecological Networks](ecological-networks.md)
- [Poisson Distribution](poisson-distribution.md)
- [Binomial Distribution](binomial-distribution.md)
- [Quantitative Methods](../math.md)
