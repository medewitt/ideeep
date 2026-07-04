# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Pairwise invasibility plot for a transmission-virulence trade-off."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from _style import apply_style, save, PALETTE, INK

apply_style()

gamma, mu, a = 0.5, 0.1, 3.0
x_star = gamma + mu   # singular strategy = argmax R0 for beta(alpha)=a*sqrt(alpha)


def R0(alpha):
    return a * np.sqrt(alpha) / (gamma + alpha + mu)


lo, hi = 0.02, 2.5
alpha = np.linspace(lo, hi, 400)
X, Y = np.meshgrid(alpha, alpha)     # X: resident, Y: mutant
invades = (R0(Y) - R0(X) > 0).astype(float)   # 1 where the mutant invades

fig, ax = plt.subplots()
cmap = ListedColormap(["#eef2f5", PALETTE[0]])
# imshow embeds a single raster (small SVG); origin lower so y increases up.
ax.imshow(invades, origin="lower", extent=[lo, hi, lo, hi], cmap=cmap,
          vmin=0, vmax=1, aspect="auto", interpolation="nearest")

ax.plot(alpha, alpha, color=INK, lw=1.0)      # neutral diagonal y = x
ax.axvline(x_star, color=PALETTE[1], lw=1.4, ls="--")
ax.axhline(x_star, color=PALETTE[1], lw=1.4, ls="--")
ax.plot(x_star, x_star, "o", color=PALETTE[1], ms=8, zorder=5)
ax.annotate("singular\nstrategy $\\alpha^*$", xy=(x_star, x_star),
            xytext=(x_star + 0.35, x_star - 0.55), fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK))

ax.text(0.35, 1.9, "mutant invades", color="white", fontsize=9,
        weight="bold")
ax.text(1.7, 0.35, "mutant\nexcluded", color=INK, fontsize=9)

ax.set_xlabel("resident virulence $\\alpha$")
ax.set_ylabel("mutant virulence $\\alpha'$")
ax.set_title("Pairwise invasibility plot")
ax.grid(False)

save(fig, "assets/figures/adaptive-dynamics.svg")
