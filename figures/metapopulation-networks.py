# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "networkx",
#     "matplotlib",
# ]
# ///
"""Metapopulation networks and the global invasion threshold.

Left: a network of subpopulations linked by mobility edges, with an outbreak
seeded in one hub spreading to the subpopulations it reaches. Center: the
global invasion threshold R* over mobility rate and degree heterogeneity, with
the R*=1 contour. Right: gravity coupling, where flux decays with distance and
grows with the product of population sizes.
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (axA, axB, axC) = plt.subplots(1, 3, figsize=(13.5, 4.3))

# ---- A: metapopulation on a network, outbreak seeded in one node ----
G = nx.barabasi_albert_graph(22, 2, seed=1834)
pos = nx.spring_layout(G, seed=1834)
deg = dict(G.degree())
seed_node = max(deg, key=deg.get)                # seed the largest hub

# Mark subpopulations reached within two mobility steps of the seed.
reached = set([seed_node]) | set(G[seed_node])
for nb in list(reached):
    reached |= set(G[nb])
colors = [PALETTE[1] if n == seed_node else
          PALETTE[4] if n in reached else PALETTE[0] for n in G.nodes()]
sizes = [120 + 90 * deg[n] for n in G.nodes()]
weights = rng.uniform(0.4, 2.6, G.number_of_edges())

nx.draw_networkx_edges(G, pos, ax=axA, width=weights, edge_color=MUTED,
                       alpha=0.5)
nx.draw_networkx_nodes(G, pos, ax=axA, node_color=colors, node_size=sizes,
                       edgecolors="white", linewidths=0.8)
axA.plot([], [], "o", color=PALETTE[1], label="seed subpopulation")
axA.plot([], [], "o", color=PALETTE[4], label="reached")
axA.plot([], [], "o", color=PALETTE[0], label="not reached")
axA.set_title("Coupled subpopulations")
axA.legend(loc="lower left", fontsize=8)
axA.axis("off")

# ---- B: global invasion threshold R* over (mobility, heterogeneity) ----
p = np.linspace(0.0, 0.05, 200)            # per-capita mobility rate
kappa = np.linspace(1.0, 12.0, 200)        # heterogeneity <k^2>/<k>
P, Kp = np.meshgrid(p, kappa)
R0 = 3.0
Rstar = 260.0 * P * Kp * (R0 - 1) ** 2 / R0 ** 2   # schematic scaling
im = axB.imshow(Rstar, origin="lower", aspect="auto", cmap="viridis",
                extent=(p.min(), p.max(), kappa.min(), kappa.max()),
                vmin=0, vmax=3)
cs = axB.contour(P, Kp, Rstar, levels=[1.0], colors="white", linewidths=2)
axB.clabel(cs, fmt={1.0: "$R_*=1$"}, fontsize=9)
fig.colorbar(im, ax=axB, label="$R_*$", fraction=0.046, pad=0.04)
axB.set_xlabel("mobility rate $p$")
axB.set_ylabel(r"degree heterogeneity $\langle k^2\rangle/\langle k\rangle$")
axB.set_title("Global invasion threshold")

# ---- C: gravity coupling, flux vs distance for two population products ----
d = np.linspace(5, 200, 300)
for prod, col, lab in [(1e10, PALETTE[0], r"$N_iN_j=10^{10}$"),
                       (1e11, PALETTE[1], r"$N_iN_j=10^{11}$")]:
    axC.loglog(d, prod / d**2, color=col, lw=2, label=lab)
axC.set_xlabel("distance $d_{ij}$")
axC.set_ylabel(r"flux $w_{ij}\propto N_iN_j/d_{ij}^2$")
axC.set_title("Gravity coupling")
axC.legend(loc="upper right", fontsize=9)

fig.suptitle("Epidemic invasion across a metapopulation network",
             fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "assets/figures/metapopulation-networks.svg")
