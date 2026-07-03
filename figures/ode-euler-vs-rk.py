# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Why the solver and step size matter. Left: on simple exponential decay, a
big Euler step badly undershoots the exact curve while a 4th-order Runge-Kutta
step tracks it almost perfectly. Right: on a predator-prey cycle (which should
trace a closed loop forever), Euler spirals outward -- inventing growth that
isn't in the biology -- while RK4 stays on the orbit.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE


def euler(f, y0, h, n):
    ys = [np.array(y0, dtype=float)]
    for _ in range(n):
        ys.append(ys[-1] + h * f(ys[-1]))
    return np.array(ys)


def rk4(f, y0, h, n):
    ys = [np.array(y0, dtype=float)]
    for _ in range(n):
        y = ys[-1]
        k1 = f(y)
        k2 = f(y + 0.5 * h * k1)
        k3 = f(y + 0.5 * h * k2)
        k4 = f(y + h * k3)
        ys.append(y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
    return np.array(ys)


apply_style()
fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.6))

# --- left: exponential decay y' = -y, exact solution e^{-t} ---
decay = lambda y: -y
t = np.linspace(0, 5, 200)
axL.plot(t, np.exp(-t), color="0.25", lw=2.2, label="exact  e^(−t)")

h = 1.0
n = int(5 / h)
tt = np.arange(n + 1) * h
axL.plot(tt, euler(decay, 1.0, h, n).ravel(), "o--", color=PALETTE[1],
         lw=1.6, ms=6, label=f"Euler  (h={h})")
axL.plot(tt, rk4(decay, 1.0, h, n).ravel(), "s-", color=PALETTE[2],
         lw=1.6, ms=6, label=f"RK4  (h={h})")
axL.set_title("accuracy: exponential decay", fontsize=10)
axL.set_xlabel("time")
axL.set_ylabel("y")
axL.legend(fontsize="small")

# --- right: predator-prey (normalized Lotka-Volterra), closed orbits ---
lv = lambda z: np.array([z[0] * (1 - z[1]), z[1] * (z[0] - 1)])
z0, h2, n2 = [1.6, 1.0], 0.06, 900
e = euler(lv, z0, h2, n2)
r = rk4(lv, z0, h2, n2)
axR.plot(r[:, 0], r[:, 1], color=PALETTE[2], lw=1.8, label="RK4 (stays on orbit)")
axR.plot(e[:, 0], e[:, 1], color=PALETTE[1], lw=1.3, alpha=0.9,
         label="Euler (spirals out)")
axR.plot([1], [1], "k+", ms=9)
axR.set_title("stability: predator–prey cycle", fontsize=10)
axR.set_xlabel("prey")
axR.set_ylabel("predators")
axR.legend(fontsize="small", loc="upper right")

fig.suptitle("The method and step size decide whether the answer is right", y=1.02)
fig.tight_layout()
save(fig, "assets/figures/ode-euler-vs-rk.svg")
