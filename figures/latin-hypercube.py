# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Latin hypercube sampling vs plain Monte Carlo, n=5 in the unit square on a
5x5 grid. Left: independent uniform draws clump and can leave whole marginal
bins empty (shaded columns/rows with no point). Right: LHS places exactly one
point in each bin of every input — one per row and per column, like a Latin
square — so no marginal stratum is ever missed."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(3)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.0, 4.0))


def grid(ax, title):
    for g in np.linspace(0, 1, 6):
        ax.axhline(g, color="#d8dee4", lw=0.8)
        ax.axvline(g, color="#d8dee4", lw=0.8)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xlabel("input 1")
    ax.set_title(title, fontsize=10)
    ax.set_xticks(np.linspace(0.1, 0.9, 5))
    ax.set_yticks(np.linspace(0.1, 0.9, 5))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(False)


# ---- plain Monte Carlo ----------------------------------------------------
grid(axL, "Plain Monte Carlo")
mc = rng.random((5, 2))
axL.scatter(mc[:, 0], mc[:, 1], s=70, color=PALETTE[1], zorder=5)
axL.set_ylabel("input 2")
# highlight an empty column and row (marginal bins with no point)
col_used = set((mc[:, 0] * 5).astype(int))
row_used = set((mc[:, 1] * 5).astype(int))
for c in set(range(5)) - col_used:
    axL.axvspan(c / 5, (c + 1) / 5, color=PALETTE[3] + "22", zorder=0)
for r in set(range(5)) - row_used:
    axL.axhspan(r / 5, (r + 1) / 5, color=PALETTE[3] + "22", zorder=0)
axL.text(0.5, -0.16, "shaded bins are empty — clumps and gaps",
         ha="center", fontsize=8, color=PALETTE[3], transform=axL.transAxes)

# ---- Latin hypercube ------------------------------------------------------
grid(axR, "Latin hypercube")
u1 = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
u2 = np.array([0.5, 0.9, 0.1, 0.7, 0.3])       # pi_2 = (3,5,1,4,2)
axR.scatter(u1, u2, s=70, color=PALETTE[0], zorder=5)
axR.text(0.5, -0.16, "one point per row and per column",
         ha="center", fontsize=8, color=PALETTE[0], transform=axR.transAxes)

fig.tight_layout()
save(fig, "assets/figures/latin-hypercube.svg")
