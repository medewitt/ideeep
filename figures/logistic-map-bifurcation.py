# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Bifurcation diagram of the logistic map: period-doubling route to chaos."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

n_r = 2000
n_iter = 600
n_transient = 400

r_values = np.linspace(2.5, 4.0, n_r)

r_plot = []
x_plot = []

for r in r_values:
    x = 0.5
    for _ in range(n_transient):
        x = r * x * (1 - x)
    for _ in range(n_iter - n_transient):
        x = r * x * (1 - x)
        r_plot.append(r)
        x_plot.append(x)

fig, ax = plt.subplots(figsize=(8, 5))
# Rasterize this dense point cloud so the SVG embeds a compact bitmap layer
# instead of ~800k vector points (which would bloat the file to tens of MB).
ax.scatter(r_plot, x_plot, s=0.05, alpha=0.3, color=PALETTE[0], marker=".",
           rasterized=True)
ax.set_xlabel("Growth rate r")
ax.set_ylabel("Attractor x")
ax.set_xlim(2.5, 4.0)
ax.set_ylim(0, 1)
ax.set_title("Logistic Map: Period-Doubling Route to Chaos")

save(fig, "assets/figures/logistic-map-bifurcation.svg")
