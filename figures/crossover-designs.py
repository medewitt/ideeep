# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""The 2x2 crossover schematic. Sequence AB receives treatment A in period 1 and
B in period 2; sequence BA receives them in the opposite order, with a washout
between periods. Each subject contributes a within-person A-versus-B contrast, and
comparing the two sequences separates the treatment effect from a period effect."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, ax = plt.subplots(figsize=(7.0, 3.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis("off")

treat_col = {"A": PALETTE[0], "B": PALETTE[1]}


def cell(x, y, label):
    ax.add_patch(Rectangle((x, y), 2.2, 1.0, facecolor=treat_col[label],
                           alpha=0.20, edgecolor=treat_col[label], lw=1.6))
    ax.text(x + 1.1, y + 0.5, f"treatment {label}", ha="center", va="center",
            fontsize=9.5, color=INK)


# column headers
ax.text(1.7, 3.6, "Period 1", ha="center", fontsize=9.5, color=INK)
ax.text(5.0, 3.6, "washout", ha="center", fontsize=9, color=MUTED, style="italic")
ax.text(8.3, 3.6, "Period 2", ha="center", fontsize=9.5, color=INK)

for row, (seq, (t1, t2)) in enumerate([("AB", ("A", "B")), ("BA", ("B", "A"))]):
    y = 2.0 - row * 1.5
    ax.text(-0.0, y + 0.5, f"seq {seq}", ha="left", va="center", fontsize=9,
            color=INK, fontweight="bold")
    cell(1.2, y, t1)
    cell(7.2, y, t2)
    # washout gap arrow
    ax.add_patch(FancyArrowPatch((3.5, y + 0.5), (7.1, y + 0.5),
                 arrowstyle="-|>", mutation_scale=12, color=MUTED, lw=1.2,
                 linestyle=(0, (4, 3))))

ax.annotate("each subject is its own control\n(within-subject A vs B)",
            xy=(8.3, 0.5), xytext=(4.2, -0.15), fontsize=8.3, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))

fig.tight_layout()
save(fig, "assets/figures/crossover-designs.svg")
