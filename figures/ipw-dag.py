# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Why time-varying confounding needs g-methods. The time-varying covariate L1 is a
confounder of the later treatment A1 (L1 -> A1 and L1 -> Y) and at the same time a
mediator of the earlier treatment A0 (A0 -> L1). Adjusting for L1 to handle the
confounding blocks part of A0's effect and opens collider bias; not adjusting leaves
A1 confounded. No single regression can do both - inverse-probability weighting and
g-estimation are built for exactly this structure."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
fig, ax = plt.subplots(figsize=(7.2, 3.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis("off")

pos = {"L0": (1.0, 1.2), "A0": (2.8, 1.2), "L1": (5.0, 2.6),
       "A1": (6.8, 1.2), "Y": (9.0, 1.2)}
label = {"L0": "$L_0$", "A0": "$A_0$", "L1": "$L_1$", "A1": "$A_1$", "Y": "$Y$"}
special = {"L1": PALETTE[1]}
for name, (x, y) in pos.items():
    col = special.get(name, PALETTE[0])
    ax.add_patch(Circle((x, y), 0.42, facecolor=col, alpha=0.18,
                        edgecolor=col, lw=1.6, zorder=3))
    ax.text(x, y, label[name], ha="center", va="center",
            fontsize=12, color=INK, zorder=4)


def arrow(a, b, color=INK, style="-|>", rad=0.0):
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                 mutation_scale=13, color=color, lw=1.4, shrinkA=16, shrinkB=16,
                 connectionstyle=f"arc3,rad={rad}", zorder=2))


arrow("L0", "A0")
arrow("A0", "L1", color=PALETTE[2])           # A0 affects L1 (mediator path)
arrow("L1", "A1", color=PALETTE[1])           # L1 confounds A1
arrow("A0", "A1", rad=-0.25)
arrow("A1", "Y")
arrow("L1", "Y", color=PALETTE[1], rad=0.15)
arrow("A0", "Y", rad=-0.35, color=MUTED)
arrow("L0", "L1", rad=0.2, color=MUTED)

ax.text(5.0, 3.35, "$L_1$: confounder of $A_1$  AND  mediator of $A_0$",
        ha="center", fontsize=9.2, color=PALETTE[1])
ax.text(3.9, 1.75, "mediator", fontsize=7.6, color=PALETTE[2], rotation=32)
ax.text(5.9, 1.95, "confounder", fontsize=7.6, color=PALETTE[1], rotation=-32)
ax.set_title("Time-varying confounding affected by prior treatment", fontsize=9.8)
fig.tight_layout()
save(fig, "assets/figures/ipw-dag.svg")
