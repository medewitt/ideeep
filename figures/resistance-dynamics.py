# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Equilibrium resistant fraction as a function of the treatment rate.

Two-strain SIS transmission model (drug-sensitive vs drug-resistant) with a
transmission cost of resistance and a small rate of de novo resistance during
treatment. Integrating to steady state over a grid of treatment rates traces
the rising S-curve of the equilibrium resistant fraction.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

beta = 0.30     # transmission rate of the sensitive strain
gamma = 0.10    # natural clearance rate (both strains)
cost = 0.30     # transmission cost of resistance
rho = 0.01      # fraction of treated infections that acquire resistance


def rhs(t, y, tau):
    S, Is, Ir = y
    new_s = beta * S * Is
    new_r = beta * (1 - cost) * S * Ir
    dIs = new_s - gamma * Is - tau * Is
    dIr = new_r - gamma * Ir + rho * tau * Is
    dS = gamma * Is + gamma * Ir + (1 - rho) * tau * Is - new_s - new_r
    return [dS, dIs, dIr]


def resistant_fraction(tau):
    y0 = [0.98, 0.01, 0.01]
    sol = solve_ivp(rhs, [0, 5000], y0, args=(tau,), rtol=1e-9, atol=1e-11)
    S, Is, Ir = sol.y[:, -1]
    total = Is + Ir
    return Ir / total if total > 1e-9 else 0.0


taus = np.linspace(0.0, 0.15, 120)
frac = np.array([resistant_fraction(t) for t in taus])

# Competitive-exclusion threshold (no de novo resistance): tau* = gamma c/(1-c).
tau_star = gamma * cost / (1 - cost)

fig, ax = plt.subplots()
ax.plot(taus, frac, color=PALETTE[1], lw=2.2)
ax.axvline(tau_star, color=MUTED, ls="--", lw=1.1)
ax.annotate(r"threshold $\tau^\ast=\gamma c/(1-c)$",
            xy=(tau_star, 0.5), xytext=(tau_star + 0.012, 0.32),
            arrowprops=dict(arrowstyle="->", color=INK), fontsize=9)

ax.set_xlabel(r"treatment rate $\tau$ (per day)")
ax.set_ylabel("equilibrium fraction resistant")
ax.set_ylim(-0.03, 1.03)
ax.set_title("More treatment selects for the resistant strain")

save(fig, "assets/figures/resistance-dynamics.svg")
