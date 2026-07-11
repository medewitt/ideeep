# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Response surface methodology. Left: the two-phase strategy — far from the
optimum the fitted plane's gradient gives the direction of steepest ascent, so
experimental steps climb the contour surface toward the peak, then a second-order
model maps the curvature near it. Right: a central composite design builds the
three levels needed for that quadratic from three pieces — the 2^k factorial
corners, 2k axial (star) points at radius alpha, and replicated center points."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.7))

# ---- contour + steepest ascent --------------------------------------------
gx, gy = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
peak = (1.4, 1.1)
Z = -((gx - peak[0]) ** 2 + 1.3 * (gy - peak[1]) ** 2) + 0.4 * gx
cs = axL.contour(gx, gy, Z, levels=10, colors=MUTED, linewidths=0.7)
axL.contourf(gx, gy, Z, levels=20, cmap="Blues", alpha=0.35)
# steepest-ascent path from a factorial region near (-2,-2)
path = np.array([[-2.2, -2.0], [-1.4, -1.2], [-0.5, -0.3], [0.4, 0.5],
                 [1.1, 0.95], [1.4, 1.1]])
for i in range(len(path) - 1):
    axL.add_patch(FancyArrowPatch(path[i], path[i + 1], arrowstyle="-|>",
                  mutation_scale=12, color=PALETTE[1], lw=1.8))
axL.scatter(*peak, s=60, marker="*", color=PALETTE[1], zorder=6)
axL.text(peak[0] + 0.1, peak[1] + 0.2, "optimum", fontsize=8, color=PALETTE[1])
axL.text(-2.9, -2.7, "steepest\nascent", fontsize=8, color=PALETTE[1])
axL.set_xlabel("factor $x_1$")
axL.set_ylabel("factor $x_2$")
axL.set_title("Climb the gradient, then map curvature", fontsize=9.3)
axL.set_xlim(-3, 3)
axL.set_ylim(-3, 3)
axL.set_aspect("equal")
axL.grid(False)

# ---- central composite design ---------------------------------------------
alpha = 2 ** 0.5
fac = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
axi = [(alpha, 0), (-alpha, 0), (0, alpha), (0, -alpha)]
axR.scatter(*zip(*fac), s=70, color=PALETTE[0], zorder=5, label="factorial (±1)")
axR.scatter(*zip(*axi), s=70, color=PALETTE[1], marker="D", zorder=5,
            label=fr"axial (±{alpha:.2f})")
axR.scatter([0], [0], s=110, color=PALETTE[2], marker="s", zorder=5,
            label="center (replicated)")
# rotatable circle through axial points
th = np.linspace(0, 2 * np.pi, 100)
axR.plot(alpha * np.cos(th), alpha * np.sin(th), color=MUTED, lw=0.8, ls=":")
# factorial square
sq = np.array(fac + [fac[0]])
axR.plot(sq[[0, 1, 3, 2, 0], 0], sq[[0, 1, 3, 2, 0], 1], color=PALETTE[0],
         lw=0.8, ls="--")
axR.set_xlabel("$x_1$")
axR.set_ylabel("$x_2$")
axR.set_title("Central composite design", fontsize=9.3)
axR.set_xlim(-1.9, 1.9)
axR.set_ylim(-1.9, 1.9)
axR.set_aspect("equal")
axR.legend(fontsize=7.4, loc="upper right")
axR.grid(False)

fig.tight_layout()
save(fig, "assets/figures/response-surface.svg")
