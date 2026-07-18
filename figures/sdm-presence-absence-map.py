# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scikit-learn", "matplotlib"]
# ///
"""Presence-absence species distribution model. The shading is the predicted
probability of occurrence from a logistic model fit to surveyed sites; filled
points are sites where the species was found, open points where it was surveyed and
absent. Presences concentrate in the high-probability core and absences dominate
the unsuitable margins - and because there are true zeros, the probabilities are
calibrated, not merely relative."""
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

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
mu, sd = X.mean(0), X.std(0)
m = LogisticRegression(C=1e6, max_iter=5000).fit((X - mu) / sd, y)

gx, gy = np.meshgrid(np.linspace(0, 10, 200), np.linspace(0, 10, 200))
G = np.column_stack([gx.ravel(), gy.ravel()])
P = m.predict_proba((feats(G) - mu) / sd)[:, 1].reshape(gx.shape)

fig, ax = plt.subplots(figsize=(5.8, 4.6))
im = ax.imshow(P, extent=[0, 10, 0, 10], origin="lower", cmap="YlGnBu",
               alpha=0.9, aspect="auto", vmin=0, vmax=1)
pr = sites[y == 1]
ab = sites[y == 0]
ax.scatter(ab[:, 0], ab[:, 1], s=18, facecolor="none", edgecolor=INK,
           linewidth=0.8, label="absent")
ax.scatter(pr[:, 0], pr[:, 1], s=22, color=PALETTE[1], edgecolor="white",
           linewidth=0.4, label="present")
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
cb.set_label("predicted P(occurrence)", fontsize=8.5)
ax.set_xlabel("west → east   (temperature 10 → 30 °C)")
ax.set_ylabel("south → north   (rainfall 50 → 100 mm)")
ax.set_title("Presence-absence yields calibrated occurrence probability",
             fontsize=9.3)
ax.legend(fontsize=8.2, loc="lower right", framealpha=0.85)
fig.tight_layout()
save(fig, "assets/figures/sdm-presence-absence-map.svg")
