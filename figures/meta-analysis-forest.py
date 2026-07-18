# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Forest plot of the worked effects example: six studies reporting a log odds
ratio, shown on the odds-ratio scale (log axis). Squares are the per-study odds
ratios (area proportional to random-effects weight) with 95% confidence intervals;
the diamonds are the fixed-effect and random-effects pooled estimates. The
random-effects diamond is a little wider because it adds the between-study variance
tau-squared to each weight."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

y = np.array([-0.25, -0.70, 0.02, -0.50, -0.88, -0.33])
se = np.array([0.16, 0.19, 0.17, 0.21, 0.20, 0.13])
k = len(y)
v = se**2
w = 1 / v
theta_fe = (w * y).sum() / w.sum()
se_fe = np.sqrt(1 / w.sum())
Q = (w * (y - theta_fe) ** 2).sum()
C = w.sum() - (w**2).sum() / w.sum()
tau2 = max(0.0, (Q - (k - 1)) / C)
ws = 1 / (v + tau2)
theta_re = (ws * y).sum() / ws.sum()
se_re = np.sqrt(1 / ws.sum())

fig, ax = plt.subplots(figsize=(6.6, 4.2))
rows = k + 2

for i in range(k):
    yy = rows - i
    lo, hi = np.exp(y[i] - 1.96 * se[i]), np.exp(y[i] + 1.96 * se[i])
    ax.plot([lo, hi], [yy, yy], color=INK, lw=1.3, zorder=2)
    ax.scatter([np.exp(y[i])], [yy], s=40 + 700 * ws[i] / ws.max(),
               color=PALETTE[0], zorder=3, edgecolor="white", linewidth=0.6)
    ax.text(0.30, yy, f"study {i+1}", va="center", ha="left", fontsize=8.2,
            color=INK)


def diamond(center, se_, yy, color, label):
    lo, hi = np.exp(center - 1.96 * se_), np.exp(center + 1.96 * se_)
    d = 0.32
    pts = [(lo, yy), (np.exp(center), yy + d), (hi, yy), (np.exp(center), yy - d)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=INK,
                         lw=1.0, zorder=4))
    ax.text(0.30, yy, label, va="center", ha="left", fontsize=8.4, color=color,
            fontweight="bold")


diamond(theta_fe, se_fe, 1.6, PALETTE[2], "fixed effect")
diamond(theta_re, se_re, 0.7, PALETTE[1], "random effects")

ax.axvline(1.0, color=MUTED, lw=1.0, ls="--")
ax.set_xscale("log")
ax.set_xlim(0.28, 1.6)
ax.set_xticks([0.3, 0.5, 0.7, 1.0, 1.5])
ax.set_xticklabels(["0.3", "0.5", "0.7", "1.0", "1.5"])
ax.set_ylim(0.0, rows + 1.0)
ax.set_yticks([])
ax.set_xlabel("odds ratio (log scale)")
ax.set_title(f"Pooled OR ≈ {np.exp(theta_re):.2f},  $I^2$ ≈ "
             f"{max(0.0,(Q-(k-1))/Q)*100:.0f}%", fontsize=9.5)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/meta-analysis-forest.svg")
