# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""Kaplan-Meier survival curves for two groups with right-censoring."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)


def simulate(event_rate, n, cens_rate=0.03):
    event = rng.exponential(1.0 / event_rate, size=n)
    censor = rng.exponential(1.0 / cens_rate, size=n)
    time = np.minimum(event, censor)
    observed = event < censor
    return time, observed


def kaplan_meier(time, observed):
    order = np.argsort(time)
    time = time[order]
    observed = observed[order]
    n = len(time)

    unique_event_times = np.unique(time[observed])
    t_grid = [0.0]
    s_grid = [1.0]
    s = 1.0
    for t in unique_event_times:
        at_risk = np.sum(time >= t)
        deaths = np.sum((time == t) & observed)
        if at_risk > 0:
            s *= (1.0 - deaths / at_risk)
        t_grid.append(t)
        s_grid.append(s)
    return np.array(t_grid), np.array(s_grid)


fig, ax = plt.subplots()

groups = [
    ("Group A", 0.08, PALETTE[0]),
    ("Group B", 0.15, PALETTE[1]),
]

for label, rate, color in groups:
    time, observed = simulate(rate, n=120)
    t, s = kaplan_meier(time, observed)
    ax.step(t, s, where="post", color=color, lw=2, label=label)
    # censoring ticks
    cens_times = time[~observed]
    # survival value at each censoring time
    s_at = np.array([s[np.searchsorted(t, ct, side="right") - 1] for ct in cens_times])
    ax.plot(cens_times, s_at, "|", color=color, markersize=8, alpha=0.7)

ax.set_xlabel("time")
ax.set_ylabel("survival probability S(t)")
ax.set_title("Kaplan-Meier")
ax.set_ylim(0, 1.02)
ax.legend()

save(fig, "assets/figures/survival-analysis.svg")
