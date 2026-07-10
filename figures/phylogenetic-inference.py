# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""JC69 distance correction with saturation and a UPGMA inferred tree."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, set_link_color_palette
from scipy.spatial.distance import pdist
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.6))

# LEFT: JC69 correction and saturation.
p = np.linspace(0.0, 0.74, 400)
d = -0.75 * np.log(1.0 - (4.0 / 3.0) * p)
axL.plot(p, d, color=PALETTE[0], lw=2, label="JC69 corrected distance")
axL.plot(p, p, color=MUTED, ls="--", lw=1.4, label="uncorrected p-distance")
axL.set_ylim(0, 1.6)
axL.set_xlim(0, 0.74)
axL.annotate(
    "saturation: raw p-distance\nunderestimates divergence",
    xy=(0.6, 0.55), xytext=(0.14, 1.15),
    fontsize=9, color=INK,
    arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8),
)
axL.set_xlabel("observed p-distance")
axL.set_ylabel("distance (substitutions/site)")
axL.legend(loc="upper left", fontsize=9)

# RIGHT: UPGMA tree from tree-like pairwise distances of 8 taxa.
labels = list("ABCDEFGH")
pts = rng.normal(size=(8, 3))
dists = pdist(pts, metric="euclidean")
Z = linkage(dists, method="average")

set_link_color_palette([INK])
dendrogram(
    Z,
    orientation="left",
    labels=labels,
    color_threshold=0,
    above_threshold_color=INK,
    ax=axR,
)
axR.set_xlabel("genetic distance (substitutions/site)")
axR.set_title("Neighbor-joining / UPGMA tree")
axR.grid(False)
axR.tick_params(axis="y", length=0)

fig.tight_layout()
save(fig, "assets/figures/phylogenetic-inference.svg")
