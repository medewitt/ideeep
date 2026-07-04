# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Coalescent tree beside a skyline estimate of the effective size."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (ax_tree, ax_sky) = plt.subplots(1, 2, figsize=(9.0, 3.9))

# --- Left: a time-scaled coalescent genealogy of five samples ---------------
# Vertical segments: (x, t_start, t_end); time runs into the past downward.
verticals = [
    (0.0, 0.0, 0.30),   # tip A
    (1.0, 0.0, 0.30),   # tip B
    (0.5, 0.30, 2.00),  # ancestor of A, B
    (2.0, 0.0, 0.70),   # tip C
    (3.0, 0.0, 0.70),   # tip D
    (2.5, 0.70, 1.20),  # ancestor of C, D
    (4.0, 0.0, 1.20),   # tip E
    (3.25, 1.20, 2.00), # ancestor of (C, D), E
]
# Horizontal coalescence bars: (t, x_left, x_right).
horizontals = [
    (0.30, 0.0, 1.0),
    (0.70, 2.0, 3.0),
    (1.20, 2.5, 4.0),
    (2.00, 0.5, 3.25),
]
for x, t0, t1 in verticals:
    ax_tree.plot([x, x], [t0, t1], color=PALETTE[0], lw=1.8)
for t, xl, xr in horizontals:
    ax_tree.plot([xl, xr], [t, t], color=PALETTE[0], lw=1.8)

for x, name in zip([0, 1, 2, 3, 4], list("ABCDE")):
    ax_tree.text(x, -0.08, name, ha="center", va="bottom",
                 fontsize=9, color=INK)
ax_tree.plot(1.875, 2.0, "o", color=PALETTE[1], ms=7)
ax_tree.annotate("TMRCA", xy=(1.875, 2.0), xytext=(2.4, 1.7),
                 fontsize=9, color=INK,
                 arrowprops=dict(arrowstyle="->", color=INK))
ax_tree.text(4.15, 0.30, "fast early\ncoalescences", fontsize=8,
             color=MUTED, va="center")
ax_tree.set_xlim(-0.4, 5.6)
ax_tree.set_ylim(2.3, -0.35)   # present at top, past downward
ax_tree.set_ylabel("time before present")
ax_tree.set_xticks([])
ax_tree.grid(False)
ax_tree.set_title("Time-scaled genealogy")

# --- Right: true N_e(t) trajectory and a piecewise-constant skyline ----------
t = np.linspace(0, 10, 240)
Ne_true = 50 + 950 / (1 + np.exp(-1.2 * (t - 5)))   # epidemic growth to plateau
ax_sky.plot(t, Ne_true, color=PALETTE[2], lw=2, label="true $N_e(t)$")

edges = np.array([0, 2, 4, 5, 6, 7, 8, 10.0])
centers = 0.5 * (edges[:-1] + edges[1:])
levels = 50 + 950 / (1 + np.exp(-1.2 * (centers - 5)))
ax_sky.step(edges, np.append(levels, levels[-1]), where="post",
            color=PALETTE[3], lw=2, label="skyline estimate")

ax_sky.set_xlabel("calendar time")
ax_sky.set_ylabel("effective population size $N_e$")
ax_sky.set_title("Skyline of $N_e(t)$")
ax_sky.legend(loc="upper left", fontsize=9)

fig.tight_layout()
save(fig, "assets/figures/phylodynamics.svg")
