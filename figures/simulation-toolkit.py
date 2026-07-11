# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "scipy"]
# ///
"""The Monte Carlo workflow. Left: the workhorse loop — start from a known
data-generating process, generate a sample, fit/estimate, record an indicator,
and repeat, then aggregate. Right: running that loop for the coverage of a 95%
t-interval (mu=5, n=20) — each repeat draws a fresh sample and forms an
interval; about 95% of the intervals cover the true mean and about 5% miss it,
so the recorded coverage converges to 0.95 by the law of large numbers."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(2026)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 3.9),
                               gridspec_kw={"width_ratios": [1, 1.15]})

# ---- Monte Carlo loop diagram ---------------------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 10)
axL.axis("off")
axL.set_title("generate · fit · record · repeat", fontsize=10)

steps = [("known DGP\n(choose the truth)", 7.9, PALETTE[3]),
         ("generate\na sample", 5.9, PALETTE[0]),
         ("fit / estimate", 3.9, PALETTE[2]),
         ("record\nindicator", 1.9, PALETTE[1])]
for text, y, col in steps:
    axL.add_patch(FancyBboxPatch((2.6, y - 0.65), 4.8, 1.3,
                  boxstyle="round,pad=0.08", linewidth=1.6, edgecolor=col,
                  facecolor=col + "14"))
    axL.text(5.0, y, text, ha="center", va="center", fontsize=8.6, color=INK)
for y in (7.25, 5.25, 3.25):
    axL.add_patch(FancyArrowPatch((5.0, y), (5.0, y - 0.6), arrowstyle="-|>",
                  mutation_scale=14, color="0.4", lw=1.5))
# loop-back arrow
axL.add_patch(FancyArrowPatch((7.4, 1.9), (7.4, 7.9), arrowstyle="-|>",
              mutation_scale=14, color=MUTED, lw=1.5,
              connectionstyle="arc3,rad=-0.55"))
axL.text(9.2, 4.9, "repeat\n×B", fontsize=8, color=MUTED, ha="center")
axL.text(5.0, 0.4, "aggregate → sampling distribution", ha="center",
         fontsize=8, color=INK, style="italic")

# ---- CI coverage ----------------------------------------------------------
mu = 5.0
n, K = 20, 30
axR.axvline(mu, color=INK, lw=1.5)
axR.text(mu + 0.03, K + 0.3, r"true $\mu=5$", fontsize=8.5, color=INK)
n_missed = 0
for k in range(K):
    y = rng.normal(mu, 1.0, n)
    lo, hi = stats.t.interval(0.95, n - 1, loc=y.mean(), scale=stats.sem(y))
    covers = lo <= mu <= hi
    n_missed += not covers
    col = PALETTE[0] if covers else PALETTE[1]
    axR.plot([lo, hi], [k, k], color=col, lw=1.6,
             solid_capstyle="butt")
    axR.plot([y.mean()], [k], marker="o", ms=2.5, color=col)
axR.set_yticks([])
axR.set_xlabel("95% confidence interval for the mean")
axR.set_title(f"{K-n_missed}/{K} intervals cover μ (~95%)", fontsize=9.5)
axR.text(mu + 1.4, 1.0, f"{n_missed} miss", fontsize=8, color=PALETTE[1])
axR.set_ylim(-1, K + 1)
axR.grid(axis="y", visible=False)

fig.tight_layout()
save(fig, "assets/figures/simulation-toolkit.svg")
