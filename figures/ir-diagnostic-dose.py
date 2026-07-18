# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""The WHO diagnostic-dose classification. Mosquitoes are exposed to a single
discriminating concentration and 24-hour mortality is scored. Mortality of 98% or
more means susceptible; 90-98% is possible resistance to confirm; below 90% is
confirmed resistance. The worked assay (82% mortality, 95% CI 73-89%) falls
clearly in the confirmed-resistance band."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()

dead, N = 82, 100
mort = dead / N * 100
ci = stats.binomtest(dead, N).proportion_ci(0.95)
lo, hi = ci.low * 100, ci.high * 100

fig, ax = plt.subplots(figsize=(6.6, 3.0))
# threshold bands
ax.axvspan(98, 100, color=PALETTE[2], alpha=0.20)
ax.axvspan(90, 98, color=PALETTE[4], alpha=0.20)
ax.axvspan(60, 90, color=PALETTE[1], alpha=0.18)
ax.text(99, 1.35, "susceptible\n≥98%", ha="center", fontsize=7.8, color=INK)
ax.text(94, 1.35, "possible\n90–98%", ha="center", fontsize=7.8, color=INK)
ax.text(78, 1.35, "confirmed resistance  <90%", ha="center", fontsize=8.2,
        color=INK)

# the measured assay
ax.errorbar([mort], [0.7], xerr=[[mort - lo], [hi - mort]], fmt="o",
            color=INK, ms=10, capsize=4, lw=1.8, zorder=5)
ax.annotate(f"{mort:.0f}% mortality\n(95% CI {lo:.0f}–{hi:.0f}%)", xy=(mort, 0.7),
            xytext=(mort, 0.18), fontsize=8.6, color=INK, ha="center")

ax.axvline(98, color=INK, lw=0.8, ls=":")
ax.axvline(90, color=INK, lw=0.8, ls=":")
ax.set_xlim(60, 100.5)
ax.set_ylim(0, 1.7)
ax.set_yticks([])
ax.set_xlabel("24-hour mortality at the diagnostic dose (%)")
ax.set_title("WHO diagnostic-dose resistance classification", fontsize=9.8)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/ir-diagnostic-dose.svg")
