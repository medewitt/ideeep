# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Org mode: one plain-text file holds everything, then exports anywhere. Left: a
single .org file is an outline of headlines (depth = number of stars) that also
carries TODOs, tables, and runnable code blocks, so your thinking and your work
live together. Right: that one file exports to HTML, a LaTeX/PDF report,
Markdown, and Beamer slides, so the same notes become a report or a talk."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from _style import apply_style, save, INK, MUTED, PALETTE

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 3.8),
                               gridspec_kw={"width_ratios": [1.2, 1]})

# ---- one .org outline -----------------------------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 10)
axL.axis("off")
axL.set_title("One .org file: outline + tasks + code", fontsize=9.5)
axL.add_patch(FancyBboxPatch((0.4, 0.5), 9.2, 8.6, boxstyle="round,pad=0.1",
              linewidth=1.6, edgecolor=PALETTE[0], facecolor="#f6f8fa"))
lines = [
    ("* Project: spillover risk", 0, INK),
    ("** Background", 1, INK),
    ("** Analysis", 1, INK),
    ("*** TODO clean data", 2, PALETTE[1]),
    ("*** DONE fit model", 2, PALETTE[2]),
    ("   | region | cases |   (table)", 3, MUTED),
    ("   #+begin_src R  (runnable code)", 3, PALETTE[3]),
    ("** Meeting notes", 1, INK),
]
y = 8.4
for text, depth, col in lines:
    axL.text(0.9 + depth * 0.35, y, text, fontsize=8.4, color=col,
             family="monospace", va="center")
    y -= 1.02

# ---- export fan-out -------------------------------------------------------
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.axis("off")
axR.set_title("Exports to many targets", fontsize=9.5)
axR.add_patch(FancyBboxPatch((0.4, 4.2), 2.6, 1.6, boxstyle="round,pad=0.06",
              linewidth=1.8, edgecolor=PALETTE[0], facecolor=PALETTE[0] + "16"))
axR.text(1.7, 5.0, ".org", ha="center", va="center", fontsize=10, color=INK)
outs = [("HTML", 8.4), ("LaTeX / PDF", 6.2), ("Markdown", 3.8), ("Beamer slides", 1.6)]
for text, y in outs:
    axR.add_patch(FancyBboxPatch((5.6, y - 0.6), 3.8, 1.2,
                  boxstyle="round,pad=0.05", linewidth=1.5, edgecolor=PALETTE[1],
                  facecolor=PALETTE[1] + "12"))
    axR.text(7.5, y, text, ha="center", va="center", fontsize=8.6, color=INK)
    axR.add_patch(FancyArrowPatch((3.0, 5.0), (5.5, y), arrowstyle="-|>",
                  mutation_scale=13, color="0.5", lw=1.3,
                  connectionstyle="arc3,rad=0.12"))

fig.tight_layout()
save(fig, "assets/figures/org-mode.svg")
