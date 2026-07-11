# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Why LAMP needs no thermocycler. qPCR must ratchet the tube between a hot
denaturation step (~95 C) and a cooler anneal/extend step (~60 C) once per
cycle, a sawtooth that requires a programmable thermal cycler. LAMP holds a
single constant temperature (~63 C) throughout, so a heat block — or body heat —
suffices, and a positive can appear in 15-30 minutes."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, ax = plt.subplots(figsize=(6.8, 3.8))

# ---- qPCR sawtooth --------------------------------------------------------
cycle = 2.0          # minutes per cycle (schematic)
hi, lo = 95.0, 60.0
t_q, T_q = [0.0], [25.0]                 # start near room temp
t = 0.0
for _ in range(12):
    t_q += [t + 0.15, t + 0.6, t + 0.75, t + cycle]
    T_q += [hi, hi, lo, lo]
    t += cycle
ax.plot(t_q, T_q, color=PALETTE[1], lw=1.8, label="qPCR — thermal cycling")

# ---- LAMP flat line -------------------------------------------------------
t_l = np.array([0, 0.6, 30])
T_l = np.array([25, 63, 63])
ax.plot(t_l, T_l, color=PALETTE[0], lw=2.2, label="LAMP — isothermal (~63 °C)")

ax.axhspan(60, 63, color=PALETTE[0] + "12", zorder=0)
ax.annotate("denaturation ~95 °C (needs a thermocycler)",
            xy=(2.6, 95), xytext=(4.4, 102), fontsize=8.5, color=PALETTE[1],
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
ax.annotate("one constant temperature —\nheat block or body heat;\npositive in 15–30 min",
            xy=(18, 63), xytext=(7.5, 34), fontsize=8.5, color=PALETTE[0],
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

ax.set_xlabel("time (min, schematic)")
ax.set_ylabel("reaction temperature (°C)")
ax.set_title("Isothermal amplification needs no thermal cycling", fontsize=11)
ax.set_xlim(0, 24)
ax.set_ylim(20, 108)
ax.legend(fontsize=8.7, loc="lower right")

fig.tight_layout()
save(fig, "assets/figures/lamp.svg")
