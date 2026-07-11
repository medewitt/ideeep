# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "networkx"]
# ///
"""Graph neural networks learn by message passing. Left: a node updates its
state by aggregating transformed messages from its neighbours, then combining
with its own -- one layer reaches one hop, K layers reach K hops. Right: on a
contact network, repeatedly aggregating an infected seed's signal over
neighbours (the core GCN operation) spreads an exposure score outward from the
source, the raw material a trained GNN turns into a risk prediction.
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch, Circle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig = plt.figure(figsize=(9.8, 4.1))

# --- left: message-passing schematic ---
ax0 = fig.add_axes([0.02, 0.06, 0.40, 0.86])
ax0.set_xlim(0, 10)
ax0.set_ylim(0, 10)
ax0.axis("off")
center = (5, 5)
neighbours = [(2, 8), (1.5, 4), (3, 1.5), (8.5, 7), (8.8, 3)]
for nb in neighbours:
    ax0.add_patch(FancyArrowPatch(nb, center, arrowstyle="-|>", mutation_scale=13,
                  color=MUTED, lw=1.4, shrinkA=10, shrinkB=14))
    ax0.add_patch(Circle(nb, 0.5, facecolor=PALETTE[0] + "33",
                  edgecolor=PALETTE[0], linewidth=1.5))
    ax0.text(nb[0], nb[1], "$u$", ha="center", va="center", fontsize=9, color=INK)
ax0.add_patch(Circle(center, 0.75, facecolor=PALETTE[1] + "33",
              edgecolor=PALETTE[1], linewidth=2))
ax0.text(center[0], center[1], "$v$", ha="center", va="center", fontsize=11,
         color=INK)
ax0.set_title("Message passing at node $v$", fontsize=10)
ax0.text(5, 0.6, r"$h_v' = \mathrm{UPDATE}\!\left(h_v,\ "
         r"\bigoplus_{u\in N(v)} \mathrm{MSG}(h_u)\right)$", ha="center",
         fontsize=10.5, color=INK)

# --- right: exposure diffusion on a contact network ---
ax1 = fig.add_axes([0.46, 0.05, 0.52, 0.88])
G = nx.karate_club_graph()
A = nx.to_numpy_array(G)
n = A.shape[0]
A_hat = A + np.eye(n)
d = A_hat.sum(1)
S = A_hat / np.sqrt(d)[:, None] / np.sqrt(d)[None, :]     # normalized adjacency
x = np.zeros(n)
seed = 0
x[seed] = 1.0
h = x.copy()
for _ in range(2):                                        # two message-passing layers
    h = S @ h
pos = nx.spring_layout(G, seed=3)
nx.draw_networkx_edges(G, pos, ax=ax1, edge_color="#c9d2da", width=0.8)
nodes = nx.draw_networkx_nodes(G, pos, ax=ax1, node_color=h, cmap="magma_r",
                               node_size=110, edgecolors=INK, linewidths=0.4)
ax1.scatter(*pos[seed], s=260, facecolors="none", edgecolors=PALETTE[2],
            linewidths=2.2, zorder=5)
ax1.text(pos[seed][0], pos[seed][1] + 0.11, "seed", ha="center", fontsize=8,
         color=PALETTE[2])
ax1.set_title("Exposure score spreading from an infected seed", fontsize=10)
ax1.axis("off")
cb = fig.colorbar(nodes, ax=ax1, fraction=0.04, pad=0.02)
cb.set_label("aggregated score", fontsize=8)
cb.ax.tick_params(labelsize=7)

save(fig, "assets/figures/graph-neural-networks.svg")
