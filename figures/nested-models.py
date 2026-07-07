# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Nesting within-host viral dynamics inside a between-host SIR model.

Panel A: within-host viral load V(t) for a sweep of replication rates.
Panel B: the transmission-virulence trade-off that emerges from the sweep.
Panel C: between-host R0 across virulence, with the emergent optimum marked.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# Within-host target-cell model: T target cells, I infected, V virus.
T0, b, d, c = 1e6, 2e-7, 1.0, 5.0


def rhs(t, y, p):
    T, I, V = y
    return [-b * T * V, b * T * V - d * I, p * I - c * V]


def peak_load(p):
    sol = solve_ivp(rhs, [0, 40], [T0, 0.0, 1.0], args=(p,),
                    method="LSODA", rtol=1e-8, atol=1e-6,
                    dense_output=True)
    t = np.linspace(0, 40, 4000)
    return t, sol.sol(t)[2]


# Maps from within-host load to between-host rates.
beta_max, Kb, a_v, d0 = 3.0, 1e4, 2e-5, 0.2   # d0 = gamma + mu
trans = lambda Vmax: beta_max * Vmax / (Vmax + Kb)
viru = lambda Vmax: a_v * Vmax

ps = np.linspace(2, 200, 40)
Vmax = np.array([peak_load(p)[1].max() for p in ps])
beta = trans(Vmax)
alpha = viru(Vmax)
R0 = beta / (alpha + d0)
istar = int(np.argmax(R0))

fig, ax = plt.subplots(1, 3, figsize=(12.4, 3.7))

# Panel A: a few within-host trajectories.
for p, col in zip([10, 50, 150], [PALETTE[0], PALETTE[2], PALETTE[1]]):
    t, V = peak_load(p)
    ax[0].plot(t, V, color=col, lw=2, label=f"p = {p}")
ax[0].set_yscale("log")
ax[0].set_xlabel("time within host (days)")
ax[0].set_ylabel("viral load $V(t)$")
ax[0].set_title("A. Fast within-host scale")
ax[0].legend(fontsize=9)

# Panel B: emergent trade-off curve.
ax[1].plot(alpha, beta, color=INK, lw=2)
ax[1].plot(alpha[istar], beta[istar], "o", color=PALETTE[1], ms=8)
ax[1].set_xlabel(r"virulence $\alpha$")
ax[1].set_ylabel(r"transmission $\beta$")
ax[1].set_title("B. Trade-off emerges")

# Panel C: between-host R0 with the emergent optimum.
ax[2].plot(alpha, R0, color=PALETTE[3], lw=2)
ax[2].plot(alpha[istar], R0[istar], "o", color=PALETTE[1], ms=8)
ax[2].axvline(alpha[istar], color=MUTED, ls="--", lw=1)
ax[2].annotate(rf"$\alpha^* \approx {alpha[istar]:.2f}$",
               xy=(alpha[istar], R0[istar]),
               xytext=(alpha[istar] + 0.4, R0[istar] * 0.85),
               arrowprops=dict(arrowstyle="->", color=INK), fontsize=9)
ax[2].set_xlabel(r"virulence $\alpha$")
ax[2].set_ylabel(r"between-host $R_0$")
ax[2].set_title("C. Slow between-host scale")

fig.tight_layout()
save(fig, "assets/figures/nested-models.svg")
