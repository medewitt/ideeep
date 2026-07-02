---
title: "Networks and Graphs"
---

# Networks and Graphs

A network encodes who is connected to whom — which hosts contact each other, which species eat which, which neurons wire together.
Turning that web of relationships into a matrix lets us bring the full machinery of linear algebra to bear on ecology and disease transmission.

## Nodes, edges, and the adjacency matrix

A **network** (or graph) is a set of **nodes** (vertices) joined by **edges** (links).
Write $N$ for the number of nodes and $E$ for the number of edges.
Edges may be **undirected** (a symmetric relationship, like a shared handshake) or **directed** (an ordered relationship, like "$i$ infects $j$"), and each edge may carry a **weight** recording contact frequency, flow, or interaction strength.

The structure is captured compactly by the **adjacency matrix** $A$, an $N\times N$ array whose entries record which pairs are connected: \[ A_{ij} = \begin{cases} 1 & \text{if nodes } i \text{ and } j \text{ are joined by an edge},\\ 0 & \text{otherwise.}\end{cases} \] For an undirected network $A$ is symmetric, $A_{ij}=A_{ji}$, whereas a directed network generally has $A_{ij}\neq A_{ji}$.
Writing a network this way — see [matrix notation](matrix-notation.md) — means that graph questions become [matrix operations](matrix-operations.md): the number of length-$2$ paths from $i$ to $j$ is the $(i,j)$ entry of $A^2$, and the [eigenvalues](eigenvalues-and-eigenvectors.md) of $A$ govern spreading dynamics, with the largest eigenvalue setting the epidemic threshold on a contact network.

## Degree and degree distribution

The **degree** $k_i$ of node $i$ is its number of connections, which for an undirected network is simply a row sum of the adjacency matrix: \[ k_i = \sum_{j=1}^{N} A_{ij}. \] In a directed network we distinguish the **in-degree** $k_i^{\text{in}}=\sum_j A_{ji}$ (edges pointing in) from the **out-degree** $k_i^{\text{out}}=\sum_j A_{ij}$ (edges pointing out).
The **degree distribution** $P(k)$ is the fraction of nodes with degree $k$, a probability distribution over the graph; its shape distinguishes homogeneous networks from heavy-tailed ones dominated by hubs.
The **mean degree** for an undirected network is \[ \langle k\rangle = \frac{2E}{N}, \] where the factor of $2$ appears because each of the $E$ edges contributes to the degree of both of its endpoints.

## Paths, components, and clustering

A **path** is a sequence of edges leading from one node to another, and the **shortest-path length** between two nodes is the fewest edges needed to connect them.
The largest shortest-path length over all pairs is the **diameter** of the network.
A **connected component** is a maximal set of nodes all mutually reachable by paths; when one component contains a finite fraction of all nodes as $N$ grows, it is called the **giant component**, and its emergence marks the point at which a pathogen can reach much of the population.

Local cohesion is measured by the **clustering coefficient** (transitivity), the probability that two neighbours of a node are themselves neighbours — "the friend of my friend is also my friend."
Overall sparsity is summarised by the **density** (connectance), the fraction of possible edges that are actually present: \[ \text{density} = \frac{E}{\binom{N}{2}} = \frac{2E}{N(N-1)}. \]

## Worked example: a 5-node graph

Take an undirected network on nodes $\{1,2,3,4,5\}$ with edges $\{1\!-\!2,\ 1\!-\!3,\ 2\!-\!3,\ 3\!-\!4,\ 4\!-\!5\}$, so $E=5$.
Its adjacency matrix is \[ A = \begin{bmatrix} 0 & 1 & 1 & 0 & 0\\ 1 & 0 & 1 & 0 & 0\\ 1 & 1 & 0 & 1 & 0\\ 0 & 0 & 1 & 0 & 1\\ 0 & 0 & 0 & 1 & 0 \end{bmatrix}. \] Summing each row gives the degrees $k_1=2,\ k_2=2,\ k_3=3,\ k_4=2,\ k_5=1$, which sum to $10=2E$ as they must.
The mean degree is $\langle k\rangle = 2E/N = 10/5 = 2$.
The density is $E/\binom{N}{2} = 5/\binom{5}{2} = 5/10 = 0.5$, so half of the ten possible edges are present.
Node $3$ is the most connected, and the whole graph is a single connected component (you can walk from node $5$ to node $1$), so its giant component contains all five nodes.

## In code

We build the example graph and read off its degrees, density, and components.

### R

```r
library(igraph)

g <- graph_from_literal(1-2, 1-3, 2-3, 3-4, 4-5)
degree(g)            # 1:2  2:2  3:3  4:2  5:1
mean(degree(g))      # 2
edge_density(g)      # 0.5
components(g)$no     # 1  (one connected component)
transitivity(g)      # global clustering coefficient
```

### Python

```python
import networkx as nx

g = nx.Graph([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
print(dict(g.degree()))                       # {1:2, 2:2, 3:3, 4:2, 5:1}
print(2 * g.number_of_edges() / g.number_of_nodes())  # 2.0
print(nx.density(g))                          # 0.5
print(nx.number_connected_components(g))      # 1
print(nx.transitivity(g))                     # global clustering
```

### Julia

```julia
using Graphs

g = SimpleGraph(5)
for (i, j) in [(1,2),(1,3),(2,3),(3,4),(4,5)]
    add_edge!(g, i, j)
end
degree(g)                       # [2, 2, 3, 2, 1]
2 * ne(g) / nv(g)               # 2.0
2 * ne(g) / (nv(g) * (nv(g)-1)) # 0.5  (density)
length(connected_components(g)) # 1
global_clustering_coefficient(g)
```

## Why it matters

Representing contact patterns, food webs, or gene-regulatory wiring as a graph turns qualitative "who interacts with whom" questions into quantitative ones.
The degree distribution predicts how fast an epidemic spreads and who the likely super-connectors are; the giant component tells you whether an outbreak can become widespread; connectance and clustering summarise how tightly an [ecological network](ecological-networks.md) is knit, which bears on its stability.
Because a network is just its adjacency matrix, node-importance scores (see [centrality](centrality.md)) and spreading thresholds follow directly from linear algebra, and comparing a real network against a [random-graph model](network-models.md) reveals which features are surprising rather than expected by chance.

## Related

- [Random-Graph Models](network-models.md)
- [Centrality](centrality.md)
- [Ecological Networks](ecological-networks.md)
- [Matrix Notation](matrix-notation.md)
- [Matrix Operations](matrix-operations.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Quantitative Methods](../math.md)
