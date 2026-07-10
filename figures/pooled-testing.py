# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Estimating per-specimen prevalence from pooled (group) tests."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# --- LEFT: bias of Minimum Infection Rate vs MLE (pool size m = 25) ---
m = 25
p = np.linspace(0.0, 0.10, 200)

# Expected fraction of positive pools, MIR, and MLE recovered from it.
kfrac = 1.0 - (1.0 - p) ** m
mir = kfrac / m
mle = 1.0 - (1.0 - kfrac) ** (1.0 / m)  # recovers p exactly

axL.plot(p, p, color=MUTED, ls="--", lw=1.4, label="true p")
axL.plot(p, mir, color=PALETTE[1], lw=2.0, label="MIR")
axL.plot(p[::12], mle[::12], color=PALETTE[0], ls="none", marker="o",
         ms=4.0, label="MLE")

axL.annotate("MIR underestimates\nas prevalence rises",
             xy=(0.085, mir[np.argmin(np.abs(p - 0.085))]),
             xytext=(0.030, 0.070), fontsize="x-small", color=PALETTE[1],
             arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.8))

axL.set_xlabel("true prevalence per specimen")
axL.set_ylabel("estimated prevalence")
axL.set_xlim(0.0, 0.10)
axL.set_ylim(0.0, 0.10)
axL.set_title("MIR vs MLE bias")
axL.legend(loc="upper left", fontsize="x-small")

# --- RIGHT: MLE point estimate vs Bayesian posterior (one dataset) ---
n = 50    # number of pools
mp = 25   # pool size
k = 8     # positive pools

grid = np.linspace(1e-4, 0.05, 600)
loglik = k * np.log(1.0 - (1.0 - grid) ** mp) \
    + (n - k) * mp * np.log(1.0 - grid)

# Normalized likelihood curve (trapezoid over the grid).
lik = np.exp(loglik - loglik.max())
lik /= np.trapezoid(lik, grid)

# MLE point estimate.
p_hat = 1.0 - (1.0 - k / n) ** (1.0 / mp)

# Bayesian posterior with a Beta(1, 1) (uniform) prior.
prior = np.ones_like(grid)
post = lik * prior
post /= np.trapezoid(post, grid)

# Central 95% credible interval from the posterior CDF over the grid.
cdf = np.cumsum(post) * (grid[1] - grid[0])
cdf /= cdf[-1]
lo = grid[np.searchsorted(cdf, 0.025)]
hi = grid[np.searchsorted(cdf, 0.975)]

axR.fill_between(grid, lik, color=PALETTE[0], alpha=0.20,
                 label="likelihood / MLE")
axR.plot(grid, lik, color=PALETTE[0], lw=1.4)
axR.plot(grid, post, color=PALETTE[3], lw=2.0, label="Bayesian posterior")
axR.fill_between(grid, post, where=(grid >= lo) & (grid <= hi),
                 color=PALETTE[3], alpha=0.18)
axR.axvline(p_hat, color=INK, ls="--", lw=1.2,
            label=f"MLE = {p_hat:.3f}")

axR.set_xlabel("prevalence per specimen p")
axR.set_ylabel("density")
axR.set_xlim(0.0, 0.05)
axR.set_ylim(0.0, None)
axR.set_title("MLE vs posterior")
axR.legend(loc="upper right", fontsize="x-small")

fig.tight_layout()

save(fig, "assets/figures/pooled-testing.svg")
