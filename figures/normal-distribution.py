# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Standard normal pdf with the 68-95-99.7 rule shaded."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)

x = np.linspace(-4, 4, 800)
y = norm.pdf(x)

fig, ax = plt.subplots()

base = PALETTE[0]
bands = [
    (3, 0.20, "99.7%"),
    (2, 0.35, "95%"),
    (1, 0.55, "68%"),
]

for k, alpha, label in bands:
    mask = np.abs(x) <= k
    ax.fill_between(x[mask], y[mask], color=base, alpha=alpha)

ax.plot(x, y, color="0.2", lw=1.8)

# Percentage labels for each band, placed at increasing heights.
label_y = [0.05, 0.12, 0.20]
for (k, _, label), ly in zip(reversed(bands), label_y):
    band_label = label + r" ($\pm" + str(k) + r"\sigma$)"
    ax.annotate(band_label,
                xy=(0, ly), ha="center", va="center", fontsize="small")

ax.set_xlim(-4, 4)
ax.set_ylim(0, 0.45)
ax.set_xlabel(r"z (standard deviations from mean)")
ax.set_ylabel("density")
ax.set_title("Standard normal: the 68-95-99.7 rule")

save(fig, "assets/figures/normal-distribution.svg")
