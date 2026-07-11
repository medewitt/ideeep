# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Rapid antigen tests. Left: a rapid test needs a relatively high pathogen load
to cross its detection threshold, so it turns positive only around peak load
near symptom onset and misses the early and late infection that a lower-threshold
PCR still catches. Right: the lateral-flow strip schematic — sample flows past a
conjugate pad, a test line, and a control line, and the two-line / one-line /
no-control readouts mean positive / negative / invalid."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.8),
                               gridspec_kw={"width_ratios": [1.25, 1]})

# ---- viral load with detection thresholds ---------------------------------
t = np.linspace(0, 21, 400)
# log10 viral load: rise, peak ~ day 5, decline
vl = 9.5 * np.exp(-0.5 * ((t - 5.0) / 3.2) ** 2) + 0.2
pcr_thr = 2.5
rat_thr = 6.0

axL.plot(t, vl, color=PALETTE[0], lw=2.0)
axL.axhline(pcr_thr, ls="--", color=PALETTE[2], lw=1.3)
axL.axhline(rat_thr, ls="--", color=PALETTE[1], lw=1.3)
axL.text(21, pcr_thr + 0.15, "PCR threshold", ha="right", fontsize=8,
         color=PALETTE[2])
axL.text(21, rat_thr + 0.15, "rapid-test threshold", ha="right", fontsize=8,
         color=PALETTE[1])

above = vl >= rat_thr
axL.fill_between(t, rat_thr, vl, where=above, color=PALETTE[1] + "33")
# early/late windows where PCR detects but RAT misses
miss = (vl >= pcr_thr) & (vl < rat_thr)
axL.fill_between(t, pcr_thr, vl, where=miss, color=PALETTE[2] + "22")
axL.text(5, 8.2, "rapid test positive", ha="center", fontsize=8.5,
         color=PALETTE[1])
axL.annotate("missed early\n(PCR still detects)", xy=(2.0, 3.3),
             xytext=(0.1, 0.5), fontsize=7.8, color=PALETTE[2],
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axL.annotate("missed late", xy=(9.2, 3.4), xytext=(12.8, 5.6),
             fontsize=7.8, color=PALETTE[2],
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))

axL.set_xlabel("days since infection")
axL.set_ylabel(r"pathogen load ($\log_{10}$)")
axL.set_title("Sensitivity tracks pathogen load", fontsize=10)
axL.set_xlim(0, 21)
axL.set_ylim(0, 11)

# ---- lateral-flow strip schematic -----------------------------------------
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.axis("off")
axR.set_title("Lateral-flow strip", fontsize=10)


def strip(y0, testline, label):
    # strip body
    axR.add_patch(FancyBboxPatch((1.2, y0), 7.2, 1.5,
                  boxstyle="round,pad=0.02", linewidth=1.2,
                  edgecolor=MUTED, facecolor="#f4f6f8"))
    # sample pad
    axR.add_patch(Rectangle((1.2, y0), 1.2, 1.5, color=PALETTE[3] + "55"))
    # control line always present; test line conditional
    axR.add_patch(Rectangle((6.6, y0 + 0.15), 0.32, 1.2, color=PALETTE[0]))
    if testline:
        axR.add_patch(Rectangle((5.0, y0 + 0.15), 0.32, 1.2, color=PALETTE[1]))
    axR.text(8.7, y0 + 0.75, label, fontsize=8.3, va="center", color=INK)


strip(7.2, True, "positive\n(test + control)")
strip(4.3, False, "negative\n(control only)")
# invalid: no control line
axR.add_patch(FancyBboxPatch((1.2, 1.4), 7.2, 1.5, boxstyle="round,pad=0.02",
              linewidth=1.2, edgecolor=MUTED, facecolor="#f4f6f8"))
axR.add_patch(Rectangle((1.2, 1.4), 1.2, 1.5, color=PALETTE[3] + "55"))
axR.text(8.7, 2.15, "invalid\n(no control)", fontsize=8.3, va="center", color=INK)

# zone labels along the top
axR.text(1.8, 9.1, "sample", fontsize=7.5, ha="center", color=MUTED)
axR.text(5.16, 9.1, "test", fontsize=7.5, ha="center", color=PALETTE[1])
axR.text(6.76, 9.1, "control", fontsize=7.5, ha="center", color=PALETTE[0])
axR.plot([5.16, 5.16], [7.2 + 1.5, 8.8], color=PALETTE[1], lw=0.6)
axR.plot([6.76, 6.76], [7.2 + 1.5, 8.8], color=PALETTE[0], lw=0.6)

fig.tight_layout()
save(fig, "assets/figures/rapid-antigen-tests.svg")
