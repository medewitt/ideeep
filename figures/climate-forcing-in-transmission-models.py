# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Seasonally forced SIRS model: stronger seasonal forcing of the transmission
rate produces larger recurrent epidemic swings.

Transmission is beta(t) = beta0 * (1 + eps * cos(2*pi*t/365)), with waning
immunity and demography so recurrence is sustained. Two deterministic runs are
integrated with solve_ivp for a weak (eps=0.05) and a strong (eps=0.25) forcing
amplitude; a multi-year transient is discarded before plotting five years of
infected prevalence. No RNG.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# --- model parameters (rates per day) --------------------------------------
beta0 = 1.0 / 3.0     # annual-mean transmission rate (R0 ~= 3)
gamma = 1.0 / 10.0    # recovery rate (10-day infectious period)
omega = 1.0 / 365.0   # waning-immunity rate (R -> S), ~1 year
mu = 1.0 / (50 * 365.0)  # birth = death rate (~50-year life expectancy)
period = 365.0        # forcing period, one year in days

transient_years = 30  # years of transient discarded before plotting
show_years = 5        # years of prevalence shown
S0, I0, R0 = 0.9, 1e-3, 0.099   # initial state (S + I + R = 1)


def rhs(t, y, eps):
    S, I, R = y
    beta = beta0 * (1.0 + eps * np.cos(2.0 * np.pi * t / period))
    lam = beta * I                       # force of infection
    return [mu - lam * S + omega * R - mu * S,
            lam * S - gamma * I - mu * I,
            gamma * I - omega * R - mu * R]


t_end = (transient_years + show_years) * period
t_plot0 = transient_years * period
t_eval = np.linspace(t_plot0, t_end, show_years * 365 + 1)

amplitudes = [
    (0.05, PALETTE[0], "weak forcing (ε=0.05)"),
    (0.25, PALETTE[1], "strong forcing (ε=0.25)"),
]

fig, ax = plt.subplots()
for eps, color, label in amplitudes:
    sol = solve_ivp(rhs, (0.0, t_end), [S0, I0, R0], args=(eps,),
                    t_eval=t_eval, rtol=1e-9, atol=1e-12, dense_output=False)
    years = (sol.t - t_plot0) / period
    ax.plot(years, sol.y[1], color=color, lw=1.6, label=label)

ax.set_xlabel("time (years)")
ax.set_ylabel("infected prevalence")
ax.set_title("Seasonal forcing drives recurrent epidemics")
ax.set_xlim(0, show_years)
ax.legend(loc="upper right")

save(fig, "assets/figures/climate-forcing-in-transmission-models.svg")
