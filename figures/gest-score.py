# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "statsmodels", "matplotlib"]
# ///
"""How g-estimation finds the effect. For a candidate effect psi, form the
treatment-free outcome H(psi) = Y - psi*A and test whether it still predicts
treatment given the confounder, by the coefficient on H in a logistic regression of
A on L and H. The true psi is the value that makes that coefficient zero - the point
where removing the effect leaves treatment unrelated to the treatment-free outcome.
Here it crosses at about -2."""
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(2)
n = 4000
L = rng.normal(0, 1, n)
A = rng.binomial(1, 1 / (1 + np.exp(-0.8 * L)))
Y = -2.0 * A + 1.5 * L + rng.normal(0, 1, n)


def score(psi):
    H = Y - psi * A
    return sm.Logit(A, sm.add_constant(np.c_[L, H])).fit(disp=0).params[-1]


psis = np.linspace(-3.5, -0.5, 40)
sc = np.array([score(p) for p in psis])
# solve for the crossing by bisection
lo, hi = -3.5, -0.5
for _ in range(40):
    mid = (lo + hi) / 2
    if score(mid) > 0:
        lo = mid
    else:
        hi = mid
psi_hat = (lo + hi) / 2

fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.axhline(0, color=MUTED, lw=1.0, ls="--")
ax.plot(psis, sc, color=PALETTE[0], lw=2.4)
ax.axvline(psi_hat, color=PALETTE[1], lw=1.8)
ax.scatter([psi_hat], [0], s=80, color=PALETTE[1], zorder=5)
ax.annotate(f"$\\hat\\psi$ = {psi_hat:.2f}\n(coef on H = 0)", xy=(psi_hat, 0),
            xytext=(psi_hat + 0.35, sc.max() * 0.55), fontsize=8.6, color=INK,
            arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.9))
ax.set_xlabel("candidate effect  $\\psi$")
ax.set_ylabel("association of $A$ with $H(\\psi)$ given $L$\n(coefficient on $H$)")
ax.set_title("G-estimation: solve for zero association", fontsize=9.8)
fig.tight_layout()
save(fig, "assets/figures/gest-score.svg")
