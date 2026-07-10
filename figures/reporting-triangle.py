# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""The reporting triangle: a delay distribution seen through right truncation."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# Time-homogeneous reporting-delay distribution: the probability that a case
# with a given event date is reported exactly d days later (a Markov "reporting
# hazard" summed to one over the delays shown).
p = np.array([0.06, 0.16, 0.24, 0.22, 0.15, 0.09, 0.05, 0.03])
p = p / p.sum()
n_delay = p.size
n_date = 10                                   # event dates, oldest at top

fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(7.8, 3.6), gridspec_kw={"width_ratios": [1.5, 1.0]})

# ---- Left: the reporting triangle -----------------------------------------
# Row s (0 = oldest, n_date-1 = today) can only observe delays d with
# s + d < n_date, so recent rows are truncated and the filled cells form a
# triangle. Every observable cell carries the same delay probability p_d.
grid = np.full((n_date, n_delay), np.nan)
for s in range(n_date):
    horizon = n_date - s                      # delays already observable
    grid[s, :horizon] = p[:horizon]

masked = np.ma.masked_invalid(grid)
cmap = plt.cm.viridis.copy()
cmap.set_bad("#eef1f4")                       # unobserved cells: pale grey

im = axL.imshow(masked, cmap=cmap, aspect="auto", vmin=0, vmax=p.max())
for s in range(n_date):
    for d in range(n_delay):
        if not np.isnan(grid[s, d]):
            axL.text(d, s, f"{grid[s, d]:.2f}", ha="center", va="center",
                     fontsize=6.5,
                     color="white" if grid[s, d] > 0.13 else INK)

axL.set_xticks(range(n_delay))
axL.set_xticklabels(range(n_delay))
axL.set_yticks(range(n_date))
ylabels = ["today"] + [f"$-{k}$" for k in range(1, n_date)]
axL.set_yticklabels(ylabels[::-1], fontsize=8)   # today at the bottom
axL.set_xlabel("reporting delay $d$ (days)")
axL.set_ylabel("event date")
axL.set_title("The reporting triangle", fontsize=10)
axL.grid(False)

# Outline the not-yet-reported region and label it.
axL.text(n_delay - 1.4, 1.2, "not yet\nreported\n(nowcast\ntarget)",
         ha="center", va="center", fontsize=7.5, color=MUTED)
axL.plot([n_date - 0.5 - 0.5, n_delay - 0.5], [n_date - 0.5, 0.5 - 0.5],
         color=MUTED, lw=1.0, ls="--")

# ---- Right: the delay distribution behind every row -----------------------
d = np.arange(n_delay)
axR.bar(d, p, width=0.72, color=PALETTE[0], label="P(report at delay $d$)")
axR.step(np.append(d, n_delay) - 0.5, np.append(np.cumsum(p), 1.0),
         where="post", color=PALETTE[1], lw=1.8,
         label="cumulative reported")
axR.set_xlabel("reporting delay $d$ (days)")
axR.set_ylabel("probability")
axR.set_title("Reporting-delay distribution", fontsize=10)
axR.set_ylim(0, 1.02)
axR.set_xticks(d)
axR.legend(loc="center right", fontsize=7.5)

fig.tight_layout()
save(fig, "assets/figures/reporting-triangle.svg")
