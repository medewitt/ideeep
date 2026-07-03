# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""Logistic regression: simulated binary data with the true fitted sigmoid."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)

b0, b1 = 0.0, 1.3
n = 200
x = rng.uniform(-4, 4, size=n)
p = 1.0 / (1.0 + np.exp(-(b0 + b1 * x)))
y = rng.binomial(1, p)

# vertical jitter so overlapping 0/1 points are visible
jitter = rng.uniform(-0.03, 0.03, size=n)

xx = np.linspace(-4, 4, 400)
pp = 1.0 / (1.0 + np.exp(-(b0 + b1 * xx)))

fig, ax = plt.subplots()

mask1 = y == 1
mask0 = y == 0
ax.scatter(x[mask0], y[mask0] + jitter[mask0], color=PALETTE[0],
           alpha=0.6, s=25, label="y = 0")
ax.scatter(x[mask1], y[mask1] + jitter[mask1], color=PALETTE[1],
           alpha=0.6, s=25, label="y = 1")

ax.plot(xx, pp, color=PALETTE[2], lw=2.5, label="true P(y=1)")

ax.set_xlabel("x")
ax.set_ylabel("P(y = 1)")
ax.set_title("Logistic regression: the fitted sigmoid")
ax.legend()

save(fig, "assets/figures/logistic-regression.svg")
