# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Gaussian heat-kernel spreading of a point release, with sqrt(t) growth of the spread."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()

rng = np.random.default_rng(0)

D = 1.0
x = np.linspace(-12, 12, 601)


def kernel(x, t):
    return np.exp(-(x**2) / (4 * D * t)) / np.sqrt(4 * np.pi * D * t)


times = [0.5, 1.0, 2.0, 4.0, 8.0]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

for i, t in enumerate(times):
    ax1.plot(x, kernel(x, t), color=PALETTE[i % len(PALETTE)], label=f"t = {t:g}")

ax1.set_xlabel("Position x")
ax1.set_ylabel("u(x, t)")
ax1.set_title("Heat kernel spreading from a point release")
ax1.legend(title="Time")

# sqrt(t) growth of the characteristic spread sigma = sqrt(2 D t) in 1D
t_grid = np.linspace(0.01, 8, 400)
sigma = np.sqrt(2 * D * t_grid)
ax2.plot(t_grid, sigma, color=PALETTE[0], label=r"$\sigma=\sqrt{2Dt}$")
ax2.scatter(times, np.sqrt(2 * D * np.array(times)), color=PALETTE[1], zorder=3)
ax2.set_xlabel("Time t")
ax2.set_ylabel("Spread  σ")
ax2.set_title("Spread grows like √t")
ax2.annotate("distance ∝ √t\n(diffusion is slow)",
             xy=(5.5, np.sqrt(2 * D * 5.5)), xytext=(0.5, 4.6),
             color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
ax2.legend()

fig.tight_layout()
save(fig, "assets/figures/spatial-diffusion.svg")
