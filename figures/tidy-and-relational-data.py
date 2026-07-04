# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""A wide table and its tidy long form, drawn side by side.

The wide layout stores one column per week; the tidy long layout puts
the week into a variable column and the count into a value column, so
each row is one observation.
"""
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (ax_w, ax_l) = plt.subplots(1, 2, figsize=(7.6, 3.6))
for ax in (ax_w, ax_l):
    ax.axis("off")
    ax.grid(False)

wide_cols = ["site", "wk1", "wk2"]
wide_rows = [["A", "12", "19"], ["B", "7", "10"]]
long_cols = ["site", "week", "cases"]
long_rows = [
    ["A", "wk1", "12"],
    ["A", "wk2", "19"],
    ["B", "wk1", "7"],
    ["B", "wk2", "10"],
]


def draw_table(ax, col_labels, rows, header_color):
    tbl = ax.table(cellText=rows, colLabels=col_labels,
                   cellLoc="center", loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1, 1.6)
    for (r, _), cell in tbl.get_celld().items():
        cell.set_edgecolor("#d8dee4")
        if r == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(color="white")
        else:
            cell.set_facecolor("white")
            cell.set_text_props(color=INK)


draw_table(ax_w, wide_cols, wide_rows, PALETTE[1])
draw_table(ax_l, long_cols, long_rows, PALETTE[0])
ax_w.set_title("Wide: a column per week", color=INK)
ax_l.set_title("Long (tidy): one row per observation", color=INK)

fig.text(0.5, 0.5, "pivot\nlonger", ha="center", va="center",
         color=MUTED, fontsize=11)
fig.suptitle("Reshaping wide to long", color=INK)
fig.tight_layout()
print("wide rows:", len(wide_rows), "long rows:", len(long_rows))
save(fig, "assets/figures/tidy-and-relational-data.svg")
