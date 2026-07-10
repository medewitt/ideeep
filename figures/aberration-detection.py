# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Prospective aberration detection with a seasonal expected-count band."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(1834)

# --- Weekly counts over 3 years (~156 weeks) ---
n_weeks = 156
week = np.arange(n_weeks)

# Seasonal baseline expected curve: level + annual sinusoid.
level = 22.0
amp = 12.0
phase = 2.0  # shifts the winter peak
expected = level + amp * np.sin(2 * np.pi * week / 52.0 - phase)
expected = np.clip(expected, 3.0, None)

# Observed counts: Poisson noise around the expected baseline.
observed = rng.poisson(expected).astype(float)

# Inject two localized outbreaks (runs of elevated weeks).
outbreak_1 = np.arange(58, 65)    # mid-year 2 outbreak
outbreak_2 = np.arange(120, 127)  # year 3 outbreak
for wk in outbreak_1:
    observed[wk] += rng.poisson(28)
for wk in outbreak_2:
    observed[wk] += rng.poisson(34)

# Upper threshold band = expected + ~2.5 SD (Poisson SD ~ sqrt(expected)).
sd = np.sqrt(expected)
threshold = expected + 2.5 * sd

# Alarms: observed exceeds the threshold.
alarm = observed > threshold

fig, ax = plt.subplots(figsize=(7.6, 3.6))

ax.fill_between(week, expected, threshold, color=PALETTE[0], alpha=0.15,
                label="threshold (expected + 2.5 SD)")
ax.plot(week, expected, color=PALETTE[0], lw=1.8, label="expected")
ax.plot(week, observed, color=INK, lw=0.8, alpha=0.7)
ax.scatter(week, observed, s=10, color=INK, alpha=0.8, label="observed")
ax.scatter(week[alarm], observed[alarm], s=55, color=PALETTE[1],
           edgecolor="white", lw=0.6, zorder=5, label="alarm")

ax.annotate("aberration flagged", xy=(61, observed[61]),
            xytext=(74, observed[61] + 8), fontsize="x-small",
            color=PALETTE[1],
            arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.8))

ax.set_xlabel("week")
ax.set_ylabel("reported cases")
ax.set_xlim(0, n_weeks - 1)
ax.set_ylim(0, None)
ax.set_title("Prospective aberration detection")
ax.legend(loc="upper left", fontsize="x-small", ncol=2)

fig.tight_layout()

print(f"weeks flagged: {int(alarm.sum())}")
print(f"alarm weeks: {list(week[alarm])}")

save(fig, "assets/figures/aberration-detection.svg")
