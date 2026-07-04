# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Time slices of a simulated spatiotemporal risk field: a cluster that moves
across the map and grows, the pattern surveillance systems track."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from _style import apply_style, save, PALETTE, INK

apply_style()

rng = np.random.default_rng(1834)

# A single-hue colormap for the risk intensity (on-brand blue).
shade = LinearSegmentedColormap.from_list("shade", ["#ffffff", PALETTE[0]])

# A regular spatial grid on the unit square.
side = 60
g = np.linspace(0, 1, side)
GX, GY = np.meshgrid(g, g)

# A latent cluster whose centre drifts and whose amplitude grows over time.
times = [0, 3, 6, 9]
centers = {t: (0.25 + 0.05 * t, 0.30 + 0.045 * t) for t in times}
amps = {t: 0.6 + 0.35 * t for t in times}
width = 0.12

fig, axes = plt.subplots(1, len(times), figsize=(11.0, 3.2))
vmax = max(amps.values()) + 0.4

for ax, t in zip(axes, times):
    cx, cy = centers[t]
    field = amps[t] * np.exp(-((GX - cx) ** 2 + (GY - cy) ** 2)
                             / (2 * width**2))
    field = field + 0.15 * rng.standard_normal(field.shape)   # observation noise
    ax.imshow(field, origin="lower", extent=(0, 1, 0, 1), cmap=shade,
              vmin=0.0, vmax=vmax, aspect="equal")
    ax.plot(cx, cy, "x", color=PALETTE[1], ms=9, mew=2)
    ax.set_title(f"week {t}", fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.suptitle("A spatiotemporal cluster drifting and growing over time",
             color=INK, fontsize=12)
fig.tight_layout()
save(fig, "assets/figures/spatiotemporal-models.svg")
