# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Scientific machine learning marries mechanism and data. Left: an SIR
epidemic curve with sparse noisy incidence observations; differentiating
through the ODE solver lets gradient descent recover the mechanistic rates that
fit the data. Right: the physics-informed idea -- a neural surrogate u(t) is
trained on a loss with two terms, a data-misfit term and a physics-residual
term that punishes any departure from the known differential equation.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.integrate import odeint
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(0)


def sir(y, t, beta, gamma):
    S, I, R = y
    return [-beta * S * I, beta * S * I - gamma * I, gamma * I]


t = np.linspace(0, 40, 200)
sol = odeint(sir, [0.99, 0.01, 0.0], t, args=(0.6, 0.2))
incidence = sol[:, 1]
tobs = np.linspace(2, 38, 12)
iobs = np.interp(tobs, t, incidence) + rng.normal(0, 0.012, tobs.size)

fig = plt.figure(figsize=(9.8, 3.9))

# --- left: SIR curve, noisy data, recovered fit ---
ax0 = fig.add_axes([0.07, 0.15, 0.42, 0.74])
ax0.plot(t, incidence, color=PALETTE[0], lw=2, label="true dynamics  $I(t)$")
ax0.scatter(tobs, iobs, s=26, color=INK, zorder=3, label="noisy observations")
sol2 = odeint(sir, [0.99, 0.01, 0.0], t, args=(0.58, 0.205))
ax0.plot(t, sol2[:, 1], color=PALETTE[1], lw=1.6, ls="--",
         label="fit via differentiable ODE")
ax0.set_title("Learn the dynamics from data")
ax0.set_xlabel("time")
ax0.set_ylabel("infectious fraction")
ax0.legend(loc="upper right", fontsize=8)

# --- right: PINN loss schematic ---
ax1 = fig.add_axes([0.55, 0.05, 0.43, 0.9])
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")


def box(x, y, w, h, text, color, fs=8.8):
    ax1.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                  linewidth=1.6, edgecolor=color, facecolor=color + "18"))
    ax1.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fs, color=INK)


box(3.0, 7.7, 4.0, 1.5, "neural surrogate\n$u_\\theta(t)$", PALETTE[0])
box(0.3, 4.6, 4.2, 1.7, "data loss\n$\\sum (u_\\theta(t_i) - y_i)^2$", PALETTE[1])
box(5.5, 4.6, 4.2, 1.7,
    "physics loss\n$\\sum \\left(\\dot u_\\theta - f(u_\\theta)\\right)^2$",
    PALETTE[2])
box(2.7, 1.2, 4.6, 1.5, "minimize the sum\n$\\to$ fits data & obeys the ODE",
    INK)
for x0 in (2.4, 7.6):
    ax1.add_patch(FancyArrowPatch((5.0, 7.65), (x0, 6.35), arrowstyle="-|>",
                  mutation_scale=13, color="0.5", lw=1.5))
for x0 in (2.4, 7.6):
    ax1.add_patch(FancyArrowPatch((x0, 4.55), (5.0, 2.75), arrowstyle="-|>",
                  mutation_scale=13, color="0.5", lw=1.5))
ax1.text(5.0, 9.7, "Physics-informed neural network", ha="center", fontsize=10,
         color=INK, fontweight="bold")

save(fig, "assets/figures/scientific-machine-learning.svg")
