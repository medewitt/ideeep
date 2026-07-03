# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""From a tangled script to a reusable package. On the left, one long script
mixes data cleaning, modelling, plotting, and copy-pasted helpers -- hard to
reuse or test. On the right, the same work is split into small single-purpose
functions in a package, with tests and docs, and the analysis script becomes a
short, readable file that just calls the package.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, INK

apply_style()

fig, ax = plt.subplots(figsize=(7.4, 4.4))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis("off")

RED, GREEN, BLUE = "#c1531f", "#3f8f5b", "#2f6f9f"


def box(x, y, w, h, text, color, fc=None, fs=9, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04",
                 linewidth=1.4, edgecolor=color,
                 facecolor=fc if fc else color + "18"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=INK, fontweight="bold" if bold else "normal")


# ---- left: one tangled script ----
ax.text(2.6, 9.4, "analysis.R  (600 lines)", ha="center", fontsize=10,
        fontweight="bold", color=RED)
ax.add_patch(FancyBboxPatch((0.5, 1.6), 4.2, 7.2, boxstyle="round,pad=0.04",
             linewidth=1.8, edgecolor=RED, facecolor=RED + "10"))
messy = ["load data", "clean data (inline)", "fit model", "a helper function",
         "MORE cleaning", "copy-pasted code", "another plot", "copy-pasted again"]
for i, m in enumerate(messy):
    box(0.9, 7.9 - i * 0.78, 3.4, 0.58, m, "#b8632f", fc="white", fs=8)

# ---- arrow ----
ax.add_patch(FancyArrowPatch((5.0, 5.2), (6.1, 5.2), arrowstyle="-|>",
             mutation_scale=20, color="0.4", lw=2.0))
ax.text(5.55, 5.7, "refactor", ha="center", fontsize=9, color="0.4",
        fontweight="bold")

# ---- right: a package ----
ax.text(10.2, 9.4, "mypkg/  (a package)", ha="center", fontsize=10,
        fontweight="bold", color=GREEN)
ax.add_patch(FancyBboxPatch((6.4, 3.2), 7.2, 5.6, boxstyle="round,pad=0.04",
             linewidth=1.8, edgecolor=GREEN, facecolor=GREEN + "10"))
box(6.8, 7.6, 3.1, 0.7, "R/clean.R", GREEN, fc="white", fs=8.5)
box(6.8, 6.7, 3.1, 0.7, "R/model.R", GREEN, fc="white", fs=8.5)
box(6.8, 5.8, 3.1, 0.7, "R/plot.R", GREEN, fc="white", fs=8.5)
box(10.2, 7.6, 3.0, 0.7, "tests/", BLUE, fc="white", fs=8.5)
box(10.2, 6.7, 3.0, 0.7, "man/  (docs)", BLUE, fc="white", fs=8.5)
box(10.2, 5.8, 3.0, 0.7, "DESCRIPTION", BLUE, fc="white", fs=8.5)
ax.text(10.0, 4.6, "small, single-purpose, tested, documented functions",
        ha="center", fontsize=8, color="0.4", style="italic")

# thin analysis script that calls the package
box(6.8, 1.5, 6.4, 1.1, "analysis.R  →  library(mypkg)  (20 lines)",
    "#26323f", fc="white", fs=9, bold=True)
ax.add_patch(FancyArrowPatch((10.0, 2.65), (10.0, 3.15), arrowstyle="-|>",
             mutation_scale=16, color="0.4", lw=1.6))

fig.suptitle("From a tangled script to a reusable package", y=1.0,
             fontsize=12, color=INK)
save(fig, "assets/figures/package-anatomy.svg")
