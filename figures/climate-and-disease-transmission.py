# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Briere thermal-performance curve: transmission peaks at an intermediate temperature."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED
apply_style()

# Briere unimodal thermal trait: f(T) = b*T*(T-T0)*sqrt(Tm-T) for T in [T0, Tm],
# zero outside. Lower thermal limit T0, upper thermal limit Tm.
T0 = 15.0   # lower thermal limit (C)
Tm = 35.0   # upper thermal limit (C)
b = 2.0e-4  # scaling constant

def briere(T):
    T = np.asarray(T, dtype=float)
    val = b * T * (T - T0) * np.sqrt(np.clip(Tm - T, 0.0, None))
    return np.where((T > T0) & (T < Tm), val, 0.0)

T = np.linspace(10.0, 40.0, 3001)
f = briere(T)
peak = f.max()
rel = f / peak                       # normalize so the peak is 1.0
T_opt = float(T[np.argmax(f)])       # thermal optimum

fig, ax = plt.subplots()

# Curve and light shading beneath it.
ax.fill_between(T, rel, color=PALETTE[0], alpha=0.12, zorder=1)
ax.plot(T, rel, color=PALETTE[0], linewidth=2.2, zorder=3,
        label="relative transmission")

# Thermal optimum.
ax.axvline(T_opt, color=MUTED, linewidth=1.2, linestyle="--", zorder=2)
ax.annotate(fr"optimum $\approx$ {T_opt:.0f} $^\circ$C",
            xy=(T_opt, 1.0), xytext=(T_opt + 1.5, 0.92),
            color=INK, fontsize="small",
            arrowprops=dict(arrowstyle="->", color=MUTED))

# Representative temperatures: highest in the middle, low at both extremes.
reps = [18.0, 25.0, 30.0, 35.0]
rvals = briere(reps) / peak
ax.scatter(reps, rvals, color=PALETTE[1], s=32, zorder=5)
for Tr, yr in zip(reps, rvals):
    ax.annotate(f"{Tr:.0f}$^\\circ$C\n{yr:.2f}",
                xy=(Tr, yr), xytext=(0, 8), textcoords="offset points",
                ha="center", va="bottom", color=MUTED, fontsize="x-small")

ax.set_xlabel("temperature (°C)")
ax.set_ylabel("relative transmission")
ax.set_xlim(10, 40)
ax.set_ylim(0, 1.12)
ax.set_title("Thermal performance curve for transmission")
ax.legend(loc="upper left", fontsize="small")

save(fig, "assets/figures/climate-and-disease-transmission.svg")
