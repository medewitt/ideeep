# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""A split-plot layout. The field is divided into whole plots that receive the
hard-to-change factor (irrigation, shaded bands), each subdivided into sub-plots
that receive the easy-to-change factor (variety, letters). The whole-plot factor
is judged against variation between whole plots; the sub-plot factor and the
interaction against the smaller variation between sub-plots within a whole plot."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, ax = plt.subplots(figsize=(6.8, 3.9))
ax.set_xlim(0, 6)
ax.set_ylim(0, 4.6)
ax.axis("off")

# two irrigation levels (whole-plot bands), three fields (whole plots) each
irr_colors = [PALETTE[0], PALETTE[1]]
irr_labels = ["irrigation $-$", "irrigation $+$"]
varieties = ["V$-$", "V$+$"]

x = 0.4
for f in range(6):                       # 6 whole plots (fields): 3 per irrigation
    irr = 0 if f < 3 else 1
    # whole-plot shaded band
    ax.add_patch(Rectangle((x, 0.5), 0.82, 3.4, facecolor=irr_colors[irr],
                           alpha=0.16, edgecolor=irr_colors[irr], lw=1.4))
    # two sub-plots inside
    for s, v in enumerate(varieties):
        y0 = 0.5 + s * 1.7
        ax.add_patch(Rectangle((x + 0.06, y0 + 0.08), 0.70, 1.5,
                               facecolor="none", edgecolor=MUTED, lw=0.9, ls="--"))
        ax.text(x + 0.41, y0 + 0.83, v, ha="center", va="center", fontsize=9,
                color=INK)
    x += 0.92

# irrigation labels above the bands
ax.text(0.4 + 1.38, 4.15, irr_labels[0], ha="center", fontsize=9.5,
        color=irr_colors[0])
ax.text(0.4 + 1.38 + 2.76, 4.15, irr_labels[1], ha="center", fontsize=9.5,
        color=irr_colors[1])

ax.annotate("whole plot (field)\n= irrigation error scale", xy=(0.9, 0.5),
            xytext=(0.3, 0.02), fontsize=8.2, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
ax.annotate("sub-plot (variety)\n= smaller error scale", xy=(4.7, 2.3),
            xytext=(3.9, 0.02), fontsize=8.2, color=INK,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

fig.tight_layout()
save(fig, "assets/figures/split-plot-designs.svg")
