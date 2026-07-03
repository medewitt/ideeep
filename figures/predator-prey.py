# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Lotka-Volterra predator-prey dynamics: time series and phase-plane orbits."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from _style import apply_style, save, PALETTE

apply_style()

a, b, d, g = 1.1, 0.4, 0.1, 0.4


def lotka_volterra(t, y):
    N, P = y
    return [a * N - b * N * P, d * N * P - g * P]


# Interior equilibrium
N_star, P_star = g / d, a / b

t_span = (0, 60)
t_eval = np.linspace(*t_span, 2000)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# LEFT: time series for one initial condition
sol = solve_ivp(lotka_volterra, t_span, [10, 5], t_eval=t_eval, rtol=1e-8, atol=1e-8)
ax1.plot(sol.t, sol.y[0], color=PALETTE[0], label="Prey N(t)")
ax1.plot(sol.t, sol.y[1], color=PALETTE[1], label="Predator P(t)")
ax1.set_xlabel("Time t")
ax1.set_ylabel("Population")
ax1.set_title("Time series")
ax1.legend()

# RIGHT: phase-plane orbits for several initial conditions
initial_conditions = [[10, 5], [10, 8], [12, 3]]
for i, ic in enumerate(initial_conditions):
    s = solve_ivp(lotka_volterra, t_span, ic, t_eval=t_eval, rtol=1e-8, atol=1e-8)
    ax2.plot(s.y[0], s.y[1], color=PALETTE[i % len(PALETTE)],
             label=f"N0={ic[0]}, P0={ic[1]}")

ax2.plot(N_star, P_star, "o", color=PALETTE[3 % len(PALETTE)],
         markersize=9, label=f"Equilibrium ({N_star:.0f}, {P_star:.2f})")
ax2.set_xlabel("Prey N")
ax2.set_ylabel("Predator P")
ax2.set_title("Phase-plane orbits")
ax2.legend()

fig.suptitle("Lotka-Volterra Predator-Prey Dynamics")
save(fig, "assets/figures/predator-prey.svg")
