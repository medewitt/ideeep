# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""ANOVA as a comparison of two spreads. Three treatment groups are plotted as
points; each group mean is marked against the dashed grand mean. The between-group
signal is how far the group means sit from the grand mean; the within-group noise
is the scatter of points around their own group mean. ANOVA asks whether the first
is large relative to the second."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(0)

groups = {"A": [8, 9, 7, 8], "B": [10, 11, 12, 11], "C": [9, 8, 10, 9]}
grand = np.mean([v for vs in groups.values() for v in vs])

fig, ax = plt.subplots(figsize=(6.4, 3.9))

for i, (name, vals) in enumerate(groups.items()):
    x = i + 1
    jit = rng.uniform(-0.08, 0.08, len(vals))
    ax.scatter(x + jit, vals, s=46, color=PALETTE[i], zorder=4, alpha=0.9)
    m = np.mean(vals)
    ax.hlines(m, x - 0.22, x + 0.22, color=PALETTE[i], lw=2.6, zorder=5)
    ax.annotate(f"$\\bar{{y}}_{name}={m:.0f}$", (x + 0.24, m), fontsize=8.5,
                color=INK, va="center")
    # within-group scatter marker for one point
    ax.vlines(x - 0.30, m, vals[1], color=MUTED, lw=1.0, ls=":")

ax.axhline(grand, color=INK, lw=1.3, ls="--")
ax.annotate(f"grand mean $\\bar{{y}}={grand:.2f}$", (3.35, grand), fontsize=8.5,
            color=INK, va="center")

# annotate between vs within
ax.annotate("between-group:\nmeans vs grand mean", xy=(2, 11), xytext=(1.15, 12.4),
            fontsize=8.3, color=INK,
            arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=1.0))
ax.annotate("within-group:\nscatter around own mean", xy=(0.70, 10.5),
            xytext=(0.55, 6.4), fontsize=8.3, color=INK,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))

ax.set_xticks([1, 2, 3])
ax.set_xticklabels(["A", "B", "C"])
ax.set_xlim(0.4, 3.9)
ax.set_ylim(6, 13)
ax.set_xlabel("treatment group")
ax.set_ylabel("response")
ax.grid(axis="x", visible=False)
fig.tight_layout()
save(fig, "assets/figures/anova.svg")
