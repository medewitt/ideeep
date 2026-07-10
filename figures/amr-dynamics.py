# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Population dynamics of resistance under a two-strain SIS model.

Left: the resistant fraction of infections over time for three community
treatment rates, converging to different equilibria. Right: the equilibrium
resistant fraction as a function of treatment rate, with the competitive-
exclusion threshold tau* = gamma c / (1 - c) marked; de novo resistance during
treatment smooths the switch into an S-curve.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

beta, gamma, cost, rho = 0.30, 0.10, 0.30, 0.01
tau_star = gamma * cost / (1 - cost)      # exclusion threshold


def rhs(t, y, tau):
    S, Is, Ir = y
    new_s = beta * S * Is
    new_r = beta * (1 - cost) * S * Ir
    dIs = new_s - gamma * Is - tau * Is
    dIr = new_r - gamma * Ir + rho * tau * Is
    dS = gamma * Is + gamma * Ir + (1 - rho) * tau * Is - new_s - new_r
    return [dS, dIs, dIr]


fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# --- Left: trajectories of the resistant fraction ------------------------
t_eval = np.linspace(0, 4000, 800)
taus = [0.02, 0.045, 0.08]
labels = [r"$\tau=0.02$ (below $\tau^*$)",
          r"$\tau=0.045$ (near $\tau^*$)",
          r"$\tau=0.08$ (above $\tau^*$)"]
for tau, col, lab in zip(taus, PALETTE, labels):
    sol = solve_ivp(rhs, [0, 4000], [0.98, 0.01, 0.01], args=(tau,),
                    t_eval=t_eval, rtol=1e-9, atol=1e-11)
    S, Is, Ir = sol.y
    frac = Ir / (Is + Ir)
    axL.plot(sol.t, frac, color=col, lw=2.0, label=lab)

axL.set_xlabel("time (days)")
axL.set_ylabel("resistant fraction of infections")
axL.set_title("dynamics toward equilibrium")
axL.set_xlim(0, 4000)
axL.set_ylim(-0.02, 1.05)
axL.legend(loc="center right", fontsize=7.5)

# --- Right: equilibrium resistant fraction vs treatment rate -------------
tau_grid = np.linspace(0, 0.15, 80)
eq_frac = np.empty_like(tau_grid)
for i, tau in enumerate(tau_grid):
    sol = solve_ivp(rhs, [0, 8000], [0.98, 0.01, 0.01], args=(tau,),
                    rtol=1e-9, atol=1e-11)
    S, Is, Ir = sol.y[:, -1]
    eq_frac[i] = Ir / (Is + Ir)

axR.plot(tau_grid, eq_frac, color=PALETTE[3], lw=2.2)
axR.axvline(tau_star, color=MUTED, lw=1.0, ls="--")
axR.annotate(r"$\tau^*=\gamma c/(1-c)$", xy=(tau_star, 0.5),
             xytext=(tau_star + 0.012, 0.32), fontsize=9, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
axR.annotate("reversal is slow\n(small fitness cost)", xy=(0.11, 0.97),
             xytext=(0.045, 0.72), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
axR.set_xlabel(r"community treatment rate $\tau$ (per day)")
axR.set_ylabel("equilibrium resistant fraction")
axR.set_title("selection at the population scale")
axR.set_xlim(0, 0.15)
axR.set_ylim(-0.02, 1.05)

fig.tight_layout()
save(fig, "assets/figures/amr-dynamics.svg")
