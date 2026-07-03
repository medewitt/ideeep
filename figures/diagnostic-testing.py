# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""ROC curve for a Normal-shift test, and how PPV collapses at low prevalence."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(7)

# --- LEFT: ROC curve for diseased ~ N(1,1), healthy ~ N(0,1) ---
# For a threshold c, we call "positive" if score > c.
# TPR = P(score > c | diseased), FPR = P(score > c | healthy).
thresholds = np.linspace(5, -5, 400)
tpr = 1 - norm.cdf(thresholds, loc=1.0, scale=1.0)
fpr = 1 - norm.cdf(thresholds, loc=0.0, scale=1.0)

# AUC for two normals with unit variance and mean difference d is Phi(d/sqrt(2)).
d = 1.0
auc_exact = norm.cdf(d / np.sqrt(2))
auc_trap = np.trapezoid(tpr, fpr)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 4.2))

axL.plot(fpr, tpr, color=PALETTE[0], lw=2.0, label="ROC curve")
axL.plot([0, 1], [0, 1], color="0.5", ls="--", lw=1.3, label="chance")
axL.set_xlim(0, 1)
axL.set_ylim(0, 1)
axL.set_xlabel("false positive rate (1 - specificity)")
axL.set_ylabel("true positive rate (sensitivity)")
axL.set_title("ROC curve")
axL.annotate(f"AUC = {auc_trap:.2f}", xy=(0.55, 0.30), fontsize="medium",
             color=PALETTE[0])
axL.legend(loc="lower right")

# --- RIGHT: PPV vs prevalence for sens = spec = 0.95 ---
sens = 0.95
spec = 0.95
prev = np.linspace(1e-4, 0.20, 400)
ppv = (sens * prev) / (sens * prev + (1 - spec) * (1 - prev))

axR.plot(prev, ppv, color=PALETTE[1], lw=2.0)
p_mark = 0.01
ppv_mark = (sens * p_mark) / (sens * p_mark + (1 - spec) * (1 - p_mark))
axR.plot([p_mark], [ppv_mark], marker="o", ms=7, color=PALETTE[3])
axR.annotate(f"prevalence 1%\nPPV = {ppv_mark:.2f}",
             xy=(p_mark, ppv_mark), xytext=(0.05, 0.30),
             arrowprops=dict(arrowstyle="->", color="0.4"), fontsize="small")
axR.set_xlim(0, 0.20)
axR.set_ylim(0, 1)
axR.set_xlabel("prevalence")
axR.set_ylabel("positive predictive value")
axR.set_title("PPV depends on prevalence (sens = spec = 0.95)")

fig.tight_layout()

print(f"AUC (exact)  = {auc_exact:.4f}")
print(f"AUC (trapz)  = {auc_trap:.4f}")
for p in [0.001, 0.01, 0.05, 0.10]:
    v = (sens * p) / (sens * p + (1 - spec) * (1 - p))
    print(f"prevalence {p:.3f} -> PPV = {v:.4f}")

save(fig, "assets/figures/diagnostic-testing.svg")
