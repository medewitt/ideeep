# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Pairwise invasibility plots contrasting a CSS with an evolutionary
branching point, using the Gaussian competition model.

Invasion fitness of a rare mutant y in a resident x at carrying capacity is
    s_x(y) = 1 - a(x, y) K(x) / K(y),
with resource kernel K(z) = exp(-z^2 / (2 sigma_k^2)) and competition kernel
a(x, y) = exp(-(x - y)^2 / (2 sigma_a^2)). The singular strategy sits at 0.
It is uninvadable (a CSS) when sigma_a > sigma_k and an evolutionary
branching point when sigma_a < sigma_k."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from _style import apply_style, save, PALETTE, INK

apply_style()


def invasion_sign(sigma_a, sigma_k, grid):
    """1 where a mutant y invades resident x, else 0, over the trait plane."""
    X, Y = np.meshgrid(grid, grid)     # X: resident, Y: mutant
    K = lambda z: np.exp(-z**2 / (2 * sigma_k**2))
    a = np.exp(-(X - Y)**2 / (2 * sigma_a**2))
    s = 1.0 - a * K(X) / K(Y)
    return (s > 0).astype(float)


lo, hi = -2.5, 2.5
grid = np.linspace(lo, hi, 400)
cmap = ListedColormap(["#eef2f5", PALETTE[0]])

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.9))
panels = [
    ("CSS: $\\sigma_a > \\sigma_k$", 1.0, 0.6),
    ("Branching point: $\\sigma_a < \\sigma_k$", 0.6, 1.0),
]

for ax, (title, sigma_a, sigma_k) in zip(axes, panels):
    invades = invasion_sign(sigma_a, sigma_k, grid)
    ax.imshow(invades, origin="lower", extent=[lo, hi, lo, hi], cmap=cmap,
              vmin=0, vmax=1, aspect="auto", interpolation="nearest")
    ax.plot(grid, grid, color=INK, lw=1.0)      # neutral diagonal y = x
    ax.axvline(0.0, color=PALETTE[1], lw=1.2, ls="--")
    ax.plot(0.0, 0.0, "o", color=PALETTE[1], ms=7, zorder=5)
    ax.set_xlabel("resident trait $x$")
    ax.set_title(title, fontsize=10)
    ax.grid(False)

axes[0].set_ylabel("mutant trait $y$")
# The vertical strip through x* is outside the invasion region for the CSS
# and inside it (both sides) at the branching point.
axes[0].text(-2.1, 1.9, "invades", color="white", fontsize=8, weight="bold")
axes[1].text(-0.9, 1.9, "invades\nboth sides", color="white", fontsize=8,
             weight="bold")

fig.suptitle("Reading stability off the pairwise invasibility plot",
             fontsize=11)
save(fig, "assets/figures/adaptive-dynamics-branching.svg")
