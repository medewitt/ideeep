# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scikit-learn", "matplotlib"]
# ///
"""ROC curve for the held-out survey sites in the presence-absence model. The area
under the curve (AUC) is the probability the model ranks a random occupied site
above a random empty one; the diagonal is chance. Evaluation is on held-out sites,
not the training data, so the number is honest."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(3)
temp = lambda x: 10 + 2.0 * x
rain = lambda y: 50 + 5.0 * y
t_opt, t_w, r_opt, r_w = 22.0, 4.0, 75.0, 12.0
S = 600
sites = rng.uniform(0, 10, size=(S, 2))
niche = -(((temp(sites[:, 0]) - t_opt) ** 2) / (2 * t_w**2)
          + ((rain(sites[:, 1]) - r_opt) ** 2) / (2 * r_w**2))
eta = 1.2 + 2.2 * niche + rng.normal(0, 0.8, S)
y = (rng.uniform(size=S) < 1 / (1 + np.exp(-eta))).astype(int)
feats = lambda P: np.column_stack([temp(P[:, 0]), temp(P[:, 0]) ** 2,
                                   rain(P[:, 1]), rain(P[:, 1]) ** 2])
X = feats(sites)
Xs = (X - X.mean(0)) / X.std(0)
idx = rng.permutation(S)
tr, te = idx[:420], idx[420:]
m = LogisticRegression(C=1e6, max_iter=5000).fit(Xs[tr], y[tr])
ph = m.predict_proba(Xs[te])[:, 1]
fpr, tpr, _ = roc_curve(y[te], ph)
auc = roc_auc_score(y[te], ph)

fig, ax = plt.subplots(figsize=(5.2, 4.4))
ax.plot([0, 1], [0, 1], color=MUTED, lw=1.2, ls="--", label="chance (AUC 0.5)")
ax.plot(fpr, tpr, color=PALETTE[0], lw=2.6, label=f"model (AUC {auc:.2f})")
ax.fill_between(fpr, tpr, alpha=0.12, color=PALETTE[0])
ax.set_xlabel("false positive rate (1 − specificity)")
ax.set_ylabel("true positive rate (sensitivity)")
ax.set_title("Held-out discrimination", fontsize=9.8)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.02)
ax.set_aspect("equal")
ax.legend(fontsize=8.6, loc="lower right")
fig.tight_layout()
save(fig, "assets/figures/sdm-presence-absence-roc.svg")
