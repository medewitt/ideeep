# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Two knobs that control a spline. Left: the smoothing penalty. The same
penalized spline fit three ways -- too little penalty chases the noise
(wiggly, high variance), too much penalty flattens toward a straight line
(over-smoothed, high bias), and an intermediate amount (chosen here by
generalized cross-validation) tracks the signal. Right: why Harrell's
restricted cubic spline tames the tails. An unrestricted cubic spline is free
to curve wildly beyond the outermost knots where data are sparse; the
restricted (natural) spline forces the fit to be linear past the boundary
knots, so extrapolation stays sane."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline, BSpline
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(7)

# ------------------------------------------------------------------ left
def truth(x):
    return np.sin(1.1 * x)

xd = np.sort(rng.uniform(0, 8, 60))
yd = truth(xd) + rng.normal(0, 0.35, xd.size)
xg = np.linspace(0, 8, 400)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.9))

axL.scatter(xd, yd, s=16, color=INK, alpha=0.55, zorder=2, label="data")
for s, col, name in [(1.0, PALETTE[1], "small penalty (under-smoothed)"),
                     (7.0, PALETTE[2], "GCV-chosen penalty"),
                     (60.0, PALETTE[3], "large penalty (over-smoothed)")]:
    sp = UnivariateSpline(xd, yd, s=s)
    axL.plot(xg, sp(xg), color=col, lw=2.0, label=name)
axL.plot(xg, truth(xg), color=MUTED, lw=1.2, ls=":", label="truth")
axL.set_title("The smoothing penalty", fontsize=10)
axL.set_xlabel("x")
axL.set_ylabel("y")
axL.legend(fontsize=7.6, loc="upper right")

# ------------------------------------------------------------------ right
# Harrell restricted cubic spline basis (RMS): linear beyond outer knots.
def rcs_basis(x, knots):
    x = np.asarray(x, float)
    kn = np.asarray(knots, float)
    K = len(kn)
    tk1, tkK = kn[-2], kn[-1]
    denom = tkK - tk1
    cols = [x]
    cube = lambda u: np.where(u > 0, u, 0.0) ** 3
    for j in range(K - 2):
        term = (cube(x - kn[j])
                - cube(x - tk1) * (tkK - kn[j]) / denom
                + cube(x - tkK) * (tk1 - kn[j]) / denom)
        cols.append(term / denom ** 2)
    return np.column_stack(cols)

# unrestricted cubic spline with the same interior knots, cubic beyond them
def cubic_spline_design(x, interior, lo, hi, k=3):
    t = np.r_[[lo] * (k + 1), interior, [hi] * (k + 1)]
    n = len(t) - k - 1
    cols = []
    for i in range(n):
        c = np.zeros(n)
        c[i] = 1.0
        cols.append(BSpline(t, c, k, extrapolate=True)(x))
    return np.column_stack(cols)

def gtruth(x):
    return 0.4 * x + 0.8 * np.sin(0.9 * x)

xd2 = np.sort(rng.uniform(1.2, 8.8, 45))       # data absent in the tails
yd2 = gtruth(xd2) + rng.normal(0, 0.4, xd2.size)
xg2 = np.linspace(0, 10, 500)                  # predict into sparse tails

knots = np.quantile(xd2, [0.05, 0.275, 0.5, 0.725, 0.95])
Br = rcs_basis(xd2, knots)
Br = np.column_stack([np.ones(len(xd2)), Br])
cr, *_ = np.linalg.lstsq(Br, yd2, rcond=None)
Brg = np.column_stack([np.ones(len(xg2)), rcs_basis(xg2, knots)])
fit_rcs = Brg @ cr

interior = knots[1:-1]
Bu = cubic_spline_design(xd2, interior, knots[0], knots[-1])
Bu = np.column_stack([np.ones(len(xd2)), Bu])
cu, *_ = np.linalg.lstsq(Bu, yd2, rcond=None)
Bug = np.column_stack([np.ones(len(xg2)),
                       cubic_spline_design(xg2, interior, knots[0], knots[-1])])
fit_un = Bug @ cu

axR.axvspan(0, knots[0], color=MUTED, alpha=0.07)
axR.axvspan(knots[-1], 10, color=MUTED, alpha=0.07)
axR.scatter(xd2, yd2, s=16, color=INK, alpha=0.55, zorder=2, label="data")
axR.plot(xg2, fit_un, color=PALETTE[1], lw=2.0, label="unrestricted cubic spline")
axR.plot(xg2, fit_rcs, color=PALETTE[0], lw=2.2, label="restricted cubic spline")
for kn in knots:
    axR.axvline(kn, color=MUTED, lw=0.7, ls="--")
axR.set_ylim(gtruth(xg2).min() - 2.5, gtruth(xg2).max() + 2.5)
axR.set_title("Restricting the tails (RCS)", fontsize=10)
axR.set_xlabel("x")
axR.set_ylabel("y")
axR.text(0.15, axR.get_ylim()[0] + 0.4, "sparse tail", fontsize=7.5, color=MUTED)
axR.legend(fontsize=7.6, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/splines-smoothing.svg")
