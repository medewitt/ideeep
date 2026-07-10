# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Capture-recapture: two-source overlap and Lincoln-Petersen estimate."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# Observed counts for the two case-ascertainment lists.
list1_only = 80
both = 30
list2_only = 50
n1 = list1_only + both          # 110 on list 1
n2 = list2_only + both          # 80 on list 2
m = both                        # 30 on both lists
n_hat = n1 * n2 / m             # Lincoln-Petersen estimate
hidden = n_hat - (list1_only + both + list2_only)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.6, 3.5))

# Left: two overlapping ellipses (Venn-style schematic).
axL.add_patch(Ellipse((0.40, 0.58), 0.55, 0.42, facecolor=PALETTE[0],
                      alpha=0.35, edgecolor=PALETTE[0], linewidth=1.0))
axL.add_patch(Ellipse((0.68, 0.58), 0.55, 0.42, facecolor=PALETTE[1],
                      alpha=0.35, edgecolor=PALETTE[1], linewidth=1.0))

axL.text(0.24, 0.58, f"list 1 only:\n{list1_only}", ha="center",
         va="center", fontsize=8.5, color=INK)
axL.text(0.54, 0.58, f"both:\n{both}", ha="center", va="center",
         fontsize=8.5, color=INK)
axL.text(0.84, 0.58, f"list 2 only:\n{list2_only}", ha="center",
         va="center", fontsize=8.5, color=INK)

axL.text(0.54, 0.18, f"in neither list (hidden): {hidden:.0f}",
         ha="center", va="center", fontsize=8.5, color=MUTED,
         style="italic")

axL.text(
    0.02, 0.95,
    f"n1 = {n1},  n2 = {n2},  m = {m}\n"
    f"N̂ = n1·n2 / m = {n_hat:.0f}",
    ha="left", va="top", fontsize=8.5, color=INK,
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
              edgecolor=MUTED, linewidth=0.8),
)

axL.set_xlim(0, 1)
axL.set_ylim(0, 1)
axL.axis("off")
axL.set_title("Two-source capture-recapture")

# Right: how N-hat depends on the observed overlap m.
m_range = np.arange(5, 81)
n_hat_curve = n1 * n2 / m_range

axR.plot(m_range, n_hat_curve, color=PALETTE[2], lw=2.0)
axR.plot([m], [n_hat], marker="o", color=PALETTE[1], markersize=7,
         zorder=5)
axR.axvline(m, color=MUTED, lw=1.0, ls="--")
axR.axhline(n_hat, color=MUTED, lw=1.0, ls="--")
axR.set_xlabel("cases on both lists (overlap m)")
axR.set_ylabel("estimated total population N̂")
axR.set_xlim(m_range.min(), m_range.max())

axR.annotate(
    "less overlap between lists\n→ larger estimated\nhidden population",
    xy=(9, n1 * n2 / 9), xytext=(30, n1 * n2 / 9 * 0.62),
    fontsize=8.5, color=INK, ha="left",
    arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1),
)

fig.tight_layout()
save(fig, "assets/figures/capture-recapture.svg")
