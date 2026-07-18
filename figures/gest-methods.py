# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "statsmodels", "matplotlib"]
# ///
"""The three g-methods agree; the naive estimate does not. On the running
confounded example (true effect -2), a naive treated-minus-control difference is
badly biased, but all three of Robins' g-methods - the g-formula (standardization),
inverse-probability weighting of a marginal structural model, and g-estimation of a
structural nested model - recover the truth. They differ in what they model
(outcome, treatment, or both) but target the same causal effect."""
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED


def all_estimates(rng):
    n = 4000
    L = rng.normal(0, 1, n)
    A = rng.binomial(1, 1 / (1 + np.exp(-0.8 * L)))
    Y = -2.0 * A + 1.5 * L + rng.normal(0, 1, n)
    naive = Y[A == 1].mean() - Y[A == 0].mean()
    # g-formula: standardization via an outcome model
    om = sm.OLS(Y, sm.add_constant(np.c_[A, L])).fit()
    X1 = np.c_[np.ones(n), np.ones(n), L]; X0 = np.c_[np.ones(n), np.zeros(n), L]
    gform = (om.predict(X1) - om.predict(X0)).mean()
    # IPW of an MSM
    e = sm.Logit(A, sm.add_constant(L)).fit(disp=0).predict()
    w = A / e + (1 - A) / (1 - e)
    ipw = (np.sum(w * A * Y) / np.sum(w * A)
           - np.sum(w * (1 - A) * Y) / np.sum(w * (1 - A)))
    # g-estimation of a structural nested model
    lo, hi = -4.0, 0.0
    for _ in range(36):
        mid = (lo + hi) / 2
        H = Y - mid * A
        c = sm.Logit(A, sm.add_constant(np.c_[L, H])).fit(disp=0).params[-1]
        if c > 0:
            lo = mid
        else:
            hi = mid
    return naive, gform, ipw, (lo + hi) / 2


apply_style()
pt = all_estimates(np.random.default_rng(2))
boot = np.array([all_estimates(np.random.default_rng(300 + k)) for k in range(120)])
lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)

labels = ["naive\n(confounded)", "g-formula\n(outcome model)",
          "IPW of MSM\n(treatment model)", "g-estimation\n(SNM)"]
cols = [MUTED, PALETTE[0], PALETTE[3], PALETTE[1]]
fig, ax = plt.subplots(figsize=(6.4, 3.7))
ax.axvline(-2.0, color=INK, lw=1.2, ls=":")
ax.text(-2.0, 4.5, "true effect = −2", ha="center", fontsize=8.2, color=INK)
for i, (est, c) in enumerate(zip(pt, cols)):
    yy = len(pt) - 1 - i
    ax.plot([lo[i], hi[i]], [yy, yy], color=c, lw=2.4)
    ax.plot([est], [yy], "o", color=c, ms=9)
    ax.annotate(f"{est:+.2f}", (est, yy + 0.16), fontsize=8.4, color=INK, ha="center")
ax.set_yticks(range(len(pt)))
ax.set_yticklabels(labels[::-1], fontsize=8.4)
ax.set_xlabel("estimated causal effect")
ax.set_title("Robins' g-methods agree; the naive estimate is biased", fontsize=9.3)
ax.set_ylim(-0.6, len(pt) - 0.1)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/gest-methods.svg")
