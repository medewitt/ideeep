# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Spatial cluster detection on a lattice: a planted high-risk cluster and the
Moran scatterplot whose slope is Moran's I."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(1834)

# A regular lattice of areal units (e.g. counties on a grid).
side = 10
n = side * side
coords = np.array([(r, c) for r in range(side) for c in range(side)], float)

# Rook adjacency: units sharing an edge are neighbours.
W = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i != j and np.abs(coords[i] - coords[j]).sum() == 1:
            W[i, j] = 1.0

# A background risk surface with a planted high-risk cluster near one corner.
risk = rng.normal(0.0, 0.5, size=n)
center = np.array([2.0, 2.0])
dist = np.linalg.norm(coords - center, axis=1)
risk += 3.0 * np.exp(-(dist**2) / (2 * 1.6**2))     # the cluster bump

# Row-standardise the weights and form the spatial lag of the standardised risk.
Wr = W / W.sum(1, keepdims=True)
z = (risk - risk.mean()) / risk.std()
lag = Wr @ z

# Moran's I is the slope of lag vs z (weights already row-standardised).
num = z @ (W @ z)
moran_i = (n / W.sum()) * num / (z @ z)

fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.2))

# ---- Panel 1: the risk map with its planted cluster --------------------------
ax = axes[0]
grid = risk.reshape(side, side)
im = ax.imshow(grid, origin="lower", cmap="RdBu_r",
               vmin=-np.abs(grid).max(), vmax=np.abs(grid).max())
# Sketch the adjacency by outlining one unit and its rook neighbours.
hi = int(np.argmax(risk))
hr, hc = divmod(hi, side)
for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    ax.plot([hc, hc + dc], [hr, hr + dr], color=INK, lw=1.4, zorder=3)
ax.scatter([hc], [hr], s=40, color=INK, zorder=4)
ax.set_title("Risk surface with a planted cluster", fontsize=10)
ax.set_xticks([])
ax.set_yticks([])
cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label("standardised risk")

# ---- Panel 2: the Moran scatterplot -----------------------------------------
ax = axes[1]
ax.axhline(0, color=MUTED, lw=0.7)
ax.axvline(0, color=MUTED, lw=0.7)
ax.scatter(z, lag, s=22, color=PALETTE[0], alpha=0.8,
           edgecolor="white", linewidth=0.4)
xs = np.linspace(z.min(), z.max(), 100)
ax.plot(xs, moran_i * xs, color=PALETTE[1], lw=2,
        label=f"slope = Moran's $I$ = {moran_i:.2f}")
ax.set_xlabel("standardised risk $z_i$")
ax.set_ylabel("spatial lag $(Wz)_i$")
ax.set_title("Moran scatterplot", fontsize=10)
ax.legend(loc="lower right", fontsize=9)

fig.suptitle("Clustering shows as positive spatial autocorrelation",
             color=INK, fontsize=12)
fig.tight_layout()
save(fig, "assets/figures/spatial-cluster-detection.svg")
