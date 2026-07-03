# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Big-O growth curves: how the number of steps grows with input size n.

The point is intuition, not precision -- the curves are drawn on a capped
y-axis so a reader can see the *ordering* of growth rates at a glance:
constant and logarithmic stay flat, linear rises steadily, and quadratic
and exponential blow up.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

n = np.linspace(1, 20, 400)

cap = 120                                   # y ceiling so the shape reads

# label anchored explicitly (x, y, ha) so the steep curves don't collide
curves = [
    ("O(2ⁿ)  exponential",  2.0**n,         "#b0332f",  (4.6,  108, "right")),
    ("O(n²)  quadratic",    n**2,           PALETTE[1], (9.3,  100, "left")),
    ("O(n log n)",          n * np.log2(n), PALETTE[3], (20.4,  86, "left")),
    ("O(n)  linear",        n,              PALETTE[4], (20.4,  20, "left")),
    ("O(log n)  log",       np.log2(n),     PALETTE[0], (20.4,   6, "left")),
    ("O(1)  constant",      np.ones_like(n),PALETTE[2], (20.4,  -3, "left")),
]

fig, ax = plt.subplots()

for label, y, color, (lx, ly, ha) in curves:
    ax.plot(n, np.minimum(y, cap * 1.02), color=color, lw=2.2, label=label)
    ax.annotate(label, xy=(lx, ly), color=color, fontsize=8.5,
                va="center", ha=ha, fontweight="bold",
                annotation_clip=False)

ax.set_ylim(0, cap)
ax.set_xlim(1, 20)
ax.set_xlabel("input size  n  (how much data)")
ax.set_ylabel("work  (number of steps)")
ax.set_title("How different algorithms scale as the data grows")
ax.text(1.2, cap * 0.93, "flat is good ·  steep is trouble",
        color=MUTED, fontsize=9, style="italic")

save(fig, "assets/figures/big-o-growth.svg")
