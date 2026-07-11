# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Survey sampling. Left: four designs drawn on the same population — simple
random sampling scatters units anywhere, stratified sampling draws within each
subgroup, cluster sampling takes whole groups, and probability-proportional-to-
size favours larger clusters. Right: design weights rescale the sample back to
the population: a proportional 10% sample is self-weighting (every weight = 10),
but oversampling rural residents (pi=0.2) gives them weight 5 versus 10 for
urban, so weighting is needed to avoid over-representing them."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(2)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 3.7),
                               gridspec_kw={"width_ratios": [1.25, 1]})

# ---- four sampling designs ------------------------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 10)
axL.axis("off")
axL.set_title("Four sampling designs", fontsize=9.8)


def panel(x0, y0, title):
    axL.add_patch(Rectangle((x0, y0), 4.2, 3.6, facecolor="#f4f6f8",
                  edgecolor=MUTED, lw=1.0))
    axL.text(x0 + 2.1, y0 + 3.8, title, ha="center", fontsize=8, color=INK)
    return x0, y0


grid = np.array([(x0 + 0.5 + i * 0.55, y0 + 0.5 + j * 0.55)
                 for i in range(7) for j in range(6)] if False else [])

# SRS
x0, y0 = panel(0.4, 5.6, "SRS")
pts = np.column_stack([rng.uniform(x0 + 0.3, x0 + 3.9, 40),
                       rng.uniform(y0 + 0.3, y0 + 3.3, 40)])
axL.scatter(pts[:, 0], pts[:, 1], s=6, color=MUTED)
sel = rng.choice(40, 8, replace=False)
axL.scatter(pts[sel, 0], pts[sel, 1], s=22, color=PALETTE[1], zorder=5)

# Stratified
x0, y0 = panel(5.4, 5.6, "stratified")
for k, col in enumerate([PALETTE[0], PALETTE[2], PALETTE[3]]):
    xs = rng.uniform(x0 + 0.3, x0 + 3.9, 14)
    ys = rng.uniform(y0 + 0.3 + k * 1.05, y0 + 0.3 + (k + 1) * 1.0, 14)
    axL.scatter(xs, ys, s=6, color=col + "66")
    s = rng.choice(14, 3, replace=False)
    axL.scatter(xs[s], ys[s], s=22, color=col, zorder=5)

# Cluster
x0, y0 = panel(0.4, 1.2, "cluster")
centers = [(x0 + 1.0, y0 + 1.0), (x0 + 3.0, y0 + 0.9), (x0 + 1.2, y0 + 2.7),
           (x0 + 3.2, y0 + 2.7)]
chosen = {1, 2}
for ci, (cx, cy) in enumerate(centers):
    xs = cx + rng.uniform(-0.5, 0.5, 8)
    ys = cy + rng.uniform(-0.5, 0.5, 8)
    col = PALETTE[1] if ci in chosen else MUTED
    axL.scatter(xs, ys, s=(18 if ci in chosen else 6), color=col)

# PPS
x0, y0 = panel(5.4, 1.2, "PPS")
sizes = [4, 8, 16, 6]
centers = [(x0 + 1.0, y0 + 1.0), (x0 + 3.0, y0 + 1.0), (x0 + 1.4, y0 + 2.8),
           (x0 + 3.2, y0 + 2.8)]
picked = 2                                     # biggest cluster
for ci, ((cx, cy), s) in enumerate(zip(centers, sizes)):
    axL.scatter([cx], [cy], s=s * 12, color=(PALETTE[1] if ci == picked else
                MUTED) + "66", edgecolor=(PALETTE[1] if ci == picked else MUTED))
axL.text(6.4, 1.4, "bigger cluster,\nhigher chance", fontsize=6.6, color=MUTED)

# ---- weighting bars -------------------------------------------------------
axR.set_title("Weights rescale to the population", fontsize=9.5)
groups = ["urban", "rural"]
x = np.arange(2)
w = 0.36
self_w = [10, 10]
over_w = [10, 5]
axR.bar(x - w / 2, self_w, width=w, color=PALETTE[0], label="proportional 10%")
axR.bar(x + w / 2, over_w, width=w, color=PALETTE[1], label="oversample rural")
for xi, (a, b) in enumerate(zip(self_w, over_w)):
    axR.text(xi - w / 2, a + 0.2, f"w={a}", ha="center", fontsize=8, color=INK)
    axR.text(xi + w / 2, b + 0.2, f"w={b}", ha="center", fontsize=8, color=INK)
axR.text(0.5, 11.4, "self-weighting", ha="center", fontsize=7.6,
         color=PALETTE[0])
axR.set_xticks(x)
axR.set_xticklabels(groups)
axR.set_ylabel(r"design weight $w_i=1/\pi_i$")
axR.set_ylim(0, 13)
axR.legend(fontsize=7.8, loc="upper right")
axR.grid(axis="x", visible=False)

fig.tight_layout()
save(fig, "assets/figures/survey-sampling.svg")
