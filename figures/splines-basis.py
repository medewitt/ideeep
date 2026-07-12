# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""How a spline is built from a basis. Left: a cubic B-spline basis over the
range, one bump per basis function, each nonzero only over a few knot spans.
Right: the fitted spline is a weighted sum of those basis functions (faint,
scaled by their fitted coefficients); it follows the data smoothly and the
joins at the interior knots (dashed) are invisible because the pieces are
constrained to match in value and first two derivatives."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(3)

k = 3                                   # cubic
interior = np.array([2.5, 4.5, 6.0, 7.5])
lo, hi = 0.0, 10.0
t = np.r_[[lo] * (k + 1), interior, [hi] * (k + 1)]
n_basis = len(t) - k - 1
xs = np.linspace(lo, hi, 500)

# Design matrix of basis functions evaluated on a grid and at data points
def design(x):
    cols = []
    for i in range(n_basis):
        c = np.zeros(n_basis)
        c[i] = 1.0
        cols.append(BSpline(t, c, k)(x))
    return np.column_stack(cols)

# --- data from a smooth truth ---
def truth(x):
    return np.sin(0.6 * x) + 0.15 * x

xd = np.sort(rng.uniform(lo, hi, 40))
yd = truth(xd) + rng.normal(0, 0.25, xd.size)

B = design(xd)
coef, *_ = np.linalg.lstsq(B, yd, rcond=None)   # least-squares spline fit
Bg = design(xs)
fit = Bg @ coef

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.4, 3.8))

# ---- left: the basis ----
for i in range(n_basis):
    c = np.zeros(n_basis)
    c[i] = 1.0
    axL.plot(xs, BSpline(t, c, k)(xs), color=PALETTE[i % len(PALETTE)], lw=1.6)
for kn in interior:
    axL.axvline(kn, color=MUTED, lw=0.8, ls="--")
axL.set_title("A cubic B-spline basis", fontsize=10)
axL.set_xlabel("x")
axL.set_ylabel("basis function value")
axL.text(0.4, 0.9, "interior knots (dashed)", fontsize=8, color=INK)

# ---- right: fit = weighted sum of basis ----
for i in range(n_basis):
    c = np.zeros(n_basis)
    c[i] = 1.0
    axR.plot(xs, coef[i] * BSpline(t, c, k)(xs),
             color=MUTED, lw=0.8, alpha=0.5)
axR.scatter(xd, yd, s=20, color=INK, zorder=4, label="data")
axR.plot(xs, fit, color=PALETTE[0], lw=2.4, label="fitted spline")
axR.plot(xs, truth(xs), color=PALETTE[1], lw=1.3, ls=":", label="truth")
for kn in interior:
    axR.axvline(kn, color=MUTED, lw=0.8, ls="--")
axR.set_title("Fit = weighted sum of basis functions", fontsize=10)
axR.set_xlabel("x")
axR.set_ylabel("y")
axR.legend(fontsize=8, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/splines-basis.svg")
