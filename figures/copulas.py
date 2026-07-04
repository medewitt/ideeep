# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Samples from Gaussian, Clayton, and Gumbel copulas with identical standard-normal
marginals, showing how the dependence structure (and joint-tail clustering) differs
even when every margin is the same."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(20260704)
n = 2000
tau = 0.5  # common Kendall's tau, so all three couplings are "equally strong"


def gaussian_copula(rng, n, tau):
    """Uniforms from a Gaussian copula with Kendall's tau via rho = sin(pi*tau/2)."""
    rho = np.sin(np.pi * tau / 2)
    cov = [[1.0, rho], [rho, 1.0]]
    z = rng.multivariate_normal([0, 0], cov, size=n)
    return norm.cdf(z)


def positive_stable(rng, alpha, n):
    """Positive stable frailty (Chambers-Mallows-Stuck) with Laplace transform exp(-t^alpha)."""
    theta = rng.uniform(0, np.pi, n)
    w = rng.exponential(1.0, n)
    return (np.sin(alpha * theta) / np.cos(theta) ** (1 / alpha)
            * (np.cos((1 - alpha) * theta) / w) ** ((1 - alpha) / alpha))


def archimedean_copula(rng, n, frailty):
    """Marshall-Olkin frailty method: u_i = psi(-log V_i / M)."""
    m = frailty
    v = rng.uniform(size=(n, 2))
    return m, v


def clayton_copula(rng, n, tau):
    theta = 2 * tau / (1 - tau)  # tau = theta / (theta + 2)
    m = rng.gamma(shape=1 / theta, scale=1.0, size=n)
    v = rng.uniform(size=(n, 2))
    return (1 - np.log(v) / m[:, None]) ** (-1 / theta)


def gumbel_copula(rng, n, tau):
    theta = 1 / (1 - tau)  # tau = 1 - 1/theta
    m = positive_stable(rng, 1 / theta, n)
    v = rng.uniform(size=(n, 2))
    return np.exp(-(-np.log(v) / m[:, None]) ** (1 / theta))


samples = {
    "Gaussian\n(no tail dependence)": gaussian_copula(rng, n, tau),
    "Clayton\n(lower-tail dependence)": clayton_copula(rng, n, tau),
    "Gumbel\n(upper-tail dependence)": gumbel_copula(rng, n, tau),
}

fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.7), sharex=True, sharey=True)
for ax, (name, u), color in zip(axes, samples.items(), PALETTE):
    z = norm.ppf(np.clip(u, 1e-6, 1 - 1e-6))  # standard-normal marginals for all three
    ax.scatter(z[:, 0], z[:, 1], s=5, alpha=0.35, color=color, edgecolors="none")
    ax.set_title(name, fontsize=10)
    ax.set_xlabel("$x$")
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect("equal")
axes[0].set_ylabel("$y$")
fig.suptitle(r"Three copulas, same normal margins, same Kendall's $\tau = 0.5$")

save(fig, "assets/figures/copulas.svg")
