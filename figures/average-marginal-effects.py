# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Why a logistic coefficient is not an effect. Left: the same slope beta on the
link scale produces a steep change in probability near p = 0.5 (tangent) but
almost none near p = 0.02, because dp/dx = beta*p(1-p). Right: the per-individual
marginal effect of age varies across the sample; the marginal effect at the
means (MEM) evaluates one synthetic average person while the average marginal
effect (AME) averages over the real population."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(42)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- logistic curve with tangents -----------------------------------------
beta = 1.0
eta = np.linspace(-6, 6, 400)
p = 1 / (1 + np.exp(-eta))
axL.plot(eta, p, color=PALETTE[0], lw=2.0)

for eta0, note in [(0.0, "steep: near p=0.5"), (-3.9, "flat: near p=0.02")]:
    p0 = 1 / (1 + np.exp(-eta0))
    slope = beta * p0 * (1 - p0)
    dx = 1.7
    axL.plot([eta0 - dx, eta0 + dx], [p0 - slope * dx, p0 + slope * dx],
             color=PALETTE[1], lw=1.8)
    axL.scatter([eta0], [p0], s=36, color=PALETTE[1], zorder=5)
    axL.annotate(f"slope $=\\beta\\,p(1-p)={slope:.2f}$\n{note}",
                 xy=(eta0, p0), xytext=(eta0 + 0.3, p0 + 0.16),
                 fontsize=8, color=INK)

axL.set_xlabel(r"linear predictor $\eta = x^\top\beta$")
axL.set_ylabel("predicted probability $p$")
axL.set_title("Same $\\beta$, different effect", fontsize=10)
axL.set_ylim(-0.02, 1.02)

# ---- distribution of per-individual marginal effects ----------------------
n = 4000
age = rng.normal(50, 12, n)
treated = rng.binomial(1, 0.5, n)
eta_i = -3.0 + 0.06 * age - 0.9 * treated
p_i = 1 / (1 + np.exp(-eta_i))
me_i = 0.06 * p_i * (1 - p_i)              # marginal effect of age per person
ame = me_i.mean()

# MEM: evaluate at covariate means
eta_bar = -3.0 + 0.06 * age.mean() - 0.9 * treated.mean()
p_bar = 1 / (1 + np.exp(-eta_bar))
mem = 0.06 * p_bar * (1 - p_bar)

axR.hist(me_i, bins=40, color=PALETTE[0] + "cc", edgecolor="white", linewidth=0.3)
axR.axvline(ame, color=PALETTE[1], lw=2.0, label=f"AME (population) = {ame:.4f}")
axR.axvline(mem, color=PALETTE[3], lw=2.0, ls="--",
            label=f"MEM (average person) = {mem:.4f}")
axR.set_xlabel("marginal effect of age on risk (per year)")
axR.set_ylabel("individuals")
axR.set_title("AME averages over real people", fontsize=10)
axR.legend(fontsize=8, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/average-marginal-effects.svg")
