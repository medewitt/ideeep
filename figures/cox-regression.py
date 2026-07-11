# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""The proportional-hazards assumption. Left: when it holds, one group's hazard
is a fixed multiple of the other's at every time (here HR = 0.66, a 34% lower
rate on the drug), so the two hazard curves never cross. Right: it fails when
an effect is time-varying — a surgery with high early risk but a long-term
benefit has a hazard ratio that starts above 1 and falls below it, so the
curves cross and a single hazard ratio no longer summarizes the effect."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

t = np.linspace(0, 10, 300)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6), sharey=True)

# ---- PH holds: constant multiple -----------------------------------------
h0 = 0.06 * (1 + 0.12 * t)                 # baseline (control), rising
HR = 0.66
axL.plot(t, h0, color=PALETTE[0], lw=2.0, label="placebo (baseline)")
axL.plot(t, HR * h0, color=PALETTE[2], lw=2.0, label="drug (HR = 0.66)")
axL.fill_between(t, HR * h0, h0, color=PALETTE[2] + "18")
axL.text(4.5, 0.045, "constant multiple\n(hazards never cross)", fontsize=8,
         color=INK)
axL.set_xlabel("time $t$")
axL.set_ylabel("hazard $h(t)$")
axL.set_title("Proportional hazards hold", fontsize=10)
axL.legend(fontsize=8.3, loc="upper left")

# ---- PH violated: crossing hazards ---------------------------------------
h_surg = 0.19 * np.exp(-0.45 * t) + 0.02   # high early, decays
h_ctrl = 0.03 + 0.008 * t                   # steady, rising
axR.plot(t, h_ctrl, color=PALETTE[0], lw=2.0, label="medical mgmt")
axR.plot(t, h_surg, color=PALETTE[1], lw=2.0, label="surgery")
# crossing point
cross = np.argmin(np.abs(h_surg - h_ctrl))
axR.scatter([t[cross]], [h_ctrl[cross]], s=40, color=INK, zorder=5)
axR.annotate("HR > 1 early,\nHR < 1 later\n→ curves cross",
             xy=(t[cross], h_ctrl[cross]), xytext=(3.4, 0.12), fontsize=8,
             color=INK, arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axR.set_xlabel("time $t$")
axR.set_title("Proportional hazards violated", fontsize=10)
axR.legend(fontsize=8.3, loc="upper right")

axL.set_ylim(0, 0.21)
fig.tight_layout()
save(fig, "assets/figures/cox-regression.svg")
