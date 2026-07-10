# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Patch network occupancy and Levins metapopulation dynamics."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.6))

# ---- LEFT: spatial patch network with occupancy ----
n_patch = 10
coords = rng.uniform(0.05, 0.95, size=(n_patch, 2))
capacity = rng.uniform(40, 200, size=n_patch)     # patch capacity
occupied = rng.random(n_patch) < 0.55             # occupancy state

# Draw dispersal edges between patches closer than a threshold distance.
thresh = 0.42
for i in range(n_patch):
    for j in range(i + 1, n_patch):
        d = np.hypot(*(coords[i] - coords[j]))
        if d < thresh:
            axL.plot([coords[i, 0], coords[j, 0]],
                     [coords[i, 1], coords[j, 1]],
                     color=MUTED, lw=0.7, alpha=0.5, zorder=1)

sizes = 60 + 2.2 * capacity
face = [PALETTE[2] if o else "white" for o in occupied]
axL.scatter(coords[:, 0], coords[:, 1], s=sizes, c=face,
            edgecolors=INK, linewidths=1.2, zorder=3)

# Recolonization arrows from occupied to nearby empty patches.
occ_idx = np.where(occupied)[0]
emp_idx = np.where(~occupied)[0]
arrows = 0
for e in emp_idx:
    if arrows >= 2:
        break
    dists = [np.hypot(*(coords[e] - coords[o])) for o in occ_idx]
    src = occ_idx[int(np.argmin(dists))]
    if np.min(dists) < thresh:
        axL.annotate("", xy=coords[e], xytext=coords[src],
                     arrowprops=dict(arrowstyle="->", color=PALETTE[1],
                                     lw=1.6, shrinkA=8, shrinkB=8))
        arrows += 1

axL.scatter([], [], s=80, c=PALETTE[2], edgecolors=INK, linewidths=1.2,
            label="occupied")
axL.scatter([], [], s=80, c="white", edgecolors=INK, linewidths=1.2,
            label="empty")
axL.plot([], [], color=PALETTE[1], lw=1.6, label="recolonization")
axL.legend(loc="lower left", fontsize=7.5)
axL.set_xlim(0, 1)
axL.set_ylim(0, 1)
axL.set_title("Patches, dispersal, and occupancy")
axL.axis("off")

# ---- RIGHT: Levins occupancy dynamics ----
c, e = 0.8, 0.3                          # colonization, extinction rates
p_star = 1.0 - e / c                     # equilibrium occupancy
t = np.linspace(0, 30, 400)
dt = t[1] - t[0]

for p0, col in [(0.05, PALETTE[0]), (0.95, PALETTE[3])]:
    p = np.empty_like(t)
    p[0] = p0
    for k in range(1, len(t)):            # forward Euler on dp/dt
        dp = c * p[k - 1] * (1 - p[k - 1]) - e * p[k - 1]
        p[k] = p[k - 1] + dp * dt
    axR.plot(t, p, color=col, lw=2, label=f"p(0) = {p0}")

axR.axhline(p_star, ls="--", color=INK, lw=1.2)
axR.annotate(r"$p^* = 1 - e/c$", (t[-1] * 0.62, p_star + 0.04),
             fontsize=9, color=INK)

axR.set_xlim(0, t[-1])
axR.set_ylim(0, 1)
axR.set_xlabel("time")
axR.set_ylabel("fraction of patches occupied")
axR.set_title("Levins occupancy dynamics")
axR.legend(loc="center right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/metapopulations.svg")
