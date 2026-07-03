# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "networkx",
#     "numpy",
#     "scipy",
# ]
# ///
"""Network visualization with nodes sized and colored by eigenvector centrality."""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from _style import apply_style, save, PALETTE
apply_style()

rng = np.random.default_rng(1)

G = nx.karate_club_graph()

cent = nx.eigenvector_centrality_numpy(G)
cvals = np.array([cent[n] for n in G.nodes()])

pos = nx.spring_layout(G, seed=1)

# Node sizes proportional to centrality.
cmin, cmax = cvals.min(), cvals.max()
norm = (cvals - cmin) / (cmax - cmin + 1e-12)
sizes = 120 + norm * 900

fig, ax = plt.subplots(figsize=(8, 7))

nx.draw_networkx_edges(G, pos, ax=ax, edge_color="0.7", width=0.6, alpha=0.6)
nodes = nx.draw_networkx_nodes(
    G, pos, ax=ax, node_size=sizes, node_color=cvals,
    cmap="viridis", edgecolors="white", linewidths=0.6)

cbar = fig.colorbar(nodes, ax=ax, shrink=0.8)
cbar.set_label("eigenvector centrality")

ax.set_title("Eigenvector centrality highlights keystone /\n"
             "superspreader nodes in a contact network")
ax.set_axis_off()

save(fig, "assets/figures/centrality.svg")
