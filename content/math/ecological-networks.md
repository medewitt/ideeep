---
title: "Networks in Ecology and Epidemiology"
---

# Networks in Ecology and Epidemiology

Who eats whom, who pollinates whom, and who contacts whom are all networks, and their structure — not just their averages — shapes ecological stability and how fast a disease spreads.
The same graph-theoretic language links keystone species in a food web to superspreaders in an outbreak.

## Food webs

A food web is a directed [network](networks.md) of $S$ species with $L$ trophic links pointing from prey to predator.
A basic descriptor of how densely connected it is is the **connectance**,

\[
C = \frac{L}{S^2},
\]

the fraction of all $S^2$ possible directed links (including cannibalism) that are actually realized.
Connectance and the pattern of who interacts with whom feed directly into stability analysis: the signs and magnitudes of the interactions form the [community matrix](community-matrix.md), whose leading eigenvalue determines whether the equilibrium is stable.
Larger, more connected webs are, all else equal, harder to stabilize — the classic complexity–stability tension.

## Mutualistic networks

Plant–pollinator and plant–seed-disperser systems are **bipartite**: links run only between two disjoint sets (plants and animals), never within a set.
These webs are typically **nested** — specialists interact with proper subsets of the partners that generalists interact with — and **modular**, organizing into loosely coupled blocks.
Nestedness tends to spread the load of mutualistic support and is associated with more species being able to coexist, echoing the conditions studied in [competition and coexistence](competition-coexistence.md).

## Contact and transmission networks

For disease, the relevant network is who contacts whom.
Crucially, the *heterogeneity* of contacts, not just the mean, governs spread.
For a network built by the [configuration model](network-models.md) with degree distribution $p_k$, the basic reproduction number scales as

\[
R_0 \;\propto\; \frac{\langle k^2 \rangle}{\langle k \rangle},
\]

where $\langle k \rangle$ is the mean degree and $\langle k^2 \rangle$ is the mean squared degree.
Because $\langle k^2 \rangle = \langle k \rangle^2 + \operatorname{Var}(k)$, any variance in the number of contacts inflates the ratio above the mean, so a few very-high-degree individuals — superspreaders — can push $R_0$ far above what the average contact rate would suggest.
This is the network analogue of the [branching-process](branching-processes.md) view of early spread, and it is why [SIR](sir.md) dynamics on a heterogeneous network differ sharply from the well-mixed model.

### The percolation / spectral threshold

Whether an epidemic can take off is a percolation problem: it corresponds to the emergence of a giant connected component among the edges that actually transmit.
For a general contact graph, the epidemic threshold is tied to the **largest eigenvalue** $\lambda_1$ of the adjacency matrix $A$: spread is possible when the per-contact transmissibility exceeds roughly $1/\lambda_1$.
Since $\lambda_1$ grows with degree heterogeneity, highly heterogeneous networks have a very low threshold — outbreaks ignite easily.
This is also why targeting high-[centrality](centrality.md) nodes for vaccination or removal, which slashes $\lambda_1$, is so effective at raising the threshold and halting spread.

## Worked example: heterogeneity raises R₀

Compare two contact populations with the **same mean degree** $\langle k \rangle = 4$ but different variance.

**Homogeneous:** every one of 5 people has exactly 4 contacts, degrees $\{4,4,4,4,4\}$.
Then $\langle k \rangle = 4$, $\langle k^2 \rangle = \tfrac{1}{5}(5 \cdot 16) = 16$, so

\[
\frac{\langle k^2 \rangle}{\langle k \rangle} = \frac{16}{4} = 4.
\]

**Heterogeneous:** degrees $\{1,1,1,1,16\}$ — four near-isolates and one hub.
The mean is still $\langle k \rangle = \tfrac{1}{5}(1+1+1+1+16) = 4$, but $\langle k^2 \rangle = \tfrac{1}{5}(1+1+1+1+256) = 52$, so

\[
\frac{\langle k^2 \rangle}{\langle k \rangle} = \frac{52}{4} = 13.
\]

The two populations have identical average connectivity, yet the heterogeneous one has a ratio — and hence an $R_0$ — more than three times larger, driven entirely by the single hub.
Averages hide superspreading; the second moment reveals it.

## In code

We compute $\langle k \rangle$, $\langle k^2 \rangle$, and their ratio for the two degree sequences.

### R

```r
homog  <- c(4,4,4,4,4)
hetero <- c(1,1,1,1,16)

ratio <- function(k) mean(k^2) / mean(k)
ratio(homog)     # 4
ratio(hetero)    # 13
```

### Python

```python
import numpy as np

homog  = np.array([4,4,4,4,4])
hetero = np.array([1,1,1,1,16])

ratio = lambda k: (k**2).mean() / k.mean()
print(ratio(homog))    # 4.0
print(ratio(hetero))   # 13.0
```

### Julia

```julia
using Statistics

homog  = [4,4,4,4,4]
hetero = [1,1,1,1,16]

ratio(k) = mean(k.^2) / mean(k)
ratio(homog)     # 4.0
ratio(hetero)    # 13.0
```

## Why it matters

Ecological and epidemiological outcomes hinge on network structure that averages throw away.
In food webs, connectance and interaction pattern feed the [community matrix](community-matrix.md) and decide stability; in mutualistic webs, nestedness underpins coexistence; and in contact networks, the ratio $\langle k^2 \rangle / \langle k \rangle$ shows why degree heterogeneity fuels superspreading and lowers the epidemic threshold.
The unifying lesson is that a handful of structurally special nodes — keystones or superspreaders — carry outsized weight, so measuring and targeting them is the highest-leverage move in both conservation and disease control.

## Related

- [Networks and Graphs](networks.md)
- [Centrality and Node Importance](centrality.md)
- [Random Graph Models](network-models.md)
- [Compartmental Models (SIR)](sir.md)
- [The Next-Generation Matrix and R₀](next-generation-matrix.md)
- [The Community Matrix](community-matrix.md)
- [Branching Processes](branching-processes.md)
- [The Evolution of Cooperation](evolution-of-cooperation.md) — network reciprocity
- [Quantitative Methods](../math.md)
