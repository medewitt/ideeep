"""Shared plotting style for site figures.

Imported by the individual figure scripts. Keeps a consistent, clean look:
transparent background (so figures sit on the page background), a muted
palette, dark slate ink that reads on the light site, and no chartjunk.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt

INK = "#26323f"        # axes, text
MUTED = "#5b6b7a"      # secondary
PALETTE = ["#2f6f9f", "#c1531f", "#3f8f5b", "#8a5cb0", "#b0842f"]


def apply_style():
    mpl.rcParams.update({
        "figure.figsize": (6.2, 3.8),
        "figure.dpi": 110,
        "savefig.transparent": True,
        "savefig.bbox": "tight",
        "font.size": 11,
        "font.family": "sans-serif",
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "axes.linewidth": 0.9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#d8dee4",
        "grid.linewidth": 0.6,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.prop_cycle": mpl.cycler(color=PALETTE),
        "legend.frameon": False,
    })


def save(fig, path):
    fig.savefig(path, format="svg")
    plt.close(fig)
    print("wrote", path)
