# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Repeated measures: same subjects across conditions. Thin lines are individual
subject trajectories over three conditions; the thick line is the condition mean.
Subjects differ a lot in level (lines are spread vertically) but each moves
similarly across conditions. A repeated-measures analysis compares the movement
within each subject, removing the vertical spread that a between-subjects analysis
would leave in the error term."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(3)

n_subj = 12
conditions = [1, 2, 3]
tau = np.array([0.0, 2.0, 3.0])            # condition effects
subj_level = rng.normal(0, 4.0, n_subj)    # large between-subject spread

fig, ax = plt.subplots(figsize=(6.4, 3.9))

for i in range(n_subj):
    y = 10 + subj_level[i] + tau + rng.normal(0, 0.6, 3)
    ax.plot(conditions, y, color=MUTED, lw=0.9, alpha=0.6, marker="o", ms=3)

mean_curve = 10 + tau
ax.plot(conditions, mean_curve, color=PALETTE[1], lw=3.0, marker="o", ms=7,
        label="condition mean", zorder=6)

# annotate the two kinds of spread
ax.annotate("between-subject spread\n(removed by pairing)", xy=(1, 16.5),
            xytext=(1.25, 18.5), fontsize=8.3, color=INK,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
ax.annotate("within-subject change\n(the signal)", xy=(2.5, mean_curve[1:].mean()),
            xytext=(2.1, 6.0), fontsize=8.3, color=PALETTE[1],
            arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.9))

ax.set_xticks(conditions)
ax.set_xticklabels(["cond 1", "cond 2", "cond 3"])
ax.set_xlim(0.8, 3.2)
ax.set_xlabel("condition")
ax.set_ylabel("response")
ax.legend(fontsize=8.5, loc="lower right")
ax.grid(axis="x", visible=False)
fig.tight_layout()
save(fig, "assets/figures/repeated-measures.svg")
