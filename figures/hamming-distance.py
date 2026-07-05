# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""Illustrative diagram of the Hamming distance between two DNA sequences.

Two equal-length genomes are aligned site by site; columns where the letters
disagree are highlighted, and the number of such columns is the Hamming
distance. This is the "number of mutations from the master" coordinate used
by the quasispecies error classes.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from _style import apply_style, save, PALETTE, INK, MUTED
apply_style()

seq1 = list("ACGTACGTAC")   # master sequence
seq2 = list("ACTTAGGTAA")   # a mutant a few steps away
L = len(seq1)
mismatch = [a != b for a, b in zip(seq1, seq2)]
d_H = sum(mismatch)

MATCH_BG = "#eef2f5"
MISS_BG = "#f7e0d3"          # tint of the palette orange
MISS = PALETTE[1]

fig, ax = plt.subplots(figsize=(6.6, 3.2))
ax.set_xlim(-1.4, L)
ax.set_ylim(-1.4, 3.0)
ax.axis("off")

y1, y2 = 1.3, 0.3            # rows for the two sequences


def cell(x, y, letter, differs):
    box = FancyBboxPatch(
        (x + 0.06, y + 0.06), 0.88, 0.88,
        boxstyle="round,pad=0.0,rounding_size=0.12",
        linewidth=1.4,
        edgecolor=MISS if differs else "#c6cfd6",
        facecolor=MISS_BG if differs else MATCH_BG,
    )
    ax.add_patch(box)
    ax.text(x + 0.5, y + 0.5, letter, ha="center", va="center",
            fontsize=15, fontweight="bold",
            color=MISS if differs else INK,
            family="monospace")


for i in range(L):
    cell(i, y1, seq1[i], mismatch[i])
    cell(i, y2, seq2[i], mismatch[i])

# Row labels on the left.
ax.text(-0.2, y1 + 0.5, "master", ha="right", va="center",
        fontsize=11, color=MUTED)
ax.text(-0.2, y2 + 0.5, "mutant", ha="right", va="center",
        fontsize=11, color=MUTED)

# Mismatch markers and a running tally beneath the columns.
seen = 0
for i in range(L):
    if mismatch[i]:
        seen += 1
        ax.text(i + 0.5, -0.35, "✕", ha="center", va="center",
                fontsize=13, color=MISS, fontweight="bold")
        ax.text(i + 0.5, -0.95, str(seen), ha="center", va="center",
                fontsize=10, color=MISS)
    else:
        ax.text(i + 0.5, -0.35, "·", ha="center", va="center",
                fontsize=13, color="#b6c0c8")

ax.text(-0.2, -0.35, "compare", ha="right", va="center",
        fontsize=11, color=MUTED)

ax.text(L / 2, 2.6,
        r"$d_H = $ number of columns that differ $= %d$" % d_H,
        ha="center", va="center", fontsize=13, color=INK)

save(fig, "assets/figures/hamming-distance.svg")
