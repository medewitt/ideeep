# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""The log-sum-exp trick, visualized. To add probabilities stored as logs you
must exponentiate -- but exp of a very negative log-probability underflows to
0, so the naive sum is 0 and its log is -inf. Subtracting the largest value
first (the 'max shift') slides everything into the representable range, you sum
safely, then add the max back. Same answer, no underflow.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

# three log-probabilities (e.g. paths through an HMM, or states at a tree node)
a = np.array([-1000.0, -1001.5, -1003.0])
labels = [f"{v:.1f}" for v in a]
m = a.max()

fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.6))

# left: naive exp(a) -- everything underflows to 0
naive = np.exp(a)                          # all 0.0 in float64
axL = axes[0]
axL.bar(range(len(a)), np.maximum(naive, 1e-320), color=PALETTE[1], width=0.6)
axL.set_ylim(0, 1.15)
axL.set_title("naïve:  exp(log p)", fontsize=10)
axL.set_xticks(range(len(a)))
axL.set_xticklabels(labels, fontsize=8)
axL.set_ylabel("value on the computer")
axL.text(1, 0.55, "all underflow\nto 0.0\n\nsum = 0\nlog(0) = −∞",
         ha="center", va="center", color="#8a3b2a", fontsize=9,
         fontweight="bold")

# right: exp(a - m) -- shifted into the safe range
shifted = np.exp(a - m)
axR = axes[1]
axR.bar(range(len(a)), shifted, color=PALETTE[2], width=0.6)
axR.set_ylim(0, 1.15)
axR.set_title("shifted:  exp(log p − max)", fontsize=10)
axR.set_xticks(range(len(a)))
axR.set_xticklabels([f"{v-m:.1f}" for v in a], fontsize=8)
lse = m + np.log(np.sum(shifted))
axR.text(1.02, 0.72, f"sum = {shifted.sum():.3f}\nlog + max\n= {lse:.2f}",
         ha="center", va="center", color="#2f5b3f", fontsize=9,
         fontweight="bold")

fig.suptitle("log-sum-exp: shift by the max, then it just works", y=1.02)
fig.tight_layout()
save(fig, "assets/figures/log-sum-exp.svg")
