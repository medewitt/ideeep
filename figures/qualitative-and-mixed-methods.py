# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Code saturation: new themes discovered flatten as interviews accumulate."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(7)

interviews = np.arange(1, 21)

# Saturating discovery curve: total distinct codes approaches a ceiling.
ceiling = 42.0
rate = 0.28
smooth = ceiling * (1 - np.exp(-rate * interviews))

# Small seeded noise, then force monotonic non-decreasing (codes never vanish).
noisy = smooth + rng.normal(0, 0.8, size=interviews.size)
cumulative = np.maximum.accumulate(noisy)
cumulative = np.round(cumulative).astype(int)

# Saturation point: where new codes per interview drops below a threshold.
new_codes = np.diff(cumulative, prepend=0)
sat_idx = np.argmax(new_codes[3:] <= 1) + 3
sat_x = interviews[sat_idx]

fig, ax = plt.subplots()
ax.plot(interviews, cumulative, color=PALETTE[0], lw=2,
        marker="o", markersize=4, label="distinct codes / themes")
ax.axvline(sat_x, color=PALETTE[1], ls="--", lw=1.4)
ax.annotate("saturation", xy=(sat_x, cumulative[sat_idx]),
            xytext=(sat_x + 0.6, cumulative[sat_idx] - 12),
            fontsize=10, color=PALETTE[1])

ax.set_xlabel("interviews analyzed")
ax.set_ylabel("cumulative distinct codes / themes")
ax.set_title("Thematic saturation in qualitative sampling")
ax.set_xticks(np.arange(2, 21, 2))
ax.set_ylim(0, ceiling + 6)
ax.legend(loc="lower right")
save(fig, "assets/figures/qualitative-and-mixed-methods.svg")
