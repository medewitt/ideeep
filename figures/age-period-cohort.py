# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""The age-period-cohort identification problem. Left: a Lexis diagram — each
cell belongs to one age band and one calendar period, and the diagonals are
birth cohorts (cohort = period - age), so every observation carries all three
clocks at once. Right: because the three linear trends are exactly collinear,
the linear split is unidentified — two different age slopes (tilted by a
constant, with the offset absorbed by period and cohort) give exactly the same
fitted values; only the curvature is estimable."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- Lexis diagram --------------------------------------------------------
periods = np.arange(2000, 2026, 5)
ages = np.arange(20, 71, 10)
for p in periods:
    axL.axvline(p, color="#d8dee4", lw=0.7)
for a in ages:
    axL.axhline(a, color="#d8dee4", lw=0.7)
# cohort diagonals: age = period - cohort
for cohort in range(1940, 2006, 10):
    xs = np.array([2000, 2025])
    ys = xs - cohort
    axL.plot(xs, ys, color=PALETTE[2], lw=1.0, alpha=0.7)
# highlight one cohort
c0 = 1970
axL.plot([2000, 2025], [2000 - c0, 2025 - c0], color=PALETTE[1], lw=2.2)
axL.text(2020.5, 2020.5 - c0 + 1.5, f"born {c0}", color=PALETTE[1], fontsize=8,
         rotation=32)
axL.text(2001.5, 44, "cohort = period − age", color=PALETTE[2], fontsize=8.2,
         rotation=32)
axL.set_xlabel("calendar period")
axL.set_ylabel("age")
axL.set_title("A Lexis diagram: three clocks, one cell", fontsize=9.3)
axL.set_xlim(2000, 2025)
axL.set_ylim(20, 70)
axL.grid(False)

# ---- same fit, different linear split -------------------------------------
age = np.arange(0, 11)
curvature = 0.35 * np.sin(age / 10 * np.pi)      # the estimable shape
for delta, col, lab in [(0.0, PALETTE[0], "one valid split"),
                        (0.12, PALETTE[1], "another valid split")]:
    axR.plot(age, curvature + delta * (age - 5), color=col, lw=2.0, marker="o",
             ms=3, label=lab)
axR.annotate("same curvature,\ndifferent tilt\n→ identical fit", xy=(5, 0.33),
             xytext=(5.5, -0.45), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axR.set_xlabel("age band")
axR.set_ylabel("estimated age effect")
axR.set_title("The linear tilt is unidentified", fontsize=9.3)
axR.legend(fontsize=8, loc="lower right")

fig.tight_layout()
save(fig, "assets/figures/age-period-cohort.svg")
