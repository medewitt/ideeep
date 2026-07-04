# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Matern correlation vs distance for nu = 1/2, 3/2, 5/2, and infinity (RBF)."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import kv, gamma
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(0)  # unused for the curves; seeded for reproducibility


def matern(r, nu, rho=1.0):
    """Matern correlation at separation r with smoothness nu and lengthscale rho."""
    r = np.asarray(r, dtype=float)
    out = np.ones_like(r)
    nz = r > 0
    s = np.sqrt(2.0 * nu) * r[nz] / rho
    out[nz] = (2.0 ** (1.0 - nu) / gamma(nu)) * s ** nu * kv(nu, s)
    return out


d = np.linspace(0, 4, 400)
rho = 1.0

fig, ax = plt.subplots(figsize=(6.2, 3.8))
ax.plot(d, matern(d, 0.5, rho), color=PALETTE[0], label=r"$\nu = 1/2$ (exponential)")
ax.plot(d, matern(d, 1.5, rho), color=PALETTE[1], label=r"$\nu = 3/2$")
ax.plot(d, matern(d, 2.5, rho), color=PALETTE[2], label=r"$\nu = 5/2$")
ax.plot(d, np.exp(-(d ** 2) / (2.0 * rho ** 2)), color=PALETTE[3],
        label=r"$\nu \to \infty$ (RBF)")

ax.set_xlabel("Distance $r$")
ax.set_ylabel("Correlation $k(r)$")
ax.set_title(r"Matern correlation ($\rho = 1$)")
ax.set_ylim(0, 1.02)
ax.legend(title="Smoothness")

save(fig, "assets/figures/covariance-functions.svg")
