# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""The competing-risks multi-state picture. A subject starts at risk and can move
to exactly one of two absorbing states, each governed by its own cause-specific
hazard. Because entering one state removes the subject from risk of the other, the
events compete: you cannot treat the other event as ordinary censoring, and each
cause needs its own cumulative incidence function."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from _style import apply_style, save, PALETTE, INK

apply_style()
fig, ax = plt.subplots(figsize=(6.8, 3.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis("off")


def box(x, y, w, h, text, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                 facecolor=color, alpha=0.16, edgecolor=color, lw=1.6))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5,
            color=INK)


box(0.4, 1.4, 2.6, 1.2, "at risk\n(infected, admitted)", PALETTE[0])
box(6.6, 2.5, 3.0, 1.1, "died of infection", PALETTE[1])
box(6.6, 0.3, 3.0, 1.1, "discharged / other cause", PALETTE[2])

ax.add_patch(FancyArrowPatch((3.0, 2.1), (6.6, 3.05), arrowstyle="-|>",
             mutation_scale=15, color=PALETTE[1], lw=1.8))
ax.add_patch(FancyArrowPatch((3.0, 1.9), (6.6, 0.85), arrowstyle="-|>",
             mutation_scale=15, color=PALETTE[2], lw=1.8))
ax.text(4.7, 2.95, "cause-specific hazard  $\\lambda_1(t)$", fontsize=8.6,
        color=PALETTE[1], rotation=15)
ax.text(4.7, 1.05, "cause-specific hazard  $\\lambda_2(t)$", fontsize=8.6,
        color=PALETTE[2], rotation=-15)
ax.text(5.0, 3.7, "entering one state removes the subject from risk of the other",
        ha="center", fontsize=8.4, color=INK, style="italic")
fig.tight_layout()
save(fig, "assets/figures/competing-risks-states.svg")
