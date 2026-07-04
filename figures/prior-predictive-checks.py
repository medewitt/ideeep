# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Prior on the logit scale pushed forward to the outcome scale.

A vague Normal prior on a logit-scale intercept implies a U-shaped prior on
the probability, piling mass at 0 and 1; a tighter prior implies a plausible
spread. This is the picture a prior predictive check makes visible.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expit
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1834)
N = 400000
edges = np.linspace(0, 1, 61)
centers = 0.5 * (edges[:-1] + edges[1:])


def implied_density(sigma):
    alpha = rng.normal(0.0, sigma, N)      # prior on the logit scale
    p = expit(alpha)                       # implied probability
    h, _ = np.histogram(p, bins=edges, density=True)
    return h


vague = implied_density(10.0)
sensible = implied_density(1.5)

fig, ax = plt.subplots()
ax.axvspan(0.2, 0.6, color=PALETTE[2], alpha=0.15,
           label="plausible prevalence")
ax.plot(centers, vague, color=PALETTE[1], lw=2,
        label=r"vague prior ($\sigma=10$)")
ax.plot(centers, sensible, color=PALETTE[0], lw=2,
        label=r"sensible prior ($\sigma=1.5$)")

ax.set_xlabel(r"implied prevalence $p=\mathrm{logit}^{-1}(\alpha)$")
ax.set_ylabel("prior predictive density")
ax.set_ylim(0, 6)
ax.set_title("A prior on the logit scale, pushed to the outcome scale")
ax.legend(loc="upper center", fontsize=9)

save(fig, "assets/figures/prior-predictive-checks.svg")
