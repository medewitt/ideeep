# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "statsmodels", "matplotlib"]
# ///
"""Propensity-score overlap. The estimated propensity — the probability of
treatment given the confounder — is plotted separately for the treated and control
groups. The distributions differ (confounding: the treated are systematically more
likely to be treated) but overlap across the whole range, so every treated unit has
comparable controls and vice versa. That overlap is the positivity assumption every
propensity method needs."""
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(2)
n = 4000
L = rng.normal(0, 1, n)
A = rng.binomial(1, 1 / (1 + np.exp(-0.8 * L)))
ehat = sm.Logit(A, sm.add_constant(L)).fit(disp=0).predict()

fig, ax = plt.subplots(figsize=(6.4, 3.9))
bins = np.linspace(0, 1, 34)
ax.hist(ehat[A == 1], bins=bins, color=PALETTE[1], alpha=0.55, density=True,
        edgecolor="white", linewidth=0.3, label="treated (A=1)")
ax.hist(ehat[A == 0], bins=bins, color=PALETTE[0], alpha=0.55, density=True,
        edgecolor="white", linewidth=0.3, label="control (A=0)")
ax.set_xlabel("estimated propensity  $\\hat e(L) = \\hat P(A=1 \\mid L)$")
ax.set_ylabel("density")
ax.set_title("Overlap of the propensity score across groups", fontsize=9.8)
ax.annotate("overlapping support\n= positivity holds", xy=(0.5, 1.2),
            xytext=(0.62, 2.2), fontsize=8.4, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
ax.legend(fontsize=8.6, loc="upper left")
fig.tight_layout()
save(fig, "assets/figures/ps-overlap.svg")
