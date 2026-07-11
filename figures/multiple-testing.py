# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Benjamini-Hochberg versus Bonferroni on the worked five-test example. The
sorted p-values are compared against two thresholds: Bonferroni's flat line at
alpha/m = 0.01 (which only the first two clear) and BH's sloped line i/m*alpha
(which the first four clear). BH's rising threshold admits more discoveries in
exchange for controlling the false discovery rate rather than the family-wise
error rate."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

p = np.array([0.001, 0.008, 0.02, 0.04, 0.5])
m = len(p)
alpha = 0.05
rank = np.arange(1, m + 1)

bonf = alpha / m                       # flat 0.01
bh = rank / m * alpha                  # 0.01, 0.02, 0.03, 0.04, 0.05

# largest rank passing BH -> reject all up to it
bh_pass = np.where(p <= bh)[0]
kmax = bh_pass.max() + 1 if bh_pass.size else 0

fig, ax = plt.subplots(figsize=(6.6, 4.0))

ax.axhline(bonf, ls="--", color=PALETTE[3], lw=1.4,
           label=r"Bonferroni  $\alpha/m=0.01$")
ax.plot(rank, bh, ls="--", color=PALETTE[2], lw=1.4, marker="s", ms=4,
        label=r"Benjamini-Hochberg  $\frac{i}{m}\alpha$")

# p-values, colored by BH rejection
rej = rank <= kmax
ax.scatter(rank[rej], p[rej], s=95, color=PALETTE[1], zorder=5,
           label="rejected (BH)")
ax.scatter(rank[~rej], p[~rej], s=95, facecolor="white",
           edgecolor=MUTED, linewidths=1.5, zorder=5, label="not rejected")

for i in range(m):
    ax.annotate(f"{p[i]:g}", (rank[i], p[i]), textcoords="offset points",
                xytext=(9, 6), fontsize=8, color=INK)

ax.axvspan(0.5, 2.5, color=PALETTE[3] + "18", zorder=0)
ax.text(1.5, 0.28, "Bonferroni:\n2 discoveries", ha="center", fontsize=8.5,
        color=PALETTE[3])
ax.text(4.4, 0.28, "BH: 4 discoveries", ha="center", fontsize=8.5,
        color=PALETTE[1])

ax.set_xlabel(r"rank $i$ of sorted p-value")
ax.set_ylabel("p-value")
ax.set_title("Why BH finds more than Bonferroni", fontsize=11)
ax.set_xticks(rank)
ax.set_ylim(-0.02, 0.55)
ax.legend(fontsize=8.3, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/multiple-testing.svg")
