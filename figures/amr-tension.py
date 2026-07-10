# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""The individual-versus-population tension in antimicrobial use.

Left: at the scale of one patient, expected benefit rises monotonically with
drug exposure, so the privately optimal choice is to treat hard. Right: at the
population scale, aggregate use erodes the shared resource (drug efficacy) as
resistance spreads, so net population benefit peaks at a moderate use rate. The
two optima diverge -- a tragedy of the commons.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# --- Left: the individual scale ------------------------------------------
# Probability of clinical cure rises and saturates with drug exposure.
dose = np.linspace(0, 1, 200)
cure = 1.0 / (1.0 + np.exp(-9 * (dose - 0.4)))          # sigmoid benefit
# Individual optimum: keep pushing exposure, benefit only rises.
axL.plot(dose, cure, color=PALETTE[0], lw=2.2, label="P(cure) for this patient")
axL.axvline(0.9, color=MUTED, lw=1.0, ls="--")
axL.annotate("private optimum:\ntreat hard", xy=(0.9, 0.55), xytext=(0.44, 0.30),
             fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
axL.set_xlabel("drug exposure for one patient")
axL.set_ylabel("expected benefit")
axL.set_title("individual scale")
axL.set_xlim(0, 1)
axL.set_ylim(-0.02, 1.05)
axL.legend(loc="lower right", fontsize=8)

# --- Right: the population scale (the commons) ---------------------------
use = np.linspace(0, 1, 200)
# Direct benefit of treating a larger share of infections (saturating).
benefit = 1.0 - np.exp(-3.0 * use)
# Resistance prevalence climbs with aggregate use and erodes efficacy;
# the realized population benefit is benefit discounted by lost efficacy.
resistance = 1.0 / (1.0 + np.exp(-10 * (use - 0.55)))    # S-curve prevalence
net = benefit * (1.0 - 0.9 * resistance)                 # efficacy discount
i_soc = int(np.argmax(net))

axR.plot(use, net, color=PALETTE[2], lw=2.2, label="net population benefit")
axR.plot(use, resistance, color=PALETTE[1], lw=1.8, ls="--",
         label="resistance prevalence")
axR.axvline(use[i_soc], color=MUTED, lw=1.0, ls=":")
axR.axvline(0.9, color=MUTED, lw=1.0, ls="--")
axR.annotate("social\noptimum", xy=(use[i_soc], net[i_soc]),
             xytext=(use[i_soc] - 0.02, 0.22), fontsize=8.5, color=INK,
             ha="right", arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
axR.annotate("private\noptimum", xy=(0.9, 0.12), xytext=(0.62, 0.05),
             fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
axR.set_xlabel("share of infections treated (community)")
axR.set_ylabel("population outcome")
axR.set_title("population scale")
axR.set_xlim(0, 1)
axR.set_ylim(-0.02, 1.05)
axR.legend(loc="upper left", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/amr-tension.svg")
