# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""A fitted (exponential) variogram with nugget/sill/range, and an ordinary-kriging surface."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(7)

# --- Variogram model: exponential, gamma(h) = c0 + c1 * (1 - exp(-3 h / a)) ---
nugget = 0.2       # c0
sill = 1.0         # c0 + c1
prange = 4.0       # practical range a (gamma reaches ~95% of sill at h = a)
c1 = sill - nugget


def gamma(h):
    return nugget + c1 * (1.0 - np.exp(-3.0 * np.asarray(h) / prange))


def cov(h):
    # C(h) = sill - gamma(h) for h > 0; the nugget lives on the diagonal only.
    h = np.asarray(h, dtype=float)
    return np.where(h == 0.0, sill, c1 * np.exp(-3.0 * h / prange))


# --- LEFT: empirical points scattered around the fitted model ---
h_emp = np.linspace(0.4, 9.0, 12)
g_emp = gamma(h_emp) + rng.normal(0.0, 0.045, size=h_emp.size)
h_fit = np.linspace(0, 9, 300)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 4.2))

axL.plot(h_fit, gamma(h_fit), color=PALETTE[0], lw=2.0, label="fitted model")
axL.scatter(h_emp, g_emp, s=28, color=PALETTE[1], zorder=3, label="empirical")

# nugget
axL.axhline(nugget, color=MUTED, ls=":", lw=1.0)
axL.annotate("nugget", xy=(0.15, nugget), xytext=(0.3, nugget - 0.16),
             fontsize="small", color=INK)
# sill
axL.axhline(sill, color=MUTED, ls="--", lw=1.0)
axL.annotate("sill", xy=(7.5, sill), xytext=(7.5, sill - 0.14),
             fontsize="small", color=INK)
# range
axL.axvline(prange, color=MUTED, ls="-.", lw=1.0)
axL.annotate("range", xy=(prange, 0.35), xytext=(prange + 0.3, 0.30),
             fontsize="small", color=INK)

axL.set_xlim(0, 9)
axL.set_ylim(0, 1.15)
axL.set_xlabel("separation distance $h$")
axL.set_ylabel(r"semivariance $\gamma(h)$")
axL.set_title("Fitted variogram")
axL.legend(loc="lower right")

# --- RIGHT: ordinary kriging surface from scattered samples ---
n = 12
sx = rng.uniform(0, 10, n)
sy = rng.uniform(0, 10, n)
# a smooth "true" field so the map looks like a real surface
sz = np.sin(0.6 * sx) + np.cos(0.5 * sy) + 0.15 * rng.standard_normal(n)

pts = np.column_stack([sx, sy])
D = np.hypot(pts[:, None, 0] - pts[None, :, 0], pts[:, None, 1] - pts[None, :, 1])
K = cov(D)
# Ordinary kriging: augment with a Lagrange multiplier (weights sum to one).
A = np.zeros((n + 1, n + 1))
A[:n, :n] = K
A[:n, n] = 1.0
A[n, :n] = 1.0
Ainv = np.linalg.inv(A)

gx = np.linspace(0, 10, 60)
gy = np.linspace(0, 10, 60)
GX, GY = np.meshgrid(gx, gy)
pred = np.empty_like(GX)
for i in range(GX.shape[0]):
    for j in range(GX.shape[1]):
        d0 = np.hypot(sx - GX[i, j], sy - GY[i, j])
        b = np.append(cov(d0), 1.0)
        w = Ainv @ b
        pred[i, j] = w[:n] @ sz

im = axR.contourf(GX, GY, pred, levels=14, cmap="viridis")
axR.scatter(sx, sy, c="white", edgecolors=INK, s=40, zorder=3, label="samples")
cb = fig.colorbar(im, ax=axR, shrink=0.9)
cb.set_label("kriged value")
axR.set_xlabel("easting")
axR.set_ylabel("northing")
axR.set_title("Ordinary-kriging surface")
axR.legend(loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/kriging.svg")
