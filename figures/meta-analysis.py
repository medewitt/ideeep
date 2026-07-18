# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Anatomy of a forest plot. Each study contributes an estimate (square, sized by
its inverse-variance weight) and a confidence interval (whisker); studies scatter
around the common effect by more than their own intervals when there is
heterogeneity. The pooled estimate is the diamond at the bottom, whose width is
its confidence interval — narrower than any single study because it borrows
strength across all of them."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# schematic studies: estimate, standard error
est = np.array([0.42, 0.15, 0.55, 0.28, 0.05, 0.38])
se = np.array([0.18, 0.13, 0.22, 0.16, 0.20, 0.11])
w = 1 / se**2
pooled = (w * est).sum() / w.sum()
pooled_se = np.sqrt(1 / w.sum())

fig, ax = plt.subplots(figsize=(6.6, 4.0))
n = len(est)
for i in range(n):
    yy = n - i
    lo, hi = est[i] - 1.96 * se[i], est[i] + 1.96 * se[i]
    ax.plot([lo, hi], [yy, yy], color=INK, lw=1.3, zorder=2)
    ax.scatter([est[i]], [yy], s=60 + 900 * w[i] / w.max(), color=PALETTE[0],
               zorder=3, edgecolor="white", linewidth=0.6)
    ax.text(-0.55, yy, f"study {i+1}", va="center", ha="left", fontsize=8.3,
            color=INK)

# pooled diamond
d = 0.34
diamond = [(pooled - 1.96 * pooled_se, 0.3), (pooled, 0.3 + d),
           (pooled + 1.96 * pooled_se, 0.3), (pooled, 0.3 - d)]
ax.add_patch(Polygon(diamond, closed=True, facecolor=PALETTE[1],
                     edgecolor=INK, lw=1.0, zorder=4))
ax.text(-0.55, 0.3, "pooled", va="center", ha="left", fontsize=8.6,
        color=PALETTE[1], fontweight="bold")

ax.axvline(0, color=MUTED, lw=1.0, ls="--")
ax.text(0, n + 0.8, "no effect", ha="center", fontsize=8, color=MUTED)
ax.annotate("square area ∝ study weight", xy=(0.15, n - 1), xytext=(0.5, n + 0.4),
            fontsize=8, color=INK, arrowprops=dict(arrowstyle="->", color=MUTED,
            lw=0.8))
ax.annotate("diamond width\n= pooled CI", xy=(pooled + 1.96 * pooled_se, 0.3),
            xytext=(0.42, 1.4), fontsize=8, color=PALETTE[1],
            arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.8))

ax.set_xlim(-0.6, 1.0)
ax.set_ylim(-0.3, n + 1.3)
ax.set_yticks([])
ax.set_xlabel("effect size")
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/meta-analysis.svg")
