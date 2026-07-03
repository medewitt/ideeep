# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Metropolis-Hastings sampling a standard normal target."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)


def log_target(x):
    # Standard normal density up to a constant.
    return -0.5 * x * x


n_iter = 5000
burn_in = 500
proposal_sd = 1.0

chain = np.empty(n_iter)
x = 0.0
lp = log_target(x)
for t in range(n_iter):
    x_prop = x + rng.normal(0.0, proposal_sd)
    lp_prop = log_target(x_prop)
    if np.log(rng.random()) < lp_prop - lp:
        x, lp = x_prop, lp_prop
    chain[t] = x

samples = chain[burn_in:]

fig, (ax_trace, ax_hist) = plt.subplots(1, 2, figsize=(10, 4))

ax_trace.plot(np.arange(n_iter), chain, color=PALETTE[0], lw=0.6)
ax_trace.axvline(burn_in, color=PALETTE[1], ls="--", lw=1.2,
                 label=f"burn-in = {burn_in}")
ax_trace.set_xlabel("iteration")
ax_trace.set_ylabel("state")
ax_trace.set_title("Trace of the chain")
ax_trace.legend(loc="upper right", fontsize="small")

ax_hist.hist(samples, bins=50, density=True, color=PALETTE[0],
             alpha=0.6, label="samples")
grid = np.linspace(-4, 4, 400)
pdf = np.exp(-0.5 * grid**2) / np.sqrt(2 * np.pi)
ax_hist.plot(grid, pdf, color=PALETTE[2 % len(PALETTE)], lw=2,
             label="N(0, 1) pdf")
ax_hist.set_xlabel("value")
ax_hist.set_ylabel("density")
ax_hist.set_title("Posterior samples")
ax_hist.legend(loc="upper right", fontsize="small")

fig.suptitle("Metropolis-Hastings sampling of a standard normal")

save(fig, "assets/figures/mcmc.svg")
