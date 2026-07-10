# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Within-host kinetics, assay limit of detection, and detection probability."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# ---- Within-host viral-load trajectory in log10 copies/mL.
# Rises from ~day 1, peaks near day 5-6 at ~1e8, back to baseline by ~day 18.
days = np.linspace(0, 20, 400)


def log_vl(d):
    """Smooth rise-and-fall log10 viral load; baseline ~1 log10."""
    peak_day, peak_val, base = 5.5, 8.0, 1.0
    rise = np.exp(-0.5 * ((d - peak_day) / 2.0) ** 2)          # up-slope
    fall = np.exp(-0.5 * ((d - peak_day) / 4.5) ** 2)          # slower decay
    shape = np.where(d <= peak_day, rise, fall)
    return base + (peak_val - base) * shape


logvl = log_vl(days)
logvl_noisy = logvl + rng.normal(0, 0.12, days.size)

lod_pcr = np.log10(1e3)         # sensitive PCR assay
lod_ag = np.log10(1e5)          # less sensitive antigen assay

fig, (axl, axr) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# ---- Left: trajectory with two LoD lines and detectable windows.
axl.plot(days, logvl_noisy, color=INK, lw=1.6, zorder=4)
axl.axhline(lod_pcr, color=PALETTE[0], ls="--", lw=1.3,
            label="PCR LoD ($10^3$)")
axl.axhline(lod_ag, color=PALETTE[1], ls="--", lw=1.3,
            label="antigen LoD ($10^5$)")

above_pcr = days[logvl >= lod_pcr]
above_ag = days[logvl >= lod_ag]
axl.axvspan(above_pcr.min(), above_pcr.max(), color=PALETTE[0], alpha=0.08)
axl.axvspan(above_ag.min(), above_ag.max(), color=PALETTE[1], alpha=0.12)

axl.annotate("detectable window",
             xy=((above_pcr.min() + above_pcr.max()) / 2, 8.6),
             xytext=(10.5, 6.5), fontsize=7.5, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axl.set_xlabel("days since infection")
axl.set_ylabel("viral load (log10 copies/mL)")
axl.set_xlim(0, 20)
axl.set_ylim(0, 9)
axl.set_title("within-host kinetics vs LoD", fontsize=10)
axl.legend(loc="upper right", fontsize=8)

# ---- Right: probability of detection vs day for the two assays.
slope = 2.2                     # logistic steepness in log10 units


def p_detect(lod):
    return 1.0 / (1.0 + np.exp(-slope * (logvl - lod)))


axr.plot(days, p_detect(lod_pcr), color=PALETTE[0], lw=2,
         label="PCR (low LoD)")
axr.plot(days, p_detect(lod_ag), color=PALETTE[1], lw=2,
         label="antigen (high LoD)")
axr.set_xlabel("days since infection")
axr.set_ylabel("probability of detection")
axr.set_xlim(0, 20)
axr.set_ylim(0, 1.05)
axr.set_title("detection probability", fontsize=10)
axr.annotate("lower LoD detects\nearlier and longer",
             xy=(3.0, p_detect(lod_pcr)[np.argmin(np.abs(days - 3.0))]),
             xytext=(8.5, 0.35), fontsize=7.5, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axr.legend(loc="upper right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/detection-probability.svg")
