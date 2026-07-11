# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Degree heterogeneity, not the mean, drives spread. Left: two contact
populations with the identical mean degree 4 — a homogeneous one (every degree
= 4) and a heterogeneous one (four near-isolates and one hub, degrees
{1,1,1,1,16}) — plotted as their degree sequences. Right: because
R0 ~ <k^2>/<k> = <k> + Var(k)/<k>, the ratio (and hence R0) grows linearly with
degree variance at fixed mean; the single hub lifts the heterogeneous case from
4 to 13."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

homog = np.array([4, 4, 4, 4, 4])
hetero = np.array([1, 1, 1, 1, 16])


def ratio(k):
    return (k**2).mean() / k.mean()


fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- degree sequences -----------------------------------------------------
x = np.arange(5)
w = 0.38
axL.bar(x - w / 2, homog, width=w, color=PALETTE[0],
        label=f"homogeneous  ⟨k²⟩/⟨k⟩ = {ratio(homog):.0f}")
axL.bar(x + w / 2, hetero, width=w, color=PALETTE[1],
        label=f"heterogeneous  ⟨k²⟩/⟨k⟩ = {ratio(hetero):.0f}")
axL.axhline(4, ls="--", color=MUTED, lw=1.1)
axL.text(4.4, 4.4, "same mean\n⟨k⟩ = 4", fontsize=8, color=MUTED, ha="right")
axL.annotate("one hub", xy=(4 + w / 2, 16), xytext=(2.3, 14),
             fontsize=8.5, color=PALETTE[1],
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axL.set_xlabel("individual")
axL.set_ylabel("number of contacts (degree)")
axL.set_title("Same mean degree, different spread", fontsize=10)
axL.set_xticks(x)
axL.set_xticklabels([f"{i+1}" for i in x])
axL.set_ylim(0, 18)
axL.legend(fontsize=8, loc="upper left")
axL.grid(axis="x", visible=False)

# ---- ratio vs variance ----------------------------------------------------
kbar = 4.0
var = np.linspace(0, 40, 200)
r = kbar + var / kbar                       # <k^2>/<k> = <k> + Var/<k>
axR.plot(var, r, color=PALETTE[0], lw=2.0)
axR.scatter([0], [4], s=45, color=PALETTE[0], zorder=5)
axR.annotate("homogeneous\nratio = 4", xy=(0, 4), xytext=(3.5, 5.6),
             fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axR.scatter([36], [13], s=45, color=PALETTE[1], zorder=5)
axR.annotate("heterogeneous\nratio = 13", xy=(36, 13), xytext=(21, 10.2),
             fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axR.set_xlabel("degree variance  Var(k)")
axR.set_ylabel(r"$\langle k^2\rangle/\langle k\rangle \ \propto\ R_0$")
axR.set_title("Variance inflates $R_0$", fontsize=10)
axR.set_xlim(0, 40)
axR.set_ylim(3, 14)

fig.tight_layout()
save(fig, "assets/figures/ecological-networks.svg")
