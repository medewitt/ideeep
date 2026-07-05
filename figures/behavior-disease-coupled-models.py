# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Behavior-disease coupled SIRS model: prevalence-dependent protective behavior
flattens and delays the epidemic peak.

Transmission is scaled by (1 - c*P), where adoption P = I/(I + k) saturates with
current prevalence. Two runs are integrated deterministically with solve_ivp:
behavior off (c=0) and behavior on (c>0). No RNG.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# --- model parameters -------------------------------------------------------
beta = 0.6      # baseline transmission rate (R0 = beta/gamma = 3)
gamma = 0.2     # recovery rate
omega = 0.02    # waning-immunity rate (R -> S)
k = 0.02        # half-saturation prevalence for behavior adoption
S0, I0, R0 = 0.999, 0.001, 0.0   # initial state (S + I + R = 1)
t_end = 200.0
t_eval = np.linspace(0.0, t_end, 4001)


def rhs(t, y, c):
    S, I, R = y
    P = I / (I + k)               # prevalence-dependent adoption, saturating
    lam = beta * (1.0 - c * P) * I  # effective force of infection
    return [-lam * S + omega * R,
            lam * S - gamma * I,
            gamma * I - omega * R]


def solve(c):
    sol = solve_ivp(rhs, (0.0, t_end), [S0, I0, R0], args=(c,),
                    t_eval=t_eval, rtol=1e-8, atol=1e-10)
    return sol.t, sol.y[1]


t_off, I_off = solve(0.0)   # behavior off
t_on, I_on = solve(0.7)     # behavior on

fig, ax = plt.subplots()
ax.plot(t_off, I_off, color=PALETTE[1], lw=2.2, label="no behavior")
ax.plot(t_on, I_on, color=PALETTE[0], lw=2.2, label="with protective behavior")

# annotate the two peaks
for t, I, col in ((t_off, I_off, PALETTE[1]), (t_on, I_on, PALETTE[0])):
    j = int(np.argmax(I))
    ax.scatter([t[j]], [I[j]], color=col, s=18, zorder=3)

ax.set_xlim(0, 120)
ax.set_ylim(bottom=0)
ax.set_xlabel("time (days)")
ax.set_ylabel("infected prevalence")
ax.set_title("Protective behavior flattens and delays the peak")
ax.legend(loc="upper right")

save(fig, "assets/figures/behavior-disease-coupled-models.svg")
