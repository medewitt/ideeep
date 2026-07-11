# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scikit-learn"]
# ///
"""Why an ensemble of trees beats a single tree. Left: one deep decision tree
carves a jagged, axis-aligned, overfit boundary. Middle: a random forest
averages hundreds of decorrelated trees into a smooth, stable boundary. Right:
held-out error falls and flattens as more trees are added, well below the
single tree's error -- variance reduction by averaging.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

X, y = make_moons(n_samples=400, noise=0.30, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.4, random_state=0)
gx, gy = np.meshgrid(np.linspace(-1.8, 2.8, 300), np.linspace(-1.4, 1.8, 300))
grid = np.c_[gx.ravel(), gy.ravel()]

tree = DecisionTreeClassifier(random_state=0).fit(Xtr, ytr)
forest = RandomForestClassifier(n_estimators=300, random_state=0).fit(Xtr, ytr)

fig, axes = plt.subplots(1, 3, figsize=(9.9, 3.5))

for ax, model, title in [(axes[0], tree, "Single decision tree"),
                         (axes[1], forest, "Random forest (300 trees)")]:
    zz = model.predict_proba(grid)[:, 1].reshape(gx.shape)
    ax.contourf(gx, gy, zz, levels=[0, 0.5, 1], colors=[PALETTE[0], PALETTE[1]],
                alpha=0.16)
    ax.contour(gx, gy, zz, levels=[0.5], colors=[INK], linewidths=1.6)
    ax.scatter(Xtr[ytr == 0, 0], Xtr[ytr == 0, 1], s=8, color=PALETTE[0])
    ax.scatter(Xtr[ytr == 1, 0], Xtr[ytr == 1, 1], s=8, color=PALETTE[1])
    ax.set_title(title, fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])

n_trees = [1, 2, 5, 10, 25, 50, 100, 200, 400]
err = []
for n in n_trees:
    m = RandomForestClassifier(n_estimators=n, random_state=0).fit(Xtr, ytr)
    err.append(1 - m.score(Xte, yte))
tree_err = 1 - tree.score(Xte, yte)
axes[2].plot(n_trees, err, "o-", color=PALETTE[2], lw=1.8, ms=4,
             label="random forest")
axes[2].axhline(tree_err, color=MUTED, lw=1.2, ls="--", label="single tree")
axes[2].set_xscale("log")
axes[2].set_title("Test error vs number of trees", fontsize=10)
axes[2].set_xlabel("number of trees")
axes[2].set_ylabel("test error")
axes[2].legend(loc="upper right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/tree-ensembles.svg")
