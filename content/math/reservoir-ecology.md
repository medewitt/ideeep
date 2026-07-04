---
title: "Reservoir Ecology"
description: "How maintenance hosts, spillover hosts, and the multi-host next-generation matrix decide whether a pathogen persists and where it comes from."
---

# Reservoir Ecology

Many pathogens that infect people do not depend on people to survive.
They circulate in one or more animal populations, the reservoir, and reach humans only through occasional spillover.
Working out which population sustains the pathogen, and whether any single host could do so alone, is the first question in the ecology of zoonotic and multi-host disease.

![Two host species each fail to maintain the pathogen alone, yet cross-species transmission lifts the community next-generation matrix above the persistence threshold; spillover reaches a dead-end human host.](../assets/figures/reservoir-ecology.svg)

## Reservoir, maintenance host, and spillover host

A **reservoir** is the population or community in which a pathogen is permanently maintained and from which it spills over into a target population such as humans.
The reservoir is defined by persistence, not by which host we happen to notice first.

Within a reservoir, hosts play different roles.

- A **maintenance host** can sustain the pathogen on its own: infection introduced into that host alone persists, which requires a per-host reproduction number above one, $R_0^{(i)} > 1$.
- A **spillover host** (or dead-end host) can be infected but does not pass enough infection onward to sustain transmission, $R_0^{(i)} < 1$.
  Humans are a dead-end host for rabies, West Nile virus, and most Ebola introductions: they get sick, but the chain of transmission usually dies out.

The distinction matters for control.
Vaccinating or culling a dead-end host does nothing to the reservoir; the pathogen keeps circulating in whatever population actually maintains it.
Rabies control in wildlife works because it targets the maintenance host (foxes, raccoon dogs), not the incidental human or livestock cases.

## The maintenance community

Sometimes no single host qualifies as a maintenance host, yet the pathogen persists.
This happens when transmission passes back and forth between species, so that infection dying out in one host is rekindled by another.
The set of hosts that jointly sustain the pathogen, none sufficient alone, is a **maintenance community**.

To decide persistence we cannot look at each host in isolation.
We need the multi-host [next-generation matrix](next-generation-matrix.md) $K$, whose entry $K_{ij}$ is the expected number of new infections in host type $i$ produced by one infectious individual of host type $j$ over its infectious lifetime.
The diagonal entry $K_{ii}$ is the single-host reproduction number: infection of type $i$ by type $i$.
The off-diagonal entries $K_{ij}$ ($i \neq j$) carry cross-species transmission.

Persistence is governed by the dominant eigenvalue of the whole matrix,

\[
R_0 = \rho(K),
\]

the community reproduction number.
The pathogen invades and persists when $\rho(K) > 1$.
A maintenance community is exactly the case where every diagonal entry is below one, $K_{ii} < 1$ for all $i$, yet $\rho(K) > 1$ because the off-diagonal coupling is strong enough.

## Which host is the reservoir?

Once $\rho(K) > 1$, the dominant right eigenvector tells us where infection concentrates at endemic equilibrium, and the dominant left eigenvector measures each host type's reproductive contribution.
A host whose removal drops $\rho(K)$ below one is a **critical** component of the reservoir: transmission collapses without it.
Field studies identify reservoirs by combining this reasoning with evidence that infection persists in the candidate host between spillover events, that the host is infected before spillover cases appear, and that phylogenies of pathogen sequences root in the animal population rather than in humans.

## A worked example

Take two host species, A and B, with the next-generation matrix

\[
K =
\begin{pmatrix}
0.7 & 0.5 \\
0.6 & 0.6
\end{pmatrix}.
\]

Read column by column: one infectious host A produces $0.7$ new A infections and $0.6$ new B infections; one infectious host B produces $0.5$ new A infections and $0.6$ new B infections.
Each species alone sits below threshold, $R_0^{(A)} = 0.7 < 1$ and $R_0^{(B)} = 0.6 < 1$, so neither could maintain the pathogen by itself.
The dominant eigenvalue of the full matrix is

\[
\rho(K) = \tfrac12\!\left(1.3 + \sqrt{1.3^2 - 4(0.7\cdot 0.6 - 0.5\cdot 0.6)}\right)
        = \tfrac12\!\left(1.3 + \sqrt{1.21}\right) = 1.2 > 1,
\]

so the two species together form a maintenance community even though each falls short alone.

## In code

We build the two-host next-generation matrix, read off each single-host reproduction number from the diagonal, and take the dominant eigenvalue for the community reproduction number.

### R

```r
K <- matrix(c(0.7, 0.6,
              0.5, 0.6), nrow = 2, byrow = FALSE)  # K[i, j]: i from j

single_host <- diag(K)                  # per-host R0
community   <- max(Mod(eigen(K)$values))

cat("single-host R0:", round(single_host, 2), "\n")
cat("community R0:  ", round(community, 3), "\n")
```

### Python

```python
import numpy as np

# Next-generation matrix K[i, j]: new infections in host i from host j.
K = np.array([[0.7, 0.5],
              [0.6, 0.6]])

single_host = np.diag(K)                       # per-host R0
community = np.max(np.abs(np.linalg.eigvals(K)))

print("single-host R0:", np.round(single_host, 2))
print("max single-host R0 < 1:", single_host.max() < 1)
print("community R0:", round(float(community), 3))
print("persists (community R0 > 1):", community > 1)
```

<!-- python-output:auto -->
```text
single-host R0: [0.7 0.6]
max single-host R0 < 1: True
community R0: 1.2
persists (community R0 > 1): True
```
<!-- /python-output:auto -->

### Julia

```julia
using LinearAlgebra

# K[i, j]: new infections in host i from one infectious host j.
K = [0.7 0.5;
     0.6 0.6]

single_host = diag(K)                    # per-host R0
community   = maximum(abs.(eigvals(K)))

@show single_host
@show community
```

## Why it matters

Whether a pathogen persists, and where it comes from, is a property of the whole host community, not of any species read in isolation.
Treating a dead-end host as the reservoir wastes control effort, and missing a maintenance community, where cross-species transmission does what no single host can, leaves a source of spillover intact.
The same next-generation-matrix reasoning that gives $R_0$ for a single population tells us which animals sustain Lyme disease, Nipah virus, or avian influenza, and which interventions would actually break the cycle.

## Related

- [Vector-Borne Disease Models](vector-borne.md)
- [Metapopulations and the Levins Model](metapopulations.md)
- [The Next-Generation Matrix and R₀](next-generation-matrix.md)
- [Ecological Networks](ecological-networks.md)
- [One Health Surveillance](../epidemiology/one-health-surveillance.md)
- [Quantitative Methods](../math.md)
