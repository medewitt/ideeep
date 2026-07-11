# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""An analysis pipeline as a directed acyclic graph. Raw data feeds cleaning,
cleaning feeds fitting, fitting feeds forecasting and figures — each step
depends only on earlier ones. When a single input changes (here the raw case
file), a build tool re-runs only the downstream targets it makes stale and
skips everything upstream, so `make` reproduces the result with one command
without redoing unaffected work."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, INK, MUTED, PALETTE

apply_style()

fig, ax = plt.subplots(figsize=(8.6, 3.4))
ax.set_xlim(0, 20)
ax.set_ylim(0, 6)
ax.axis("off")

CHANGED, REBUILD, SKIP = PALETTE[1], "#c1531f", MUTED
nodes = [
    ("raw/\ncases.csv", 0.6, "changed"),
    ("01-clean", 3.4, "rebuild"),
    ("derived/\nclean.csv", 6.2, "rebuild"),
    ("02-fit", 9.0, "rebuild"),
    ("model.rds", 11.8, "rebuild"),
    ("03-forecast", 14.6, "rebuild"),
    ("figures/\nforecast.png", 17.4, "rebuild"),
]
style = {
    "changed": (PALETTE[1], PALETTE[1] + "33", "changed input"),
    "rebuild": (PALETTE[3], PALETTE[3] + "20", "re-run (stale)"),
}
w, h, y = 2.4, 1.5, 2.3
centers = []
for text, x, kind in nodes:
    edge, face, _ = style[kind]
    is_script = "-" in text and "/" not in text
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.06" if not is_script else "sawtooth,pad=0.04",
                 linewidth=1.8, edgecolor=edge, facecolor=face))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8,
            color=INK)
    centers.append(x + w)
for i in range(len(nodes) - 1):
    x1 = nodes[i][1] + w
    x2 = nodes[i + 1][1]
    ax.add_patch(FancyArrowPatch((x1, y + h / 2), (x2, y + h / 2),
                 arrowstyle="-|>", mutation_scale=13, color="0.4", lw=1.5))

ax.annotate("edit one input…", xy=(1.8, y + h), xytext=(1.0, 4.7), fontsize=8.5,
            color=PALETTE[1], arrowprops=dict(arrowstyle="->", color=PALETTE[1],
            lw=1.0))
ax.text(10.5, 0.9, "make re-runs only the downstream targets it makes stale; "
        "unaffected work is skipped", ha="center", fontsize=8.5, color=INK,
        style="italic")

# legend
ax.add_patch(FancyBboxPatch((0.6, 5.1), 0.5, 0.4, boxstyle="round,pad=0.02",
             edgecolor=PALETTE[1], facecolor=PALETTE[1] + "33"))
ax.text(1.3, 5.3, "changed", fontsize=8, va="center", color=INK)
ax.add_patch(FancyBboxPatch((4.2, 5.1), 0.5, 0.4, boxstyle="round,pad=0.02",
             edgecolor=PALETTE[3], facecolor=PALETTE[3] + "20"))
ax.text(4.9, 5.3, "rebuilt (downstream)", fontsize=8, va="center", color=INK)

save(fig, "assets/figures/project-workflow.svg")
