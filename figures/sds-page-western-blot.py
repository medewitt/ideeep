# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""SDS-PAGE and Western blotting. Left: SDS coats every protein with uniform
negative charge, so migration through the gel depends on size alone — run beside
a ladder of known molecular weights, smaller proteins travel farther, and
migration distance is linear in log(molecular weight). Right: the Western blot
adds a second, independent constraint — transfer the bands to a membrane, block,
probe with a primary + labelled secondary antibody, and a signal appears only at
the target protein's size, so size AND antibody recognition must agree."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 3.8),
                               gridspec_kw={"width_ratios": [1.1, 1]})

# ---- migration vs log(MW) + gel lane --------------------------------------
mw = np.array([250, 150, 100, 75, 50, 37, 25, 15])       # kDa ladder
# migration distance: linear in -log10(MW)
dist = 1.2 + 3.4 * (np.log10(250) - np.log10(mw)) / (np.log10(250) - np.log10(15))
axL.plot(np.log10(mw), dist, color=PALETTE[0], lw=1.6, marker="o", ms=4,
         zorder=3)
axL.invert_yaxis()
axL.set_xlabel(r"$\log_{10}$ molecular weight (kDa)")
axL.set_ylabel("migration distance →")
axL.set_title("Migration is linear in log(MW)", fontsize=9.5)
axL.annotate("smaller = faster\n(travels farther)", xy=(np.log10(15), dist[-1]),
             xytext=(1.55, 3.2), fontsize=7.8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

# schematic gel lane (inset-style, on the right of the axes)
gx = 2.55
axL.add_patch(Rectangle((gx, 0.6), 0.5, 4.4, transform=axL.transData,
              facecolor="#eef2f5", edgecolor=MUTED, lw=0.8, clip_on=False))
for d in dist:
    axL.add_patch(Rectangle((gx, d - 0.06), 0.5, 0.12, facecolor=INK,
                  clip_on=False))
axL.text(gx + 0.25, 0.35, "ladder", fontsize=7, ha="center", color=INK)
axL.set_xlim(1.1, 2.5)

# ---- Western blot workflow ------------------------------------------------
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.axis("off")
axR.set_title("Western blot: size + antibody", fontsize=9.5)
steps = [("1. transfer\nto membrane", 8.4, PALETTE[0]),
         ("2. block", 6.4, PALETTE[2]),
         ("3. probe: primary +\nlabelled secondary Ab", 4.2, PALETTE[3]),
         ("4. detect band at\nthe target's size", 1.9, PALETTE[1])]
for text, y, col in steps:
    axR.add_patch(FancyBboxPatch((1.4, y - 0.7), 7.0, 1.4,
                  boxstyle="round,pad=0.06", linewidth=1.6, edgecolor=col,
                  facecolor=col + "16"))
    axR.text(5.0, y, text, ha="center", va="center", fontsize=8.2, color=INK)
for y in (7.6, 5.6, 3.4):
    axR.add_patch(FancyArrowPatch((5.0, y), (5.0, y - 0.5), arrowstyle="-|>",
                  mutation_scale=13, color="0.4", lw=1.4))

fig.tight_layout()
save(fig, "assets/figures/sds-page-western-blot.svg")
