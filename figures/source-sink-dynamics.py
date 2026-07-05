# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Source-sink dynamics: a two-patch BIDE flow diagram, sink abundance held
above zero by immigration subsidy, and inflation under environmental
autocorrelation."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.6))

# (a) Two-patch source -> sink flow, annotated with the BIDE terms.
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis("off")
ax.set_title("(a) BIDE flow")
BLUE, ORANGE = PALETTE[0], PALETTE[1]
ax.add_patch(FancyBboxPatch((0.4, 3.0), 3.6, 2.2, boxstyle="round,pad=0.08",
             linewidth=1.8, edgecolor=BLUE, facecolor=BLUE + "14"))
ax.text(2.2, 4.1, "SOURCE\n$\\lambda_{loc}>1$\nB > D", ha="center",
        va="center", fontsize=8.5, color=INK)
ax.add_patch(FancyBboxPatch((6.0, 3.0), 3.6, 2.2, boxstyle="round,pad=0.08",
             linewidth=1.8, edgecolor=ORANGE, facecolor=ORANGE + "14"))
ax.text(7.8, 4.1, "SINK\n$\\lambda_{loc}<1$\nD > B", ha="center",
        va="center", fontsize=8.5, color=INK)
ax.add_patch(FancyArrowPatch((4.1, 4.1), (5.9, 4.1), arrowstyle="-|>",
             mutation_scale=18, color="0.4", lw=2.0))
ax.text(5.0, 4.6, "emigration\n$\\to$ immigration", ha="center", fontsize=8,
        color=INK)
ax.text(2.2, 6.1, "surplus births\nexported", ha="center", fontsize=7.5,
        color=MUTED)
ax.text(7.8, 6.1, "deaths exceed\nbirths", ha="center", fontsize=7.5,
        color=MUTED)

# (b) Sink equilibrium n2* = I/(1-lambda2) rises with the immigration subsidy.
lam2 = 0.7                              # sink local finite rate of increase < 1
I = np.linspace(0, 20, 200)            # immigration subsidy
n2_star = I / (1 - lam2)
axes[1].plot(I, n2_star, color=ORANGE, lw=2.2)
axes[1].scatter([0], [0], s=40, color=INK, zorder=3)
axes[1].annotate("no subsidy:\n$n^*=0$", xy=(0, 0), xytext=(4, 8),
                 fontsize=8, color=INK,
                 arrowprops=dict(arrowstyle="->", color=INK))
axes[1].set_xlabel("immigration subsidy $I$")
axes[1].set_ylabel(r"sink equilibrium $n_2^*$")
axes[1].set_title(r"(b) subsidy sustains the sink")

# (c) Inflation: positive environmental autocorrelation lifts a sink's mean.
lam_mean, lam_sd = 0.9, 0.35            # geometric-mean local rate < 1
subsidy = 2.0
rhos = np.linspace(0.0, 0.9, 10)
means = []
for rho in rhos:
    eps = rng.normal(0, lam_sd, 4000)
    x = np.zeros_like(eps)
    for t in range(1, x.size):         # AR(1) environmental driver
        x[t] = rho * x[t - 1] + np.sqrt(1 - rho**2) * eps[t]
    lam_t = lam_mean * np.exp(x - 0.5 * lam_sd**2)
    n = 1.0
    traj = []
    for lt in lam_t:
        n = lt * n + subsidy
        traj.append(n)
    means.append(np.mean(traj[1000:]))
axes[2].plot(rhos, means, color=PALETTE[2], lw=2.2, marker="o", ms=4)
axes[2].set_xlabel(r"environmental autocorrelation $\rho$")
axes[2].set_ylabel("mean sink abundance")
axes[2].set_title("(c) inflationary effect")

fig.tight_layout()
save(fig, "assets/figures/source-sink-dynamics.svg")
