# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""k-anonymity: coarsening one quasi-identifier lifts the smallest group above the threshold."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

K = 5  # re-identification-risk threshold

# Four fine-grained quasi-identifier groups (age band, sex, reporting week),
# matching the worked example on the page. Dropping the "week" identifier
# coarsens them into two groups, so each fine-grained group inherits the size
# of the merged group it now belongs to.
labels = [
    "30-39\nF, wk27",
    "30-39\nF, wk28",
    "40-49\nM, wk27",
    "40-49\nM, wk28",
]
fine = np.array([3, 2, 5, 2])       # min k = 2
coarse = np.array([5, 5, 7, 7])     # merged (30-39,F)=5, (40-49,M)=7; min k = 5

x = np.arange(len(labels))
w = 0.38

fig, ax = plt.subplots(figsize=(6.6, 4.0))

ax.bar(x - w / 2, fine, width=w, color=PALETTE[1], label="fine-grained")
ax.bar(x + w / 2, coarse, width=w, color=PALETTE[0], label="coarsened")

# Re-identification-risk threshold: groups below this line are risky.
ax.axhline(K, ls="--", lw=1.4, color=INK, zorder=3)
ax.annotate(f"k = {K} threshold", xy=(len(labels) - 0.5, K), xytext=(0, 4),
            textcoords="offset points", ha="right", va="bottom",
            fontsize="small", color=INK)

# Flag the fine-grained groups that fall below the threshold.
for xi, h in zip(x - w / 2, fine):
    if h < K:
        ax.annotate("risky", xy=(xi, h), xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize="x-small", color=MUTED)

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylim(0, 8)
ax.set_xlabel("quasi-identifier group")
ax.set_ylabel("group size k")
ax.set_title("Coarsening raises the minimum k-anonymity group size")
ax.legend(loc="upper left")

fig.tight_layout()

print(f"fine-grained  min k = {fine.min()}, failing k<{K}: {(fine < K).sum()} of {len(fine)}")
print(f"coarsened     min k = {coarse.min()}, failing k<{K}: {(coarse < K).sum()} of {len(coarse)}")

save(fig, "assets/figures/research-data-ethics-and-governance.svg")
