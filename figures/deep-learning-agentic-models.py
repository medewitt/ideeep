# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""An agentic model is a language model placed in a loop with tools. It reasons
about a goal, calls a tool (query a line list, run an Rt model, search the
literature), observes the result, and repeats until the task is done -- then
hands a human the draft. The intelligence is old-fashioned; the leverage is the
loop and the tools it can reach.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, INK

apply_style()

BLUE, GREEN, ORANGE, PURPLE = "#2f6f9f", "#3f8f5b", "#c1531f", "#8a5cb0"

fig, ax = plt.subplots(figsize=(8.2, 4.6))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis("off")


def box(x, y, w, h, text, color, fs=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                 linewidth=1.8, edgecolor=color, facecolor=color + "16"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=INK)


box(5.0, 6.7, 4.0, 1.7, "Goal\n\"is county X aberrant?\"", INK, fs=9.5)
box(0.6, 3.4, 4.2, 1.9, "LLM agent\nreason · plan · decide", BLUE)
box(9.2, 3.4, 4.2, 1.9, "Tools\nSQL · $R_t$ model · maps · search", GREEN)
box(5.0, 0.4, 4.0, 1.7, "Draft brief\nfor a human to check", ORANGE)

# goal -> agent
ax.add_patch(FancyArrowPatch((5.2, 6.8), (3.0, 5.35), arrowstyle="-|>",
             mutation_scale=16, color="0.45", lw=1.7))
# agent -> tools (act)
ax.add_patch(FancyArrowPatch((4.9, 4.7), (9.1, 4.7), arrowstyle="-|>",
             mutation_scale=16, color=ORANGE, lw=1.9))
ax.text(7.0, 5.0, "call a tool", ha="center", fontsize=8.8, color=INK,
        fontweight="bold")
# tools -> agent (observe)
ax.add_patch(FancyArrowPatch((9.1, 3.9), (4.9, 3.9), arrowstyle="-|>",
             mutation_scale=16, color=GREEN, lw=1.9))
ax.text(7.0, 3.45, "observe result", ha="center", fontsize=8.8, color=INK)
# loop label
ax.text(7.0, 2.55, "repeat until confident", ha="center", fontsize=8.5,
        color=PURPLE, style="italic")
# agent -> draft
ax.add_patch(FancyArrowPatch((3.0, 3.35), (5.2, 1.9), arrowstyle="-|>",
             mutation_scale=16, color="0.45", lw=1.7))
# human-in-the-loop emphasis
ax.add_patch(FancyArrowPatch((7.0, 0.35), (7.0, -0.05), arrowstyle="-",
             color="0.45", lw=0.1))

fig.suptitle("An agent = a model in a loop with tools", y=0.99, fontsize=12,
             color=INK)
save(fig, "assets/figures/deep-learning-agentic-models.svg")
