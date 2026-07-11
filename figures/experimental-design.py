# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Two pillars of experimental design. Left: randomization balances confounders.
In an observational study an unmeasured confounder U feeds both the exposure X
and the outcome Y, biasing the X->Y estimate; randomly assigning X severs the
U->X arrow, so the remaining X->Y path is the causal effect. Right: blocking
groups similar units (by age or site) and randomizes treatment within each
block, removing that nuisance variation from the comparison."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.7),
                               gridspec_kw={"width_ratios": [1.15, 1]})

# ---- observational vs randomized DAGs -------------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 10)
axL.axis("off")
axL.set_title("Randomization severs the confounder", fontsize=9.8)


def dag(ax, x0, y0, sever, label, color):
    nodes = {"U": (x0 + 1.5, y0 + 2.6), "X": (x0, y0), "Y": (x0 + 3.0, y0)}
    cols = {"U": MUTED, "X": color, "Y": PALETTE[1]}
    for n, (x, y) in nodes.items():
        ax.add_patch(Circle((x, y), 0.52, facecolor=cols[n] + "22",
                     edgecolor=cols[n], lw=1.8))
        ax.text(x, y, n, ha="center", va="center", fontsize=10, color=INK)

    def arr(a, b, dashed=False, crossed=False):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        v = np.array([x2 - x1, y2 - y1], float)
        v /= np.hypot(*v)
        s = (x1 + v[0] * 0.52, y1 + v[1] * 0.52)
        e = (x2 - v[0] * 0.52, y2 - v[1] * 0.52)
        ax.add_patch(FancyArrowPatch(s, e, arrowstyle="-|>", mutation_scale=13,
                     color=("#c0392b" if crossed else "0.4"), lw=1.6,
                     linestyle="--" if dashed else "-"))
        if crossed:
            mx, my = (s[0] + e[0]) / 2, (s[1] + e[1]) / 2
            ax.plot([mx - 0.22, mx + 0.22], [my - 0.22, my + 0.22],
                    color="#c0392b", lw=2.2)
            ax.plot([mx - 0.22, mx + 0.22], [my + 0.22, my - 0.22],
                    color="#c0392b", lw=2.2)
    arr("X", "Y")
    arr("U", "Y")
    arr("U", "X", crossed=sever)
    ax.text(x0 + 1.5, y0 - 1.1, label, ha="center", fontsize=8.5, color=color)


dag(axL, 1.0, 6.0, False, "observational: X–Y biased by U", PALETTE[3])
dag(axL, 1.0, 1.2, True, "randomized: U→X cut", PALETTE[0])

# ---- blocking -------------------------------------------------------------
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.axis("off")
axR.set_title("Blocking removes nuisance variation", fontsize=9.8)
blocks = [("young", 7.4), ("middle", 4.6), ("older", 1.8)]
rng = np.random.default_rng(0)
for name, y in blocks:
    axR.add_patch(Rectangle((0.6, y - 1.0), 8.8, 2.0, facecolor="#eef2f5",
                  edgecolor=MUTED, lw=1.0))
    axR.text(1.0, y + 0.75, f"block: {name}", fontsize=7.6, color=INK)
    # 8 units, randomized to treat (green) / control (blue) within the block
    assign = rng.permutation([0, 0, 0, 0, 1, 1, 1, 1])
    for i, a in enumerate(assign):
        cx = 2.0 + i * 0.85
        axR.add_patch(Circle((cx, y - 0.1), 0.28,
                      color=(PALETTE[2] if a else PALETTE[0])))
axR.scatter([], [], color=PALETTE[2], label="treatment")
axR.scatter([], [], color=PALETTE[0], label="control")
axR.legend(fontsize=8, loc="lower center", ncol=2)

fig.tight_layout()
save(fig, "assets/figures/experimental-design.svg")
