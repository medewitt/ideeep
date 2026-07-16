# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""The Bayesian posterior distribution of I-squared for the effects example. A
single DerSimonian-Laird point estimate (dashed line) reports one number, but with
only six studies the between-study variance is barely identified, so the posterior
for I-squared is broad. The Bayesian approach carries that uncertainty forward
instead of hiding it. Computed from the closed-form marginal posterior of
tau-squared under a half-normal prior."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

y = np.array([-0.25, -0.70, 0.02, -0.50, -0.88, -0.33])
se = np.array([0.16, 0.19, 0.17, 0.21, 0.20, 0.13])
k = len(y)
v = se**2
w = 1 / v
# DerSimonian-Laird point I^2
theta_fe = (w * y).sum() / w.sum()
Q = (w * (y - theta_fe) ** 2).sum()
I2_dl = max(0.0, (Q - (k - 1)) / Q) * 100
# Higgins-Thompson "typical" within-study variance
s2 = (k - 1) * w.sum() / (w.sum() ** 2 - (w**2).sum())


def log_marg(t2):
    Vi = v + t2
    wi = 1 / Vi
    mu = (wi * y).sum() / wi.sum()
    return (-0.5 * np.sum(np.log(2 * np.pi * Vi) + (y - mu) ** 2 / Vi)
            + 0.5 * np.log(2 * np.pi / wi.sum()))


# grid over tau (the standard deviation) directly, so the half-normal prior needs
# no change-of-variable Jacobian
taus = np.linspace(1e-4, 2.0, 6000)
lp = np.array([log_marg(t * t) for t in taus]) + stats.halfnorm.logpdf(
    taus, scale=0.5)
post = np.exp(lp - lp.max())
post /= np.trapezoid(post, taus)
# inverse-CDF sampling (deterministic) to get an I^2 density
cdf = np.cumsum(post) * (taus[1] - taus[0])
cdf /= cdf[-1]
u = np.linspace(1e-4, 1 - 1e-4, 20000)
tau_s = np.interp(u, cdf, taus)
I2_s = tau_s**2 / (tau_s**2 + s2) * 100
mean_I2 = I2_s.mean()
lo, hi = np.percentile(I2_s, [2.5, 97.5])

fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.hist(I2_s, bins=np.linspace(0, 100, 46), density=True, color=PALETTE[0],
        alpha=0.55, edgecolor="white", linewidth=0.3)
ax.axvline(I2_dl, color=INK, lw=1.8, ls="--",
           label=f"DerSimonian–Laird point = {I2_dl:.0f}%")
ax.axvspan(lo, hi, color=PALETTE[1], alpha=0.12)
ax.axvline(mean_I2, color=PALETTE[1], lw=2.0,
           label=f"posterior mean = {mean_I2:.0f}%")
ax.plot([lo, hi], [0.001, 0.001], color=PALETTE[1], lw=3,
        solid_capstyle="butt")
ax.text((lo + hi) / 2, 0.004, f"95% CrI [{lo:.0f}, {hi:.0f}]%", ha="center",
        fontsize=8, color=PALETTE[1])

ax.set_xlabel("$I^2$ (%)")
ax.set_ylabel("posterior density")
ax.set_title("Posterior for $I^2$ — a point estimate hides this spread",
             fontsize=9.3)
ax.set_xlim(0, 100)
ax.legend(fontsize=8, loc="upper left")
ax.grid(axis="x", visible=False)
fig.tight_layout()
save(fig, "assets/figures/meta-analysis-i2.svg")
