# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Reproductive value: life cycle, the two eigenvectors, and elasticities.

Panel (a) draws a three-stage life cycle beside its Lefkovitch matrix.
Panel (b) contrasts the stable stage distribution (right eigenvector) with
reproductive value (left eigenvector). Panel (c) shows the elasticity of the
growth rate to each matrix entry as a heatmap.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
np.random.seed(1834)

# Stage-structured (Lefkovitch) projection matrix: juvenile, subadult, adult.
A = np.array([[0.20, 1.20, 4.00],
              [0.50, 0.30, 0.00],
              [0.00, 0.40, 0.65]])
stages = ["Juv", "Sub", "Adult"]

# Dominant eigenvalue, right eigenvector w, left eigenvector v.
vals, vecs = np.linalg.eig(A)
i = int(np.argmax(vals.real))
lam = vals[i].real
w = np.abs(vecs[:, i].real)
w /= w.sum()
lvals, lvecs = np.linalg.eig(A.T)
j = int(np.argmax(lvals.real))
v = np.abs(lvecs[:, j].real)
v /= v[0]  # scale so juveniles have reproductive value 1

# Sensitivity and elasticity of lambda to each matrix entry.
sens = np.outer(v, w) / (v @ w)
elas = (A / lam) * sens

fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.7))

# Panel (a): life-cycle graph.
ax = axes[0]
pos = {0: (0.15, 0.62), 1: (0.5, 0.62), 2: (0.85, 0.62)}
for k, (x, y) in pos.items():
    ax.add_patch(plt.Circle((x, y), 0.09, color=PALETTE[0], alpha=0.18, zorder=1))
    ax.text(x, y, stages[k], ha="center", va="center", fontsize=10,
            color=INK, zorder=3)


def arrow(a, b, rad, color, lw=1.6):
    ax.add_patch(FancyArrowPatch(pos[a], pos[b], connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle="-|>", mutation_scale=13, lw=lw,
                                 color=color, shrinkA=15, shrinkB=15, zorder=2))


# Survival / growth transitions (sub-diagonal) in green.
arrow(0, 1, 0.0, PALETTE[2])
arrow(1, 2, 0.0, PALETTE[2])
# Fecundity (top row) in orange, curving back to juveniles.
arrow(1, 0, -0.45, PALETTE[1])
arrow(2, 0, -0.6, PALETTE[1])
ax.text(0.5, 0.16, "green: survival  ·  orange: fecundity",
        ha="center", fontsize=8.5, color=MUTED)
# Matrix printed beside the graph.
mtxt = "\n".join("  ".join(f"{a:.2f}" for a in row) for row in A)
ax.text(0.5, 0.90, r"$\mathbf{A}=$", ha="right", fontsize=10, color=INK)
ax.text(0.53, 0.90, mtxt, ha="left", va="center", fontsize=8.5,
        family="monospace", color=INK)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_title("(a) life cycle and matrix", fontsize=10)

# Panel (b): the two eigenvectors.
ax = axes[1]
x = np.arange(3)
ax.bar(x - 0.2, w, width=0.4, color=PALETTE[0], label=r"stable stage $\mathbf{w}$")
ax.bar(x + 0.2, v / v.sum(), width=0.4, color=PALETTE[1],
       label=r"reprod. value $\mathbf{v}$")
ax.set_xticks(x)
ax.set_xticklabels(stages)
ax.set_ylabel("relative weight")
ax.set_title("(b) who is common vs who is valuable", fontsize=10)
ax.legend(fontsize=8.5)

# Panel (c): elasticity heatmap.
ax = axes[2]
im = ax.imshow(elas, cmap="cividis", aspect="equal")
ax.set_xticks(range(3))
ax.set_xticklabels(stages)
ax.set_yticks(range(3))
ax.set_yticklabels(stages)
ax.set_xlabel("from stage $j$")
ax.set_ylabel("to stage $i$")
kmax = np.unravel_index(np.argmax(elas), elas.shape)
for r in range(3):
    for c in range(3):
        col = "white" if elas[r, c] < elas.max() * 0.6 else INK
        ax.text(c, r, f"{elas[r, c]:.2f}", ha="center", va="center",
                fontsize=8.5, color=col)
ax.add_patch(plt.Rectangle((kmax[1] - 0.5, kmax[0] - 0.5), 1, 1, fill=False,
                           edgecolor=PALETTE[1], lw=2.2))
ax.set_title(f"(c) elasticity of $\\lambda={lam:.2f}$", fontsize=10)
ax.grid(False)
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

fig.tight_layout()
save(fig, "assets/figures/reproductive-value.svg")
