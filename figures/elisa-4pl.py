# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""An ELISA calibration curve fit with the four-parameter logistic (4PL) model."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(11)

def fourpl(x, a, d, c, b):
    # a = bottom (blank OD), d = top (saturation), c = EC50, b = Hill slope
    return d + (a - d) / (1 + (x / c) ** b)

a, d, c, b = 0.05, 3.2, 30.0, 1.3
conc = np.array([1, 3, 10, 30, 100, 300, 1000.0])       # ng/mL, log-spaced
od = fourpl(conc, a, d, c, b) + rng.normal(0, 0.05, conc.size)

xs = np.logspace(0, 3, 200)
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.scatter(conc, od, s=45, color=PALETTE[0], zorder=3, label="calibrators")
ax.plot(xs, fourpl(xs, a, d, c, b), color=PALETTE[1], lw=1.8, label="4PL fit")
ax.axvline(c, color=MUTED, lw=0.9, ls=":")
ax.text(c * 1.1, 0.4, f"EC₅₀ = {c:.0f} ng/mL", fontsize=9, color=MUTED)
ax.axhline(a, color="#c9d3db", lw=0.8, ls="--")
ax.axhline(d, color="#c9d3db", lw=0.8, ls="--")
ax.set_xscale("log")
ax.set_xlabel("analyte concentration (ng/mL, log scale)")
ax.set_ylabel("optical density (OD)")
ax.set_title("ELISA standard curve (four-parameter logistic)")
ax.legend(loc="upper left", fontsize=8.5)
save(fig, "assets/figures/elisa-4pl.svg")
