# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Short-term incidence forecast from a log-linear fit, with an uncertainty fan."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()
rng = np.random.default_rng(1834)

# Early exponential growth with observation noise on the log scale.
day = np.arange(21)
r_true = 0.16
mu = np.log(12) + r_true * day
obs = np.exp(mu + rng.normal(0, 0.18, day.size))

# Observe the first 14 days; forecast the rest.
n_obs = 14
d_obs, y_obs = day[:n_obs], obs[:n_obs]

# Log-linear (exponential-growth) fit.
b1, b0 = np.polyfit(d_obs, np.log(y_obs), 1)
resid = np.log(y_obs) - (b0 + b1 * d_obs)
sigma = resid.std(ddof=2)

# Project ahead; predictive spread widens with the forecast horizon.
fdays = np.arange(n_obs - 1, 24)
h = fdays - (n_obs - 1)
center = np.exp(b0 + b1 * fdays)
sd = sigma * np.sqrt(1.0 + h / 3.0)

fig, ax = plt.subplots(figsize=(6.6, 3.8))
# 95% and 50% fans.
ax.fill_between(fdays, center * np.exp(-1.96 * sd), center * np.exp(1.96 * sd),
                color=PALETTE[1], alpha=0.15, label="95% interval")
ax.fill_between(fdays, center * np.exp(-0.674 * sd), center * np.exp(0.674 * sd),
                color=PALETTE[1], alpha=0.25, label="50% interval")
ax.plot(fdays, center, color=PALETTE[1], lw=2.0, label="forecast")

ax.scatter(d_obs, y_obs, color=PALETTE[0], s=22, zorder=5, label="observed")
ax.scatter(day[n_obs:], obs[n_obs:], facecolors="none",
           edgecolors=MUTED, s=22, zorder=5, label="later (held out)")
ax.axvline(n_obs - 1, color="0.5", ls=":", lw=1.2)
ax.text(n_obs - 1.2, obs.max() * 0.9, "forecast date", ha="right",
        color=MUTED, fontsize=8.5)

ax.set_xlabel("day")
ax.set_ylabel("incidence")
ax.set_title("Short-term forecast is a fan, not a line")
ax.legend(loc="upper left", fontsize=8.5)
save(fig, "assets/figures/epidemic-forecasting.svg")
