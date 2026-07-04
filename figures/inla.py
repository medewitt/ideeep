# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""SPDE finite-element mesh: a Delaunay triangulation of a spatial domain with
scattered observation points, the discretization underlying INLA's SPDE approach."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(11)

# Study domain: unit square. Build a mesh from a scattered set of interior
# nodes plus a regular boundary ring, then triangulate (the FEM mesh).
n_interior = 60
interior = rng.uniform(0.06, 0.94, size=(n_interior, 2))

t = np.linspace(0, 1, 13)[:-1]
boundary = np.concatenate([
    np.column_stack([t, np.zeros_like(t)]),
    np.column_stack([np.ones_like(t), t]),
    np.column_stack([1 - t, np.ones_like(t)]),
    np.column_stack([np.zeros_like(t), 1 - t]),
])

nodes = np.vstack([interior, boundary])
tri = Delaunay(nodes)

# A handful of observation locations (data) sitting on the continuous domain.
obs = rng.uniform(0.12, 0.88, size=(14, 2))

fig, ax = plt.subplots(figsize=(6.2, 6.0))

ax.triplot(nodes[:, 0], nodes[:, 1], tri.simplices,
           color=MUTED, lw=0.6, alpha=0.8, zorder=1)
ax.plot(nodes[:, 0], nodes[:, 1], "o", ms=2.5,
        color=PALETTE[0], zorder=2, label="mesh nodes")
ax.plot(obs[:, 0], obs[:, 1], "*", ms=13, color=PALETTE[1],
        markeredgecolor=INK, markeredgewidth=0.5, zorder=3,
        label="observations")

ax.set_title("SPDE mesh over a spatial domain")
ax.set_xlabel("easting")
ax.set_ylabel("northing")
ax.set_xlim(-0.03, 1.03)
ax.set_ylim(-0.03, 1.03)
ax.set_aspect("equal")
ax.grid(False)
ax.legend(loc="upper right", fontsize=9)

save(fig, "assets/figures/inla.svg")
