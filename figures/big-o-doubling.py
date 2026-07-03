# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""The doubling test: if you double the data, how much more work is it?

This is the practical, everyday intuition for complexity. You rarely need
the formula -- you need to know what happens when your sample size doubles.
Each bar shows the factor by which the work multiplies when n -> 2n.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()

# factor by which work grows when the input doubles (n -> 2n)
classes = [
    ("O(1)\nconstant",       1.0,  PALETTE[2]),
    ("O(log n)\nlog",        1.1,  PALETTE[0]),   # +1 step; ~unchanged
    ("O(n)\nlinear",         2.0,  PALETTE[4]),
    ("O(n log n)",           2.1,  PALETTE[3]),   # just above 2x
    ("O(n²)\nquadratic",     4.0,  PALETTE[1]),
    ("O(2ⁿ)\nexponential",  10.0,  "#b0332f"),    # squares -> off the chart
]

labels = [c[0] for c in classes]
factors = [c[1] for c in classes]
colors = [c[2] for c in classes]

fig, ax = plt.subplots(figsize=(6.6, 3.8))
x = np.arange(len(classes))
bars = ax.bar(x, factors, color=colors, width=0.68)

ax.axhline(1, color="0.55", ls="--", lw=1.0)
ax.text(len(classes) - 0.5, 1.15, "no extra work", color="0.4",
        fontsize=8, ha="right")

readout = ["1×", "~1×", "2×", "~2×", "4×", "explodes"]
for xi, f, txt in zip(x, factors, readout):
    ax.annotate(txt, xy=(xi, f), xytext=(0, 3), textcoords="offset points",
                ha="center", fontsize=9, fontweight="bold", color=INK)

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylim(0, 11)
ax.set_yticks([1, 2, 4, 6, 8, 10])
ax.set_ylabel("work multiplies by…")
ax.set_title("Double the data — how much more work?")
ax.grid(axis="x", visible=False)

save(fig, "assets/figures/big-o-doubling.svg")
