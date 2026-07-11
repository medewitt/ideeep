# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""How files are found. Storage is a tree of nested folders, and every file has
a path. An absolute path starts at the root and works from anywhere; a relative
path is interpreted from the current working directory. Here the same target,
cases.csv, is reached two ways: by the absolute path from the root, and by the
short relative path data/cases.csv from the highlighted working directory."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, INK, MUTED, PALETTE

apply_style()

fig, ax = plt.subplots(figsize=(8.0, 4.4))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis("off")

FOLDER, FILE, CWD, TARGET = PALETTE[0], MUTED, PALETTE[2], PALETTE[1]

# tree nodes: (label, x, y, kind)  kind in {folder, cwd, file, target}
nodes = {
    "/": (0.6, 8.6, "folder"),
    "home/": (2.2, 7.2, "folder"),
    "alice/": (3.8, 5.8, "folder"),
    "projects/": (5.4, 4.4, "folder"),
    "flu-study/": (7.0, 3.0, "cwd"),
    "data/": (8.6, 1.6, "folder"),
    "cases.csv": (10.4, 0.5, "target"),
}
edges = [("/", "home/"), ("home/", "alice/"), ("alice/", "projects/"),
         ("projects/", "flu-study/"), ("flu-study/", "data/"),
         ("data/", "cases.csv")]
colmap = {"folder": FOLDER, "cwd": CWD, "file": FILE, "target": TARGET}

for a, b in edges:
    (x1, y1, _), (x2, y2, _) = nodes[a], nodes[b]
    ax.plot([x1 + 0.5, x2 + 0.2], [y1, y2 + 0.25], color="#c9d2da", lw=1.0,
            zorder=1)

for label, (x, y, kind) in nodes.items():
    col = colmap[kind]
    ax.add_patch(FancyBboxPatch((x, y - 0.28), 1.7, 0.72,
                 boxstyle="round,pad=0.04", linewidth=1.6, edgecolor=col,
                 facecolor=col + ("2e" if kind != "file" else "18")))
    ax.text(x + 0.85, y + 0.08, label, ha="center", va="center", fontsize=8.4,
            color=INK)

# working-directory marker
ax.annotate("working directory\n(you are here)", xy=(7.85, 3.0),
            xytext=(3.4, 2.2), fontsize=8, color=CWD,
            arrowprops=dict(arrowstyle="->", color=CWD, lw=1.1))

# the two paths to the same file
ax.text(0.4, 9.6, "absolute path — from the root, works anywhere:",
        fontsize=8.5, color=TARGET)
ax.text(0.6, 9.1, "/home/alice/projects/flu-study/data/cases.csv",
        fontsize=8.2, color=INK, family="monospace")
ax.text(6.6, 6.0, "relative path — from the working directory:", fontsize=8.5,
        color=CWD)
ax.text(6.8, 5.5, "data/cases.csv", fontsize=8.6, color=INK, family="monospace")
ax.add_patch(FancyArrowPatch((8.0, 5.35), (9.6, 0.8), arrowstyle="-|>",
             mutation_scale=13, color=CWD, lw=1.3,
             connectionstyle="arc3,rad=0.3"))

save(fig, "assets/figures/computer-basics.svg")
