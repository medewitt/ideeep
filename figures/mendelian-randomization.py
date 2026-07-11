# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Mendelian randomization. Left: the inverse-variance-weighted estimate is the
slope of a weighted regression of the SNP-outcome effects on the SNP-exposure
effects through the origin — for the five worked SNPs the fit passes through
(0,0) with slope ~0.303, and the points are sized by their weight 1/se^2.
Right: when the variants have directional (horizontal) pleiotropy, every
outcome effect is lifted, so the through-origin IVW slope is biased while an
MR-Egger regression that allows an intercept exposes the pleiotropy as a
non-zero intercept."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

gamma = np.array([0.20, 0.35, 0.10, 0.50, 0.25])       # SNP-exposure
Gamma = np.array([0.061, 0.104, 0.031, 0.152, 0.073])  # SNP-outcome
se = np.array([0.020, 0.025, 0.030, 0.018, 0.022])
w = 1 / se**2

ivw = np.sum(gamma * Gamma * w) / np.sum(gamma**2 * w)   # ~0.303

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6), sharey=False)

# ---- clean IVW through the origin -----------------------------------------
sizes = 20 + 4000 * (w / w.max()) * 0.02 * 20
axL.scatter(gamma, Gamma, s=w / w.max() * 120 + 20, color=PALETTE[0] + "cc",
            zorder=5, label="SNPs (size ∝ weight)")
xx = np.array([0, 0.55])
axL.plot(xx, ivw * xx, color=PALETTE[1], lw=2.0,
         label=fr"IVW slope $\approx{ivw:.3f}$")
axL.scatter([0], [0], marker="+", s=90, color=INK, zorder=6)
axL.annotate("through the origin\n(exclusion restriction)", xy=(0, 0),
             xytext=(0.06, 0.13), fontsize=7.8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axL.set_xlabel(r"SNP–exposure effect $\hat\gamma_j$")
axL.set_ylabel(r"SNP–outcome effect $\hat\Gamma_j$")
axL.set_title("IVW = weighted regression through 0", fontsize=9.5)
axL.set_xlim(0, 0.56)
axL.set_ylim(0, 0.17)
axL.legend(fontsize=8, loc="upper left")

# ---- pleiotropy: MR-Egger intercept ---------------------------------------
pleio = 0.03
Gp = Gamma + pleio                                       # every outcome lifted
ivw_p = np.sum(gamma * Gp * w) / np.sum(gamma**2 * w)    # biased (through 0)
# MR-Egger: weighted regression with intercept
W = np.diag(w)
X = np.column_stack([np.ones_like(gamma), gamma])
coef = np.linalg.solve(X.T @ W @ X, X.T @ W @ Gp)
egger_int, egger_slope = coef

axR.scatter(gamma, Gp, s=w / w.max() * 120 + 20, color=PALETTE[3] + "cc",
            zorder=5)
axR.plot(xx, ivw_p * xx, color=PALETTE[1], lw=1.8, ls="--",
         label=fr"IVW through 0 (biased {ivw_p:.2f})")
axR.plot(xx, egger_int + egger_slope * xx, color=PALETTE[2], lw=2.0,
         label=fr"MR-Egger (slope {egger_slope:.2f})")
axR.scatter([0], [egger_int], s=45, color=PALETTE[2], zorder=6)
axR.annotate(f"non-zero intercept\n≈ {egger_int:.2f}\n→ directional pleiotropy",
             xy=(0, egger_int), xytext=(0.1, 0.05), fontsize=7.6,
             color=PALETTE[2], arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axR.set_xlabel(r"SNP–exposure effect $\hat\gamma_j$")
axR.set_ylabel(r"SNP–outcome effect $\hat\Gamma_j$")
axR.set_title("MR-Egger intercept flags pleiotropy", fontsize=9.5)
axR.set_xlim(0, 0.56)
axR.set_ylim(0, 0.20)
axR.legend(fontsize=7.6, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/mendelian-randomization.svg")
