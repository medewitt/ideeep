# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "networkx",
#     "matplotlib",
# ]
# ///
"""Conceptual reach comparison: a false rumor spreads widely through a social
network while an accurate pamphlet, though true, reaches far fewer people."""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

SEED = 7
rng = np.random.default_rng(SEED)

# One shared population graph, one fixed layout, used in both panels.
G = nx.connected_watts_strogatz_graph(60, 4, 0.25, seed=SEED)
pos = nx.spring_layout(G, seed=SEED, k=0.42, iterations=200)

# Rumor: starts from a well-connected seed and spreads across most of the graph
# via a breadth-first cascade (wide reach).
seed_rumor = max(G.degree, key=lambda kv: kv[1])[0]
rumor = set([seed_rumor])
frontier = [seed_rumor]
# probabilistic cascade with deterministic rng -> large connected reached set
while frontier:
    nxt = []
    for u in frontier:
        for v in G.neighbors(u):
            if v not in rumor and rng.random() < 0.72:
                rumor.add(v)
                nxt.append(v)
    frontier = nxt
    if len(rumor) > 44:
        break

# Pamphlet: reaches only a small handful of people (narrow reach).
seed_pamph = seed_rumor
pamphlet = set([seed_pamph]) | set(list(G.neighbors(seed_pamph))[:4])

fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.2))

panels = [
    (axes[0], rumor, PALETTE[1], "False rumor via social network", "reached"),
    (axes[1], pamphlet, PALETTE[0], "Accurate pamphlet", "reached"),
]

for ax, reached, color, title, word in panels:
    ax.set_aspect("equal")
    ax.axis("off")

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#d8dee4", width=0.7)

    unreached = [n for n in G.nodes if n not in reached]
    reached_nodes = [n for n in G.nodes if n in reached]

    nx.draw_networkx_nodes(G, pos, nodelist=unreached, ax=ax,
                           node_color="white", edgecolors=MUTED,
                           linewidths=0.8, node_size=70)
    nx.draw_networkx_nodes(G, pos, nodelist=reached_nodes, ax=ax,
                           node_color=color, edgecolors="white",
                           linewidths=0.8, node_size=110)

    ax.set_title(title, fontsize=11, color=INK, pad=8)
    ax.text(0.5, -0.04, f"{len(reached)} of {G.number_of_nodes()} people {word}",
            transform=ax.transAxes, ha="center", va="top",
            fontsize=10, color=color, fontweight="bold")

fig.suptitle("Wide reach of a falsehood vs. narrow reach of accurate print",
             fontsize=12, color=INK, y=1.0)
fig.tight_layout(rect=(0, 0.03, 1, 0.96))

save(fig, "assets/figures/misinformation-network-reach.svg")
