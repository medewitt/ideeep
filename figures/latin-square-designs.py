# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""A 4x4 Latin square: rows are one blocking factor (e.g. subjects), columns
another (e.g. periods), and the letters A-D are treatments. Each letter occurs once
in every row and once in every column, so averaging over the square balances both
blocking factors against every treatment."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from _style import apply_style, save, PALETTE, INK

apply_style()

letters = ["A", "B", "C", "D"]
square = [[letters[(j + i) % 4] for j in range(4)] for i in range(4)]  # cyclic
col_of = {L: PALETTE[i] for i, L in enumerate(letters)}
n = 4

fig, ax = plt.subplots(figsize=(5.4, 4.4))
ax.set_xlim(-0.9, n)
ax.set_ylim(-0.9, n)
ax.set_aspect("equal")
ax.axis("off")

for i in range(n):
    row = n - 1 - i
    for j in range(n):
        L = square[i][j]
        ax.add_patch(Rectangle((j, row), 1, 1, facecolor=col_of[L], alpha=0.20,
                               edgecolor=col_of[L], lw=1.6))
        ax.text(j + 0.5, row + 0.5, L, ha="center", va="center", fontsize=13,
                color=INK, fontweight="bold")

for j in range(n):
    ax.text(j + 0.5, n + 0.02, f"period {j+1}", ha="center", fontsize=8.3, color=INK)
for i in range(n):
    ax.text(-0.12, n - 1 - i + 0.5, f"subj {i+1}", ha="right", va="center",
            fontsize=8.3, color=INK)

ax.text(n / 2, -0.5, "each treatment once per row and once per column",
        ha="center", fontsize=8.3, color=INK)
ax.text(n / 2, n + 0.45, "column blocking factor", ha="center", fontsize=8.8,
        color=INK)
ax.text(-0.72, n / 2, "row blocking factor", rotation=90, va="center",
        fontsize=8.8, color=INK)

fig.tight_layout()
save(fig, "assets/figures/latin-square-designs.svg")
