# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Dynamic programming, made concrete: global sequence alignment
(Needleman-Wunsch). Each cell holds the best score for aligning the prefixes
of the two sequences, and is filled once from three neighbours it already
knows. The optimal alignment is read back by tracing the path of best choices
from the bottom-right corner to the top-left -- the essence of DP.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save

apply_style()

A = "GCATGCU"      # columns
B = "GATTACA"      # rows
MATCH, MISMATCH, GAP = 1, -1, -1

n, m = len(B), len(A)
H = np.zeros((n + 1, m + 1), dtype=int)
H[0, :] = np.arange(0, -(m + 1), -1)
H[:, 0] = np.arange(0, -(n + 1), -1)
for i in range(1, n + 1):
    for j in range(1, m + 1):
        s = MATCH if B[i - 1] == A[j - 1] else MISMATCH
        H[i, j] = max(H[i - 1, j - 1] + s, H[i - 1, j] + GAP, H[i, j - 1] + GAP)

# traceback from the bottom-right corner
path = [(n, m)]
i, j = n, m
while (i, j) != (0, 0):
    if i > 0 and j > 0:
        s = MATCH if B[i - 1] == A[j - 1] else MISMATCH
        if H[i, j] == H[i - 1, j - 1] + s:
            i, j = i - 1, j - 1
        elif H[i, j] == H[i - 1, j] + GAP:
            i = i - 1
        else:
            j = j - 1
    elif i > 0:
        i = i - 1
    else:
        j = j - 1
    path.append((i, j))

fig, ax = plt.subplots(figsize=(6.4, 5.2))
ax.imshow(H, cmap="BuGn", origin="upper", alpha=0.85)

for i in range(n + 1):
    for j in range(m + 1):
        ax.text(j, i, str(H[i, j]), ha="center", va="center",
                fontsize=10, color="#26323f")

pr = [p[0] for p in path]
pc = [p[1] for p in path]
ax.plot(pc, pr, color="#b0332f", lw=2.4, marker="o", ms=7,
        markerfacecolor="#b0332f", zorder=5, label="optimal traceback")

ax.set_xticks(range(m + 1))
ax.set_xticklabels(["–"] + list(A))
ax.set_yticks(range(n + 1))
ax.set_yticklabels(["–"] + list(B))
ax.set_xlabel("sequence A")
ax.set_ylabel("sequence B")
ax.xaxis.set_label_position("top")
ax.xaxis.tick_top()
ax.set_title("Sequence alignment as dynamic programming", pad=28)
ax.grid(False)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.legend(loc="lower left", bbox_to_anchor=(0.0, -0.14), fontsize="small")

save(fig, "assets/figures/dynamic-programming-alignment.svg")
