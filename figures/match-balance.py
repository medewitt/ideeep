# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "statsmodels", "matplotlib"]
# ///
"""Matching restores covariate balance. Standardized mean differences for three
confounders are large before matching (the treated and control groups differ), and
collapse toward zero after propensity-score matching and after coarsened exact
matching. The dashed lines at plus and minus 0.1 are the usual rule-of-thumb for
acceptable balance."""
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from collections import defaultdict
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(4)
n = 2000
L1, L2, L3 = rng.normal(0, 1, n), rng.normal(0, 1, n), rng.normal(0, 1, n)
A = rng.binomial(1, 1 / (1 + np.exp(-(0.7 * L1 + 0.6 * L2 - 0.4 * L3))))
X = np.column_stack([L1, L2, L3])
tr, co = np.where(A == 1)[0], np.where(A == 0)[0]


def smd(xt, xc, wc=None):
    return np.array([((xt[:, j].mean()
                       - (xc[:, j].mean() if wc is None else np.average(xc[:, j], weights=wc)))
                      / np.sqrt((xt[:, j].var() + xc[:, j].var()) / 2)) for j in range(xt.shape[1])])


before = smd(X[tr], X[co])
e = sm.Logit(A, sm.add_constant(X)).fit(disp=0).predict()
lps = np.log(e / (1 - e))
mc = np.array([co[np.argmin(np.abs(lps[co] - lps[i]))] for i in tr])
ps = smd(X[tr], X[mc])
bins = [np.quantile(X[:, j], [.25, .5, .75]) for j in range(3)]
key = lambda i: tuple(int(np.digitize(X[i, j], bins[j])) for j in range(3))
strata = defaultdict(lambda: ([], []))
for i in range(n):
    strata[key(i)][A[i]].append(i)
kt, kc, wc = [], [], []
for cc, ct in strata.values():
    if cc and ct:
        kt += ct; kc += cc; wc += [len(ct) / len(cc)] * len(cc)
cem = smd(X[np.array(kt)], X[np.array(kc)], wc=np.array(wc))

fig, ax = plt.subplots(figsize=(6.4, 3.8))
labels = ["$L_1$", "$L_2$", "$L_3$"]
yy = np.arange(3)[::-1]
ax.axvline(0, color=INK, lw=0.8)
for x0 in (-0.1, 0.1):
    ax.axvline(x0, color=MUTED, lw=1.0, ls="--")
ax.scatter(before, yy, s=90, color=MUTED, label="before matching", zorder=3)
ax.scatter(ps, yy, s=90, color=PALETTE[0], marker="s", label="propensity matching",
           zorder=4)
ax.scatter(cem, yy, s=90, color=PALETTE[1], marker="D", label="coarsened exact",
           zorder=4)
ax.set_yticks(yy)
ax.set_yticklabels(labels, fontsize=10)
ax.set_xlabel("standardized mean difference (treated − control)")
ax.set_title("Balance before and after matching", fontsize=9.8)
ax.set_xlim(-0.2, 0.75)
ax.legend(fontsize=8.2, loc="lower right")
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/match-balance.svg")
