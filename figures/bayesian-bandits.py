# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Bayesian bandit for adaptive survey sampling over four sites.

Left: the Beta posteriors on each site's positivity after 40 rounds of
Thompson-sampled allocation. Right: the cumulative share of the testing
budget each site receives over time -- the sampler concentrates effort on
the high-positivity site (C) while still probing the others.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(20260711)

sites = ["A", "B", "C", "D"]
p_true = np.array([0.06, 0.10, 0.22, 0.09])   # unknown to the sampler
n_sites = len(sites)

rounds = 40
batch = 25                    # tests placed each round
a = np.ones(n_sites)          # Beta(1,1) priors
b = np.ones(n_sites)

alloc_hist = np.zeros((rounds, n_sites))
for t in range(rounds):
    counts = np.zeros(n_sites, dtype=int)
    # Thompson sampling: each test goes to the site with the largest draw
    draws = rng.beta(a[None, :], b[None, :], size=(batch, n_sites))
    picks = draws.argmax(axis=1)
    for k in range(n_sites):
        n_k = int((picks == k).sum())
        counts[k] = n_k
        if n_k:
            y_k = rng.binomial(n_k, p_true[k])   # positives observed
            a[k] += y_k
            b[k] += n_k - y_k
    alloc_hist[t] = counts

cum = alloc_hist.cumsum(axis=0)
cum_frac = cum / cum.sum(axis=1, keepdims=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.8))

# --- left: final posteriors -----------------------------------------------
grid = np.linspace(0, 0.4, 500)
for k in range(n_sites):
    dens = stats.beta.pdf(grid, a[k], b[k])
    ax1.plot(grid, dens, color=PALETTE[k], lw=2, label=f"site {sites[k]}")
    ax1.axvline(p_true[k], color=PALETTE[k], lw=1, ls=":")
ax1.set_xlim(0, 0.4)
ax1.set_xlabel("positivity $\\theta$")
ax1.set_ylabel("posterior density")
ax1.set_title("Posterior on each site's positivity")
ax1.legend(loc="upper right", fontsize=9)
ax1.annotate("dotted = true rate", xy=(0.22, 1), xytext=(0.255, 6),
             fontsize=8, color=MUTED)

# --- right: allocation share over time ------------------------------------
for k in range(n_sites):
    ax2.plot(np.arange(1, rounds + 1), cum_frac[:, k],
             color=PALETTE[k], lw=2, label=f"site {sites[k]}")
ax2.set_xlim(1, rounds)
ax2.set_ylim(0, 1)
ax2.set_xlabel("round")
ax2.set_ylabel("cumulative share of tests")
ax2.set_title("Budget shifts toward the positive site")
ax2.legend(loc="center right", fontsize=9)

fig.tight_layout()
save(fig, "assets/figures/bayesian-bandits.svg")
