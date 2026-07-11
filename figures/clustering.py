# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scikit-learn"]
# ///
"""No single clustering algorithm fits every shape. Left: k-means recovers
well-separated, roughly spherical blobs. Middle: on two interleaving crescents
k-means fails -- it can only cut space into straight-edged (Voronoi) cells, so
it slices each crescent in half. Right: DBSCAN, which grows clusters by density,
recovers the crescents and flags sparse points as noise.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_moons
from sklearn.cluster import KMeans, DBSCAN
from _style import apply_style, save, PALETTE, INK

apply_style()

Xb, _ = make_blobs(n_samples=500, centers=4, cluster_std=0.9, random_state=0)
Xm, _ = make_moons(n_samples=500, noise=0.06, random_state=0)

km_b = KMeans(n_clusters=4, n_init=10, random_state=0).fit(Xb)
km_m = KMeans(n_clusters=2, n_init=10, random_state=0).fit(Xm)
db_m = DBSCAN(eps=0.2, min_samples=5).fit(Xm)

fig, axes = plt.subplots(1, 3, figsize=(9.9, 3.5))


def plot(ax, X, labels, title, centers=None):
    for lab in sorted(set(labels)):
        m = labels == lab
        if lab == -1:                      # DBSCAN noise
            ax.scatter(X[m, 0], X[m, 1], s=9, color="0.7", marker="x",
                       label="noise")
        else:
            ax.scatter(X[m, 0], X[m, 1], s=9, color=PALETTE[lab % len(PALETTE)])
    if centers is not None:
        ax.scatter(centers[:, 0], centers[:, 1], marker="*", s=170,
                   color=INK, edgecolors="white", linewidths=0.6, zorder=5)
    ax.set_title(title, fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])


plot(axes[0], Xb, km_b.labels_, "k-means on blobs ✓", km_b.cluster_centers_)
plot(axes[1], Xm, km_m.labels_, "k-means on crescents ✗", km_m.cluster_centers_)
plot(axes[2], Xm, db_m.labels_, "DBSCAN on crescents ✓")

fig.tight_layout()
save(fig, "assets/figures/clustering.svg")
