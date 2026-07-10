# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Branching processes: lineage extinction and extinction probability."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# Left: Galton-Watson lineages, Poisson offspring mean R0.
R0 = 1.3
n_lineages = 40
n_gen = 15
gens = np.arange(n_gen + 1)

trajectories = []
for _ in range(n_lineages):
    size = 1
    path = [size]
    for _ in range(n_gen):
        size = int(rng.poisson(R0 * size)) if size > 0 else 0
        path.append(size)
    trajectories.append(np.array(path))

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.4))

for path in trajectories:
    extinct = path[-1] == 0
    if extinct:
        axL.plot(gens, path, color=MUTED, lw=0.7, alpha=0.6)
    else:
        axL.plot(gens, path, color=PALETTE[0], lw=1.6, alpha=0.9)

axL.set_xlabel("generation")
axL.set_ylabel("number infected")
axL.set_title("stochastic lineages (R0 = 1.3)")
axL.set_xlim(0, n_gen)
axL.annotate("most chains go extinct", xy=(6, 0.6), xytext=(4.4, 6.5),
             fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))

# Right: extinction probability q vs R0.
# q is smallest root of q = exp(R0 (q - 1)); iterate to fixed point.
R0_grid = np.linspace(0.0, 4.0, 200)
q = np.ones_like(R0_grid)
for i, r in enumerate(R0_grid):
    if r <= 1.0:
        q[i] = 1.0
    else:
        qi = 0.0
        for _ in range(2000):
            qi = np.exp(r * (qi - 1.0))
        q[i] = qi

axR.plot(R0_grid, q, color=PALETTE[1], lw=2.0)
axR.axvline(1.0, color=MUTED, lw=1.0, ls="--")
axR.set_xlabel("basic reproduction number R0")
axR.set_ylabel("probability of extinction")
axR.set_title("extinction probability")
axR.set_xlim(0, 4)
axR.set_ylim(-0.02, 1.05)
axR.annotate("R0 > 1: q < 1\n(outbreak possible)",
             xy=(2.4, np.exp(0)), xytext=(1.9, 0.62),
             fontsize=8.5, color=INK)

fig.tight_layout()
save(fig, "assets/figures/branching-processes.svg")
