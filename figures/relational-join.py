# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Relational data, drawn out: two tidy tables that share a key column are
combined with a JOIN. Keeping sample measurements and sample metadata in
separate tables linked by an id -- rather than one giant spreadsheet -- avoids
repetition and errors, and a JOIN stitches them together on demand. This is the
mental model behind both tidy data and SQL.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from _style import apply_style, save, INK

apply_style()

fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.set_xlim(0, 12.7)
ax.set_ylim(0, 10)
ax.axis("off")

KEYCOL = "#2f6f9f"
HEAD = "#26323f"


def table(x, y, title, headers, rows, keycol=0, title_color=HEAD):
    ax.text(x + len(headers) * 0.75, y + 0.55, title, ha="center",
            fontsize=10.5, fontweight="bold", color=title_color)
    cw, rh = 1.5, 0.62
    all_rows = [headers] + rows
    for r, row in enumerate(all_rows):
        yy = y - r * rh
        for c, cell in enumerate(row):
            xx = x + c * cw
            is_head = (r == 0)
            fc = "#e8edf1" if is_head else "white"
            if c == keycol and not is_head:
                fc = KEYCOL + "22"
            ax.add_patch(FancyBboxPatch((xx, yy - rh), cw, rh,
                         boxstyle="round,pad=0.01", linewidth=1.0,
                         edgecolor="#b8c2cc", facecolor=fc))
            ax.text(xx + cw / 2, yy - rh / 2, str(cell), ha="center",
                    va="center", fontsize=8.6,
                    fontweight="bold" if is_head else "normal",
                    color=HEAD if is_head else INK)


# left: measurements
table(0.2, 9.2, "samples", ["id", "Ct"],
      [["S1", "22.4"], ["S2", "19.8"], ["S3", "31.1"]])

# middle: metadata
table(4.0, 9.2, "sites", ["id", "site"],
      [["S1", "clinic A"], ["S2", "clinic B"], ["S3", "clinic A"]])

# right: joined result
table(7.7, 7.4, "samples ⋈ sites   (JOIN on id)", ["id", "Ct", "site"],
      [["S1", "22.4", "clinic A"],
       ["S2", "19.8", "clinic B"],
       ["S3", "31.1", "clinic A"]],
      title_color=KEYCOL)

ax.annotate("", xy=(7.5, 5.8), xytext=(6.9, 7.2),
            arrowprops=dict(arrowstyle="-|>", color=KEYCOL, lw=2.0))
ax.text(3.9, 5.4, "the shaded  id  column is the key both tables share",
        ha="center", color=KEYCOL, fontsize=9, fontweight="bold")

save(fig, "assets/figures/relational-join.svg")
