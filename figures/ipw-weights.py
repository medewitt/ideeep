# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "statsmodels", "matplotlib"]
# ///
"""Why weights are stabilized. Unstabilized inverse-probability weights (1/e for the
treated, 1/(1-e) for controls) have a heavy right tail: units with a propensity near
0 or 1 get enormous weight and dominate the estimate, inflating its variance.
Stabilized weights multiply by the marginal treatment probability, pulling the whole
distribution toward 1 while preserving the same balance."""
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

w = A / ehat + (1 - A) / (1 - ehat)                      # unstabilized
pA = A.mean()
sw = A * pA / ehat + (1 - A) * (1 - pA) / (1 - ehat)     # stabilized

fig, ax = plt.subplots(figsize=(6.4, 3.9))
bins = np.linspace(0, w.max(), 60)
ax.hist(w, bins=bins, color=PALETTE[1], alpha=0.5, edgecolor="white",
        linewidth=0.3, label=f"unstabilized (max {w.max():.1f})")
ax.hist(sw, bins=bins, color=PALETTE[0], alpha=0.6, edgecolor="white",
        linewidth=0.3, label=f"stabilized (max {sw.max():.1f})")
ax.axvline(1.0, color=INK, lw=1.0, ls=":")
ax.annotate("stabilized weights\ncluster near 1", xy=(1.0, n * 0.06),
            xytext=(3.0, n * 0.09), fontsize=8.4, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
ax.set_xlabel("inverse-probability weight")
ax.set_ylabel("count")
ax.set_title("Stabilizing tames the weight tail", fontsize=9.8)
ax.set_xlim(0, 8)
ax.legend(fontsize=8.4, loc="upper right")
fig.tight_layout()
save(fig, "assets/figures/ipw-weights.svg")
