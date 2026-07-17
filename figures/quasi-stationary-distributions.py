# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Quasi-stationary distribution of the stochastic SIS model.

Two panels built from the sub-generator of the finite-state birth-death
process for the number infectious, with an absorbing state at I = 0:
(a) the quasi-stationary distribution nu (leading left eigenvector of the
    sub-generator) for two values of R0, each a bump around the
    deterministic endemic equilibrium I* = N(1 - 1/R0);
(b) the mean time to extinction 1/lambda1 versus population size N, which
    grows only slowly below threshold (R0 < 1) but explodes exponentially
    in N above threshold (R0 > 1) -- the quasi-stationary reading of the
    critical community size.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()


def sub_generator(N, R0, gamma=1.0):
    """Sub-generator C on transient states I = 1..N for the stochastic SIS.

    Infection (I -> I+1) at rate beta * I * (N - I) / N, recovery
    (I -> I-1) at rate gamma * I; state 0 is absorbing and excluded.
    """
    beta = R0 * gamma
    I = np.arange(1, N + 1)
    b = beta * I * (N - I) / N          # up rate
    d = gamma * I                        # down rate
    C = np.zeros((N, N))
    C[np.arange(N), np.arange(N)] = -(b + d)
    C[np.arange(N - 1), np.arange(1, N)] = b[:-1]        # I -> I+1
    C[np.arange(1, N), np.arange(N - 1)] = d[1:]         # I -> I-1
    return C


def qsd(N, R0, gamma=1.0):
    """Return (nu, lambda1): the QSD and the extinction rate from it."""
    C = sub_generator(N, R0, gamma)
    vals, vecs = np.linalg.eig(C.T)
    k = np.argmax(vals.real)             # eigenvalue closest to zero
    nu = np.abs(vecs[:, k].real)
    nu = nu / nu.sum()
    return nu, -vals[k].real


# --- Panel (a): the QSD as a bump around the endemic equilibrium ----------
N = 120
fig, (axA, axB) = plt.subplots(1, 2, figsize=(9.4, 3.9))

for color, R0 in zip((PALETTE[0], PALETTE[1]), (1.6, 2.4)):
    nu, lam = qsd(N, R0)
    support = np.arange(1, N + 1)
    axA.plot(support, nu, color=color, lw=1.8, label=f"$R_0={R0}$")
    istar = N * (1 - 1 / R0)
    axA.axvline(istar, color=color, ls=":", lw=1.1)

axA.set_xlabel("number infectious $I$")
axA.set_ylabel(r"quasi-stationary mass $\nu_I$")
axA.set_title("(a) the endemic bump", loc="left", fontsize=11)
axA.set_xlim(0, N)
axA.legend(loc="upper right")
axA.text(0.02, 0.96, "dotted: deterministic $I^*$", transform=axA.transAxes,
         va="top", ha="left", fontsize=9, color=MUTED)

# --- Panel (b): mean persistence time versus population size --------------
Ns = np.arange(10, 161, 5)
for color, R0, lab in zip((MUTED, PALETTE[2], PALETTE[3]),
                          (0.8, 1.3, 2.0),
                          ("$R_0=0.8$", "$R_0=1.3$", "$R_0=2.0$")):
    mean_T = [1.0 / qsd(N, R0)[1] for N in Ns]
    axB.plot(Ns, mean_T, color=color, lw=1.8, label=lab)

axB.set_yscale("log")
axB.set_xlabel("population size $N$")
axB.set_ylabel(r"mean persistence $1/\lambda_1$")
axB.set_title("(b) persistence explodes above threshold", loc="left", fontsize=11)
axB.legend(loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/quasi-stationary-distributions.svg")
