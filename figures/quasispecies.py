# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""Eigen's quasispecies error threshold on a single-peak landscape.

Equilibrium frequency of the master sequence as a function of the per-genome
mutation rate U = L*mu, for several values of the master's selective
superiority sigma. Neglecting back-mutation, the master is maintained only
while sigma * Q > 1 with Q = e^{-U}, so it delocalizes at U_c = ln(sigma):
the error catastrophe.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE
apply_style()

U = np.linspace(0, 4, 400)          # per-genome mutation rate L*mu
Q = np.exp(-U)                      # genome copy fidelity q^L ~ e^{-U}

fig, ax = plt.subplots()

for sigma, color in zip((2.0, 4.0, 10.0), PALETTE):
    x_master = np.clip((sigma * Q - 1) / (sigma - 1), 0, None)
    ax.plot(U, x_master, color=color, linewidth=1.8,
            label=fr"$\sigma={sigma:g}$")
    Uc = np.log(sigma)              # error threshold U_c = ln(sigma)
    ax.axvline(Uc, color=color, linestyle=":", linewidth=1.0, alpha=0.7)

ax.set_xlabel(r"Per-genome mutation rate $U = L\mu$")
ax.set_ylabel("Equilibrium master frequency $x_0$")
ax.set_ylim(-0.02, 1.02)
ax.set_xlim(0, 4)
ax.set_title("The error catastrophe: the master sequence\n"
             r"delocalizes at $U_c=\ln\sigma$ (dotted lines)")
ax.legend(title="master superiority", loc="upper right", fontsize="small")

save(fig, "assets/figures/quasispecies.svg")
