# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Fractional factorial designs. Left: the 2^{3-1} half fraction is a geometric
half of the full 2^3 cube — the four runs (-,-,+), (+,-,-), (-,+,-), (+,+,+)
selected by the generator C = AB are alternating vertices (no two share an edge).
Right: resolution measures how badly effects are aliased — III aliases main
effects with two-factor interactions, IV keeps main effects clear but aliases
two-factor interactions with each other, V keeps both clear; higher resolution
tangles fewer important effects at the cost of more runs."""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig = plt.figure(figsize=(8.6, 3.7))
ax = fig.add_subplot(1, 2, 1, projection="3d")
axR = fig.add_subplot(1, 2, 2)

# ---- 2^3 cube with half-fraction vertices ---------------------------------
verts = np.array([[a, b, c] for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)])
frac = np.array([[-1, -1, 1], [1, -1, -1], [-1, 1, -1], [1, 1, 1]])
# cube edges
for i in range(len(verts)):
    for j in range(i + 1, len(verts)):
        if np.sum(np.abs(verts[i] - verts[j])) == 2:
            ax.plot(*zip(verts[i], verts[j]), color="#c9d2da", lw=0.9)
in_frac = np.array([any(np.all(v == f) for f in frac) for v in verts])
ax.scatter(verts[~in_frac, 0], verts[~in_frac, 1], verts[~in_frac, 2],
           s=35, color=MUTED, depthshade=False)
ax.scatter(frac[:, 0], frac[:, 1], frac[:, 2], s=70, color=PALETTE[1],
           depthshade=False)
ax.set_xlabel("A", fontsize=8, labelpad=-8)
ax.set_ylabel("B", fontsize=8, labelpad=-8)
ax.set_zlabel("C", fontsize=8, labelpad=-8)
ax.set_xticks([-1, 1]); ax.set_yticks([-1, 1]); ax.set_zticks([-1, 1])
ax.tick_params(labelsize=6, pad=-3)
ax.set_title("Half fraction $2^{3-1}$ (C = AB)", fontsize=9.5, pad=0)
ax.view_init(elev=22, azim=-52)

# ---- resolution ladder ----------------------------------------------------
axR.axis("off")
axR.set_title("Resolution: what gets aliased", fontsize=9.5)
rows = [
    ("III", "main ↔ 2-factor interaction", PALETTE[1], "cheapest, risky"),
    ("IV", "main clear; 2fi ↔ 2fi", PALETTE[4], "moderate"),
    ("V", "main & 2fi all clear", PALETTE[2], "most runs, safest"),
]
for i, (res, txt, col, cost) in enumerate(rows):
    y = 2.5 - i
    axR.text(1.1, y, f"Res {res}", fontsize=11, color=col, fontweight="bold",
             va="center")
    axR.text(2.4, y, txt, fontsize=8.6, color=INK, va="center")
    axR.text(2.4, y - 0.32, cost, fontsize=7.4, color=MUTED, va="center",
             style="italic")
axR.annotate("", xy=(0.55, 3.0), xytext=(0.55, -0.6),
             arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4))
axR.text(0.32, 1.2, "more runs, fewer effects tangled", rotation=90,
         fontsize=7.6, color=MUTED, va="center")
axR.set_xlim(0, 7)
axR.set_ylim(-1, 3.4)

fig.tight_layout()
save(fig, "assets/figures/fractional-factorial-designs.svg")
