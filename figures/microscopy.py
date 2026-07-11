# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Diagnostic microscopy. Left: under polarized light a shape-and-colour rule
tells two arthritides apart — monosodium urate crystals (gout) are needle-shaped
and negatively birefringent (yellow when parallel to the compensator, blue when
perpendicular), while calcium pyrophosphate crystals (pseudogout) are rhomboid
and positively birefringent (the opposite colours). Right: the two malaria blood
films — a thick film stacks many layers to detect parasites at low density,
while a thin film preserves red-cell morphology to speciate and quantify
parasitemia."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

YELLOW, BLUE = "#c9a227", "#2f6f9f"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 3.9))

# ---- crystal shape x birefringence colour ---------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 10)
axL.axis("off")
axL.set_title("Crystals under polarized light", fontsize=9.8)
# column headers
axL.text(5.0, 9.3, "parallel ∥", ha="center", fontsize=8, color=INK)
axL.text(8.0, 9.3, "perpendicular ⊥", ha="center", fontsize=8, color=INK)


def needle(ax, x, y, color, ang=25):
    ax.add_patch(Rectangle((x - 0.9, y - 0.12), 1.8, 0.24, angle=ang,
                 rotation_point="center", facecolor=color, edgecolor=INK,
                 lw=0.6))


def rhomb(ax, x, y, color):
    pts = np.array([[x - 0.7, y], [x, y + 0.5], [x + 0.7, y], [x, y - 0.5]])
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=INK,
                 lw=0.6))


# urate row (gout): needle, negatively birefringent -> yellow parallel
axL.text(1.6, 6.6, "urate\n(gout)\nneedle,\nnegative", fontsize=7.6,
         color=INK, ha="center", va="center")
needle(axL, 5.0, 6.6, YELLOW)
needle(axL, 8.0, 6.6, BLUE)
# CPPD row (pseudogout): rhomboid, positively birefringent -> blue parallel
axL.text(1.6, 3.0, "CPPD\n(pseudogout)\nrhomboid,\npositive", fontsize=7.6,
         color=INK, ha="center", va="center")
rhomb(axL, 5.0, 3.0, BLUE)
rhomb(axL, 8.0, 3.0, YELLOW)
axL.axhline(0.06, xmin=0.06, xmax=0.06)   # no-op keeps layout tidy
axL.text(5.0, 0.7, "shape + colour ⇒ diagnosis in minutes", ha="center",
         fontsize=8, color=MUTED, style="italic")

# ---- thick vs thin malaria film -------------------------------------------
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.axis("off")
axR.set_title("Malaria blood films", fontsize=9.8)
rng = np.random.default_rng(4)

# thick film: overlapping cells, a couple of parasites
axR.text(2.6, 9.2, "thick film", ha="center", fontsize=8.5, color=PALETTE[1])
axR.add_patch(Circle((2.6, 5.6), 2.2, facecolor=PALETTE[1] + "18",
              edgecolor=PALETTE[1], lw=1.0))
for _ in range(40):
    a = rng.uniform(0, 2 * np.pi); r = rng.uniform(0, 1.8)
    axR.add_patch(Circle((2.6 + r * np.cos(a), 5.6 + r * np.sin(a)), 0.28,
                  facecolor=MUTED + "44", edgecolor="none"))
for px, py in [(2.2, 6.0), (3.1, 5.0), (2.7, 6.3)]:
    axR.add_patch(Circle((px, py), 0.13, color=PALETTE[3]))
axR.text(2.6, 2.9, "many layers →\ndetect low density", ha="center",
         fontsize=7.6, color=INK)

# thin film: single layer of intact RBCs, ring forms inside
axR.text(7.4, 9.2, "thin film", ha="center", fontsize=8.5, color=PALETTE[0])
for i in range(4):
    for j in range(3):
        cx, cy = 5.9 + i * 1.0, 4.7 + j * 1.0
        axR.add_patch(Circle((cx, cy), 0.42, facecolor="none",
                      edgecolor=PALETTE[1], lw=1.2))
# a couple of infected cells with a ring
for cx, cy in [(6.9, 5.7), (7.9, 4.7)]:
    axR.add_patch(Circle((cx, cy), 0.42, facecolor="none", edgecolor=PALETTE[1],
                  lw=1.2))
    axR.add_patch(Circle((cx + 0.12, cy + 0.1), 0.12, facecolor="none",
                  edgecolor=PALETTE[3], lw=1.6))
axR.text(7.4, 2.9, "intact cells →\nspeciate & quantify", ha="center",
         fontsize=7.6, color=INK)

fig.tight_layout()
save(fig, "assets/figures/microscopy.svg")
