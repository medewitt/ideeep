# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scikit-learn", "matplotlib"]
# ///
"""Recovering the thermal niche from presence-only data. The presence-versus-
background logistic model (the Poisson point process) recovers the unimodal
temperature response and its optimum near 22 C, matching the true niche in shape;
the absolute height is not identifiable from presence-only data, so both curves are
scaled to their peak."""
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1)
temp = lambda x: 10 + 2.0 * x
rain = lambda y: 50 + 5.0 * y
t_opt, t_w, r_opt, r_w = 22.0, 4.0, 75.0, 12.0
suit = lambda x, y: np.exp(-((temp(x) - t_opt) ** 2) / (2 * t_w**2)
                           - ((rain(y) - r_opt) ** 2) / (2 * r_w**2))

cand = rng.uniform(0, 10, size=(20000, 2))
pres = cand[rng.uniform(size=len(cand)) < suit(cand[:, 0], cand[:, 1])][:300]
bg = rng.uniform(0, 10, size=(3000, 2))
feats = lambda P: np.column_stack([temp(P[:, 0]), temp(P[:, 0]) ** 2,
                                   rain(P[:, 1]), rain(P[:, 1]) ** 2])
X = np.vstack([feats(pres), feats(bg)])
y = np.r_[np.ones(len(pres)), np.zeros(len(bg))]
w = np.r_[np.ones(len(pres)), np.full(len(bg), len(pres) / len(bg))]
mu, sd = X.mean(0), X.std(0)
m = LogisticRegression(C=1e6, max_iter=5000).fit((X - mu) / sd, y, sample_weight=w)
b = m.coef_[0] / sd
t_hat = -b[0] / (2 * b[1])

tt = np.linspace(12, 30, 200)
true_resp = np.exp(-((tt - t_opt) ** 2) / (2 * t_w**2))
lin = b[0] * tt + b[1] * tt**2
fit_resp = np.exp(lin - lin.max())

fig, ax = plt.subplots(figsize=(6.2, 4.0))
ax.plot(tt, true_resp, color=INK, lw=2.2, ls="--", label="true niche")
ax.plot(tt, fit_resp, color=PALETTE[0], lw=2.4, label="recovered (presence vs background)")
ax.axvline(t_opt, color=MUTED, lw=1.0, ls=":")
ax.axvline(t_hat, color=PALETTE[1], lw=1.6)
ax.annotate(f"recovered optimum {t_hat:.1f} °C\n(true {t_opt:.0f} °C)",
            xy=(t_hat, 0.5), xytext=(24.2, 0.62), fontsize=8.3, color=INK,
            arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.9))
ax.set_xlabel("temperature (°C)")
ax.set_ylabel("relative suitability (scaled to peak)")
ax.set_title("Presence-only recovers the response shape, not the level", fontsize=9.4)
ax.legend(fontsize=8.4, loc="upper left")
ax.set_ylim(0, 1.12)
fig.tight_layout()
save(fig, "assets/figures/sdm-presence-only-response.svg")
