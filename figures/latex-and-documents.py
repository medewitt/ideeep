# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""One plain-text math source, many outputs. The same LaTeX notation written
once — inline as $...$ or in an .Rmd / .qmd source — renders through the same
toolchain (LaTeX/tinytex for print, KaTeX or MathJax for the web) into a paper
PDF, an HTML page, slides, and a notebook, so the equation you type is portable
across every target."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, INK, MUTED, PALETTE

apply_style()

fig, ax = plt.subplots(figsize=(8.2, 4.0))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis("off")

# source box
ax.add_patch(FancyBboxPatch((0.5, 3.0), 3.7, 2.0, boxstyle="round,pad=0.08",
             linewidth=2.0, edgecolor=PALETTE[0], facecolor=PALETTE[0] + "16"))
ax.text(2.35, 4.35, "one source", ha="center", fontsize=10, color=INK)
ax.text(2.35, 3.65, r"$\hat\beta=(X^\top X)^{-1}X^\top y$", ha="center",
        fontsize=10, color=INK)
ax.text(2.35, 2.55, ".tex · .Rmd · .qmd", ha="center", fontsize=8, color=MUTED)

# toolchain hub
ax.add_patch(FancyBboxPatch((5.3, 3.3), 2.6, 1.4, boxstyle="round,pad=0.06",
             linewidth=1.6, edgecolor=PALETTE[3], facecolor=PALETTE[3] + "14"))
ax.text(6.6, 4.0, "LaTeX / tinytex\nKaTeX · MathJax", ha="center",
        va="center", fontsize=8, color=INK)
ax.add_patch(FancyArrowPatch((4.2, 4.0), (5.3, 4.0), arrowstyle="-|>",
             mutation_scale=15, color="0.4", lw=1.7))

# output cards
outs = [("paper PDF", 6.6), ("HTML page", 4.9), ("slides", 3.2), ("notebook", 1.5)]
for text, y in outs:
    ax.add_patch(FancyBboxPatch((10.4, y - 0.55), 3.0, 1.1,
                 boxstyle="round,pad=0.05", linewidth=1.5, edgecolor=PALETTE[1],
                 facecolor=PALETTE[1] + "12"))
    ax.text(11.9, y, text, ha="center", va="center", fontsize=8.6, color=INK)
    ax.add_patch(FancyArrowPatch((7.9, 4.0), (10.3, y), arrowstyle="-|>",
                 mutation_scale=13, color="0.5", lw=1.3,
                 connectionstyle="arc3,rad=0.12"))

ax.text(7.0, 7.4, "the same math notation is portable across every output",
        ha="center", fontsize=9.5, color=INK, style="italic")

save(fig, "assets/figures/latex-and-documents.svg")
