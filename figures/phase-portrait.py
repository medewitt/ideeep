# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Phase portrait of a damped linear system spiraling to a stable focus."""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

d = 0.2  # damping


def rhs(t, s):
    x, y = s
    return [-d * x - y, x - d * y]


# Vector field.
xg = np.linspace(-2.2, 2.2, 22)
yg = np.linspace(-2.2, 2.2, 22)
X, Y = np.meshgrid(xg, yg)
U = -d * X - Y
V = X - d * Y

fig, ax = plt.subplots()
ax.streamplot(X, Y, U, V, color="#c3ccd4", density=1.1, linewidth=0.7,
              arrowsize=0.8)

# One trajectory spiraling inward.
sol = solve_ivp(rhs, [0, 40], [2.0, 0.0], t_eval=np.linspace(0, 40, 4000),
                rtol=1e-8, atol=1e-10)
ax.plot(sol.y[0], sol.y[1], color=PALETTE[0], lw=1.8, label="trajectory")
ax.plot(2.0, 0.0, "o", color=PALETTE[1], ms=7, label="start")
ax.plot(0, 0, "o", color=PALETTE[3], ms=9, zorder=5)
ax.annotate("stable focus\n(0, 0)", xy=(0, 0), xytext=(0.55, 0.9),
            arrowprops=dict(arrowstyle="->", color="#26323f"), fontsize=9)

print(f"damping d={d}; final state ({sol.y[0,-1]:.3f}, {sol.y[1,-1]:.3f})")

ax.set_xlim(-2.3, 2.3)
ax.set_ylim(-2.3, 2.3)
ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Damped phase portrait (stable spiral)")
ax.legend(loc="upper right", fontsize=9)

save(fig, "assets/figures/phase-portrait.svg")
