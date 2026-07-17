# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Hierarchical calibration across ELISA plates. Left: standards from four plates
with their independent four-parameter-logistic fits; plate 4 has only three
standards and cannot be fit on its own. Right: the recovered concentration of each
plate's unknown (true value 40). Independent fitting recovers plates 1-3 but fails
for plate 4; the hierarchical model recovers all four, rescuing plate 4 by
borrowing the shared curve shape, with an appropriately wider interval."""
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()


def fourpl(x, a, d, c, b):
    return d + (a - d) / (1 + (x / c) ** b)


# reproduce the page's simulated plates (same rng sequence)
rng = np.random.default_rng(0)
a_t, d_pop, c_t, b_t, noise = 0.03, 3.1, 30.0, 1.10, 0.05
tops = d_pop * np.array([1.00, 0.85, 1.15, 0.92])
full = np.array([0.5, 1.5, 5, 15, 50, 150, 500.0])
standards = {0: full, 1: full, 2: full, 3: np.array([5, 50, 500.0])}
data = {}
for p in range(4):
    ys = [fourpl(x, a_t, tops[p], c_t, b_t) + rng.normal(0, noise)
          for x in standards[p]]
    rng.normal(0, noise)                       # consume the unknown draw (page parity)
    data[p] = (standards[p], np.array(ys))

# recovered-unknown results committed by the page's executed NumPyro block
indep = [43.5, 41.4, 39.1, np.nan]             # plate 4 cannot be fit
hier_mean = [41.7, 40.4, 40.5, 38.5]
hier_lo = [37.2, 35.3, 36.4, 33.9]
hier_hi = [46.8, 46.5, 44.8, 44.0]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.0, 4.0))

# ---- panel A: per-plate standards and independent fits --------------------
xx = np.logspace(np.log10(0.4), np.log10(600), 200)
for p in range(4):
    xs, ys = data[p]
    col = PALETTE[p]
    axL.scatter(xs, ys, s=34, color=col, edgecolor="white", linewidth=0.4,
                zorder=3, label=f"plate {p+1}" + (" (3 std)" if p == 3 else ""))
    if p < 3:
        (a, d, c, b), _ = curve_fit(fourpl, xs, ys, p0=[0.03, 3.1, 30, 1.0],
                                    maxfev=20000)
        axL.plot(xx, fourpl(xx, a, d, c, b), color=col, lw=1.5, zorder=2)
axL.annotate("plate 4: 3 standards,\ncannot fit 4 parameters alone",
             xy=(50, fourpl(50, a_t, tops[3], c_t, b_t)), xytext=(1.0, 2.4),
             fontsize=8.0, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axL.set_xscale("log")
axL.set_xlim(0.4, 600)
axL.set_ylim(0, 3.6)
axL.set_xlabel("concentration (units/mL, log scale)")
axL.set_ylabel("optical density")
axL.set_title("Standards drift plate to plate", fontsize=9.6)
axL.legend(fontsize=7.6, loc="upper left", ncol=1)

# ---- panel B: recovered unknown, independent vs hierarchical ---------------
axR.axvline(40, color=MUTED, lw=1.1, ls=":")
axR.text(40, 4.55, "true = 40", ha="center", fontsize=8, color=MUTED)
for p in range(4):
    y = 4 - p
    axR.errorbar(hier_mean[p], y + 0.13, xerr=[[hier_mean[p] - hier_lo[p]],
                 [hier_hi[p] - hier_mean[p]]], fmt="o", color=PALETTE[0], ms=7,
                 capsize=3, lw=1.6, zorder=4,
                 label="hierarchical" if p == 0 else None)
    if np.isnan(indep[p]):
        axR.scatter([52], [y - 0.13], marker="x", s=60, color=PALETTE[1],
                    zorder=4)
        axR.text(50.6, y - 0.13, "independent fails", color=PALETTE[1],
                 fontsize=8.0, va="center", ha="right")
    else:
        axR.scatter([indep[p]], [y - 0.13], marker="s", s=42, color=PALETTE[1],
                    zorder=4, label="independent" if p == 0 else None)
    axR.text(30.5, y, f"plate {p+1}", ha="right", va="center", fontsize=8.4,
             color=INK)
axR.set_yticks([])
axR.set_ylim(0.3, 4.9)
axR.set_xlim(30, 56)
axR.set_xlabel("recovered unknown concentration (units/mL)")
axR.set_title("Hierarchical model rescues the sparse plate", fontsize=9.6)
axR.legend(fontsize=8.2, loc="upper right")
axR.grid(axis="y", visible=False)

fig.tight_layout()
save(fig, "assets/figures/hierarchical-plates.svg")
