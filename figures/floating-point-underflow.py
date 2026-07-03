# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Why a likelihood becomes exactly zero: multiplying many probabilities
underflows the smallest number a computer can hold (~1e-308 in float64), so
the product snaps to 0 and log(0) = -inf breaks everything downstream. Adding
the *logarithms* instead keeps the value finite forever.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

p = 0.01                                  # a per-observation probability
N = np.arange(1, 260)

# exact order of magnitude (log10) of the product p^N -- always finite
true_log10 = N * np.log10(p)

# what float64 actually computes for the product p**N
computed = p ** N.astype(float)
computed_log10 = np.where(computed > 0.0, np.log10(computed), np.nan)

# the underflow cliff: smallest positive float64 is ~1e-308
underflow_N = 308 / abs(np.log10(p))

fig, ax = plt.subplots()

ax.axhspan(-308, -520, color="#e9c9c2", alpha=0.35, zorder=0)
ax.text(8, -337, "below here float64 rounds to exactly 0",
        color="#8a3b2a", fontsize=8.5, style="italic")

# multiply (orange, thick) coincides with the log line until it underflows
ax.plot(N, computed_log10, color=PALETTE[1], lw=3.0,
        label="multiply the probabilities  (float64)")
# add-the-logs (green, dashed) sits on top and continues forever
ax.plot(N, true_log10, color=PALETTE[2], lw=1.7, dashes=(4, 3),
        label="add the log-probabilities  (stays finite)")

ax.axhline(-308, color="#8a3b2a", lw=1.0, alpha=0.7)
ax.plot([underflow_N], [-308], "o", color="#b0332f", ms=9, zorder=6,
        clip_on=False)
ax.annotate("product underflows to 0\n→ log(0) = −∞\n→ your MCMC crashes",
            xy=(underflow_N, -308), xytext=(172, -150),
            color="#b0332f", fontsize=9.5, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color="#b0332f", lw=1.4))

ax.set_ylim(-520, 20)
ax.set_xlim(0, 260)
ax.set_xlabel("number of probabilities multiplied  (sites · reads · observations)")
ax.set_ylabel("order of magnitude  (log₁₀ of the value)")
ax.set_title("Work in log space, or your likelihood hits zero")
ax.legend(loc="lower left", fontsize="small")

save(fig, "assets/figures/floating-point-underflow.svg")
