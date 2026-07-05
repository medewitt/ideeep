# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Cost-effectiveness plane: two strategies against a willingness-to-pay threshold."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# Incremental effect (QALYs gained) and incremental cost (£) vs the comparator.
# A: +120 QALYs, +£1.5M  -> ICER = 12,500 £/QALY
# B: +180 QALYs, +£2.9M  -> ICER vs A = 1.4M / 60 = 23,333 £/QALY
comparator = (0.0, 0.0)
A = (120.0, 1_500_000.0)
B = (180.0, 2_900_000.0)

wtp = 30_000.0  # willingness-to-pay threshold, £/QALY

fig, ax = plt.subplots(figsize=(6.4, 4.2))

# Willingness-to-pay threshold line through the origin.
x_line = np.array([0.0, 210.0])
ax.plot(x_line, wtp * x_line, linestyle="--", color=MUTED, linewidth=1.2,
        zorder=1)
ax.annotate("WTP threshold\n£30,000/QALY", (200.0, wtp * 200.0),
            xytext=(-6, 10), textcoords="offset points", ha="right",
            fontsize=8.5, color=MUTED)

# Efficiency frontier: origin -> A -> B.
fx = [comparator[0], A[0], B[0]]
fy = [comparator[1], A[1], B[1]]
ax.plot(fx, fy, color=INK, linewidth=0.9, alpha=0.6, zorder=2)

# Strategy points.
ax.scatter(*comparator, s=60, color=MUTED, edgecolor="white", linewidth=1.0,
           zorder=3)
ax.annotate("comparator\n(no intervention)", comparator, xytext=(8, -4),
            textcoords="offset points", ha="left", va="top", fontsize=8.5,
            color=MUTED)

ax.scatter(*A, s=110, color=PALETTE[0], edgecolor="white", linewidth=1.0,
           zorder=3)
ax.annotate("A", A, xytext=(10, -2), textcoords="offset points", ha="left",
            fontsize=12, color=PALETTE[0], fontweight="bold")

ax.scatter(*B, s=110, color=PALETTE[1], edgecolor="white", linewidth=1.0,
           zorder=3)
ax.annotate("B", B, xytext=(10, -2), textcoords="offset points", ha="left",
            fontsize=12, color=PALETTE[1], fontweight="bold")

ax.set_xlim(0, 210)
ax.set_ylim(0, 6_400_000)
ax.set_xlabel("incremental QALYs gained")
ax.set_ylabel("incremental cost (£)")
ax.set_title("Cost-effectiveness plane")

# Millions on the y-axis for readability.
ax.set_yticks([0, 1e6, 2e6, 3e6, 4e6, 5e6, 6e6])
ax.set_yticklabels(["0", "£1M", "£2M", "£3M", "£4M", "£5M", "£6M"])

save(fig, "assets/figures/cost-effectiveness-analysis.svg")
