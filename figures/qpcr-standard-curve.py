# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""A qPCR standard curve: Ct vs log10 template, and the amplification efficiency."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(7)

# A 10-fold dilution series spanning 10^1 .. 10^7 copies
log10_copies = np.arange(1, 8)
slope, intercept = -3.32, 40.0            # slope -3.32 -> ~100% efficiency
ct = intercept + slope * log10_copies + rng.normal(0, 0.15, log10_copies.size)

# Fit
b, a = np.polyfit(log10_copies, ct, 1)
efficiency = 10 ** (-1 / b) - 1

xs = np.linspace(0.5, 7.5, 50)
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.scatter(log10_copies, ct, s=45, color=PALETTE[0], zorder=3, label="standards")
ax.plot(xs, a + b * xs, color=PALETTE[1], lw=1.8,
        label=f"Ct = {a:.1f} − {abs(b):.2f}·log₁₀(copies)")
ax.text(4.4, 34, f"slope = {b:.2f}\nefficiency = {efficiency*100:.0f}%",
        fontsize=9, color=INK,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#d8dee4"))
ax.set_xlabel("log₁₀ template copies")
ax.set_ylabel("quantification cycle (Ct)")
ax.set_title("qPCR standard curve")
ax.legend(loc="upper right", fontsize=8.5)
ax.invert_yaxis()   # higher copies amplify earlier (lower Ct) -> put them on top
save(fig, "assets/figures/qpcr-standard-curve.svg")
