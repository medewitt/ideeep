# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Instrumental variables. Left: the causal DAG behind an IV analysis — the
instrument Z affects the exposure X, which affects the outcome Y, while an
unmeasured confounder U opens a back-door into both X and Y; the two dashed
arrows (Z->U and a direct Z->Y) are the forbidden paths that the independence
and exclusion assumptions rule out. Right: on confounded data OLS is biased
(~2.66) while 2SLS recovers the true effect beta = 2."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.7),
                               gridspec_kw={"width_ratios": [1.25, 1]})

# ---- causal DAG -----------------------------------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 8)
axL.axis("off")
axL.set_title("The IV assumptions as a DAG", fontsize=10)

nodes = {"Z": (1.3, 2.3), "X": (4.3, 2.3), "Y": (7.6, 2.3), "U": (5.95, 6.2)}
cols = {"Z": PALETTE[2], "X": PALETTE[0], "Y": PALETTE[1], "U": MUTED}
for name, (x, y) in nodes.items():
    axL.add_patch(Circle((x, y), 0.62, facecolor=cols[name] + "22",
                  edgecolor=cols[name], lw=2.0))
    axL.text(x, y, name, ha="center", va="center", fontsize=11, color=INK)


def arr(a, b, color, style="-|>", dashed=False, rad=0.0, lw=1.7):
    (x1, y1), (x2, y2) = nodes[a], nodes[b]
    ax_ = np.array([x2 - x1, y2 - y1], float)
    ax_ /= np.hypot(*ax_)
    s = (x1 + ax_[0] * 0.62, y1 + ax_[1] * 0.62)
    e = (x2 - ax_[0] * 0.62, y2 - ax_[1] * 0.62)
    axL.add_patch(FancyArrowPatch(s, e, arrowstyle=style, mutation_scale=14,
                  color=color, lw=lw, linestyle="--" if dashed else "-",
                  connectionstyle=f"arc3,rad={rad}"))


arr("Z", "X", INK)
arr("X", "Y", INK)
arr("U", "X", MUTED)
arr("U", "Y", MUTED)
# forbidden paths (crossed out)
arr("Z", "U", PALETTE[3], dashed=True, rad=-0.25, lw=1.3)
arr("Z", "Y", PALETTE[3], dashed=True, rad=-0.4, lw=1.3)
axL.text(2.7, 2.75, "relevance", fontsize=7.8, color=INK, ha="center")
axL.text(5.7, 0.6, "exclusion: no direct  Z→Y  (dashed = forbidden)",
         fontsize=7.6, color=PALETTE[3], ha="center")
axL.text(3.2, 5.2, "independence:\nno  Z→U", fontsize=7.6, color=PALETTE[3])

# ---- OLS vs 2SLS ----------------------------------------------------------
n = 5000
U = rng.normal(size=n)
Z = rng.normal(size=n)
X = 0.8 * Z + 1.0 * U + rng.normal(size=n)
beta = 2.0
Y = beta * X + 2.0 * U + rng.normal(size=n)
ols = np.polyfit(X, Y, 1)[0]
twosls = np.cov(Z, Y)[0, 1] / np.cov(Z, X)[0, 1]

axR.axhline(beta, ls="--", color=MUTED, lw=1.3)
axR.text(1.5, beta + 0.04, r"true $\beta=2$", fontsize=8.5, color=MUTED,
         ha="center")
bars = axR.bar([0, 1], [ols, twosls], width=0.55,
               color=[PALETTE[3], PALETTE[0]])
for x, v in [(0, ols), (1, twosls)]:
    axR.annotate(f"{v:.2f}", (x, v), textcoords="offset points",
                 xytext=(0, 4), ha="center", fontsize=9, color=INK)
axR.set_xticks([0, 1])
axR.set_xticklabels(["OLS\n(biased)", "2SLS\n(recovers β)"], fontsize=8.8)
axR.set_ylabel(r"estimated effect of $X$ on $Y$")
axR.set_title("Confounding vs the instrument", fontsize=10)
axR.set_ylim(0, 3.0)
axR.grid(axis="x", visible=False)

fig.tight_layout()
save(fig, "assets/figures/instrumental-variables.svg")
