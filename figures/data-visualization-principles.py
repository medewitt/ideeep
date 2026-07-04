# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Before/after: a truncated y-axis exaggerates small differences.

Left panel starts the y-axis near the data and makes four nearly equal
group means look dramatically different. Right panel shows the same
numbers honestly, from zero, with standard-error intervals.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

sites = ["A", "B", "C", "D"]
means = np.array([0.42, 0.45, 0.47, 0.44])   # positivity by site
ses = np.array([0.015, 0.014, 0.016, 0.015])
x = np.arange(len(sites))

fig, (ax_bad, ax_good) = plt.subplots(1, 2, figsize=(7.4, 3.6))

# Misleading: truncated axis, no uncertainty, rainbow-ish per-bar color.
bad_colors = PALETTE[:4]
ax_bad.bar(x, means, color=bad_colors)
ax_bad.set_ylim(0.40, 0.48)          # truncated: exaggerates gaps
ax_bad.set_xticks(x)
ax_bad.set_xticklabels(sites)
ax_bad.set_title("Misleading", color=PALETTE[1])
ax_bad.set_xlabel("site")
ax_bad.set_ylabel("positivity")
ax_bad.grid(False)

# Honest: axis from zero, one color, intervals, direct labels.
ax_good.bar(x, means, color=PALETTE[0], width=0.6)
ax_good.errorbar(x, means, yerr=ses, fmt="none", ecolor=INK, capsize=4, lw=1.2)
ax_good.set_ylim(0, 0.6)
ax_good.set_xticks(x)
ax_good.set_xticklabels(sites)
ax_good.set_title("Honest", color=PALETTE[2])
ax_good.set_xlabel("site")
ax_good.set_ylabel("positivity")
for xi, m in zip(x, means):
    ax_good.text(xi, m + 0.03, f"{m:.2f}", ha="center", color=INK, fontsize=9)

fig.suptitle("Same four means, drawn two ways", color=INK)
fig.tight_layout()
print("range shown, truncated axis:", round(means.max() - means.min(), 3))
save(fig, "assets/figures/data-visualization-principles.svg")
