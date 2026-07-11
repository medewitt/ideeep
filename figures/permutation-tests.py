# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "scipy"]
# ///
"""A permutation test builds the null distribution by relabelling. For the
worked two-group example there are only C(6,3)=20 ways to split the six pooled
values into two groups of three; recomputing the mean difference for each traces
out the exact null distribution. The observed statistic T_obs = 1.033 sits far
in the right tail, and the p-value is the fraction of permutations at least as
extreme — with n=3 vs 3 the smallest attainable value is 1/20 = 0.05."""
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

a = [5.1, 6.3, 5.8]
b = [4.2, 4.9, 5.0]
pool = np.array(a + b)
obs = np.mean(a) - np.mean(b)          # 1.033

# all 20 splits into two groups of three
diffs = []
idx_all = set(range(6))
for grp in combinations(range(6), 3):
    ga = pool[list(grp)]
    gb = pool[list(idx_all - set(grp))]
    diffs.append(ga.mean() - gb.mean())
diffs = np.array(diffs)

fig, ax = plt.subplots(figsize=(6.6, 3.9))
bins = np.linspace(-1.4, 1.4, 15)
extreme = np.abs(diffs) >= abs(obs) - 1e-9
ax.hist(diffs[~extreme], bins=bins, color=PALETTE[0] + "bb", edgecolor="white",
        linewidth=0.5, label="permutations")
ax.hist(diffs[extreme], bins=bins, color=PALETTE[1] + "cc", edgecolor="white",
        linewidth=0.5, label=r"$|T^*|\geq|T_{obs}|$")
ax.axvline(obs, color=INK, lw=1.6)
ax.annotate(fr"$T_{{obs}}={obs:.3f}$", xy=(obs, 3.2), xytext=(obs - 1.25, 3.3),
            fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
p = (extreme.sum()) / len(diffs)
ax.text(-1.3, 2.4, f"all 20 label splits\n(C(6,3)=20)\n"
        fr"$p={extreme.sum()}/20={p:.2f}$", fontsize=8.5, color=INK)
ax.set_xlabel(r"permuted statistic  $\bar X_A - \bar X_B$")
ax.set_ylabel("number of permutations")
ax.set_title("The permutation null distribution", fontsize=11)
ax.legend(fontsize=8.5, loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/permutation-tests.svg")
