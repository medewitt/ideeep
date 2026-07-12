# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "statsmodels", "pandas", "matplotlib"]
# ///
"""What the proportional-odds Python block produces. The same seeded ordinal
data are fit with statsmodels' OrderedModel. Left: the fitted cumulative
probabilities P(Y >= j | x) for control (solid) vs treated (dashed) -- the
treatment shifts every curve to the left by the same amount, the single
odds ratio printed above (about 3.79). Right: the model reproduces the data,
observed category proportions (bars) vs model-predicted (dots), split by arm."""
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.miscmodels.ordinal_model import OrderedModel
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# ---- identical DGP to the page's Python block (rng seed 0) ----
rng = np.random.default_rng(0)
n = 500
x = rng.normal(size=n)
treat = rng.integers(0, 2, size=n)
latent = 1.0 * x + 1.3 * treat + rng.logistic(size=n)
cuts = np.quantile(latent, [0.25, 0.50, 0.75])
y = np.digitize(latent, cuts)                       # ordered outcome 0,1,2,3

X = np.column_stack([x, treat])
res = OrderedModel(y, X, distr="logit").fit(method="bfgs", disp=False)
b_t = float(res.params[1])
OR = np.exp(b_t)

# cumulative fitted probs P(Y >= j) from category probs P(Y = k)
def cum_ge(exog):
    P = np.atleast_2d(res.predict(exog))            # (m, 4): P(Y = 0..3)
    return np.cumsum(P[:, ::-1], axis=1)[:, ::-1]   # col k = P(Y >= k)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.9))

# ---- left: fitted cumulative-probability curves, control vs treated ----
xg = np.linspace(x.min(), x.max(), 200)
ge0 = cum_ge(np.column_stack([xg, np.zeros_like(xg)]))
ge1 = cum_ge(np.column_stack([xg, np.ones_like(xg)]))
for j, col in zip((1, 2, 3), PALETTE):
    axL.plot(xg, ge0[:, j], color=col, lw=2.0, label=fr"$Y \geq {j}$")
    axL.plot(xg, ge1[:, j], color=col, lw=2.0, ls="--")
axL.plot([], [], color=INK, lw=2.0, label="control (solid)")
axL.plot([], [], color=INK, lw=2.0, ls="--", label="treated (dashed)")
axL.set_ylim(0, 1)
axL.set_xlabel("x")
axL.set_ylabel(r"$P(Y \geq j \mid x)$")
axL.set_title("Fitted cumulative probabilities", fontsize=10)
axL.text(0.03, 0.06, fr"treatment OR $= e^{{{b_t:.2f}}} \approx {OR:.2f}$",
         transform=axL.transAxes, fontsize=8.5, color=INK)
axL.legend(fontsize=7.4, loc="upper right", ncol=1)

# ---- right: observed vs model-predicted category proportions, by arm ----
cats = np.arange(4)
w = 0.38
for t, off, col, name in [(0, -w / 2, PALETTE[0], "control"),
                          (1, +w / 2, PALETTE[1], "treated")]:
    mask = treat == t
    obs = np.array([(y[mask] == k).mean() for k in cats])
    pred = np.atleast_2d(res.predict(X[mask])).mean(axis=0)
    axR.bar(cats + off, obs, width=w, color=col, alpha=0.85, label=f"{name} (observed)")
    axR.scatter(cats + off, pred, s=34, color=INK, zorder=5,
                edgecolor="white", linewidth=0.7,
                label="model-predicted" if t == 0 else None)
axR.set_xticks(cats)
axR.set_xlabel("ordinal category")
axR.set_ylabel("probability")
axR.set_title("Observed vs fitted, by treatment arm", fontsize=10)
axR.legend(fontsize=7.4, loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/proportional-odds-fit.svg")
