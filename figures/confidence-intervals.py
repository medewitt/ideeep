# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Confidence-interval coverage: 95% t-intervals for the mean over 100 samples."""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)

mu, sigma, n = 0.0, 1.0, 30
n_intervals = 100
conf = 0.95

tcrit = stats.t.ppf(1 - (1 - conf) / 2, df=n - 1)

covers_count = 0
fig, ax = plt.subplots(figsize=(6, 7))

for i in range(n_intervals):
    x = rng.normal(mu, sigma, size=n)
    xbar = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    lo, hi = xbar - tcrit * se, xbar + tcrit * se
    covers = lo <= mu <= hi
    covers_count += covers
    color = PALETTE[0] if covers else PALETTE[1]
    ax.plot([lo, hi], [i, i], color=color, lw=1.3, alpha=0.9)
    ax.plot([xbar], [i], marker="o", ms=2.5, color=color)

ax.axvline(mu, color="0.3", ls="--", lw=1.5)
coverage = covers_count / n_intervals

ax.set_xlabel("interval for the mean")
ax.set_ylabel("sample index")
ax.set_title(f"95% t-intervals: empirical coverage = {coverage:.0%} "
             f"({covers_count}/{n_intervals})")

save(fig, "assets/figures/confidence-intervals.svg")
