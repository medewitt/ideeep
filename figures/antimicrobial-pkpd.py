# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""The three PK/PD indices read off one concentration-time curve, and how dosing
shape trades between them. Left: the worked IV-bolus profile C(t) = 40 e^{-0.35 t}
against MIC = 2, showing the peak (Cmax/MIC), the exposure (shaded AUC/MIC), and
the time the free concentration stays above the MIC (%T>MIC = 100% here). Right:
the same total daily dose delivered as a short bolus, an extended infusion, or a
continuous infusion keeps concentration over the MIC for very different fractions
of the interval."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

C0, k, tau, MIC = 40.0, 0.35, 8.0, 2.0

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.7))

# ---- one interval: the three indices --------------------------------------
t = np.linspace(0, tau, 400)
C = C0 * np.exp(-k * t)

axL.plot(t, C, color=PALETTE[0], lw=2.0)
axL.axhline(MIC, ls="--", color=PALETTE[1], lw=1.3)
axL.fill_between(t, MIC, C, where=C > MIC, color=PALETTE[0] + "26",
                 label="AUC above MIC")
axL.text(tau, MIC + 0.7, "MIC = 2", ha="right", fontsize=8.5, color=PALETTE[1])

axL.scatter([0], [C0], s=40, color=PALETTE[0], zorder=5)
axL.annotate(r"$C_{max}/MIC = 20$", xy=(0, C0), xytext=(1.4, 34),
             fontsize=8.5, color=INK)
axL.annotate("free drug stays above MIC\nfor the whole interval:\n%T>MIC = 100%",
             xy=(5.5, C0 * np.exp(-k * 5.5)), xytext=(2.8, 12),
             fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axL.set_xlabel("time since dose (h)")
axL.set_ylabel("free concentration (mg/L)")
axL.set_title("Three indices on one curve", fontsize=10)
axL.set_xlim(0, tau)
axL.set_ylim(0, 42)
axL.legend(fontsize=8.3, loc="upper right")

# ---- dosing shape and time above MIC --------------------------------------
tt = np.linspace(0, tau, 500)
# short bolus (as above)
bolus = C0 * np.exp(-k * tt)
# extended 3-h infusion: lower peak, same total dose (approx by rise then decay)
ext_peak, T_inf = 18.0, 3.0
extended = np.where(tt <= T_inf,
                    ext_peak * (1 - np.exp(-k * tt)) / (1 - np.exp(-k * T_inf)),
                    ext_peak * np.exp(-k * (tt - T_inf)))
# continuous infusion: flat steady level above MIC
cont = np.full_like(tt, 6.0)

for y, col, lab in [(bolus, PALETTE[3], "short bolus (tall peak)"),
                    (extended, PALETTE[2], "extended infusion"),
                    (cont, PALETTE[0], "continuous infusion")]:
    axR.plot(tt, y, color=col, lw=1.9, label=lab)

axR.axhline(MIC, ls="--", color=PALETTE[1], lw=1.3)
axR.text(tau, MIC + 0.6, "MIC", ha="right", fontsize=8.5, color=PALETTE[1])
axR.set_xlabel("time (h)")
axR.set_ylabel("free concentration (mg/L)")
axR.set_title("Dosing shape reshapes the profile", fontsize=10)
axR.set_xlim(0, tau)
axR.set_ylim(0, 42)
axR.legend(fontsize=8, loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/antimicrobial-pkpd.svg")
