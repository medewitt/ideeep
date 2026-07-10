# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Genes in (dS, dN) space and the dN/dS = 1 neutral diagonal."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# Simulate genes in three selection regimes.
# Purifying: dN well below dS. Neutral: dN ~ dS. Positive: dN above dS.
n_pur, n_neu, n_pos = 44, 10, 6

dS_pur = rng.uniform(0.02, 0.5, n_pur)
dN_pur = dS_pur * rng.uniform(0.05, 0.45, n_pur)

dS_neu = rng.uniform(0.02, 0.5, n_neu)
dN_neu = dS_neu * rng.uniform(0.85, 1.15, n_neu)

dS_pos = rng.uniform(0.02, 0.35, n_pos)
dN_pos = dS_pos * rng.uniform(1.4, 2.6, n_pos)

fig, ax = plt.subplots(figsize=(6.2, 4.2))

lim = 0.62
# Diagonal dN = dS.
ax.plot([0, lim], [0, lim], "--", color=INK, lw=1.4,
        label="dN/dS = 1 (neutral)")

# Shade the two regions.
ax.fill_between([0, lim], [0, lim], 0, color=PALETTE[0], alpha=0.06)
ax.fill_between([0, lim], [0, lim], lim, color=PALETTE[1], alpha=0.06)

ax.scatter(dS_pur, dN_pur, s=28, color=PALETTE[0], edgecolors="white",
           linewidths=0.5, label="purifying (dN < dS)", zorder=3)
ax.scatter(dS_neu, dN_neu, s=28, color=MUTED, edgecolors="white",
           linewidths=0.5, label="neutral (dN ≈ dS)", zorder=3)
ax.scatter(dS_pos, dN_pos, s=28, color=PALETTE[1], edgecolors="white",
           linewidths=0.5, label="positive (dN > dS)", zorder=3)

ax.annotate("dN/dS < 1:\npurifying selection", (0.44, 0.14),
            fontsize=9, color=PALETTE[0], ha="center")
ax.annotate("dN/dS > 1:\npositive selection", (0.16, 0.5),
            fontsize=9, color=PALETTE[1], ha="center")

ax.set_xlim(0, lim)
ax.set_ylim(0, lim)
ax.set_aspect("equal")
ax.set_xlabel("synonymous substitutions per site (dS)")
ax.set_ylabel("nonsynonymous per site (dN)")
ax.set_title("Selection signatures in dN/dS space")
ax.legend(loc="upper left", fontsize=8)

save(fig, "assets/figures/dn-ds.svg")
