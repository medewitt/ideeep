# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""The E-value bias plot. To explain away an observed risk ratio of 1.8, an
unmeasured confounder would need associations with both the exposure and the
outcome lying on or above the curve. The E-value is the point where the two
required associations are equal (both 3.0): a confounder weaker than that on either
axis cannot account for the finding. The dashed curve is the weaker requirement to
shift the confidence-interval bound to the null."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()


def evalue(rr):
    return rr + np.sqrt(rr * (rr - 1))


def curve(rr, ru):
    return rr * (ru - 1) / (ru - rr)          # required confounder-outcome assoc


rr_pt, rr_ci = 1.8, 1.3
E_pt, E_ci = evalue(rr_pt), evalue(rr_ci)

fig, ax = plt.subplots(figsize=(5.8, 4.6))
ru = np.linspace(rr_pt + 0.01, 9, 400)
ax.plot(ru, curve(rr_pt, ru), color=PALETTE[0], lw=2.4,
        label=f"explains away RR = {rr_pt}")
ru2 = np.linspace(rr_ci + 0.01, 9, 400)
ax.plot(ru2, curve(rr_ci, ru2), color=PALETTE[1], lw=1.8, ls="--",
        label=f"shifts CI bound ({rr_ci}) to null")
ax.fill_between(ru, curve(rr_pt, ru), 9, color=PALETTE[0], alpha=0.10)

ax.scatter([E_pt], [E_pt], s=90, color=PALETTE[0], zorder=5, edgecolor="white")
ax.annotate(f"E-value = {E_pt:.1f}", xy=(E_pt, E_pt), xytext=(E_pt + 0.6, E_pt + 1.4),
            fontsize=9, color=INK, arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
ax.scatter([E_ci], [E_ci], s=70, color=PALETTE[1], zorder=5, edgecolor="white")
ax.annotate(f"E-value (CI) = {E_ci:.2f}", xy=(E_ci, E_ci), xytext=(E_ci + 0.5, E_ci - 1.2),
            fontsize=8.4, color=PALETTE[1],
            arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.9))
ax.plot([1, 9], [1, 9], color=MUTED, lw=0.8, ls=":")

ax.set_xlabel("confounder–exposure association  $RR_{EU}$")
ax.set_ylabel("confounder–outcome association  $RR_{UD}$")
ax.set_title("What a confounder would need to explain away the effect", fontsize=9.2)
ax.set_xlim(1, 9)
ax.set_ylim(1, 9)
ax.legend(fontsize=8.2, loc="upper right")
fig.tight_layout()
save(fig, "assets/figures/evalue-biasplot.svg")
