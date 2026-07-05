# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Schematic of the RCCE communication continuum: one-way -> two-way -> three-way."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, ax = plt.subplots(figsize=(7.6, 3.6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.set_aspect("equal")
ax.axis("off")

stages = [
    (2.0, "One-way\ndissemination", "Authority broadcasts;\nno reply expected", PALETTE[0]),
    (6.0, "Two-way\ndialogue", "Community questions\nshape the message", PALETTE[2]),
    (10.0, "Three-way\ncommunity\nparticipation", "Affected people\nco-design the response", PALETTE[3]),
]

node_y = 4.1
node_r = 0.55

# background progression bar showing increasing engagement
ax.annotate(
    "", xy=(11.4, 1.15), xytext=(0.6, 1.15),
    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4),
)
ax.text(6.0, 0.6, "increasing engagement and participation",
        ha="center", va="center", fontsize=9.5, color=MUTED, style="italic")

for i, (x, title, sub, color) in enumerate(stages):
    # authority node (top) and community node (bottom) for each stage
    auth = (x, node_y + 0.0)
    comm = (x, node_y - 1.9)

    ax.add_patch(Circle(auth, node_r, facecolor=color, edgecolor="white", lw=1.5, zorder=4))
    ax.add_patch(Circle(comm, node_r * 0.85, facecolor="white", edgecolor=color, lw=1.8, zorder=4))
    ax.text(auth[0], auth[1], "A", ha="center", va="center", color="white",
            fontsize=10, fontweight="bold", zorder=5)
    ax.text(comm[0], comm[1], "C", ha="center", va="center", color=color,
            fontsize=10, fontweight="bold", zorder=5)

    top = (auth[0], auth[1] - node_r)
    bot = (comm[0], comm[1] + node_r * 0.85)

    if i == 0:
        # single arrow: one-way push down to community
        ax.add_patch(FancyArrowPatch(top, bot, arrowstyle="-|>",
                     mutation_scale=16, color=color, lw=2.0, zorder=3))
    elif i == 1:
        # double-headed arrow: dialogue both ways
        lx = x - 0.22
        rx = x + 0.22
        ax.add_patch(FancyArrowPatch((lx, top[1]), (lx, bot[1]), arrowstyle="-|>",
                     mutation_scale=14, color=color, lw=2.0, zorder=3))
        ax.add_patch(FancyArrowPatch((rx, bot[1]), (rx, top[1]), arrowstyle="-|>",
                     mutation_scale=14, color=color, lw=2.0, zorder=3))
    else:
        # double-headed arrow plus among-community loop
        lx = x - 0.22
        rx = x + 0.22
        ax.add_patch(FancyArrowPatch((lx, top[1]), (lx, bot[1]), arrowstyle="-|>",
                     mutation_scale=14, color=color, lw=2.0, zorder=3))
        ax.add_patch(FancyArrowPatch((rx, bot[1]), (rx, top[1]), arrowstyle="-|>",
                     mutation_scale=14, color=color, lw=2.0, zorder=3))
        # community peers reached and a small loop among them
        peers = [(x - 1.05, comm[1]), (x + 1.05, comm[1])]
        for px, py in peers:
            ax.add_patch(Circle((px, py), node_r * 0.7, facecolor="white",
                         edgecolor=color, lw=1.6, zorder=4))
            ax.text(px, py, "C", ha="center", va="center", color=color,
                    fontsize=9, fontweight="bold", zorder=5)
        ax.add_patch(FancyArrowPatch((comm[0] - node_r * 0.85, comm[1]),
                     (peers[0][0] + node_r * 0.7, peers[0][1]), arrowstyle="<|-|>",
                     mutation_scale=11, color=color, lw=1.6, zorder=3))
        ax.add_patch(FancyArrowPatch((comm[0] + node_r * 0.85, comm[1]),
                     (peers[1][0] - node_r * 0.7, peers[1][1]), arrowstyle="<|-|>",
                     mutation_scale=11, color=color, lw=1.6, zorder=3))

    ax.text(x, node_y + node_r + 0.55, title, ha="center", va="bottom",
            fontsize=10.5, fontweight="bold", color=INK)
    ax.text(x, comm[1] - node_r - 0.35, sub, ha="center", va="top",
            fontsize=8.2, color=MUTED)

# stage-to-stage progression arrows between the top nodes
for (x0, *_), (x1, *_) in zip(stages[:-1], stages[1:]):
    ax.add_patch(FancyArrowPatch((x0 + node_r + 0.15, node_y),
                 (x1 - node_r - 0.15, node_y), arrowstyle="-|>",
                 mutation_scale=16, color=INK, lw=1.2, zorder=2,
                 connectionstyle="arc3,rad=0.0"))

ax.set_title("The risk-communication continuum", fontsize=12, pad=6)

save(fig, "assets/figures/rcce-communication-continuum.svg")
