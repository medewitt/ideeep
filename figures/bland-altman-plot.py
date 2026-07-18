# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""The Bland-Altman plot for the worked example: the difference between the two
assays against their mean. The solid line is the mean difference (bias); the
dashed lines are the 95% limits of agreement, bias plus or minus 1.96 SD, within
which 95% of differences fall. The sloping trend line shows proportional bias -
the disagreement grows with concentration - which a single bias number would
miss."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(7)
n = 50
true = rng.uniform(20, 300, n)
B = true + rng.normal(0, 6, n)
A = true + 8 + 0.05 * (true - 160) + rng.normal(0, 8, n)
diff = A - B
avg = (A + B) / 2
bias = diff.mean()
sd = diff.std(ddof=1)
lo, hi = bias - 1.96 * sd, bias + 1.96 * sd
slope, intercept, rr, p, se = stats.linregress(avg, diff)

fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.scatter(avg, diff, s=34, color=PALETTE[0], alpha=0.85, edgecolor="white",
           linewidth=0.4, zorder=3)
ax.axhline(bias, color=PALETTE[1], lw=2.0, zorder=2)
ax.axhline(hi, color=INK, lw=1.3, ls="--", zorder=2)
ax.axhline(lo, color=INK, lw=1.3, ls="--", zorder=2)
ax.axhline(0, color=MUTED, lw=0.9, ls=":", zorder=1)

xx = np.linspace(avg.min(), avg.max(), 50)
ax.plot(xx, intercept + slope * xx, color=PALETTE[3], lw=1.6, ls="-.",
        label=f"proportional bias (slope {slope:.02f}, p={p:.3f})")

x1 = avg.max()
ax.text(x1, bias + 1.2, f"bias = {bias:.1f}", color=PALETTE[1], fontsize=8.5,
        ha="right", fontweight="bold")
ax.text(x1, hi + 1.2, f"+1.96 SD = {hi:.1f}", color=INK, fontsize=8.2, ha="right")
ax.text(x1, lo - 3.0, f"−1.96 SD = {lo:.1f}", color=INK, fontsize=8.2, ha="right")

ax.set_xlabel("mean of the two assays  $(A+B)/2$  (BAU/mL)")
ax.set_ylabel("difference  $A - B$  (BAU/mL)")
ax.set_title("Bland–Altman plot: bias and 95% limits of agreement", fontsize=9.6)
ax.legend(fontsize=8.2, loc="lower left")
fig.tight_layout()
save(fig, "assets/figures/bland-altman-plot.svg")
