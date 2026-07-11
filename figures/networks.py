# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Networks and graphs. Left: the worked five-node example (edges 1-2, 1-3, 2-3,
3-4, 4-5) drawn as a node-link diagram, nodes sized and labelled by degree — the
degrees (2,2,3,2,1) sum to 2E=10, node 3 is the hub, and the whole graph is one
connected component. Right: the shape of the degree distribution P(k)
distinguishes a homogeneous network (degrees clustered near the mean) from a
heavy-tailed one dominated by a few high-degree hubs."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.6))

# ---- node-link diagram of the 5-node graph --------------------------------
axL.set_xlim(-1, 6)
axL.set_ylim(-2, 2)
axL.set_aspect("equal")
axL.axis("off")
axL.set_title("The worked 5-node graph", fontsize=10)

pos = {1: (0, 1.1), 2: (0, -1.1), 3: (1.7, 0), 4: (3.4, 0), 5: (5.0, 0.9)}
edges = [(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)]
deg = {1: 2, 2: 2, 3: 3, 4: 2, 5: 1}
for a, b in edges:
    axL.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=MUTED,
             lw=1.3, zorder=1)
for nid, (x, y) in pos.items():
    r = 0.24 + 0.10 * deg[nid]
    col = PALETTE[1] if nid == 3 else PALETTE[0]
    axL.add_patch(Circle((x, y), r, facecolor=col + "cc", edgecolor="white",
                  lw=1.2, zorder=5))
    axL.text(x, y, str(nid), ha="center", va="center", fontsize=9,
             color="white", zorder=6)
    axL.annotate(f"k={deg[nid]}", (x, y), textcoords="offset points",
                 xytext=(0, 20 if nid in (1, 3) else -22), ha="center",
                 fontsize=7.5, color=INK)
axL.text(2.5, -1.8, "one connected component · ⟨k⟩ = 2E/N = 2 · density 0.5",
         ha="center", fontsize=7.6, color=MUTED)

# ---- homogeneous vs heavy-tailed degree distribution ----------------------
kk = np.arange(0, 13)
homog = np.exp(-0.5 * ((kk - 4) / 1.0) ** 2)
homog /= homog.sum()
heavy = 1.0 / (kk + 1) ** 1.9
heavy /= heavy.sum()
w = 0.4
axR.bar(kk - w / 2, homog, width=w, color=PALETTE[0], label="homogeneous")
axR.bar(kk + w / 2, heavy, width=w, color=PALETTE[1], label="heavy-tailed (hubs)")
axR.annotate("a few hubs\nat high k", xy=(10, heavy[10]), xytext=(7, 0.28),
             fontsize=8, color=PALETTE[1],
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axR.set_xlabel("degree $k$")
axR.set_ylabel("$P(k)$")
axR.set_title("What the degree distribution reveals", fontsize=10)
axR.legend(fontsize=8.3, loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/networks.svg")
