# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scikit-learn"]
# ///
"""Linear vs nonlinear dimensionality reduction on the 8x8 handwritten digits
(64 dimensions). Left: PCA projects onto the two directions of greatest
variance -- a faithful linear summary, but the ten digit classes overlap.
Right: t-SNE, a nonlinear manifold method, pulls apart the classes into
separated clusters by preserving local neighbourhoods -- great for
visualization, though its distances and cluster sizes are not to be read
literally.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from _style import apply_style, save, INK

apply_style()

digits = load_digits()
X, y = digits.data, digits.target

pca = PCA(n_components=2, svd_solver="full").fit(X)
emb_pca = pca.transform(X)
emb_tsne = TSNE(n_components=2, init="pca", perplexity=30,
                random_state=0).fit_transform(X)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.8, 4.2))
cmap = plt.get_cmap("tab10")

sc = ax0.scatter(emb_pca[:, 0], emb_pca[:, 1], c=y, cmap=cmap, s=8, alpha=0.8)
ax0.set_title(f"PCA  ({100*pca.explained_variance_ratio_.sum():.0f}% of variance)",
              fontsize=10)
ax0.set_xlabel("PC 1", fontsize=9)
ax0.set_ylabel("PC 2", fontsize=9)
ax0.set_xticks([]); ax0.set_yticks([])

ax1.scatter(emb_tsne[:, 0], emb_tsne[:, 1], c=y, cmap=cmap, s=8, alpha=0.8)
ax1.set_title("t-SNE  (nonlinear manifold)", fontsize=10)
ax1.set_xlabel("dim 1", fontsize=9)
ax1.set_ylabel("dim 2", fontsize=9)
ax1.set_xticks([]); ax1.set_yticks([])

cb = fig.colorbar(sc, ax=(ax0, ax1), fraction=0.03, pad=0.02, ticks=range(10))
cb.set_label("digit", fontsize=8)
cb.ax.tick_params(labelsize=7)

save(fig, "assets/figures/dimensionality-reduction.svg")
