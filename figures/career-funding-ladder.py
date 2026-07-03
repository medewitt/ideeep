# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""A rough map of US fellowship and grant mechanisms across the research career."""
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

NIH, NSF, PVT = PALETTE[0], PALETTE[2], PALETTE[3]

# (label, start_year, end_year, color)  -- years since starting the PhD
mechanisms = [
    ("NSF GRFP",            0,  3, NSF),
    ("NIH F31 (predoc)",    2,  5, NIH),
    ("Foundation predoc",   1,  4, PVT),
    ("NIH F32 (postdoc)",   6,  9, NIH),
    ("NIH K99/R00",         7, 11, NIH),
    ("HHMI / BWF postdoc",  6, 10, PVT),
    ("NIH K08/K23",        10, 15, NIH),
    ("NSF CAREER",         11, 16, NSF),
    ("NIH R01",            12, 20, NIH),
]

fig, ax = plt.subplots(figsize=(7.4, 4.0))
ax.grid(axis="y", visible=False)
for i, (label, x0, x1, color) in enumerate(mechanisms):
    y = len(mechanisms) - i
    ax.barh(y, x1 - x0, left=x0, height=0.62, color=color, alpha=0.85)
    ax.text(x0 + 0.15, y, label, va="center", ha="left", fontsize=8.5, color="white")

# Career-stage bands
bands = [(0, 5.5, "PhD"), (5.5, 11, "postdoc"), (11, 20, "early faculty")]
for x0, x1, name in bands:
    ax.axvspan(x0, x1, color="#eef1f4", zorder=0)
    ax.text((x0 + x1) / 2, len(mechanisms) + 0.7, name, ha="center",
            va="bottom", fontsize=9, color=MUTED)
for x in (5.5, 11):
    ax.axvline(x, color="#c9d3db", lw=0.8, zorder=0)

ax.set_yticks([])
ax.set_xlim(0, 20)
ax.set_ylim(0.3, len(mechanisms) + 1.4)
ax.set_xlabel("approximate years since starting the PhD")
ax.set_title("A funding ladder through the research career")
ax.legend(handles=[Patch(color=NIH, label="NIH"), Patch(color=NSF, label="NSF"),
                   Patch(color=PVT, label="foundation / private")],
          loc="lower right", fontsize=8.5)
save(fig, "assets/figures/career-funding-ladder.svg")
