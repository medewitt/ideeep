# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""A regular expression IS a finite-state machine. This one recognizes a
sample accession like WF0231 -- the pattern WF\\d+. The machine reads the text
one character at a time, moving between a finite set of states; if it ends in
the double-circled accept state, the string matched. Seeing regex this way
explains both why it is fast (a single left-to-right scan) and why it cannot
handle nested structure (a finite machine can't count).
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from _style import apply_style, save, INK

apply_style()

fig, ax = plt.subplots(figsize=(7.2, 3.2))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5)
ax.axis("off")
ax.set_aspect("equal")

BLUE, GREEN = "#2f6f9f", "#3f8f5b"
states = {"q0": (1.6, 2.5), "q1": (4.4, 2.5), "q2": (7.2, 2.5), "q3": (10.0, 2.5)}
labels = {"q0": "start", "q1": "W", "q2": "WF", "q3": "WF\\d⁺"}

for name, (x, y) in states.items():
    accept = name == "q3"
    ax.add_patch(Circle((x, y), 0.62, facecolor="white",
                 edgecolor=GREEN if accept else BLUE, linewidth=1.8, zorder=3))
    if accept:
        ax.add_patch(Circle((x, y), 0.5, facecolor="none",
                     edgecolor=GREEN, linewidth=1.5, zorder=3))
    ax.text(x, y, labels[name], ha="center", va="center", fontsize=9.5,
            color=INK, zorder=4)


def arrow(p, q, text, rad=0.0):
    a = FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}",
                        arrowstyle="-|>", mutation_scale=16,
                        color="0.35", lw=1.5, zorder=2)
    ax.add_patch(a)
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    ax.text(mx, my + (0.55 if rad == 0 else 1.15), text, ha="center",
            fontsize=10, color=INK, fontweight="bold")


# start arrow
ax.add_patch(FancyArrowPatch((0.4, 2.5), (0.95, 2.5), arrowstyle="-|>",
             mutation_scale=16, color="0.35", lw=1.5))

arrow((2.25, 2.5), (3.75, 2.5), "W")
arrow((5.05, 2.5), (6.55, 2.5), "F")
arrow((7.85, 2.5), (9.35, 2.5), "0–9")

# self-loop on accept state (another digit)
loop = FancyArrowPatch((9.7, 3.05), (10.3, 3.05),
                       connectionstyle="arc3,rad=-2.2", arrowstyle="-|>",
                       mutation_scale=14, color="0.35", lw=1.5)
ax.add_patch(loop)
ax.text(10.0, 4.35, "0–9", ha="center", fontsize=10, color=INK, fontweight="bold")

ax.text(6.0, 0.55, r"regex:  WF\d+     — reads one character at a time, "
        "left to right", ha="center", fontsize=9.5, color="0.4", style="italic")
ax.set_title("A regular expression is a finite-state machine", y=1.0)

save(fig, "assets/figures/finite-state-machine.svg")
