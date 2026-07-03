# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Eigenvectors keep their direction under a linear map A."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

np.random.seed(0)

A = np.array([[2.0, 1.0], [0.0, 3.0]])
vals, vecs = np.linalg.eig(A)
# order by eigenvalue for stable labeling
order = np.argsort(vals)
vals = vals[order]
vecs = vecs[:, order]

theta = np.linspace(0, 2 * np.pi, 200)
circle = np.vstack([np.cos(theta), np.sin(theta)])
mapped = A @ circle

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.4, 4.4))


def draw_eigs(ax, scale_by_eigval):
    for i in range(2):
        v = vecs[:, i]
        lam = vals[i]
        vec = v * (lam if scale_by_eigval else 1.0)
        ax.annotate("", xy=(vec[0], vec[1]), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=PALETTE[i + 1],
                                    linewidth=2.2))
        label = f"eigvec {i+1}" if not scale_by_eigval else f"×{lam:g}"
        ax.annotate(label, xy=(vec[0], vec[1]),
                    xytext=(vec[0] * 1.08 + 0.1, vec[1] * 1.08 + 0.1),
                    color=PALETTE[i + 1], fontsize=9)


axL.plot(circle[0], circle[1], color=PALETTE[0], linewidth=1.6,
         label="unit circle")
draw_eigs(axL, scale_by_eigval=False)
axL.set_title("before")

axR.plot(mapped[0], mapped[1], color=PALETTE[0], linewidth=1.6,
         label="A · circle")
draw_eigs(axR, scale_by_eigval=True)
axR.set_title("after applying A")

for ax in (axL, axR):
    ax.axhline(0, color="#d8dee4", linewidth=0.8)
    ax.axvline(0, color="#d8dee4", linewidth=0.8)
    ax.set_aspect("equal")
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="lower right")

fig.suptitle(f"A = [[2,1],[0,3]]   eigenvalues λ = {vals[0]:g}, {vals[1]:g}",
             color="#26323f")

print("A =", A.tolist())
print(f"eigenvalues = {vals[0]:g}, {vals[1]:g}")
for i in range(2):
    print(f"  lambda={vals[i]:g}  eigvec={vecs[:, i].round(3).tolist()}")

save(fig, "assets/figures/eigenvectors.svg")
