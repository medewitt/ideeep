# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""The transmission-virulence trade-off. Left: with beta(alpha) = a*sqrt(alpha),
R0(alpha) rises then falls, peaking at an intermediate optimum alpha* = gamma+mu
= 0.6 that beats both a more benign (0.2) and a more aggressive (1.5) strain.
Right: the pairwise-invasibility plot (PIP) for the same model — a mutant
invades where its R0 exceeds the resident's (shaded); the singular strategy at
alpha* is an ESS because its whole vertical line lies outside the invasion
region."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

gamma, mu, a = 0.5, 0.1, 3.0
astar = gamma + mu                       # 0.6


def R0(al):
    return a * np.sqrt(al) / (gamma + al + mu)


fig, (axL, axP) = plt.subplots(1, 2, figsize=(8.4, 3.7))

# ---- R0(alpha) curve ------------------------------------------------------
al = np.linspace(0.01, 3.0, 400)
axL.plot(al, R0(al), color=PALETTE[0], lw=2.0)
axL.axvline(astar, ls="--", color=MUTED, lw=1.0)

for a_i, col, lab in [(0.2, PALETTE[2], "benign"),
                      (astar, PALETTE[1], "optimum $\\alpha^*$"),
                      (1.5, PALETTE[3], "aggressive")]:
    axL.scatter([a_i], [R0(a_i)], s=42, color=col, zorder=4)
    axL.annotate(f"{lab}\n$\\alpha={a_i:g},\\ R_0={R0(a_i):.2f}$",
                 xy=(a_i, R0(a_i)), xytext=(a_i + 0.15, R0(a_i) - 0.42),
                 fontsize=8, color=INK)

axL.set_xlabel(r"virulence $\alpha$ (host mortality)")
axL.set_ylabel(r"$R_0(\alpha)=\beta(\alpha)/(\gamma+\alpha+\mu)$")
axL.set_title("Intermediate optimal virulence", fontsize=10)
axL.set_ylim(0, 2.2)

# ---- pairwise-invasibility plot -------------------------------------------
g = np.linspace(0.01, 2.0, 400)
res, mut = np.meshgrid(g, g)
invade = np.sign(R0(mut) - R0(res))      # +1 where mutant invades resident

axP.contourf(res, mut, invade, levels=[-1.5, 0, 1.5],
             colors=[PALETTE[0] + "22", PALETTE[1] + "44"])
axP.plot(g, g, color=MUTED, lw=0.9)
axP.axvline(astar, ls="--", color=INK, lw=1.0)
axP.axhline(astar, ls="--", color=INK, lw=1.0)
axP.scatter([astar], [astar], s=45, color=PALETTE[1], zorder=5)

axP.text(0.95, 1.62, "mutant\ninvades", fontsize=8.5, color=PALETTE[1], ha="center")
axP.text(1.5, 0.5, "mutant\ndies out", fontsize=8.5, color=PALETTE[0], ha="center")
axP.annotate("ESS $\\alpha^*=\\gamma+\\mu$", xy=(astar, astar),
             xytext=(0.75, 1.25), fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axP.set_xlabel(r"resident virulence $\alpha$")
axP.set_ylabel(r"mutant virulence $\alpha'$")
axP.set_title("Pairwise-invasibility plot", fontsize=10)
axP.set_xlim(0, 2)
axP.set_ylim(0, 2)
axP.grid(False)

fig.tight_layout()
save(fig, "assets/figures/evolution-of-virulence.svg")
