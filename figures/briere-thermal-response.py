# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Briere thermal-response function over its support for several parameter sets."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED
apply_style()

# Briere unimodal thermal trait: f(T) = b*T*(T-T0)*sqrt(Tm-T) for T in [T0, Tm],
# zero outside. T0 is the lower thermal limit, Tm the upper, b a scaling constant.
def briere(T, b, T0, Tm):
    T = np.asarray(T, dtype=float)
    val = b * T * (T - T0) * np.sqrt(np.clip(Tm - T, 0.0, None))
    return np.where((T > T0) & (T < Tm), val, 0.0)

# Three parameter sets that shift the thermal optimum and breadth: a cool-narrow
# set, a moderate set, and a warm-broad set.
params = [
    dict(b=2.0e-4, T0=12.0, Tm=30.0, label=r"$T_0=12,\ T_m=30$ (cool)"),
    dict(b=2.0e-4, T0=15.0, Tm=35.0, label=r"$T_0=15,\ T_m=35$ (moderate)"),
    dict(b=1.4e-4, T0=18.0, Tm=40.0, label=r"$T_0=18,\ T_m=40$ (warm, broad)"),
]

T = np.linspace(5.0, 45.0, 4001)

fig, ax = plt.subplots()
for p, color in zip(params, PALETTE):
    f = briere(T, p["b"], p["T0"], p["Tm"])
    rel = f / f.max()                 # normalize each curve so its peak is 1.0
    T_opt = float(T[np.argmax(f)])    # thermal optimum
    ax.plot(T, rel, color=color, linewidth=2.2, label=p["label"])
    ax.scatter([T_opt], [1.0], color=color, s=24, zorder=5)

ax.set_xlabel("temperature (°C)")
ax.set_ylabel("trait / relative rate")
ax.set_xlim(5, 45)
ax.set_ylim(0, 1.12)
ax.set_title("Briere thermal-response function for several parameter sets")
ax.legend(loc="upper left", fontsize="small")

save(fig, "assets/figures/briere-thermal-response.svg")
