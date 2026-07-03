---
title: "Graph & Network Algorithms"
---

# Graph & Network Algorithms

A great deal of biology is fundamentally about **connections**: who contacted whom in an outbreak, which genes regulate which, which species eat which, how reads overlap into a genome.
The natural representation is a **graph** — a set of **nodes** joined by **edges** — and a handful of classic graph algorithms answer the questions you actually ask of these networks.

The [Math side](../math/networks.md) of this program covers network *models* — degree distributions, [centrality](../math/centrality.md), [ecological networks](../math/ecological-networks.md).
This page is about the *algorithms*: how a computer actually traverses a graph and computes things on it.

## Graphs and How They're Stored

A graph is nodes plus edges.
Edges can be **undirected** (a contact between two people) or **directed** (gene A regulates gene B), and **weighted** (a distance, a transmission probability) or not.

How you store the graph determines what is cheap — a [data-structures](data-structures.md) choice:

- An **adjacency list** (a [hash map](data-structures.md) from each node to its neighbours) is compact for the *sparse* networks common in biology and makes "who are my neighbours?" instant.
  This is the default.
- An **adjacency matrix** (an `n × n` grid of 0/1) is simple and good for dense graphs, but costs `O(n²)` memory — prohibitive for a network of 100,000 nodes.

Traversing a graph with an adjacency list costs `O(V + E)` (nodes plus edges) — linear, and fast.

## Breadth-First Search: Explore in Layers

**Breadth-first search (BFS)** starts at a node and visits the graph in expanding **layers**: all neighbours first, then *their* neighbours, and so on.
In an unweighted graph BFS finds the **shortest path** (fewest edges) from the start to every other node — and in an outbreak that shortest path length is exactly the **transmission generation**.

![A contact network with nodes coloured by breadth-first-search distance from the index case; each layer outward is one more transmission generation, showing BFS distance equals generation number.](../assets/figures/graph-bfs-transmission.svg)

## Depth-First Search: Go Deep

**Depth-first search (DFS)** instead follows one path as far as it can before backtracking.
It is the tool for **cycle detection** (is there a feedback loop in this regulatory network?), **topological sorting** (ordering steps that depend on each other), and exploring tree/graph structure — closely related to the [recursion](recursion-and-dynamic-programming.md) that walks a phylogeny.

## Connected Components: Who Is Reachable

A **connected component** is a set of nodes all reachable from one another.
Finding components (a few BFS/DFS sweeps) answers a genuinely epidemiological question: **which cases form one linked cluster**, and which outbreaks are actually separate.
The same operation identifies isolated subpopulations in a contact network or disconnected contigs in an assembly graph.

```python
import networkx as nx

G = nx.Graph()
G.add_edges_from([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"),
                  ("D", "E"), ("E", "F"),           # one cluster
                  ("G", "H")])                       # a separate cluster

print("clusters:", [sorted(c) for c in nx.connected_components(G)])
print("generations from A (BFS distance):")
for node, d in sorted(nx.shortest_path_length(G, "A").items()):
    print(f"  {node}: {d}")
```

<!-- python-output:auto -->
```text
clusters: [['A', 'B', 'C', 'D', 'E', 'F'], ['G', 'H']]
generations from A (BFS distance):
  A: 0
  B: 1
  C: 1
  D: 2
  E: 3
  F: 4
```
<!-- /python-output:auto -->

## Shortest Paths and Centrality

When edges carry **weights** — travel time, geographic distance, a transmission cost — plain BFS no longer suffices and you use **Dijkstra's algorithm** for the shortest weighted path (or all-pairs methods for every pair).
Building on paths, **centrality** measures rank how important each node is — degree, betweenness (how many shortest paths cross a node), eigenvector centrality — which identify likely superspreaders or keystone species; see [centrality](../math/centrality.md).

## Where Graph Algorithms Show Up in Biology

- **Transmission and contact networks** — reachability bounds a potential outbreak; components are clusters; centrality flags superspreaders.
- **Phylogenetic trees** — a tree is a special graph, traversed by the same DFS/recursion.
- **Genome assembly** — de Bruijn and overlap graphs turn read assembly into a path-finding problem.
- **Metabolic & gene-regulatory networks** — shortest paths, cycles, and reachability describe pathways and feedback.
- **Food webs and haplotype networks** — connectivity, centrality, and community structure.

Don't reimplement these — use a battle-tested library:

```r
# R: igraph
library(igraph)
g <- graph_from_edgelist(el, directed = FALSE)
components(g)$membership          # connected components
distances(g, v = "A")            # shortest-path distances
```

```julia
# Julia: Graphs.jl
using Graphs
comps = connected_components(g)
d = gdistances(g, 1)             # BFS distances from node 1
```

## A Short Checklist

- **Model linked data as a graph**, and store sparse networks as adjacency lists.
- **BFS** for shortest unweighted paths and transmission generations; **DFS** for cycles and ordering.
- **Connected components** to find outbreak clusters and reachable sets.
- **Dijkstra** when edges are weighted; **centrality** to rank important nodes.
- **Use a graph library** (`igraph`, `networkx`, `Graphs.jl`) rather than rolling your own.

## Related

- [Data Structures & Choosing the Right Container](data-structures.md) — adjacency lists, and why the representation matters
- [Big-O Notation & Computational Complexity](big-o-and-complexity.md) — the `O(V+E)` cost of traversal
- [Recursion & Dynamic Programming](recursion-and-dynamic-programming.md) — DFS and tree traversal
- [Networks](../math/networks.md), [Ecological Networks](../math/ecological-networks.md), [Network Models](../math/network-models.md), [Centrality](../math/centrality.md) — the modelling side
- [Programming & Computing](../programming.md)
