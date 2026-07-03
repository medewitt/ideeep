# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "networkx"]
# ///
"""Breadth-first search on a contact network is the same thing as counting
transmission generations. Starting from the index case, BFS visits every node
one 'layer' at a time -- everyone one contact away, then two contacts away, and
so on -- which is exactly the shortest number of transmission steps from the
source. Nodes here are coloured by that BFS distance.
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from _style import apply_style, save

apply_style()

G = nx.Graph()
edges = [
    (0, 1), (0, 2), (0, 3),           # index case 0 contacts 1,2,3
    (1, 4), (1, 5), (2, 5), (3, 6),   # generation 2
    (4, 7), (5, 8), (6, 9), (6, 10),  # generation 3
    (8, 11), (9, 12),                 # generation 4
]
G.add_edges_from(edges)

source = 0
dist = nx.shortest_path_length(G, source)          # BFS distance = generation
gens = np.array([dist[n] for n in G.nodes()])

pos = nx.spring_layout(G, seed=3, k=0.9)
fig, ax = plt.subplots(figsize=(6.8, 4.4))

cmap = plt.cm.YlOrRd
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#c2ccd4", width=1.5)
nodes = nx.draw_networkx_nodes(
    G, pos, ax=ax, node_color=gens, cmap=cmap, vmin=0, vmax=gens.max(),
    node_size=560, edgecolors="#26323f", linewidths=1.2)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_color="#26323f")

# mark the index case
ax.annotate("index case", xy=pos[0], xytext=(pos[0][0] - 0.15, pos[0][1] + 0.34),
            fontsize=9, fontweight="bold", color="#26323f",
            arrowprops=dict(arrowstyle="->", color="#26323f", lw=1.2))

cbar = fig.colorbar(nodes, ax=ax, ticks=range(int(gens.max()) + 1), shrink=0.8)
cbar.set_label("transmission generation  (BFS distance from index)", fontsize=9)

ax.set_title("Breadth-first search = transmission generations")
ax.axis("off")
save(fig, "assets/figures/graph-bfs-transmission.svg")
