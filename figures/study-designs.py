# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Schematic of epidemiologic study designs by direction of inquiry and timing."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, ax = plt.subplots(figsize=(7.4, 4.2))
ax.grid(False)
ax.set_yticks([])
for spine in ("left", "top", "right"):
    ax.spines[spine].set_visible(False)

x_present = 5.0


def box(x, y, w, text, color):
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - 0.22), w, 0.44,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=0, facecolor=color, alpha=0.9))
    ax.text(x, y, text, ha="center", va="center", fontsize=8.5, color="white")


def arrow(x0, x1, y, color):
    ax.add_patch(FancyArrowPatch(
        (x0, y), (x1, y), arrowstyle="-|>", mutation_scale=14,
        lw=1.8, color=color, shrinkA=2, shrinkB=2))


rows = [3.0, 2.0, 1.0, 0.0]
names = ["Randomized trial", "Cohort", "Case-control", "Cross-sectional"]

# Randomized trial: randomize now, follow forward to outcome.
box(5.0, rows[0], 2.0, "randomize", PALETTE[3])
box(8.0, rows[0], 1.8, "outcome", PALETTE[1])
arrow(6.1, 7.05, rows[0], INK)

# Cohort: exposure first, follow forward to outcome.
box(3.6, rows[1], 1.8, "exposure", PALETTE[0])
box(8.0, rows[1], 1.8, "outcome", PALETTE[1])
arrow(4.55, 7.05, rows[1], INK)

# Case-control: start from outcome, look back to exposure.
box(2.2, rows[2], 1.8, "exposure", PALETTE[0])
box(6.4, rows[2], 2.0, "cases / controls", PALETTE[1])
arrow(5.35, 3.15, rows[2], MUTED)

# Cross-sectional: exposure and outcome measured together, one snapshot.
box(5.0, rows[3], 2.6, "exposure + outcome", PALETTE[2])

# Row labels on the left.
for y, name in zip(rows, names):
    ax.text(-2.9, y, name, ha="left", va="center", fontsize=9.5, color=INK)

# Present line and time axis.
ax.axvline(x_present, ls=":", lw=1.0, color=MUTED, zorder=0)
ax.text(x_present, 3.75, "present", ha="center", va="bottom",
        fontsize=8.5, color=MUTED)
ax.annotate("", xy=(9.2, -0.9), xytext=(0.2, -0.9),
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
ax.text(0.2, -1.15, "past", ha="left", va="top", fontsize=8.5, color=INK)
ax.text(9.2, -1.15, "future", ha="right", va="top", fontsize=8.5, color=INK)
ax.text(4.7, -1.15, "time", ha="center", va="top", fontsize=8.5, color=MUTED)

ax.set_xlim(-3.0, 9.6)
ax.set_ylim(-1.5, 4.1)
ax.set_title("Study designs by direction of inquiry")
save(fig, "assets/figures/study-designs.svg")
