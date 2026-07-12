# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""What the Python code block produces. The same seeded data are fit two ways:
a GCV-penalized smoothing spline (scipy `make_smoothing_spline`) and a
Harrell-style restricted cubic spline with 5 quantile knots. The two fits
nearly coincide over the bulk of the data. The three squares mark the printed
smoothing-spline predictions at x = 2, 5, 8 — the numbers echoed in the
output block above."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_smoothing_spline
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# ---- identical DGP to the page's Python block (rng seed 0) ----
rng = np.random.default_rng(0)
x = np.sort(rng.uniform(0, 10, 120))
y = np.sin(0.7 * x) + 0.2 * x + rng.normal(0, 0.3, x.size)


def truth(t):
    return np.sin(0.7 * t) + 0.2 * t


# penalized smoothing spline (lambda by GCV)
spl = make_smoothing_spline(x, y)


# Harrell restricted cubic spline basis (linear beyond outer knots)
def rcs(x, knots):
    x = np.asarray(x, float); k = np.asarray(knots, float); K = len(k)
    tk1, tkK = k[-2], k[-1]; d = tkK - tk1
    cube = lambda u: np.where(u > 0, u, 0.0) ** 3
    cols = [x]
    for j in range(K - 2):
        cols.append((cube(x - k[j])
                     - cube(x - tk1) * (tkK - k[j]) / d
                     + cube(x - tkK) * (tk1 - k[j]) / d) / d ** 2)
    return np.column_stack(cols)


knots = np.quantile(x, [0.05, 0.275, 0.50, 0.725, 0.95])
B = np.column_stack([np.ones(x.size), rcs(x, knots)])
beta, *_ = np.linalg.lstsq(B, y, rcond=None)
xg = np.linspace(0, 10, 400)
Bg = np.column_stack([np.ones(xg.size), rcs(xg, knots)])
rcs_fit = Bg @ beta

fig, ax = plt.subplots(figsize=(6.6, 3.9))

ax.scatter(x, y, s=16, color=INK, alpha=0.45, zorder=2, label="data")
ax.plot(xg, truth(xg), color=MUTED, lw=1.2, ls=":", label="truth")
ax.plot(xg, rcs_fit, color=PALETTE[2], lw=2.0, label="restricted cubic spline (5 knots)")
ax.plot(xg, spl(xg), color=PALETTE[0], lw=2.2, label="smoothing spline (GCV)")

# knot markers along the bottom
for kn in knots:
    ax.axvline(kn, color=MUTED, lw=0.6, ls="--", alpha=0.6)

# the three printed evaluation points
xe = np.array([2.0, 5.0, 8.0])
ye = spl(xe)
ax.scatter(xe, ye, s=70, color=PALETTE[1], marker="s", zorder=6,
           edgecolor="white", linewidth=0.8, label="printed fit at x = 2, 5, 8")
for xi, yi in zip(xe, ye):
    ax.annotate(f"({xi:.0f}, {yi:.3f})", xy=(xi, yi), xytext=(0, 12),
                textcoords="offset points", fontsize=8, color=INK, ha="center")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Two spline fits to the same data", fontsize=10)
ax.legend(fontsize=8, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/splines-python-fit.svg")
