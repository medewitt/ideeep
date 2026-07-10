# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Next-generation matrix K: R0 is its dominant eigenvalue."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

groups = ["children", "adults", "elderly"]

# K_ij = new infections in type i caused by one infectious type j.
K = np.array([
    [1.8, 0.6, 0.2],
    [0.7, 1.1, 0.4],
    [0.3, 0.5, 0.9],
])

eigvals = np.linalg.eig(K)[0]
R0 = float(np.max(eigvals.real))

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.4))

# Left: heatmap of K with numeric entries.
im = axL.imshow(K, cmap="viridis", aspect="equal")
axL.set_xticks(range(3))
axL.set_yticks(range(3))
axL.set_xticklabels(groups)
axL.set_yticklabels(groups)
axL.set_xlabel("infector group")
axL.set_ylabel("infectee group")
axL.set_title(f"K matrix   R0 = ρ(K) = {R0:.2f}")
axL.grid(False)
vmid = 0.5 * (K.min() + K.max())
for i in range(3):
    for j in range(3):
        txt = "white" if K[i, j] < vmid else INK
        axL.text(j, i, f"{K[i, j]:.1f}", ha="center", va="center",
                 color=txt, fontsize=10)
fig.colorbar(im, ax=axL, fraction=0.046, pad=0.04)

# Right: who-infects-whom schematic (triangle of nodes).
axR.set_title("who infects whom")
axR.axis("off")
axR.set_xlim(-1.35, 1.35)
axR.set_ylim(-1.15, 1.35)

pos = np.array([[0.0, 1.0], [-1.0, -0.6], [1.0, -0.6]])
wmax = K.max()

for j in range(3):
    for i in range(3):
        if i == j:
            continue
        p0, p1 = pos[j], pos[i]
        d = p1 - p0
        p0s = p0 + 0.22 * d
        p1s = p1 - 0.22 * d
        lw = 0.6 + 5.0 * (K[i, j] / wmax)
        axR.annotate(
            "", xy=p1s, xytext=p0s,
            arrowprops=dict(arrowstyle="-|>", color=MUTED,
                            lw=lw, alpha=0.75,
                            connectionstyle="arc3,rad=0.12"),
        )

for k, (x, y) in enumerate(pos):
    axR.scatter([x], [y], s=1500, color=PALETTE[k], zorder=3,
                edgecolor="white", linewidth=1.2)
    axR.text(x, y, groups[k], ha="center", va="center",
             color="white", fontsize=8.5, zorder=4, fontweight="bold")

axR.annotate(
    "R0 is the dominant eigenvalue of K,\nnot any single entry",
    xy=(0, -1.05), ha="center", fontsize=8.5, color=INK)

fig.tight_layout()
save(fig, "assets/figures/next-generation-matrix.svg")
