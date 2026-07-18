# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""How coarsened exact matching works. Each covariate is coarsened into bins,
carving the covariate space into cells. Treated (orange) and control (blue) units
are then exact-matched within cells: cells holding both are kept (shaded), and
units in cells with only one group are pruned. This bounds imbalance directly,
without a propensity model, at the cost of dropping unmatched units."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(7)
n = 260
L1 = rng.normal(0, 1, n)
L2 = rng.normal(0, 1, n)
A = rng.binomial(1, 1 / (1 + np.exp(-(1.1 * L1 + 0.9 * L2))))

cuts = np.array([-1.2, -0.4, 0.4, 1.2])              # coarsening cut points
bx = np.digitize(L1, cuts)
by = np.digitize(L2, cuts)
kept = np.zeros(n, bool)
grid = np.linspace(-2.6, 2.6, 100)
edges = np.concatenate(([-2.6], cuts, [2.6]))

fig, ax = plt.subplots(figsize=(5.8, 4.8))
for i in range(len(edges) - 1):
    for j in range(len(edges) - 1):
        cell = (bx == i) & (by == j)
        has_t = (A[cell] == 1).any()
        has_c = (A[cell] == 0).any()
        if has_t and has_c:
            ax.add_patch(plt.Rectangle((edges[i], edges[j]), edges[i+1]-edges[i],
                         edges[j+1]-edges[j], facecolor=PALETTE[2], alpha=0.14,
                         edgecolor="none", zorder=0))
            kept |= cell
for c in cuts:
    ax.axvline(c, color=MUTED, lw=0.7, ls=":")
    ax.axhline(c, color=MUTED, lw=0.7, ls=":")
ax.scatter(L1[(A == 0) & kept], L2[(A == 0) & kept], s=26, color=PALETTE[0],
           edgecolor="white", linewidth=0.3, label="control (matched)", zorder=3)
ax.scatter(L1[(A == 1) & kept], L2[(A == 1) & kept], s=26, color=PALETTE[1],
           edgecolor="white", linewidth=0.3, label="treated (matched)", zorder=3)
ax.scatter(L1[~kept], L2[~kept], s=20, color=MUTED, alpha=0.5, marker="x",
           label="pruned (no match)", zorder=2)
ax.set_xlabel("covariate $L_1$")
ax.set_ylabel("covariate $L_2$")
ax.set_title(f"Coarsened exact matching  ({kept.sum()} of {n} kept)", fontsize=9.6)
ax.set_xlim(-2.6, 2.6)
ax.set_ylim(-2.6, 2.6)
ax.legend(fontsize=7.8, loc="upper left", framealpha=0.9)
fig.tight_layout()
save(fig, "assets/figures/match-cem.svg")
