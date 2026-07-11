# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""D-optimal design for a straight line. Left: with two runs at +/-d on [-1,1],
the information determinant det(X'X) = 4d^2 grows with the spread, so it is
maximized by pushing the points to the endpoints (d=1, det=4) rather than the
interior (d=0.5, det=1). Right: the same fact as precision — the endpoint design
gives a small, tight joint confidence ellipse for (beta0, beta1), while the
interior design gives a large one; D-optimality minimizes that ellipse's
volume."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- det(X'X) = 4 d^2 -----------------------------------------------------
d = np.linspace(0, 1, 200)
axL.plot(d, 4 * d**2, color=PALETTE[0], lw=2.0)
for dv, col, lab in [(1.0, PALETTE[1], "endpoints"), (0.5, PALETTE[3], "interior")]:
    axL.scatter([dv], [4 * dv**2], s=55, color=col, zorder=5)
    axL.annotate(f"{lab}\n$d={dv}$, det $={4*dv**2:.0f}$", (dv, 4 * dv**2),
                 textcoords="offset points", xytext=(-6, -4),
                 ha="right", fontsize=8, color=INK)
axL.set_xlabel("spread of the two runs $d$")
axL.set_ylabel(r"information $\det(X^\top X)=4d^2$")
axL.set_title("Spread points to gain information", fontsize=9.5)
axL.set_xlim(0, 1.05)
axL.set_ylim(0, 4.4)

# ---- confidence ellipses --------------------------------------------------
th = np.linspace(0, 2 * np.pi, 100)
circ = np.array([np.cos(th), np.sin(th)])
for dv, col, lab in [(1.0, PALETTE[1], "endpoints (tight)"),
                     (0.5, PALETTE[3], "interior (wide)")]:
    XtX = np.array([[2, 0], [0, 2 * dv**2]])
    cov = np.linalg.inv(XtX)                 # ∝ Var(beta-hat)
    L = np.linalg.cholesky(cov)
    ell = 2.2 * (L @ circ)
    axR.plot(ell[0], ell[1], color=col, lw=2.0, label=lab)
axR.scatter([0], [0], s=25, color=INK, zorder=5)
axR.set_xlabel(r"$\hat\beta_0$")
axR.set_ylabel(r"$\hat\beta_1$ (slope)")
axR.set_title("Smaller ellipse = more precise", fontsize=9.5)
axR.set_aspect("equal")
axR.legend(fontsize=8, loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/optimal-design.svg")
