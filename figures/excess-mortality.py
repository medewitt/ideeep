# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Excess mortality: Serfling baseline, observed shock, and undercount."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# Weekly all-cause deaths over ~5 years (260 weeks).
weeks = np.arange(260)

# Serfling-style expected baseline: level + mild trend + annual sinusoid
# peaking in winter (week 0 = midwinter, higher deaths).
level = 1050.0
trend = 0.45 * weeks
seasonal = 120.0 * np.cos(2 * np.pi * weeks / 52.0)
baseline = level + trend + seasonal

# Prediction interval width for the baseline.
sd = 45.0

# Observed = baseline + noise, then inject a pandemic shock (weeks 205-235).
noise = rng.normal(0.0, sd, size=weeks.size)
observed = baseline + noise

shock = (weeks >= 205) & (weeks <= 235)
peak_week = 220.0
bump = 620.0 * np.exp(-0.5 * ((weeks - peak_week) / 8.0) ** 2)
observed = observed + bump * shock

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# Left: baseline with prediction interval, observed line, excess shading.
axL.fill_between(
    weeks, baseline - 2 * sd, baseline + 2 * sd,
    color=PALETTE[0], alpha=0.15, linewidth=0,
)
axL.plot(weeks, baseline, color=PALETTE[0], lw=1.8,
         label="expected baseline")
axL.plot(weeks, observed, color=INK, lw=1.2, label="observed")
axL.fill_between(
    weeks, baseline, observed, where=observed > baseline,
    color=PALETTE[1], alpha=0.4, linewidth=0, label="excess",
)
axL.set_xlabel("week")
axL.set_ylabel("all-cause deaths per week")
axL.set_xlim(0, 259)
axL.legend(loc="upper left", fontsize=8.5)

# Right: cumulative excess vs cumulative reported over the shock period.
sw = weeks[shock]
weekly_excess = np.clip(observed[shock] - baseline[shock], 0.0, None)
cum_excess = np.cumsum(weekly_excess)
cum_reported = 0.65 * cum_excess  # cause-specific attribution undercounts

axR.plot(sw, cum_excess, color=PALETTE[1], lw=2.0,
         label="cumulative excess")
axR.plot(sw, cum_reported, color=PALETTE[0], lw=2.0,
         label="cumulative reported")
axR.fill_between(sw, cum_reported, cum_excess, color=PALETTE[1],
                 alpha=0.15, linewidth=0)
axR.set_xlabel("week of the shock")
axR.set_ylabel("cumulative deaths")
axR.set_xlim(sw.min(), sw.max())
axR.legend(loc="upper left", fontsize=8.5)

axR.annotate(
    "excess > reported:\nundercount",
    xy=(sw[-1], 0.5 * (cum_excess[-1] + cum_reported[-1])),
    xytext=(sw.min() + 3, cum_excess[-1] * 0.72),
    fontsize=8.5, color=INK, ha="left",
    arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1),
)

fig.tight_layout()
save(fig, "assets/figures/excess-mortality.svg")
