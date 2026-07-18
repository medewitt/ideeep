# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""A paired forest plot for diagnostic-accuracy meta-analysis. Sensitivity (left)
and specificity (right) are shown for each study with 95% Wilson intervals, with
the bivariate pooled estimates as diamonds at the foot. Displaying the two side by
side is the Cochrane convention - but they are estimated jointly, not as two
independent pools, so the summary respects their negative threshold correlation."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(15)
k = 16
cov = np.array([[0.7**2, -0.5 * 0.7 * 0.6], [-0.5 * 0.7 * 0.6, 0.6**2]])
theta = rng.multivariate_normal([1.7, 2.0], cov, k)
sens, spec = 1 / (1 + np.exp(-theta[:, 0])), 1 / (1 + np.exp(-theta[:, 1]))
n_dis, n_hlth = rng.integers(20, 120, k), rng.integers(30, 200, k)
TP, FP = rng.binomial(n_dis, sens), rng.binomial(n_hlth, 1 - spec)
TN = n_hlth - FP


def wilson(x, n, z=1.96):
    ph = x / n; d = 1 + z**2 / n
    c = (ph + z**2 / (2 * n)) / d
    h = z * np.sqrt(ph * (1 - ph) / n + z**2 / (4 * n**2)) / d
    return c - h, c + h


expit = lambda v: 1 / (1 + np.exp(-v))
pool_se, pool_sp = expit(1.584), expit(2.092)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 5.0), sharey=True)
for ax, val, num, den, title, col in [
        (axL, TP / n_dis, TP, n_dis, "Sensitivity", PALETTE[0]),
        (axR, TN / n_hlth, TN, n_hlth, "Specificity", PALETTE[2])]:
    for i in range(k):
        yy = k - i
        lo, hi = wilson(num[i], den[i])
        ax.plot([lo, hi], [yy, yy], color=INK, lw=1.1)
        ax.scatter([val[i]], [yy], s=16 + 0.4 * den[i], color=col, zorder=3,
                   edgecolor="white", linewidth=0.3)
    pool = pool_se if title == "Sensitivity" else pool_sp
    ax.add_patch(Polygon([(pool - 0.03, 0), (pool, 0.35), (pool + 0.03, 0),
                          (pool, -0.35)], closed=True, facecolor=PALETTE[1],
                         edgecolor=INK, lw=1.0))
    ax.set_title(f"{title}  (pooled {pool*100:.0f}%)", fontsize=9.6)
    ax.set_xlim(0.45, 1.0)
    ax.set_xlabel("proportion")
    ax.grid(axis="y", visible=False)
axL.set_yticks(list(range(1, k + 1)) + [0])
axL.set_yticklabels([f"study {i}" for i in range(k, 0, -1)] + ["pooled"], fontsize=7)
axL.set_ylim(-0.7, k + 0.7)
fig.tight_layout()
save(fig, "assets/figures/dta-forest.svg")
