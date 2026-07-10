# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Halloran-Struchiner decomposition of vaccine effects."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# Attack rates (per 1000) under dependent happenings. Four groups:
#  0 unvaccinated, no program (reference)
#  1 unvaccinated, with program (indirect protection only)
#  2 vaccinated, with program (direct + indirect)
#  3 whole-program community average
labels = [
    "unvaccinated,\nno program",
    "unvaccinated,\nwith program",
    "vaccinated,\nwith program",
    "whole program\ncommunity",
]
ar = np.array([90.0, 55.0, 20.0, 32.0])
colors = [PALETTE[1], PALETTE[3], PALETTE[0], PALETTE[2]]

fig, ax = plt.subplots(figsize=(7.8, 4.0))

x = np.arange(4)
bars = ax.bar(x, ar, width=0.6, color=colors, edgecolor="white", lw=0.6)
bars[3].set_alpha(0.55)  # community average shown fainter

for xi, v in zip(x, ar):
    ax.text(xi, v + 1.5, f"{v:.0f}", ha="center", va="bottom",
            fontsize="x-small", color=INK)

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize="x-small")
ax.set_ylabel("attack rate (per 1000)")
ax.set_ylim(0, 132)
ax.set_title("Direct, indirect, total, and overall effects")


def contrast(a, b, y, text, color):
    """Draw a bracket between bars a and b at height y with a label."""
    tick = 2.0
    ax.plot([a, a, b, b], [ar[a] + 3, y, y, ar[b] + 3],
            color=color, lw=1.0, clip_on=False)
    ax.text((a + b) / 2, y + 1.5, text, ha="center", va="bottom",
            fontsize="x-small", color=color)


# Staggered heights so the four brackets do not overlap.
# INDIRECT: bar 1 vs bar 0 (unvaccinated, program vs no program).
contrast(0, 1, 100, "indirect", MUTED)
# DIRECT: bar 2 vs bar 1 (vaccinated vs unvaccinated, both in program).
contrast(1, 2, 74, "direct", PALETTE[0])
# TOTAL: bar 2 vs bar 0 (vaccinated-program vs unvaccinated-no-program).
contrast(0, 2, 116, "total", INK)
# OVERALL: bar 3 vs bar 0 (community average vs no program).
contrast(0, 3, 128, "overall", PALETTE[2])

fig.tight_layout()

print("indirect:", ar[0] - ar[1], " direct:", ar[1] - ar[2],
      " total:", ar[0] - ar[2], " overall:", ar[0] - ar[3])

save(fig, "assets/figures/vaccine-effects-direct-indirect.svg")
