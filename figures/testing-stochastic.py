# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""How to test code that is supposed to be random. You cannot assert that one
run equals a fixed number -- it won't. Instead you assert a *statistical*
property: run the estimator many times on simulated data with a known truth,
and check that the distribution of estimates is centred on that truth. Any
single run scatters; the average lands on the right answer.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)
true_rate = 2.0
n_rep, n_obs = 4000, 200

ests = np.empty(n_rep)
for i in range(n_rep):
    x = rng.exponential(1 / true_rate, size=n_obs)   # simulate known truth
    ests[i] = 1 / x.mean()                            # estimate the rate

fig, ax = plt.subplots()
ax.hist(ests, bins=50, density=True, color=PALETTE[0], alpha=0.8,
        label="estimates from individual runs")

ax.axvline(true_rate, color="#b0332f", lw=2.4, label=f"true value = {true_rate}")
ax.axvline(ests.mean(), color=PALETTE[2], lw=2.0, ls="--",
           label=f"mean of runs = {ests.mean():.3f}")

# tolerance band the *mean* must fall inside for the test to pass
tol = 0.02 * true_rate
ax.axvspan(true_rate - tol, true_rate + tol, color="#b0332f", alpha=0.12,
           label="±2% test tolerance (on the mean)")

ax.annotate("individual runs scatter widely,\nbut their mean lands on the truth",
            xy=(2.18, 1.7), color="0.35", fontsize=9)

ax.set_xlabel("estimated rate")
ax.set_ylabel("density")
ax.set_xlim(1.4, 2.7)
ax.set_title("Testing stochastic code: assert a property, not a value")
ax.legend(fontsize="small", loc="upper right")

save(fig, "assets/figures/testing-stochastic.svg")
