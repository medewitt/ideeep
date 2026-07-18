# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""The stepped-wedge grid: clusters as rows, time periods as columns, cells shaded
once a cluster has switched from control to intervention. Randomization sets the
order in which clusters step over; by the final period all are exposed. Because
later periods are more intervened and also simply later, the intervention effect
must be separated from any secular time trend."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from _style import apply_style, save, PALETTE, INK

apply_style()

n_clusters, n_periods = 5, 5
switch = {c: c + 1 for c in range(n_clusters)}   # cluster c switches at period c+1

fig, ax = plt.subplots(figsize=(6.4, 3.9))
ax.set_xlim(-0.6, n_periods)
ax.set_ylim(-0.6, n_clusters)
ax.set_aspect("equal")
ax.axis("off")

ctrl = "#d8dee4"
inter = PALETTE[2]
for c in range(n_clusters):
    row = n_clusters - 1 - c                      # top row = first to switch
    for p in range(n_periods):
        exposed = p >= switch[c]
        ax.add_patch(Rectangle((p, row), 1, 1, facecolor=inter if exposed else ctrl,
                               alpha=0.85 if exposed else 1.0,
                               edgecolor="white", lw=1.5))
        label = "I" if exposed else "C"
        ax.text(p + 0.5, row + 0.5, label, ha="center", va="center", fontsize=9,
                color="white" if exposed else INK)

for p in range(n_periods):
    ax.text(p + 0.5, n_clusters + 0.02, f"{p+1}", ha="center", fontsize=8.5,
            color=INK)
for c in range(n_clusters):
    row = n_clusters - 1 - c
    ax.text(-0.12, row + 0.5, f"cl {c+1}", ha="right", va="center", fontsize=8.5,
            color=INK)
ax.text(n_periods / 2, n_clusters + 0.45, "time period", ha="center", fontsize=9,
        color=INK)

# legend patches
ax.add_patch(Rectangle((0, -0.55), 0.4, 0.32, facecolor=ctrl, edgecolor="white"))
ax.text(0.5, -0.39, "control", va="center", fontsize=8.3, color=INK)
ax.add_patch(Rectangle((2.1, -0.55), 0.4, 0.32, facecolor=inter, alpha=0.85,
                       edgecolor="white"))
ax.text(2.6, -0.39, "intervention", va="center", fontsize=8.3, color=INK)

fig.tight_layout()
save(fig, "assets/figures/stepped-wedge-designs.svg")
