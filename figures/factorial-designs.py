# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Why factorial designs beat one-factor-at-a-time. Left: an interaction plot of
the worked 2x2 corner means — the response vs A at low B and at high B are two
non-parallel lines, and the gap between their slopes is the AB interaction (5):
the boost from A is larger when B is high. Right: the factorial design visits all
four corners of the (A,B) square, so the (+,+) combination that reveals the
interaction is measured, whereas an OFAT path never leaves the low level of the
other factor and misses it."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# corner means y[(A,B)]
y = {(-1, -1): 20, (1, -1): 30, (-1, 1): 25, (1, 1): 45}

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.7))

# ---- interaction plot -----------------------------------------------------
A = [-1, 1]
axL.plot(A, [y[(-1, -1)], y[(1, -1)]], color=PALETTE[0], lw=2.0, marker="o",
         ms=6, label="B low")
axL.plot(A, [y[(-1, 1)], y[(1, 1)]], color=PALETTE[1], lw=2.0, marker="s",
         ms=6, label="B high")
for (a, b), val in y.items():
    axL.annotate(f"{val}", (a, val), textcoords="offset points",
                 xytext=(6, -4), fontsize=8.5, color=INK)
# non-parallel slopes => interaction
axL.annotate("non-parallel lines\n= interaction (AB = 5)", xy=(1, 45),
             xytext=(-0.95, 40), fontsize=8.3, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axL.set_xlabel("factor $A$")
axL.set_ylabel("mean response")
axL.set_xticks([-1, 1])
axL.set_xticklabels(["low (−1)", "high (+1)"])
axL.set_title("Interaction plot", fontsize=10)
axL.set_ylim(15, 50)
axL.legend(fontsize=8.5, title="factor $B$", title_fontsize=8.5)

# ---- factorial square vs OFAT ---------------------------------------------
axR.set_xlim(-1.8, 1.8)
axR.set_ylim(-1.8, 2.0)
axR.set_aspect("equal")
axR.axis("off")
axR.set_title("Full factorial vs OFAT", fontsize=10)

# square edges
for (x1, y1, x2, y2) in [(-1, -1, 1, -1), (1, -1, 1, 1), (1, 1, -1, 1),
                         (-1, 1, -1, -1)]:
    axR.plot([x1, x2], [y1, y2], color=MUTED, lw=1.0, ls=":", zorder=1)
# OFAT path: (-,-) -> (+,-) -> ... stays, never reaches (+,+)
axR.add_patch(FancyArrowPatch((-1, -1), (1, -1), arrowstyle="-|>",
              mutation_scale=14, color=PALETTE[3], lw=2.0))
axR.add_patch(FancyArrowPatch((-1, -1), (-1, 1), arrowstyle="-|>",
              mutation_scale=14, color=PALETTE[3], lw=2.0))
axR.text(0, -1.55, "OFAT path", color=PALETTE[3], fontsize=8.5, ha="center")

for (a, b), lab in [((-1, -1), "(−,−)"), ((1, -1), "(+,−)"),
                    ((-1, 1), "(−,+)"), ((1, 1), "(+,+)")]:
    filled = True
    col = PALETTE[0]
    axR.scatter([a], [b], s=140, color=col, zorder=5)
    axR.annotate(lab, (a, b), textcoords="offset points", xytext=(0, 11),
                 ha="center", fontsize=8.3, color=INK)
axR.annotate("factorial also\nmeasures here", xy=(1, 1), xytext=(0.1, 1.6),
             fontsize=8, color=PALETTE[0],
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axR.text(0, -1.9, "OFAT never visits the (+,+) corner",
         fontsize=8, color=INK, ha="center")
axR.set_xlabel("")

fig.tight_layout()
save(fig, "assets/figures/factorial-designs.svg")
