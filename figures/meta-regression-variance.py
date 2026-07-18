# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Heterogeneity explained by the moderator. The total between-study variance
(tau-squared) from a plain random-effects meta-analysis splits into a part
explained by the moderator and a residual part left over after the meta-regression.
Here the moderator accounts for about two-thirds of the heterogeneity - but a third
remains, so the studies still disagree for reasons unmeasured."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(8)
k = 14
x = rng.uniform(0, 10, k)
se = rng.uniform(0.12, 0.35, k)
y = -0.15 - 0.10 * x + rng.normal(0, 0.05, k) + rng.normal(0, se)
v = se**2


def tau2(X):
    w = 1 / v
    b = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
    Q = np.sum(w * (y - X @ b) ** 2); p = X.shape[1]
    H = np.linalg.inv(X.T @ (w[:, None] * X))
    tr = np.sum(w) - np.trace(H @ (X.T @ ((w**2)[:, None] * X)))
    return max(0, (Q - (k - p)) / tr)


t_total = tau2(np.ones((k, 1)))
t_resid = tau2(np.column_stack([np.ones(k), x]))
t_expl = t_total - t_resid
R2 = t_expl / t_total * 100

fig, ax = plt.subplots(figsize=(5.2, 3.8))
ax.bar(0, t_total, width=0.5, color=PALETTE[0], alpha=0.6, label="total $\\tau^2$")
ax.bar(1, t_expl, width=0.5, color=PALETTE[2], label=f"explained ({R2:.0f}%)")
ax.bar(1, t_resid, width=0.5, bottom=t_expl, color=PALETTE[1],
       label=f"residual ({100-R2:.0f}%)")
ax.set_xticks([0, 1])
ax.set_xticklabels(["meta-analysis\n(no moderator)", "meta-regression\n(+ moderator)"],
                   fontsize=8.4)
ax.set_ylabel("between-study variance  $\\tau^2$")
ax.set_title("The moderator explains part of the heterogeneity", fontsize=9.3)
ax.legend(fontsize=8.2, loc="upper right")
ax.grid(axis="x", visible=False)
fig.tight_layout()
save(fig, "assets/figures/meta-regression-variance.svg")
