# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Explaining a model with SHAP. Left: a local explanation for one patient --
each feature's SHAP value pushes the prediction up (toward risk) or down from
the population baseline, and they sum exactly to the model's output. Right: the
global picture -- averaging the magnitude of each feature's SHAP values across
patients ranks how much each drives predictions overall.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1)

features = ["age", "CRP", "O2 sat", "comorbidity", "BMI"]
# a linear-logit model, for which SHAP contributions are exact: w_j * (x_j - E[x_j])
w = np.array([1.1, 0.9, -1.3, 0.7, 0.3])
X = rng.normal(0, 1, (400, 5))
base = 0.0                                     # baseline logit (mean contribution 0)
# --- one patient's local explanation ---
x = np.array([1.6, 1.2, -1.4, 0.5, -0.3])
contrib = w * x                                # SHAP values (features centered at 0)
pred = base + contrib.sum()

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.8, 3.9))

order = np.argsort(np.abs(contrib))
cols = [PALETTE[1] if c > 0 else PALETTE[0] for c in contrib[order]]
ax0.barh(range(5), contrib[order], color=cols, edgecolor=INK, linewidth=0.5)
ax0.set_yticks(range(5))
ax0.set_yticklabels([features[i] for i in order], fontsize=9)
ax0.axvline(0, color=INK, lw=0.9)
ax0.set_title(f"Local: one patient (logit {pred:+.2f})", fontsize=10)
ax0.set_xlabel("SHAP value  (← lowers   raises →)", fontsize=9)
ax0.text(0.02, 0.02, "red raises risk · blue lowers", transform=ax0.transAxes,
         fontsize=7.5, color=MUTED)

# --- global importance: mean |SHAP| across patients ---
shap_all = X * w                               # each patient's contributions
mean_abs = np.abs(shap_all).mean(0)
gorder = np.argsort(mean_abs)
ax1.barh(range(5), mean_abs[gorder], color=PALETTE[3], edgecolor=INK,
         linewidth=0.5)
ax1.set_yticks(range(5))
ax1.set_yticklabels([features[i] for i in gorder], fontsize=9)
ax1.set_title("Global: mean |SHAP| over patients", fontsize=10)
ax1.set_xlabel("mean absolute SHAP value", fontsize=9)

fig.tight_layout()
save(fig, "assets/figures/interpretability-shap.svg")
