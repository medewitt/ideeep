# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Spatial synchrony and the Moran effect.

Left: two coupled phase oscillators, whose phase difference drifts at weak
coupling but locks to a constant once coupling exceeds the detuning. Center:
between-patch synchrony rising with the correlation of environmental noise
(the Moran effect), with dispersal adding a baseline. Right: a schematic
traveling-wave phase map, with epidemic phase lagging with distance from a
large core city.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()

fig, (axA, axB, axC) = plt.subplots(1, 3, figsize=(13.5, 4.2))

# ---- A: two coupled oscillators locking into phase ----
domega = 0.6                              # frequency detuning
t = np.linspace(0, 60, 600)
for K, col in zip([0.15, 0.30, 0.60], PALETTE[:3]):
    # phase difference psi obeys psi' = domega - 2 K sin(psi)
    sol = solve_ivp(lambda tt, y: domega - 2 * K * np.sin(y),
                    (0, 60), [0.1], t_eval=t, rtol=1e-9)
    locks = 2 * K > domega
    axA.plot(t, sol.y[0], color=col, lw=2,
             label=f"$K={K}$ ({'locked' if locks else 'drifting'})")
axA.set_xlabel("time")
axA.set_ylabel(r"phase difference $\psi$")
axA.set_title("Phase locking vs coupling")
axA.legend(loc="upper left", fontsize=8.5)

# ---- B: synchrony vs environmental-noise correlation (Moran effect) ----
rho = np.linspace(0, 1, 200)
axB.plot(rho, rho, color=PALETTE[0], lw=2, label="no dispersal (Moran)")
w = 0.3                                   # dispersal baseline synchrony
axB.plot(rho, w + (1 - w) * rho, color=PALETTE[1], lw=2,
         label="with dispersal")
axB.plot([0, 1], [0, 1], color=MUTED, ls=":", lw=1.0)
axB.set_xlabel(r"environmental noise correlation $\rho$")
axB.set_ylabel("between-patch synchrony")
axB.set_title("The Moran effect")
axB.legend(loc="upper left", fontsize=8.5)

# ---- C: traveling-wave phase map seeded from a large city ----
gx, gy = np.meshgrid(np.linspace(0, 10, 200), np.linspace(0, 10, 200))
core = (2.0, 8.0)                          # large source city
speed = 1.6                                # wave speed (distance / week)
phase = np.hypot(gx - core[0], gy - core[1]) / speed   # weeks of lag
im = axC.imshow(phase, origin="lower", aspect="auto", cmap="viridis",
                extent=(0, 10, 0, 10))
axC.plot(*core, "*", color="white", ms=16, mec=PALETTE[1], mew=1.2)
axC.annotate("large city\n(source)", core, color="white", fontsize=8.5,
             ha="center", va="bottom", xytext=(core[0], core[1] + 0.5))
fig.colorbar(im, ax=axC, label="phase lag (weeks)", fraction=0.046, pad=0.04)
axC.set_xlabel("distance (x)")
axC.set_ylabel("distance (y)")
axC.set_title("Travelling wave")

fig.suptitle("Spatial synchrony: the Moran effect and travelling waves",
             fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "assets/figures/spatial-synchrony.svg")
