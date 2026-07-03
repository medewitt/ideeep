# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""A race condition, drawn out. Two threads each try to add 1 to a shared
counter. Because "read, add, write" is not atomic, both can read the same old
value before either writes back -- so one update is silently lost and two
increments produce a final count of 1 instead of 2. This is why shared mutable
state needs locks, and why parallel bugs are so hard to reproduce.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from _style import apply_style, save, INK

apply_style()

fig, ax = plt.subplots(figsize=(6.8, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

GREEN, RED, BLUE = "#3f8f5b", "#b0332f", "#2f6f9f"


def box(x, y, w, h, text, color):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                 boxstyle="round,pad=0.08", linewidth=1.4,
                 edgecolor=color, facecolor=color + "22"))
    ax.text(x, y, text, ha="center", va="center", fontsize=8.8, color=INK)


# lane headers
ax.text(2.2, 9.4, "Thread A", ha="center", fontsize=11, fontweight="bold", color=BLUE)
ax.text(5.7, 9.4, "Thread B", ha="center", fontsize=11, fontweight="bold", color="#8a5cb0")
ax.text(8.7, 9.4, "shared\ncount", ha="center", fontsize=10, fontweight="bold", color=INK)

# time arrow
ax.annotate("", xy=(0.5, 0.6), xytext=(0.5, 9.0),
            arrowprops=dict(arrowstyle="->", color="0.5", lw=1.4))
ax.text(0.32, 5.0, "time", rotation=90, va="center", color="0.5", fontsize=9)

# shared-count track values after each step
for y, val, col in [(8.2, "0", "0.4"), (6.6, "0", "0.4"),
                    (5.0, "1", GREEN), (3.4, "1", RED)]:
    ax.text(8.7, y, val, ha="center", va="center", fontsize=13,
            fontweight="bold", color=col)

# the interleaved operations
box(2.2, 8.2, 3.0, 0.9, "read count → sees 0", BLUE)
box(5.7, 6.6, 3.0, 0.9, "read count → sees 0", "#8a5cb0")
box(2.2, 5.0, 3.0, 0.9, "write 0 + 1 → 1", GREEN)
box(5.7, 3.4, 3.0, 0.9, "write 0 + 1 → 1", RED)

ax.annotate("both read the SAME old value",
            xy=(5.7, 6.6), xytext=(3.0, 7.4), fontsize=8.5, color="0.35",
            arrowprops=dict(arrowstyle="->", color="0.55", lw=1.0))
ax.annotate("this update is lost!",
            xy=(7.2, 3.4), xytext=(6.3, 2.1), fontsize=9, color=RED,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

ax.text(5.0, 0.7, "Two increments, but count = 1, not 2 — a race condition.",
        ha="center", fontsize=9.5, fontweight="bold", color=RED)

save(fig, "assets/figures/race-condition.svg")
