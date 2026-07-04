# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""A schematic project directory tree, drawn as text (not a real listing).

The layout keeps raw data read-only, separates code from outputs, and
uses relative paths inside the project root so it moves between machines
unchanged.
"""
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# (indent level, label, is_dir)
tree = [
    (0, "project/", True),
    (1, "data/", True),
    (2, "raw/        (read-only inputs)", False),
    (2, "clean/      (derived, regenerated)", False),
    (1, "R/", True),
    (2, "01-clean.R", False),
    (2, "02-model.R", False),
    (1, "figures/    (*.py -> *.svg)", True),
    (1, "results/", True),
    (1, "README.md", False),
]

fig, ax = plt.subplots(figsize=(6.6, 4.0))
ax.axis("off")
ax.grid(False)

n = len(tree)
for i, (indent, label, is_dir) in enumerate(tree):
    y = n - i
    x = 0.06 + indent * 0.10
    color = PALETTE[0] if is_dir else INK
    weight = "bold" if is_dir else "normal"
    if indent > 0:
        ax.plot([x - 0.045, x - 0.015], [y, y], color=MUTED, lw=0.8)
    ax.text(x, y, label, color=color, fontweight=weight,
            family="monospace", fontsize=11, va="center")

ax.set_xlim(0, 1)
ax.set_ylim(0.4, n + 0.6)
ax.set_title("A project as a directory tree", color=INK)
print("entries:", n, "directories:", sum(1 for t in tree if t[2]))
save(fig, "assets/figures/plain-text-and-filesystems.svg")
