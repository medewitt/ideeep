# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Pairwise SNP-distance heatmap for a toy set of aligned genomes.

Six short aligned sequences give a 6x6 matrix of Hamming (SNP) distances.
The samples are ordered so that two transmission clusters -- close pairs and
triples within the single-linkage threshold -- fall as dark low-distance
blocks on the diagonal, outlined with rectangles.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from _style import apply_style, save, PALETTE, INK, MUTED
apply_style()

# Fixed toy alignment: six 20-nt sequences ordered so clusters are adjacent.
ids = ["S1", "S2", "S3", "S4", "S5", "S6"]
seqs = [
    "ACGTACGTACGTACGTACGT",  # S1  cluster 1
    "ACGTACGTACGTACGTACGA",  # S2  1 SNP from S1
    "ACGTACGTACGTACGTACTA",  # S3  2 SNPs from S1
    "TGCATGCATGCATGCATGCA",  # S4  cluster 2
    "TGCATGCATGCATGCATGCT",  # S5  1 SNP from S4
    "GGGGCCCCTTTTAAAACGCG",  # S6  singleton
]
S = np.array([list(s) for s in seqs])
n = len(seqs)

# Pairwise Hamming / SNP distances.
D = np.array([[int((S[i] != S[j]).sum()) for j in range(n)] for i in range(n)])

# Single-linkage clustering at a threshold of <= 2 SNPs.
threshold = 2
cluster = list(range(n))
for i in range(n):
    for j in range(i + 1, n):
        if D[i, j] <= threshold:
            lo, hi = sorted((cluster[i], cluster[j]))
            cluster = [lo if c == hi else c for c in cluster]

fig, ax = plt.subplots(figsize=(5.6, 4.6))
ax.grid(False)

im = ax.imshow(D, cmap="viridis_r", vmin=0, vmax=D.max())

cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("SNP distance", color=INK)
cbar.ax.tick_params(colors=INK)
cbar.outline.set_edgecolor(MUTED)

# Annotate each cell with its integer SNP distance.
mid = D.max() / 2.0
for i in range(n):
    for j in range(n):
        v = D[i, j]
        ax.text(j, i, str(v), ha="center", va="center", fontsize=10,
                color="white" if v <= mid else INK)

# Ticks / sample IDs.
ax.set_xticks(range(n))
ax.set_yticks(range(n))
ax.set_xticklabels(ids)
ax.set_yticklabels(ids)
ax.set_xlabel("sample")
ax.set_ylabel("sample")
ax.tick_params(length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

# Outline single-linkage cluster blocks (contiguous runs of a label).
runs = []
start = 0
for k in range(1, n + 1):
    if k == n or cluster[k] != cluster[start]:
        runs.append((start, k - 1))
        start = k
for a, b in runs:
    if b > a:  # only draw multi-member clusters
        ax.add_patch(Rectangle((a - 0.5, a - 0.5), b - a + 1, b - a + 1,
                               fill=False, edgecolor=PALETTE[1],
                               linewidth=2.4, zorder=5))

ax.set_title(f"Pairwise SNP distances (clusters at ≤{threshold} SNPs)")

save(fig, "assets/figures/genomic-surveillance.svg")
