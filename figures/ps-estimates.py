# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "statsmodels", "matplotlib"]
# ///
"""Every principled propensity method recovers the true effect; the naive
comparison does not. The true average treatment effect is -2. A crude
treated-minus-control difference is badly confounded (about -0.9), but propensity
matching, stratification, and inverse-probability weighting all land near -2. Bars
are 95% bootstrap intervals."""
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()


def estimates(rng):
    n = 4000
    L = rng.normal(0, 1, n)
    A = rng.binomial(1, 1 / (1 + np.exp(-0.8 * L)))
    Y = -2.0 * A + 1.5 * L + rng.normal(0, 1, n)
    ehat = sm.Logit(A, sm.add_constant(L)).fit(disp=0).predict()
    naive = Y[A == 1].mean() - Y[A == 0].mean()
    w = A / ehat + (1 - A) / (1 - ehat)
    ipw = (np.sum(w * A * Y) / np.sum(w * A)
           - np.sum(w * (1 - A) * Y) / np.sum(w * (1 - A)))
    q = np.quantile(ehat, np.linspace(0, 1, 6)); q[0] -= 1e-9
    st = np.digitize(ehat, q[1:-1]); d, wt = [], []
    for s in np.unique(st):
        m = st == s
        if A[m].sum() and (1 - A[m]).sum():
            d.append(Y[m][A[m] == 1].mean() - Y[m][A[m] == 0].mean()); wt.append(m.sum())
    strat = np.average(d, weights=wt)
    co = np.where(A == 0)[0]; ec = ehat[co]
    match = np.mean([Y[i] - Y[co[np.argmin(np.abs(ec - ehat[i]))]]
                     for i in np.where(A == 1)[0]])
    return naive, match, strat, ipw


pt = estimates(np.random.default_rng(2))
boot = np.array([estimates(np.random.default_rng(100 + k)) for k in range(200)])
lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)

labels = ["naive\n(confounded)", "PS matching", "PS stratification",
          "IPW (weighting)"]
cols = [MUTED, PALETTE[0], PALETTE[2], PALETTE[3]]
fig, ax = plt.subplots(figsize=(6.4, 3.6))
ax.axvline(-2.0, color=INK, lw=1.2, ls=":")
ax.text(-2.0, 4.5, "true ATE = −2", ha="center", fontsize=8.2, color=INK)
for i, (est, c) in enumerate(zip(pt, cols)):
    yy = len(pt) - 1 - i
    ax.plot([lo[i], hi[i]], [yy, yy], color=c, lw=2.4)
    ax.plot([est], [yy], "o", color=c, ms=9)
    ax.annotate(f"{est:+.2f}", (est, yy + 0.16), fontsize=8.4, color=INK, ha="center")
ax.set_yticks(range(len(pt)))
ax.set_yticklabels(labels[::-1], fontsize=8.6)
ax.set_xlabel("estimated average treatment effect")
ax.set_title("Naive is biased; propensity methods recover the truth", fontsize=9.4)
ax.set_ylim(-0.6, len(pt) - 0.1)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/ps-estimates.svg")
