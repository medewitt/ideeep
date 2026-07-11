# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Reproducibility is a stack of small habits, not one action. Scripts record
every step, a fixed random seed makes stochastic results identical, a locked
environment pins package versions, project-relative paths keep the code portable,
and a deterministic one-command rebuild ties them together — together these
layers let the same inputs reproduce the same outputs on another machine."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, INK, MUTED, PALETTE

apply_style()

fig, ax = plt.subplots(figsize=(7.6, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

layers = [
    ("scripts — a re-runnable record of every decision", 8.4, PALETTE[0]),
    ("fixed random seed — identical stochastic results", 6.9, PALETTE[2]),
    ("locked environment — pinned package versions (renv.lock)", 5.4, PALETTE[3]),
    ("project-relative paths — portable across machines", 3.9, PALETTE[4]),
    ("deterministic one-command rebuild (make clean && make)", 2.4, PALETTE[1]),
]
for text, y, col in layers:
    ax.add_patch(FancyBboxPatch((0.6, y - 0.6), 8.8, 1.2,
                 boxstyle="round,pad=0.04", linewidth=1.6, edgecolor=col,
                 facecolor=col + "18"))
    ax.text(5.0, y, text, ha="center", va="center", fontsize=8.4, color=INK)

# brace + outcome
ax.add_patch(FancyArrowPatch((9.6, 8.4), (9.6, 2.4), arrowstyle="-",
             color=MUTED, lw=1.4))
ax.annotate("same inputs\n→ same outputs", xy=(9.6, 5.4), xytext=(9.9, 5.4),
            fontsize=8.2, color=INK, va="center")
ax.text(5.0, 0.9, "reproducibility is the stack, not any single layer",
        ha="center", fontsize=8.6, color=MUTED, style="italic")
ax.set_xlim(0, 13)

save(fig, "assets/figures/reproducibility.svg")
