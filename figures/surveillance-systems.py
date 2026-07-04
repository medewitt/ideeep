# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""The surveillance pyramid: infections attrit at each level, so a
reported count is the visible tip of a much larger base of infections."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# Fraction of the level below that passes to each successive level.
levels = [
    ("Infections", 1.000, PALETTE[0]),
    ("Symptomatic", 0.600, PALETTE[2]),
    ("Seek care", 0.360, PALETTE[4]),
    ("Tested", 0.216, PALETTE[3]),
    ("Reported", 0.130, PALETTE[1]),
]

fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.set_axis_off()
ax.grid(False)

n = len(levels)
row_h = 1.0
for i, (label, frac, color) in enumerate(levels):
    # Widen toward the base: the bottom level is widest, the tip narrow.
    top = (n - i) / n
    bot = (n - i - 1) / n
    y0 = (n - 1 - i) * row_h
    y1 = y0 + row_h
    poly = Polygon([(-top, y1), (top, y1), (bot, y0), (-bot, y0)],
                   closed=True, facecolor=color, edgecolor="white", lw=1.5)
    ax.add_patch(poly)
    ax.text(0, y0 + row_h / 2, f"{label}\n{frac:.0%} of infections",
            ha="center", va="center", color="white", fontsize=9,
            fontweight="bold")

ax.text(0, n * row_h + 0.25, "Surveillance pyramid", ha="center",
        fontsize=11, color=INK, fontweight="bold")
ax.annotate("only the tip is\ncounted as a case",
            xy=(0.12, 0.5), xytext=(1.15, 0.7), fontsize=8, color=MUTED,
            arrowprops=dict(arrowstyle="->", color=INK))
ax.annotate("every infection\nsits in the base",
            xy=(-0.9, n - 0.5), xytext=(-1.9, n - 1.1), fontsize=8,
            color=MUTED, arrowprops=dict(arrowstyle="->", color=INK))

ax.set_xlim(-2.1, 2.1)
ax.set_ylim(-0.3, n * row_h + 0.7)
save(fig, "assets/figures/surveillance-systems.svg")
