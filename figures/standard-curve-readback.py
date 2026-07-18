# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Reading an unknown off a standard curve. A four-parameter logistic curve is fit
to standards of known concentration (points); an unknown sample's optical density
is projected onto the curve (dashed lines) to recover its concentration. Because
the sample was pre-diluted 1:100 to bring it into the assay's dynamic range, the
interpolated value is multiplied back by 100 for the reported concentration."""
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()


def fourpl(x, a, d, c, b):
    return d + (a - d) / (1 + (x / c) ** b)


conc = np.array([0.5, 1.5, 5, 15, 50, 150, 500.0])
od = np.array([0.05, 0.11, 0.30, 0.85, 1.8, 2.6, 3.0])
(a, d, c, b), _ = curve_fit(fourpl, conc, od, p0=[0.03, 3.1, 20, 1.0], maxfev=20000)

od_u = 1.10
df = 100
conc_u = c * ((a - d) / (od_u - d) - 1) ** (1 / b)

fig, ax = plt.subplots(figsize=(6.4, 4.2))
xx = np.logspace(np.log10(0.4), np.log10(600), 300)
ax.plot(xx, fourpl(xx, a, d, c, b), color=PALETTE[0], lw=2.0,
        label="4PL fit", zorder=2)
ax.scatter(conc, od, s=48, color=PALETTE[0], edgecolor="white", linewidth=0.5,
           zorder=3, label="standards")

# project the unknown OD onto the curve
ax.plot([0.4, conc_u], [od_u, od_u], color=PALETTE[1], lw=1.4, ls="--", zorder=4)
ax.plot([conc_u, conc_u], [0, od_u], color=PALETTE[1], lw=1.4, ls="--", zorder=4)
ax.scatter([conc_u], [od_u], s=80, color=PALETTE[1], zorder=5)
ax.annotate(f"OD {od_u} → {conc_u:.1f} units/mL\n×{df} dilution = {conc_u*df:.0f} units/mL",
            xy=(conc_u, od_u), xytext=(conc_u * 1.4, od_u - 0.9), fontsize=8.4,
            color=INK, arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=1.0))

ax.set_xscale("log")
ax.set_xlim(0.4, 600)
ax.set_ylim(0, 3.3)
ax.set_xlabel("concentration (units/mL, log scale)")
ax.set_ylabel("optical density")
ax.set_title(f"ELISA standard curve  (EC50 ≈ {c:.0f})", fontsize=9.6)
ax.legend(fontsize=8.4, loc="upper left")
fig.tight_layout()
save(fig, "assets/figures/standard-curve-readback.svg")
