# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Two ways observation distorts a delay: right truncation and interval censoring."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.6, 3.4))

# ---- Left: right truncation during a growing epidemic -------------------
# Cases infected over time; only those whose secondary event happened before
# the observation cutoff T are seen. Long delays are missing (truncated).
T = 30.0
n = 220
infection_time = rng.uniform(0, T, n)
delay = rng.gamma(shape=2.4, scale=3.0, size=n)
observed = infection_time + delay <= T

axL.scatter(infection_time[observed], delay[observed], s=12,
            color=PALETTE[0], alpha=0.8, label="observed")
axL.scatter(infection_time[~observed], delay[~observed], s=12,
            color="#c9d3db", alpha=0.9, label="not yet observed")
xs = np.linspace(0, T, 100)
axL.plot(xs, T - xs, color=PALETTE[1], lw=1.6)
axL.text(2, T - 2 - 4, "observation\ncutoff  $T$", color=PALETTE[1], fontsize=8.5)
axL.set_xlabel("infection time")
axL.set_ylabel("delay to observed event")
axL.set_title("Right truncation", fontsize=11)
axL.legend(loc="upper right", fontsize=8)
axL.set_xlim(0, T)
axL.set_ylim(0, delay.max() * 1.05)

# ---- Right: interval censoring (events known only to the day) ------------
axR.grid(False)
x = np.linspace(0, 10, 400)
pdf = (x**1.6) * np.exp(-x / 1.4)
pdf /= np.trapezoid(pdf, x)
axR.plot(x, pdf, color=INK, lw=1.6, label="true continuous delay")
for d in range(0, 10):
    mask = (x >= d) & (x < d + 1)
    axR.fill_between(x[mask], pdf[mask], step=None, alpha=0.0)
    axR.bar(d + 0.5, np.trapezoid(pdf[mask], x[mask]), width=0.94,
            color=PALETTE[2], alpha=0.35, align="center")
for d in range(0, 11):
    axR.axvline(d, color="#d8dee4", lw=0.7, zorder=0)
axR.set_xlabel("delay (days)")
axR.set_ylabel("density")
axR.set_title("Interval censoring", fontsize=11)
axR.text(6.2, pdf.max() * 0.8, "recorded only\nto the day", fontsize=8.5, color=MUTED)
axR.set_xlim(0, 10)

save(fig, "assets/figures/delay-truncation-censoring.svg")
