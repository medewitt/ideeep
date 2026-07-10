# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Simulated transmission tree and posterior who-infected-whom heatmap."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

n = 18
onset = np.zeros(n)
infector = np.full(n, -1, dtype=int)
depth = np.zeros(n, dtype=int)
children = {i: [] for i in range(n)}

# Simulate: index case at day 0, each later case gets an earlier infector
# and a gamma serial interval (mean ~5 days, shape 4).
for j in range(1, n):
    i = rng.integers(0, j)
    infector[j] = i
    onset[j] = onset[i] + rng.gamma(shape=4.0, scale=5.0 / 4.0)
    depth[j] = depth[i] + 1
    children[i].append(j)

# Leaf-order y layout: recurse from the index, spreading leaves evenly.
y = np.zeros(n)
leaf_counter = [0.0]

def layout(node):
    kids = children[node]
    if not kids:
        y[node] = leaf_counter[0]
        leaf_counter[0] += 1.0
        return y[node]
    ys = [layout(k) for k in kids]
    y[node] = float(np.mean(ys))
    return y[node]

layout(0)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.6))

# LEFT: transmission tree
for j in range(1, n):
    i = infector[j]
    axL.annotate(
        "",
        xy=(onset[j], y[j]),
        xytext=(onset[i], y[i]),
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8, alpha=0.7),
    )
sc = axL.scatter(
    onset, y, c=depth, cmap="viridis", s=60, zorder=3,
    edgecolors="white", linewidths=0.6,
)
axL.set_xlabel("onset day")
axL.set_yticks([])
axL.set_ylabel("")
axL.set_title("Transmission tree (who infected whom)")
axL.margins(y=0.08)

# RIGHT: posterior infector-probability matrix, cases ordered by onset.
order = np.argsort(onset)
rank = np.empty(n, dtype=int)
rank[order] = np.arange(n)

P = np.zeros((n, n))  # rows = candidate infector, cols = infectee
true_cell = np.full(n, -1, dtype=int)
for j in range(1, n):
    col = rank[j]
    true_row = rank[infector[j]]
    true_cell[col] = true_row
    p_true = rng.uniform(0.6, 0.85)
    P[true_row, col] = p_true
    # Distribute the remainder among 1-3 other earlier cases.
    earlier = [r for r in range(col) if r != true_row]
    if earlier:
        k = min(len(earlier), rng.integers(1, 4))
        others = rng.choice(earlier, size=k, replace=False)
        w = rng.uniform(0.5, 1.0, size=k)
        w = w / w.sum() * (1.0 - p_true)
        for r, wr in zip(others, w):
            P[r, col] = wr

im = axR.imshow(P, cmap="viridis", aspect="auto", vmin=0, vmax=1)
# Mark the true infector cell of each column.
for col in range(1, n):
    axR.scatter(
        col, true_cell[col], s=26, facecolors="none",
        edgecolors="#e03b3b", linewidths=1.2,
    )
axR.set_xlabel("infectee (ordered by onset)")
axR.set_ylabel("candidate infector")
axR.set_title("Posterior infector probabilities")
axR.grid(False)
cb = fig.colorbar(im, ax=axR, fraction=0.046, pad=0.04)
cb.set_label("P(infector)")

fig.tight_layout()
save(fig, "assets/figures/transmission-tree.svg")
