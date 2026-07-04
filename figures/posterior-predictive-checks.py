# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Posterior predictive check for an overdispersed count model.

Overdispersed counts are fit with a Poisson-gamma model. Replicate datasets
drawn from the posterior predictive are too tight: the observed variance sits
far in the tail of the replicate reference distribution, so the posterior
predictive p-value is small and the Poisson assumption is rejected.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()

rng = np.random.default_rng(1834)

# Observed counts are overdispersed (negative binomial), so Poisson misfits.
y = rng.negative_binomial(2, 2 / 5, size=40)
n = len(y)
s = y.sum()

# Conjugate Poisson-gamma update: Gamma(1,1) prior -> Gamma(1+s, 1+n).
a_post, b_post = 1.0 + s, 1.0 + n
M = 4000
lam = rng.gamma(a_post, 1.0 / b_post, M)
y_rep = rng.poisson(lam[:, None], size=(M, n))

var_obs = y.var()
var_rep = y_rep.var(axis=1)
p_value = np.mean(var_rep >= var_obs)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.6))

# Left: observed count distribution vs a band of replicate distributions.
bins = np.arange(0, y.max() + 2) - 0.5
for i in range(40):
    h, _ = np.histogram(y_rep[i], bins=bins, density=True)
    ax1.step(0.5 * (bins[:-1] + bins[1:]), h, where="mid",
             color=MUTED, alpha=0.15, lw=1)
h_obs, _ = np.histogram(y, bins=bins, density=True)
ax1.step(0.5 * (bins[:-1] + bins[1:]), h_obs, where="mid",
         color=PALETTE[1], lw=2.4, label="observed")
ax1.plot([], [], color=MUTED, lw=1, label="replicates")
ax1.set_xlabel("count")
ax1.set_ylabel("frequency")
ax1.set_title("Replicated vs observed data")
ax1.legend(loc="upper right", fontsize=9)

# Right: reference distribution of the test statistic with observed overlaid.
ax2.hist(var_rep, bins=30, color=PALETTE[0], alpha=0.8, density=True)
ax2.axvline(var_obs, color=PALETTE[1], lw=2.4,
            label=f"observed (p={p_value:.3f})")
ax2.set_xlabel(r"replicate variance $T(\tilde y)$")
ax2.set_ylabel("density")
ax2.set_title("Posterior predictive p-value")
ax2.legend(loc="upper right", fontsize=9)

fig.tight_layout()
save(fig, "assets/figures/posterior-predictive-checks.svg")
