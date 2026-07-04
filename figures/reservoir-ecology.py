# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Multi-host reservoir schematic and community persistence.

Two host species each fail to maintain the pathogen alone (single-host
R0 < 1), yet the coupled community sustains it (dominant eigenvalue of
the next-generation matrix > 1). Spillover reaches a dead-end human host.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axl, axr) = plt.subplots(
    1, 2, figsize=(8.4, 3.8), gridspec_kw={"width_ratios": [1.15, 1.0]}
)

# ---- Left panel: multi-host transmission schematic ----
axl.set_xlim(0, 10)
axl.set_ylim(0, 10)
axl.axis("off")
axl.set_title("Maintenance community", fontsize=11)


def box(ax, xy, w, h, color, label):
    x, y = xy
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.15,rounding_size=0.25",
        linewidth=1.6, edgecolor=color, facecolor=color + "22"))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=9.5, color=INK)


box(axl, (0.6, 6.2), 3.4, 2.2, PALETTE[0], "Host A\n$R_0^{A}=0.7$")
box(axl, (0.6, 1.4), 3.4, 2.2, PALETTE[2], "Host B\n$R_0^{B}=0.6$")
box(axl, (6.4, 3.8), 3.0, 2.2, PALETTE[1], "Humans\n(dead-end)")


def arrow(ax, a, b, color, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(
        a, b, arrowstyle="-|>", mutation_scale=13, linewidth=1.6,
        color=color, linestyle=ls,
        connectionstyle=f"arc3,rad={rad}"))


# Cross-species transmission couples the two hosts.
arrow(axl, (3.4, 6.4), (3.4, 3.6), PALETTE[0], rad=-0.35)
arrow(axl, (1.2, 3.6), (1.2, 6.2), PALETTE[2], rad=-0.35)
axl.text(4.3, 5.0, "cross-species\ntransmission", ha="left", va="center",
         fontsize=8.5, color=MUTED)
# Spillover to humans (dead-end, no return).
arrow(axl, (4.0, 6.6), (6.4, 5.2), PALETTE[1], rad=0.15, ls="--")
arrow(axl, (4.0, 2.2), (6.4, 4.2), PALETTE[1], rad=-0.15, ls="--")
axl.text(5.2, 6.6, "spillover", ha="center", va="center",
         fontsize=8.5, color=MUTED)

# ---- Right panel: community R0 vs coupling strength ----
# Neither host alone exceeds 1; coupling lifts the dominant eigenvalue > 1.
kappa = np.linspace(0.0, 1.0, 200)     # cross-species coupling strength
Raa, Rbb, Rref = 0.7, 0.6, 0.9
Rab = kappa * Rref
Rba = kappa * Rref
tr = Raa + Rbb
det = Raa * Rbb - Rab * Rba
lam = 0.5 * (tr + np.sqrt(tr**2 - 4 * det))

axr.plot(kappa, lam, color=PALETTE[3], lw=2.2, label="community $R_0$")
axr.axhline(1.0, color=INK, lw=1.0, ls=":", zorder=1)
axr.axhline(Raa, color=PALETTE[0], lw=1.4, ls="--", label="host A alone")
axr.axhline(Rbb, color=PALETTE[2], lw=1.4, ls="--", label="host B alone")

cross = np.interp(1.0, lam, kappa)
axr.plot([cross], [1.0], "o", color=PALETTE[3], ms=7, zorder=5)
axr.annotate("persistence\nthreshold", xy=(cross, 1.0),
             xytext=(cross + 0.06, 1.28), fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK))
axr.set_xlabel("cross-species coupling")
axr.set_ylabel("dominant eigenvalue")
axr.set_title("Persistence needs the community", fontsize=11)
axr.set_ylim(0.4, 1.9)
axr.legend(loc="upper left", fontsize=8)

save(fig, "assets/figures/reservoir-ecology.svg")
