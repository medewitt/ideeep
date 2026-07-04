# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""One Health surveillance: integrated streams and a leading signal.

Left: three surveillance streams (human, animal, environmental) feed one
integrated signal. Right: an environmental (wastewater) stream rises
before the human case curve, and the lead time is the cross-correlation
peak lag.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axl, axr) = plt.subplots(
    1, 2, figsize=(8.6, 3.9), gridspec_kw={"width_ratios": [0.95, 1.15]}
)

# ---- Left panel: three streams -> integrated signal ----
axl.set_xlim(0, 10)
axl.set_ylim(0, 10)
axl.axis("off")
axl.set_title("Integrated streams", fontsize=11)


def box(ax, xy, w, h, color, label):
    x, y = xy
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.12,rounding_size=0.22",
        linewidth=1.6, edgecolor=color, facecolor=color + "22"))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=9, color=INK)


streams = [
    ((0.4, 7.3), PALETTE[1], "Human\ncases"),
    ((0.4, 4.1), PALETTE[2], "Animal\nsentinels"),
    ((0.4, 0.9), PALETTE[0], "Environment\n(wastewater)"),
]
for xy, color, label in streams:
    box(axl, xy, 3.4, 1.9, color, label)

box(axl, (6.2, 4.1), 3.2, 1.9, PALETTE[3], "Integrated\nearly warning")

for (xy, color, _), y_mid in zip(streams, (8.25, 5.05, 1.85)):
    axl.add_patch(FancyArrowPatch(
        (3.8, y_mid), (6.2, 5.05), arrowstyle="-|>", mutation_scale=12,
        linewidth=1.5, color=color, connectionstyle="arc3,rad=0.12"))

# ---- Right panel: leading environmental signal ----
t = np.arange(0, 120)
lead = 10          # true environmental lead in days


def wave(peak, amp):
    return amp * np.exp(-0.5 * ((t - peak) / 14.0) ** 2)


env = wave(45, 1.0)
human = wave(45 + lead, 1.0)

axr.plot(t, env, color=PALETTE[0], lw=2.2, label="environmental")
axr.plot(t, human, color=PALETTE[1], lw=2.2, label="human cases")

pe, ph = t[np.argmax(env)], t[np.argmax(human)]
axr.annotate("", xy=(ph, 1.02), xytext=(pe, 1.02),
             arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
axr.text((pe + ph) / 2, 1.08, f"lead {ph - pe} d", ha="center",
         va="bottom", fontsize=9, color=INK)
axr.set_xlabel("time (days)")
axr.set_ylabel("scaled signal")
axr.set_title("A signal that leads the human curve", fontsize=11)
axr.set_ylim(0, 1.25)
axr.legend(loc="upper right", fontsize=9)

save(fig, "assets/figures/one-health-surveillance.svg")
