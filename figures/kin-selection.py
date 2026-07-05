# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Kin selection: a relatedness schematic, the Hamilton's-rule threshold,
and the Price partition of total change."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.4))

# (a) Relatedness schematic: an actor and neighbours sharing alleles by descent.
ax = axes[0]
ax.set_axis_off()
ax.set_title("(a) relatedness $r$")
actor = (0.5, 0.85)
kin = [(0.2, 0.35), (0.5, 0.35), (0.8, 0.35)]
labels = ["full sib\n$r=1/2$", "half sib\n$r=1/4$", "cousin\n$r=1/8$"]
for (x, y), lab in zip(kin, labels):
    ax.plot([actor[0], x], [actor[1], y], color=MUTED, lw=1)
    ax.text(x, y - 0.16, lab, ha="center", va="top", fontsize=7.5, color=INK)
ax.scatter(*actor, s=260, color=PALETTE[1], zorder=3)
ax.text(actor[0], actor[1], "actor", ha="center", va="center",
        fontsize=7.5, color="white")
ax.scatter([k[0] for k in kin], [k[1] for k in kin], s=200,
           color=PALETTE[0], zorder=3)
ax.set_xlim(0, 1)
ax.set_ylim(0.05, 1)

# (b) Hamilton's rule: rb = c separates spread from loss.
b = np.linspace(0, 4, 200)
for r, col in zip([0.5, 0.25, 0.125], PALETTE[:3]):
    ax = axes[1]
    ax.plot(b, r * b, color=col, lw=2, label=f"$r={r}$")
axes[1].fill_between(b, 0, 2.0, color=PALETTE[2], alpha=0.06)
axes[1].set_xlabel("benefit to recipients $b$")
axes[1].set_ylabel("cost to actor $c$")
axes[1].set_title(r"(b) Hamilton's rule $rb=c$")
axes[1].text(3.0, 0.35, "helping spreads\n($rb>c$)", fontsize=7.5,
             color=INK, ha="center")
axes[1].set_ylim(0, 2.0)
axes[1].legend(fontsize=8, loc="upper left")

# (c) Price partition: within- vs between-group components of total change.
n_groups = 30
group_r = rng.uniform(0.05, 0.6, n_groups)          # helping-allele frequency
between = 0.8 * (group_r - group_r.mean())           # between-group selection
within = -0.5 * group_r + rng.normal(0, 0.03, n_groups)  # within-group cost
total = between + within
axes[2].axhline(0, color=MUTED, lw=0.8)
axes[2].scatter(group_r, within, s=16, color=PALETTE[1],
                label="within-group", alpha=0.8, edgecolor="none")
axes[2].scatter(group_r, between, s=16, color=PALETTE[0],
                label="between-group", alpha=0.8, edgecolor="none")
axes[2].scatter(group_r, total, s=16, color=INK,
                label="total $\\Delta\\bar z$", alpha=0.9, edgecolor="none")
axes[2].set_xlabel("group helping frequency")
axes[2].set_ylabel("selection component")
axes[2].set_title("(c) Price partition")
axes[2].legend(fontsize=7.5, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/kin-selection.svg")
