---
title: "Centrality and Node Importance"
---

# Centrality and Node Importance

Centrality measures rank the nodes of a network by their structural importance, turning a vague notion like "keystone species" or "superspreader" into a number you can compute.
Different measures capture different kinds of importance — raw connectivity, reach, brokerage, or influence — and each suggests a different node to protect, vaccinate, or remove.

![A network with nodes sized and colored by eigenvector centrality, highlighting the most influential nodes.](../assets/figures/centrality.svg)

## Setting

A network on $n$ nodes is described by its adjacency matrix $A$, where $A_{ij} = 1$ if there is an edge from $i$ to $j$ and $0$ otherwise (see [networks](networks.md)).
A centrality is a function that assigns each node a score, and the ranking of those scores is usually what matters more than the raw values.

## Degree centrality

The simplest measure is the [degree](networks.md) $k_i$: the number of edges incident to node $i$.

\[
k_i = \sum_{j=1}^{n} A_{ij}.
\]

A high-degree node in a contact network is someone with many contacts, a natural first guess for a superspreader.
Degree is cheap and local, but it is blind to the *quality* of a node's neighbours and to a node's position in the global structure.

## Closeness centrality

Closeness rewards nodes that can reach everyone else quickly.
Let $d(i,j)$ be the shortest-path distance from $i$ to $j$.
Closeness is the inverse of the mean distance to all other nodes,

\[
C_i = \frac{n-1}{\sum_{j \ne i} d(i,j)}.
\]

A node with high closeness sits near the "centre" of the network, so a rumour or pathogen starting there tends to saturate the population fastest.

## Betweenness centrality

Betweenness identifies bridges and brokers — nodes that lie on many shortest paths and therefore control flow between otherwise separated regions.
Let $\sigma_{st}$ be the number of shortest paths from $s$ to $t$, and $\sigma_{st}(i)$ the number of those that pass through $i$.

\[
B_i = \sum_{s \ne i \ne t} \frac{\sigma_{st}(i)}{\sigma_{st}}.
\]

Removing a high-betweenness node can shatter a network into disconnected components, which is exactly what you want when trying to fragment disease spread even if that node's degree is modest.

## Eigenvector centrality

Degree counts neighbours equally, but influence is recursive: a node is important if it is connected to *other important* nodes.
Writing each node's score as proportional to the sum of its neighbours' scores gives

\[
x_i = \frac{1}{\lambda_1} \sum_{j=1}^{n} A_{ij}\, x_j,
\qquad\text{i.e.}\qquad
A\mathbf{x} = \lambda_1 \mathbf{x}.
\]

The centrality vector $\mathbf{x}$ is the leading [eigenvector](eigenvalues-and-eigenvectors.md) of $A$ — the one paired with the largest eigenvalue $\lambda_1$.
Because $A$ is non-negative, the Perron–Frobenius theorem guarantees this leading eigenvector has all-positive entries, so every node gets a sensible positive score.
**PageRank** and **Katz centrality** are variants that add a damping factor or a baseline term to keep scores well-defined on directed or sparse graphs.

## Worked example

Consider an undirected "paw" graph on nodes $\{1,2,3,4\}$: a triangle on $1,2,3$ plus a pendant node $4$ attached only to node $1$.
Its adjacency matrix is

\[
A = \begin{bmatrix}
0 & 1 & 1 & 1 \\
1 & 0 & 1 & 0 \\
1 & 1 & 0 & 0 \\
1 & 0 & 0 & 0
\end{bmatrix}.
\]

### Degree centrality

Summing rows gives degrees $k_1 = 3,\ k_2 = 2,\ k_3 = 2,\ k_4 = 1$.
By degree, node $1$ is the clear hub.

### Eigenvector centrality

We seek $\mathbf{x}$ with $A\mathbf{x} = \lambda_1 \mathbf{x}$.
The characteristic polynomial factors so that the dominant root satisfies $\lambda_1 \approx 2.170$.
Solving $(A - \lambda_1 I)\mathbf{x} = 0$ and normalizing so the largest entry is $1$ gives approximately

\[
\mathbf{x} \approx (1.000,\ 0.740,\ 0.740,\ 0.461).
\]

Node $1$ leads on both measures, but notice the pendant node $4$ — degree $1$ — still scores $0.461$ because its only neighbour is the most important node.
Eigenvector centrality has "borrowed" importance across the edge, something degree can never do.

## In code

Each library reports the same four centralities; results match the worked example up to normalization.

### R

```r
library(igraph)

A <- rbind(c(0,1,1,1),
           c(1,0,1,0),
           c(1,1,0,0),
           c(1,0,0,0))
g <- graph_from_adjacency_matrix(A, mode = "undirected")

degree(g)                          # 3 2 2 1
round(eigen_centrality(g)$vector, 3)  # 1.000 0.740 0.740 0.461
round(closeness(g), 3)
round(betweenness(g), 3)           # node 1 is the only broker
```

### Python

```python
import numpy as np
import networkx as nx

A = np.array([[0,1,1,1],
              [1,0,1,0],
              [1,1,0,0],
              [1,0,0,0]])
G = nx.from_numpy_array(A)

print(dict(G.degree()))                        # {0:3, 1:2, 2:2, 3:1}
ev = nx.eigenvector_centrality_numpy(G)
print({k: round(v/max(ev.values()), 3) for k, v in ev.items()})
# {0: 1.0, 1: 0.74, 2: 0.74, 3: 0.461}
print({k: round(v, 3) for k, v in nx.betweenness_centrality(G).items()})
```

### Julia

```julia
using Graphs, LinearAlgebra

A = [0 1 1 1;
     1 0 1 0;
     1 1 0 0;
     1 0 0 0]
g = SimpleGraph(A)

degree(g)                                       # [3, 2, 2, 1]
ev = eigenvector_centrality(g)
round.(ev ./ maximum(ev), digits = 3)           # [1.0, 0.74, 0.74, 0.461]
round.(betweenness_centrality(g), digits = 3)
```

## Why it matters

Centrality translates "which node matters?" into arithmetic you can act on.
In food webs, high-centrality species are candidate keystones whose loss cascades through the community (see [ecological networks](ecological-networks.md)); in contact networks, high-degree and high-eigenvector nodes are the superspreaders, and high-betweenness nodes are the bridges between communities.
Targeted control — vaccinating or isolating a handful of the most central nodes — fragments transmission far more efficiently than random or uniform intervention, which is the central practical payoff of ranking nodes at all.

## Related

- [Networks and Graphs](networks.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Random Graph Models](network-models.md)
- [Networks in Ecology and Epidemiology](ecological-networks.md)
- [Quantitative Methods](../math.md)
