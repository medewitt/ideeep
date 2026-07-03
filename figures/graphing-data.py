# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Four workhorse chart types on epidemiological-flavored data: a distribution,
a relationship, a trend, and a group comparison."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()
rng = np.random.default_rng(1)

fig, axes = plt.subplots(2, 2, figsize=(8.6, 6.2))

# (a) distribution: right-skewed incubation periods (histogram)
inc = rng.lognormal(mean=1.5, sigma=0.5, size=2000)
axes[0, 0].hist(inc, bins=40, color=PALETTE[0], edgecolor="white", linewidth=0.3)
axes[0, 0].set_title("Distribution — incubation period")
axes[0, 0].set_xlabel("days"); axes[0, 0].set_ylabel("count")

# (b) relationship: mobility vs cases (scatter + trend)
mob = rng.uniform(0.3, 1.0, 120)
cases = 200 * mob + rng.normal(0, 25, 120)
b1 = np.cov(mob, cases, ddof=1)[0, 1] / np.var(mob, ddof=1)
b0 = cases.mean() - b1 * mob.mean()
axes[0, 1].scatter(mob, cases, s=14, color=PALETTE[0], alpha=0.7)
xr = np.array([mob.min(), mob.max()])
axes[0, 1].plot(xr, b0 + b1 * xr, color=PALETTE[1], lw=2)
axes[0, 1].set_title("Relationship — mobility vs cases")
axes[0, 1].set_xlabel("mobility index"); axes[0, 1].set_ylabel("weekly cases")

# (c) trend: epidemic curves for two regions (line)
t = np.arange(60)
def epi(peak, height):
    return height * np.exp(-((t - peak) / 10.0) ** 2)
axes[1, 0].plot(t, epi(25, 300), color=PALETTE[0], label="region A")
axes[1, 0].plot(t, epi(38, 220), color=PALETTE[1], label="region B")
axes[1, 0].set_title("Trend — the epidemic curve")
axes[1, 0].set_xlabel("day"); axes[1, 0].set_ylabel("incidence")
axes[1, 0].legend(fontsize=8)

# (d) comparison: viral load by group (boxplot)
groups = [rng.normal(m, 1.0, 80) for m in (4.0, 5.2, 3.3)]
axes[1, 1].boxplot(groups, tick_labels=["untreated", "drug A", "drug B"])
axes[1, 1].set_title("Comparison — viral load by group")
axes[1, 1].set_ylabel("log$_{10}$ viral load")

fig.tight_layout()
save(fig, "assets/figures/graphing-data.svg")
print("rendered 4-panel chart-type overview")
