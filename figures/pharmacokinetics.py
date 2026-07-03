# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""One-compartment pharmacokinetics: IV bolus vs first-order oral absorption."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)

D = 100.0
Vd = 20.0
k = 0.2
F = 1.0
ka = 1.0

t = np.linspace(0, 24, 500)

# IV bolus
C_iv = (D / Vd) * np.exp(-k * t)

# Oral, first-order absorption
C_oral = (F * D * ka) / (Vd * (ka - k)) * (np.exp(-k * t) - np.exp(-ka * t))

# analytic Tmax / Cmax for oral
Tmax = np.log(ka / k) / (ka - k)
Cmax = (F * D * ka) / (Vd * (ka - k)) * (np.exp(-k * Tmax) - np.exp(-ka * Tmax))

fig, ax = plt.subplots()

ax.plot(t, C_iv, color=PALETTE[0], lw=2.5, label="IV bolus")
ax.plot(t, C_oral, color=PALETTE[1], lw=2.5, label="Oral (first-order abs.)")

ax.plot([Tmax], [Cmax], "o", color=PALETTE[1])
ax.annotate(
    f"Cmax = {Cmax:.2f}\nTmax = {Tmax:.2f} h",
    xy=(Tmax, Cmax),
    xytext=(Tmax + 3, Cmax + 0.5),
    arrowprops=dict(arrowstyle="->", color="0.4"),
    color="0.3",
)

ax.set_xlabel("time (h)")
ax.set_ylabel("concentration")
ax.set_title("One-compartment pharmacokinetics")
ax.legend()

save(fig, "assets/figures/pharmacokinetics.svg")
