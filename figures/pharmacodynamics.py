# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""Sigmoid Emax (Hill) dose-response curves for varying Hill coefficients."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)

Emax = 100.0
EC50 = 10.0

C = np.logspace(-1, 3, 400)  # 0.1 to 1000

fig, ax = plt.subplots()

for i, h in enumerate([1, 2, 4]):
    E = Emax * C**h / (EC50**h + C**h)
    ax.plot(C, E, color=PALETTE[i % len(PALETTE)], lw=2.5, label=f"h = {h}")

ax.axvline(EC50, color="0.5", ls="--", lw=1.2)
ax.axhline(Emax / 2, color="0.5", ls="--", lw=1.2)
ax.annotate("EC50", xy=(EC50, 5), xytext=(EC50 * 1.3, 8), color="0.4")

ax.set_xscale("log")
ax.set_xlabel("concentration C")
ax.set_ylabel("effect E")
ax.set_title("Pharmacodynamics: Hill coefficient sets steepness of potency")
ax.legend()

save(fig, "assets/figures/pharmacodynamics.svg")
