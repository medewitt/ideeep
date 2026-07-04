# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Reporting delays drag the recent epidemic curve down; a nowcast fills it in."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()

# Reporting-delay distribution (days from event to report), discretized.
p = np.array([0.10, 0.30, 0.30, 0.20, 0.10])   # P(delay = 0, 1, 2, 3, 4)
F = np.cumsum(p)                                # fraction reported within d days

# A growing epidemic by event date; "today" is the last day on the axis.
T = 30
t = np.arange(T)
eventual = np.round(20 * np.exp(0.12 * t)).astype(float)

# Fraction of each date's cases already reported by today.
lag = (T - 1) - t
frac = np.where(lag >= len(F), 1.0, F[np.clip(lag, 0, len(F) - 1)])
observed = eventual * frac                      # right-truncated curve

# Multiplicative nowcast: divide observed by the reported fraction.
nowcast = observed / frac

fig, ax = plt.subplots(figsize=(6.6, 3.8))
ax.plot(t, eventual, color=PALETTE[2], lw=2.0, label="eventual counts (nowcast)")
ax.plot(t, observed, color=PALETTE[1], lw=2.0, marker="o", ms=3,
        label="observed so far (right-truncated)")

# Shade the region where truncation bites (the last few event dates).
ax.axvspan(T - len(F), T - 1, color=MUTED, alpha=0.10)
ax.text(T - len(F) - 0.2, eventual[-1] * 0.55, "reporting\nnot complete",
        ha="right", color=MUTED, fontsize=8.5)

ax.set_xlabel("event date (days ago counted forward)")
ax.set_ylabel("cases")
ax.set_title("The recent tail is biased down by reporting delays")
ax.legend(loc="upper left", fontsize=9)
save(fig, "assets/figures/nowcasting.svg")
