# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""The (7,3,1) balanced incomplete block design as an incidence grid: 7 treatments
(rows) across 7 blocks (columns), each block holding 3 treatments (filled cells).
Every treatment appears in 3 blocks and every pair of treatments shares exactly one
block, so no comparison is systematically better estimated than any other."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from _style import apply_style, save, PALETTE, INK

apply_style()

blocks = [(1, 2, 3), (1, 4, 5), (1, 6, 7), (2, 4, 6),
          (2, 5, 7), (3, 4, 7), (3, 5, 6)]        # Fano lines
t, b = 7, 7

fig, ax = plt.subplots(figsize=(6.0, 4.2))
ax.set_xlim(-0.6, b)
ax.set_ylim(-0.9, t)
ax.set_aspect("equal")
ax.axis("off")

for treat in range(1, t + 1):
    row = t - treat
    for blk in range(b):
        filled = treat in blocks[blk]
        ax.add_patch(Rectangle((blk, row), 1, 1,
                               facecolor=PALETTE[0] if filled else "#eef1f4",
                               alpha=0.85 if filled else 1.0,
                               edgecolor="white", lw=1.6))

for treat in range(1, t + 1):
    ax.text(-0.14, t - treat + 0.5, f"t{treat}", ha="right", va="center",
            fontsize=8.5, color=INK)
for blk in range(b):
    ax.text(blk + 0.5, t + 0.02, f"B{blk+1}", ha="center", fontsize=8.5, color=INK)
ax.text(b / 2, t + 0.5, "block", ha="center", fontsize=9, color=INK)
ax.text(-0.5, t / 2, "treatment", rotation=90, va="center", fontsize=9, color=INK)

ax.text(b / 2, -0.55,
        "t=7, b=7, k=3, r=3, $\\lambda$=1  —  every pair shares exactly one block",
        ha="center", fontsize=8.3, color=INK)

fig.tight_layout()
save(fig, "assets/figures/balanced-incomplete-block-designs.svg")
