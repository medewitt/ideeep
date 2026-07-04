# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Sample paths of standard Brownian motion (the scaling limit of a random walk)
with the +/- sqrt(t) standard-deviation envelope overlaid."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()
rng = np.random.default_rng(7)

T = 1.0
n = 500                      # time steps
dt = T / n
t = np.linspace(0, T, n + 1)

fig, ax = plt.subplots(figsize=(6.6, 4.0))

n_paths = 6
for i in range(n_paths):
    incr = rng.normal(0.0, np.sqrt(dt), size=n)   # W(t+dt)-W(t) ~ N(0, dt)
    w = np.concatenate([[0.0], np.cumsum(incr)])
    ax.plot(t, w, color=PALETTE[i % len(PALETTE)], lw=1.0, alpha=0.9)

# +/- sqrt(t) envelope: SD of W(t) grows like sqrt(t)
ax.plot(t, np.sqrt(t), color=MUTED, lw=1.6, ls="--", label=r"$\pm\sqrt{t}$")
ax.plot(t, -np.sqrt(t), color=MUTED, lw=1.6, ls="--")
ax.axhline(0.0, color=MUTED, lw=0.8, alpha=0.5)

ax.set_xlabel("Time $t$")
ax.set_ylabel("$W(t)$")
ax.set_title("Brownian motion: sample paths and the $\\pm\\sqrt{t}$ envelope")
ax.legend(loc="upper left")

save(fig, "assets/figures/random-walk-brownian-motion.svg")
