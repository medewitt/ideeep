# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""A meta-regression bubble plot. Each study's effect is plotted against a
study-level moderator; the bubble area is proportional to the study's weight, and
the line is the random-effects meta-regression fit with its 95% band. The clear
downward slope shows the moderator explains much of the between-study
heterogeneity that a plain pooled estimate would have hidden."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(8)
k = 14
x = rng.uniform(0, 10, k)
se = rng.uniform(0.12, 0.35, k)
theta = -0.15 - 0.10 * x + rng.normal(0, 0.05, k)
y = theta + rng.normal(0, se)
v = se**2


def re_fit(X):
    w = 1 / v
    b = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
    Q = np.sum(w * (y - X @ b) ** 2); p = X.shape[1]
    H = np.linalg.inv(X.T @ (w[:, None] * X))
    tr = np.sum(w) - np.trace(H @ (X.T @ ((w**2)[:, None] * X)))
    t2 = max(0, (Q - (k - p)) / tr); ws = 1 / (v + t2)
    b = np.linalg.lstsq(X * np.sqrt(ws)[:, None], y * np.sqrt(ws), rcond=None)[0]
    cov = np.linalg.inv(X.T @ (ws[:, None] * X))
    return b, cov, t2, ws


X = np.column_stack([np.ones(k), x])
b, cov, t2, ws = re_fit(X)

fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.scatter(x, y, s=40 + 1400 * ws / ws.max(), color=PALETTE[0], alpha=0.55,
           edgecolor=INK, linewidth=0.5, zorder=3)
xx = np.linspace(0, 10, 100)
Xg = np.column_stack([np.ones(100), xx])
pred = Xg @ b
sep = np.sqrt(np.einsum("ij,jk,ik->i", Xg, cov, Xg))
ax.plot(xx, pred, color=PALETTE[1], lw=2.2, label="meta-regression fit")
ax.fill_between(xx, pred - 1.96 * sep, pred + 1.96 * sep, color=PALETTE[1], alpha=0.15)
ax.axhline(0, color=INK, lw=0.8, ls=":")
ax.set_xlabel("study-level moderator (e.g. latitude)")
ax.set_ylabel("study effect (log risk ratio)")
ax.set_title(f"Effect depends on the moderator (slope {b[1]:.02f})", fontsize=9.6)
ax.annotate("bubble area ∝ study weight", xy=(0.5, 0.02), xycoords="axes fraction",
            fontsize=8, color=INK)
ax.legend(fontsize=8.4, loc="upper right")
fig.tight_layout()
save(fig, "assets/figures/meta-regression-bubble.svg")
