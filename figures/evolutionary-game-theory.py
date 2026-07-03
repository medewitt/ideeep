# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Replicator dynamics for the Hawk-Dove game converging to the mixed ESS."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

V, C = 2.0, 3.0
ess = V / C  # mixed ESS fraction of Hawks = 2/3


def replicator(x):
    f_H = x * (V - C) / 2 + (1 - x) * V
    f_D = x * 0 + (1 - x) * V / 2
    mean = x * f_H + (1 - x) * f_D
    return x * (f_H - mean)


# Integrate with simple RK4
t_max = 20.0
dt = 0.01
n = int(t_max / dt)
t = np.linspace(0, t_max, n + 1)

x0_list = [0.05, 0.3, 0.9, 0.99]

fig, ax = plt.subplots(figsize=(10, 6))

for i, x0 in enumerate(x0_list):
    x = np.empty(n + 1)
    x[0] = x0
    for j in range(n):
        xc = x[j]
        k1 = replicator(xc)
        k2 = replicator(xc + 0.5 * dt * k1)
        k3 = replicator(xc + 0.5 * dt * k2)
        k4 = replicator(xc + dt * k3)
        x[j + 1] = xc + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    ax.plot(t, x, color=PALETTE[i % len(PALETTE)], label=f"x0 = {x0}")

ax.axhline(ess, linestyle="--", color="0.4",
           label=f"ESS = V/C = {ess:.3f}")

ax.set_xlabel("Time t")
ax.set_ylabel("Fraction of Hawks x")
ax.set_ylim(0, 1)
ax.set_title("Hawk-Dove Replicator Dynamics (V=2, C=3)")
ax.legend()

save(fig, "assets/figures/evolutionary-game-theory.svg")
