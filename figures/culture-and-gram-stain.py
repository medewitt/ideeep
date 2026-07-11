# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Culture and the Gram stain. Left: the Gram stain sorts bacteria by cell-wall
structure — a thick peptidoglycan layer (Gram-positive) traps the crystal
violet-iodine complex through the alcohol wash and stays purple, while a thin
wall behind an outer membrane (Gram-negative) decolorizes and takes up the pink
safranin counterstain. Right: disk diffusion (Kirby-Bauer) reads antibiotic
susceptibility from the diameter of the growth-free zone around each disk, which
maps to susceptible / intermediate / resistant."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

PURPLE, PINK, GREEN = "#8a5cb0", "#c1531f", "#3f8f5b"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 3.8),
                               gridspec_kw={"width_ratios": [1.15, 1]})

# ---- Gram cell-wall schematic ---------------------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 10)
axL.axis("off")
axL.set_title("Cell wall decides the colour", fontsize=10)


def membrane(x0, y0, w, color, h=0.32):
    axL.add_patch(Rectangle((x0, y0), w, h, color=color))


# Gram-positive: thick peptidoglycan, stays purple
axL.text(2.5, 9.2, "Gram-positive", ha="center", fontsize=9.5, color=PURPLE)
membrane(0.5, 6.4, 4.0, INK)                        # plasma membrane
axL.add_patch(Rectangle((0.5, 6.8), 4.0, 1.9, facecolor=PURPLE + "55",
              edgecolor=PURPLE, lw=1.2))
axL.text(2.5, 7.75, "thick\npeptidoglycan", ha="center", va="center",
         fontsize=8, color=INK)
axL.text(2.5, 5.6, "traps crystal-violet–\niodine → stays purple", ha="center",
         fontsize=8, color=PURPLE)
axL.add_patch(Circle((2.5, 3.9), 0.9, facecolor=PURPLE + "88",
              edgecolor=PURPLE, lw=1.5))
axL.text(2.5, 3.9, "purple", ha="center", va="center", fontsize=8, color="white")

# Gram-negative: thin wall + outer membrane, turns pink
axL.text(7.5, 9.2, "Gram-negative", ha="center", fontsize=9.5, color=PINK)
membrane(5.5, 6.4, 4.0, INK)                        # plasma membrane
axL.add_patch(Rectangle((5.5, 6.75), 4.0, 0.5, facecolor=PINK + "55",
              edgecolor=PINK, lw=1.0))               # thin peptidoglycan
membrane(5.5, 7.45, 4.0, "#b0842f")                  # outer membrane
axL.text(9.9, 7.5, "outer\nmembrane", ha="left", va="center", fontsize=7,
         color="#b0842f")
axL.text(7.5, 5.6, "loses the dye in alcohol →\npink safranin", ha="center",
         fontsize=8, color=PINK)
axL.add_patch(Circle((7.5, 3.9), 0.9, facecolor=PINK + "88",
              edgecolor=PINK, lw=1.5))
axL.text(7.5, 3.9, "pink", ha="center", va="center", fontsize=8, color="white")

axL.text(5.0, 1.6, "thin peptidoglycan (0.5 wide) vs thick (1.9)",
         ha="center", fontsize=7.5, color=MUTED, style="italic")

# ---- Kirby-Bauer disk diffusion -------------------------------------------
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.set_aspect("equal")
axR.axis("off")
axR.set_title("Disk diffusion (Kirby–Bauer)", fontsize=10)

# plate = lawn of bacteria
axR.add_patch(Circle((5, 5.3), 4.3, facecolor=GREEN + "44", edgecolor=GREEN,
              lw=1.5))
axR.text(5, 9.3, "bacterial lawn", ha="center", fontsize=8, color=GREEN)

disks = [((3.4, 6.4), 1.7, "susceptible", PALETTE[0]),
         ((6.7, 6.3), 1.0, "intermediate", PALETTE[4]),
         ((5.0, 2.9), 0.45, "resistant", PALETTE[1])]
for (cx, cy), zr, lab, col in disks:
    # zone of inhibition (clear)
    axR.add_patch(Circle((cx, cy), zr, facecolor="white", edgecolor=col,
                  lw=1.3, zorder=3))
    # antibiotic disk
    axR.add_patch(Circle((cx, cy), 0.32, facecolor="#d8dee4",
                  edgecolor=INK, lw=0.8, zorder=4))
    axR.annotate("", xy=(cx + zr, cy), xytext=(cx, cy),
                 arrowprops=dict(arrowstyle="<->", color=col, lw=1.0), zorder=5)
    axR.text(cx, cy - zr - 0.25, lab, ha="center", va="top", fontsize=7.6,
             color=col)

axR.text(5, 0.4, "larger clear zone → more susceptible",
         ha="center", fontsize=8, color=INK)

fig.tight_layout()
save(fig, "assets/figures/culture-and-gram-stain.svg")
