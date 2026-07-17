# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Serial dilution and the neutralization titer. Left: a two-fold serial dilution
chain — each tube carries half the concentration of the one before, so the
reciprocal dilution doubles down the row. Right: the percent-neutralization
dose-response for a serum; the 50% neutralization titer (NT50) is read where the
curve crosses 50%, interpolated between the bracketing dilutions, here about
1:196."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.8),
                               gridspec_kw={"width_ratios": [1, 1.15]})

# ---- serial dilution schematic -------------------------------------------
axL.set_xlim(0, 6.4)
axL.set_ylim(0, 4)
axL.axis("off")
axL.set_title("Two-fold serial dilution", fontsize=9.6)
recip = [10, 20, 40, 80, 160, 320]
for k, r in enumerate(recip):
    x = 0.3 + k * 1.02
    shade = 0.85 * 0.62**k + 0.05
    axL.add_patch(Rectangle((x, 1.2), 0.66, 1.6, facecolor=PALETTE[0],
                            alpha=shade, edgecolor=INK, lw=1.0))
    axL.text(x + 0.33, 0.95, f"1:{r}", ha="center", va="top", fontsize=7.8,
             color=INK)
    if k < len(recip) - 1:
        axL.add_patch(FancyArrowPatch((x + 0.7, 2.0), (x + 1.0, 2.0),
                      arrowstyle="-|>", mutation_scale=10, color=MUTED, lw=1.1))
        axL.text(x + 0.85, 2.3, "×2", ha="center", fontsize=7, color=MUTED)
axL.text(3.2, 3.4, "concentration halves each step", ha="center", fontsize=8.3,
         color=INK)

# ---- neutralization dose-response ----------------------------------------
recip = np.array([10, 20, 40, 80, 160, 320, 640, 1280.0])
pct = np.array([98, 95, 88, 72, 55, 38, 20, 8.0])
lx = np.log2(recip)
# NT50 by log-linear interpolation between the bracketing dilutions
i = np.where(pct >= 50)[0][-1]
xstar = lx[i] + (pct[i] - 50) / (pct[i] - pct[i + 1]) * (lx[i + 1] - lx[i])
nt50 = 2**xstar

axR.plot(lx, pct, color=PALETTE[0], lw=1.8, marker="o", ms=6, zorder=3)
axR.axhline(50, color=MUTED, lw=1.0, ls=":")
axR.axvline(xstar, color=PALETTE[1], lw=1.8, ls="--")
axR.scatter([xstar], [50], s=70, color=PALETTE[1], zorder=5)
axR.annotate(f"NT50 ≈ 1:{nt50:.0f}", xy=(xstar, 50), xytext=(xstar - 3.3, 66),
             fontsize=9, color=PALETTE[1], fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=1.0))
axR.set_xticks(lx)
axR.set_xticklabels([f"1:{int(r)}" for r in recip], rotation=45, fontsize=7.6)
axR.set_xlabel("serum dilution")
axR.set_ylabel("% neutralization")
axR.set_title("50% neutralization titer", fontsize=9.6)
axR.set_ylim(0, 105)
fig.tight_layout()
save(fig, "assets/figures/serial-dilution.svg")
