# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "networkx",
#     "numpy",
#     "scipy",
# ]
# ///
"""Areal CAR smoothing on a small region graph: noisy vs CAR-smoothed values."""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from _style import apply_style, save, INK

apply_style()

rng = np.random.default_rng(4)

# A small lattice of "regions"; edges encode shared borders (adjacency).
G = nx.grid_2d_graph(4, 4)
nodes = list(G.nodes())
pos = {n: (n[1], -n[0]) for n in nodes}           # row/col -> x/y
n = len(nodes)

# Adjacency W and degree D from the neighbourhood graph.
W = nx.to_numpy_array(G, nodelist=nodes)
D = np.diag(W.sum(1))

# A smooth latent surface plus observation noise -> noisy region values.
xy = np.array([pos[v] for v in nodes], float)
latent = 1.4 * np.sin(0.9 * xy[:, 0]) + 1.1 * np.cos(0.8 * xy[:, 1])
y = latent + rng.normal(0, 0.9, size=n)           # noisy observed values

# One CAR smoothing step: posterior mean of x given y with
# prior precision tau^-2 (D - alpha W) and observation precision kappa.
alpha, tau2, kappa = 0.98, 0.35, 1.0
Q = (D - alpha * W) / tau2
xhat = np.linalg.solve(kappa * np.eye(n) + Q, kappa * y)

vmin = min(y.min(), xhat.min())
vmax = max(y.max(), xhat.max())

fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2))
for ax, vals, title in ((axes[0], y, "Noisy region values"),
                        (axes[1], xhat, "CAR-smoothed")):
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="0.72", width=1.0)
    nc = nx.draw_networkx_nodes(
        G, pos, ax=ax, node_size=520, node_color=vals,
        cmap="RdBu_r", vmin=vmin, vmax=vmax,
        edgecolors="white", linewidths=1.2)
    ax.set_title(title, color=INK)
    ax.set_axis_off()
    ax.set_aspect("equal")

cbar = fig.colorbar(nc, ax=axes, shrink=0.75, pad=0.02)
cbar.set_label("region value")
fig.suptitle("Neighbouring regions are pulled together by the CAR prior",
             color=INK)

save(fig, "assets/figures/areal-models-car.svg")
