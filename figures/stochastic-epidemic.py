# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Gillespie stochastic SIR trajectories overlaid on the deterministic ODE."""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(42)

N = 200
beta, gamma = 0.4, 0.1
I0 = 3
R0 = beta / gamma
tmax = 120.0
print(f"stochastic SIR: R0 = beta/gamma = {R0:.1f}")


def gillespie():
    S, I = N - I0, I0
    t = 0.0
    ts, Is = [0.0], [I]
    while I > 0 and t < tmax:
        inf = beta * S * I / N
        rec = gamma * I
        tot = inf + rec
        if tot <= 0:
            break
        t += rng.exponential(1 / tot)
        if rng.random() < inf / tot:
            S -= 1
            I += 1
        else:
            I -= 1
        ts.append(min(t, tmax))
        Is.append(I)
    return np.array(ts), np.array(Is)


fig, ax = plt.subplots()

n_traj = 40
fizzles = 0
for k in range(n_traj):
    ts, Is = gillespie()
    if Is.max() < 10:  # never really took off
        fizzles += 1
    ax.step(ts, Is, where="post", color=PALETTE[0], lw=0.7, alpha=0.28)

# Deterministic ODE.
def rhs(t, y):
    S, I = y
    inf = beta * S * I / N
    return [-inf, inf - gamma * I]


sol = solve_ivp(rhs, [0, tmax], [N - I0, I0],
                t_eval=np.linspace(0, tmax, 600), rtol=1e-8, atol=1e-8)
ax.plot(sol.t, sol.y[1], color=PALETTE[1], lw=2.6, label="deterministic ODE")

ax.plot([], [], color=PALETTE[0], lw=1.2, alpha=0.6,
        label=f"{n_traj} stochastic runs")
print(f"{fizzles}/{n_traj} trajectories fizzled (peak I < 10)")
ax.annotate(f"{fizzles} of {n_traj} runs fizzle\n(minor outbreaks)",
            xy=(4, 4), xytext=(35, 40), fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#26323f"))
ax.text(0.98, 0.5, f"$R_0=\\beta/\\gamma={R0:.0f}$", transform=ax.transAxes,
        ha="right", fontsize=10, color="#26323f")

ax.set_xlabel("time")
ax.set_ylabel("prevalence I(t)")
ax.set_title("Stochastic vs deterministic SIR")
ax.legend(loc="upper right", fontsize=9)

save(fig, "assets/figures/stochastic-epidemic.svg")
