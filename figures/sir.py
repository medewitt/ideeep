# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""SIR epidemic trajectory."""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

beta, gamma, N = 0.5, 0.1, 1000.0   # R0 = beta/gamma = 5


def sir(t, y):
    S, I, R = y
    inf = beta * S * I / N
    return [-inf, inf - gamma * I, gamma * I]


sol = solve_ivp(sir, [0, 80], [N - 1, 1, 0], t_eval=np.linspace(0, 80, 400))
t = sol.t

fig, ax = plt.subplots()
ax.plot(t, sol.y[0], color=PALETTE[0], label="Susceptible")
ax.plot(t, sol.y[1], color=PALETTE[1], label="Infectious")
ax.plot(t, sol.y[2], color=PALETTE[2], label="Recovered")
ax.set_xlabel("time (days)")
ax.set_ylabel("individuals")
ax.set_title(r"SIR dynamics ($R_0=\beta/\gamma=5$)")
ax.legend(loc="center right")
save(fig, "assets/figures/sir.svg")
