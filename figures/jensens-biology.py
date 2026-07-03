# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Jensen's inequality in biology: a fluctuating temperature lowers mean
performance below the performance at the mean temperature."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

Topt, width, Pmax = 28.0, 8.0, 1.0
P = lambda T: Pmax * np.exp(-((T - Topt) / width) ** 2)   # thermal performance curve

T = np.linspace(8, 48, 400)
T1, T2 = 20.0, 36.0                 # two equally likely temperatures, mean = Topt
Tbar = 0.5 * (T1 + T2)
P_at_mean = P(Tbar)                 # performance AT the mean temperature
mean_P = 0.5 * (P(T1) + P(T2))      # MEAN performance across temperatures
gap = P_at_mean - mean_P

print(f"P(mean T)   = {P_at_mean:.3f}   (performance at the average temperature)")
print(f"E[P(T)]     = {mean_P:.3f}   (average performance across temperatures)")
print(f"Jensen gap  = {gap:.3f}   (concave curve -> fluctuation HURTS)")

fig, ax = plt.subplots()
ax.plot(T, P(T), color=PALETTE[0], lw=2.2, label="performance curve $P(T)$")
ax.plot([T1, T2], [P(T1), P(T2)], color=PALETTE[1], lw=1.6, ls="--",
        label="average of the two temperatures")
ax.scatter([T1, T2], [P(T1), P(T2)], color=PALETTE[1], zorder=5)
ax.scatter([Tbar], [P_at_mean], color=PALETTE[0], zorder=5)
ax.scatter([Tbar], [mean_P], color=PALETTE[1], zorder=5)
ax.annotate("", xy=(Tbar, P_at_mean), xytext=(Tbar, mean_P),
            arrowprops=dict(arrowstyle="<->", color="#26323f", lw=1.4))
ax.text(Tbar + 0.8, 0.5 * (P_at_mean + mean_P),
        f"Jensen gap\n= {gap:.2f}", va="center", fontsize=9)
ax.text(Tbar, P_at_mean + 0.03, f"$P(\\bar T) = {P_at_mean:.2f}$",
        ha="center", fontsize=9, color=PALETTE[0])
ax.text(Tbar, mean_P - 0.07, f"$E[P(T)] = {mean_P:.2f}$",
        ha="center", fontsize=9, color=PALETTE[1])
for x in (T1, T2):
    ax.plot([x, x], [0, P(x)], color="#c8d0d6", lw=0.7, zorder=0)
ax.set_ylim(0, 1.12)
ax.set_xlabel("temperature (°C)")
ax.set_ylabel("performance (e.g., growth rate)")
ax.set_title("Fluctuating temperature lowers mean performance (concave curve)")
ax.legend(loc="upper left", fontsize=9)
save(fig, "assets/figures/jensens-biology.svg")
