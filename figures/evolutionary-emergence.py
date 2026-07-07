# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Evolutionary emergence: a race between adaptation and extinction.

Panel A: a stuttering wild-type transmission chain (R0 < 1) rescued when a
mutation (color change) lifts a sub-lineage above R0 = 1.
Panel B: probability of emergence versus initial R0 for several mutation
supplies, from the Antia et al. rare-mutation approximation.
Panel C: an evolutionary-rescue trajectory - the wild type declines while the
adapted type rises, so total incidence turns back up.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# --- Panel A: a hand-built genealogy that stutters then is rescued. ----------
# children[node] = list of offspring; the mutant lineage starts at node 4.
children = {
    0: [1, 2], 1: [3], 2: [4], 3: [],
    4: [5, 6], 5: [7, 8], 6: [9], 7: [10, 11], 8: [12],
    9: [13, 14], 10: [15], 11: [16, 17], 12: [], 13: [18],
    14: [], 15: [], 16: [], 17: [], 18: [],
}
mutant = set()  # nodes descended from (and including) node 4


def mark_mutant(node):
    mutant.add(node)
    for ch in children.get(node, []):
        mark_mutant(ch)


mark_mutant(4)

gen = {0: 0}
for parent, kids in children.items():
    for ch in kids:
        gen[ch] = gen[parent] + 1

# Assign leaves evenly, internal nodes at the mean of their children (DFS).
ypos, leaf_counter = {}, [0]


def layout(node):
    kids = children.get(node, [])
    if not kids:
        ypos[node] = leaf_counter[0]
        leaf_counter[0] += 1
        return ypos[node]
    ys = [layout(ch) for ch in kids]
    ypos[node] = sum(ys) / len(ys)
    return ypos[node]


layout(0)

fig, ax = plt.subplots(1, 3, figsize=(12.6, 3.8))

for parent, kids in children.items():
    for ch in kids:
        col = PALETTE[1] if ch in mutant else PALETTE[0]
        ax[0].plot([gen[parent], gen[ch]], [ypos[parent], ypos[ch]],
                   color=col, lw=1.6, zorder=1)
for node in gen:
    col = PALETTE[1] if node in mutant else PALETTE[0]
    ax[0].plot(gen[node], ypos[node], "o", color=col, ms=6, zorder=2)
ax[0].plot([], [], "o", color=PALETTE[0], label=r"wild type ($R_0<1$)")
ax[0].plot([], [], "o", color=PALETTE[1], label=r"adapted ($R_0>1$)")
ax[0].set_xlabel("transmission generation")
ax[0].set_title("A. A rescued chain")
ax[0].set_yticks([])
ax[0].legend(fontsize=8, loc="upper left")

# --- Panel B: emergence probability vs initial R0 (rare-mutation formula). ---
n, pm = 10, 0.16                        # mutant contacts and per-contact risk
qm = 0.0
for _ in range(1000):
    qm = (1 - pm + pm * qm) ** n        # mutant extinction probability
pi_est = 1 - qm                         # mutant establishment probability
Rw = np.linspace(0.3, 0.99, 300)
for mu, col in zip([5e-4, 2e-3, 8e-3], [PALETTE[2], PALETTE[0], PALETTE[3]]):
    P = 1 - np.exp(-mu * Rw / (1 - Rw) * pi_est)
    ax[1].plot(Rw, P, color=col, lw=2, label=rf"$\mu = {mu:g}$")
ax[1].set_xlabel(r"initial $R_0$ of the spillover")
ax[1].set_ylabel("probability of emergence")
ax[1].set_title("B. Emergence vs initial $R_0$")
ax[1].legend(fontsize=8, loc="upper left")

# --- Panel C: an evolutionary-rescue trajectory. ----------------------------
t = np.arange(0, 26)
Rw0, Rm0, t_mut = 0.82, 1.5, 8
wild = Rw0 ** t
adapted = np.where(t >= t_mut, Rm0 ** (t - t_mut), 0.0)
total = wild + adapted
ax[2].plot(t, wild, color=PALETTE[0], lw=2, label="wild type")
ax[2].plot(t, adapted, color=PALETTE[1], lw=2, label="adapted type")
ax[2].plot(t, total, color=INK, lw=1.5, ls="--", label="total")
ax[2].axvline(t_mut, color=MUTED, ls=":", lw=1)
ax[2].annotate("mutation", xy=(t_mut, 0.05), xytext=(t_mut + 1.5, 0.3),
               arrowprops=dict(arrowstyle="->", color=INK), fontsize=9)
ax[2].set_yscale("log")
ax[2].set_ylim(1e-2, 1e3)
ax[2].set_xlabel("transmission generation")
ax[2].set_ylabel("expected cases")
ax[2].set_title("C. Evolutionary rescue")
ax[2].legend(fontsize=8, loc="lower left")

fig.tight_layout()
save(fig, "assets/figures/evolutionary-emergence.svg")
