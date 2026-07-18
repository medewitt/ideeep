# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Pooling disease prevalence across seven sites. Each site shows its observed
prevalence with a 95% Wilson interval (wider where the sample is small); the
diamond is the random-effects pooled prevalence, estimated on the logit scale so
the interval respects the 0-1 boundary. The shaded band is the pooled confidence
interval, far narrower than any single small site."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

pos = np.array([12, 30, 8, 25, 5, 40, 18], float)
n = np.array([200, 450, 150, 300, 120, 500, 260], float)
p = pos / n


def wilson(k_, n_, z=1.96):
    ph = k_ / n_
    denom = 1 + z**2 / n_
    center = (ph + z**2 / (2 * n_)) / denom
    half = z * np.sqrt(ph * (1 - ph) / n_ + z**2 / (4 * n_**2)) / denom
    return center - half, center + half


# random-effects pooling on the logit scale (DerSimonian-Laird)
lp = np.log(p / (1 - p))
vl = 1 / (n * p * (1 - p))
w = 1 / vl
mu_fe = (w * lp).sum() / w.sum()
Q = (w * (lp - mu_fe) ** 2).sum()
C = w.sum() - (w**2).sum() / w.sum()
tau2 = max(0.0, (Q - (len(p) - 1)) / C)
ws = 1 / (vl + tau2)
mu = (ws * lp).sum() / ws.sum()
se_mu = np.sqrt(1 / ws.sum())
expit = lambda x: 1 / (1 + np.exp(-x))
pooled = expit(mu)
plo, phi = expit(mu - 1.96 * se_mu), expit(mu + 1.96 * se_mu)

fig, ax = plt.subplots(figsize=(6.6, 4.0))
m = len(p)
rows = m + 1
for i in range(m):
    yy = rows - i
    lo, hi = wilson(pos[i], n[i])
    ax.plot([lo * 100, hi * 100], [yy, yy], color=INK, lw=1.3, zorder=2)
    ax.scatter([p[i] * 100], [yy], s=30 + 500 * (n[i] / n.max()),
               color=PALETTE[0], zorder=3, edgecolor="white", linewidth=0.6)
    ax.text(0.2, yy, f"site {i+1} ({int(pos[i])}/{int(n[i])})", va="center",
            ha="left", fontsize=8.0, color=INK)

ax.axvspan(plo * 100, phi * 100, color=PALETTE[1], alpha=0.12)
d = 0.34
pts = [(plo * 100, 0.9), (pooled * 100, 0.9 + d), (phi * 100, 0.9),
       (pooled * 100, 0.9 - d)]
ax.add_patch(Polygon(pts, closed=True, facecolor=PALETTE[1], edgecolor=INK,
                     lw=1.0, zorder=4))
ax.text(0.2, 0.9, "pooled (RE)", va="center", ha="left", fontsize=8.4,
        color=PALETTE[1], fontweight="bold")

ax.set_xlim(0, 12)
ax.set_ylim(0.3, rows + 1.0)
ax.set_yticks([])
ax.set_xlabel("prevalence (%)")
ax.set_title(f"Pooled prevalence ≈ {pooled*100:.1f}%  "
             f"(95% CI {plo*100:.1f}–{phi*100:.1f}%)", fontsize=9.3)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/meta-analysis-prevalence.svg")
