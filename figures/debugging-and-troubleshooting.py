# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Debugging is a calm, ordered process, not panic-editing. Read the whole error
message, reduce the problem to a minimal reproducible example, isolate the
failure by printing intermediate values, and check the types and shapes of your
data. If it still fails, that same reprex is exactly what you need to search
effectively or ask for help — then you loop back with what you learned."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, INK, MUTED, PALETTE

apply_style()

fig, ax = plt.subplots(figsize=(6.6, 4.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis("off")

steps = [
    ("Read the whole error message", 10.8, PALETTE[0]),
    ("Reproduce it minimally (a reprex)", 9.0, PALETTE[0]),
    ("Isolate: print intermediate values", 7.2, PALETTE[2]),
    ("Check types and shapes", 5.4, PALETTE[2]),
    ("Fixed?", 3.6, PALETTE[3]),
    ("Search / ask — with the reprex", 1.6, PALETTE[1]),
]
for text, y, col in steps:
    diamond = text == "Fixed?"
    w = 3.4 if diamond else 6.6
    ax.add_patch(FancyBboxPatch((5 - w / 2, y - 0.6), w, 1.2,
                 boxstyle="round,pad=0.05", linewidth=1.7, edgecolor=col,
                 facecolor=col + "16"))
    ax.text(5, y, text, ha="center", va="center", fontsize=8.8, color=INK)

for i in range(len(steps) - 1):
    y1 = steps[i][1] - 0.6
    y2 = steps[i + 1][1] + 0.6
    ax.add_patch(FancyArrowPatch((5, y1), (5, y2), arrowstyle="-|>",
                 mutation_scale=14, color="0.4", lw=1.5))

# "yes -> done" off the Fixed? node
ax.add_patch(FancyArrowPatch((6.7, 3.6), (8.6, 3.6), arrowstyle="-|>",
             mutation_scale=13, color=PALETTE[2], lw=1.5))
ax.text(8.7, 3.6, "done", fontsize=8.5, color=PALETTE[2], va="center")
ax.text(5.5, 2.7, "still stuck", fontsize=7.6, color=MUTED)
# loop back from the bottom to "reproduce" with what you learned
ax.add_patch(FancyArrowPatch((1.7, 1.6), (1.7, 9.0), arrowstyle="-|>",
             mutation_scale=13, color=MUTED, lw=1.4,
             connectionstyle="arc3,rad=-0.35"))
ax.text(0.35, 5.4, "loop back with\nwhat you learned", fontsize=7.6,
        color=MUTED, rotation=90, va="center", ha="center")

save(fig, "assets/figures/debugging-and-troubleshooting.svg")
