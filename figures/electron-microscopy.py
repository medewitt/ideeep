# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Electron microscopy. Left: a log-scale size/resolution ladder — light
microscopy runs out near 200 nm, too coarse to see a virus, while electrons
resolve down to about 1 nm, bringing virions and proteins into view. Right: the
two modes — transmission EM (TEM) passes electrons through an ultrathin section
to show internal structure, while scanning EM (SEM) sweeps a beam across the
surface to build a three-dimensional image of the exterior."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 3.8),
                               gridspec_kw={"width_ratios": [1.1, 1]})

# ---- resolution / size ladder ---------------------------------------------
axL.set_xscale("log")
axL.set_xlim(1, 1e5)
axL.set_ylim(0, 6)
axL.set_yticks([])
axL.set_title("What each microscope can resolve", fontsize=10)

# resolution limits
axL.axvspan(1, 200, color=PALETTE[0] + "18", zorder=0)
axL.axvline(200, color=PALETTE[1], lw=1.6)
axL.text(230, 5.4, "light-microscopy\nlimit ~200 nm", fontsize=8,
         color=PALETTE[1])
axL.axvline(1, color=PALETTE[0], lw=1.6)
axL.text(1.2, 5.4, "EM limit\n~1 nm", fontsize=8, color=PALETTE[0])
axL.annotate("", xy=(1, 4.6), xytext=(200, 4.6),
             arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.0))
axL.text(15, 4.75, "only EM can see here", fontsize=7.6, color=MUTED,
         ha="center")

objs = [("protein", 5, 1.0, PALETTE[3]), ("virion", 100, 2.2, PALETTE[1]),
        ("bacterium", 1000, 3.2, PALETTE[2]), ("human cell", 20000, 3.2,
        PALETTE[4])]
for name, size, y, col in objs:
    axL.scatter([size], [y], s=70, color=col, zorder=5)
    axL.annotate(f"{name}\n(~{size} nm)", (size, y),
                 textcoords="offset points", xytext=(0, 8), ha="center",
                 fontsize=7.4, color=INK)
axL.set_xlabel("size (nm, log scale)")

# ---- TEM vs SEM schematic -------------------------------------------------
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.axis("off")
axR.set_title("Two modes", fontsize=10)

# TEM (top): beam through thin section
axR.text(5, 9.4, "TEM — through a thin section", ha="center", fontsize=8.5,
         color=PALETTE[0])
axR.add_patch(Rectangle((3.5, 7.2), 3.0, 0.28, color=INK))       # section
for x in np.linspace(4.0, 6.0, 4):
    axR.add_patch(FancyArrowPatch((x, 8.6), (x, 7.5), arrowstyle="-|>",
                  mutation_scale=10, color=PALETTE[0], lw=1.2))
    axR.add_patch(FancyArrowPatch((x, 7.2), (x, 6.2), arrowstyle="-|>",
                  mutation_scale=10, color=PALETTE[0] + "66", lw=1.0))
axR.text(7.0, 7.3, "internal\nstructure", fontsize=7.6, color=INK, va="center")

# SEM (bottom): beam sweeps surface
axR.text(5, 4.6, "SEM — sweeps the surface", ha="center", fontsize=8.5,
         color=PALETTE[1])
axR.add_patch(Rectangle((3.5, 1.6), 3.0, 0.9, facecolor=MUTED + "44",
              edgecolor=MUTED))
for i, x in enumerate(np.linspace(4.0, 6.0, 4)):
    axR.add_patch(FancyArrowPatch((x - 0.4, 3.9), (x, 2.55), arrowstyle="-|>",
                  mutation_scale=10, color=PALETTE[1], lw=1.2))
    # scattered back up
    axR.add_patch(FancyArrowPatch((x, 2.55), (x + 0.5, 3.7), arrowstyle="-|>",
                  mutation_scale=9, color=PALETTE[1] + "66", lw=1.0))
axR.text(7.0, 2.05, "3-D surface", fontsize=7.6, color=INK, va="center")

fig.tight_layout()
save(fig, "assets/figures/electron-microscopy.svg")
