# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""A population-biology example of complexity: an individual-based epidemic
model. If every individual can contact every other one, each timestep costs
O(N^2); if individuals only contact a fixed number of local neighbours, it
costs O(N). The modelling choice, not the hardware, decides whether the run
finishes in seconds or days.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

N = np.array([100, 300, 1000, 3000, 10_000, 30_000, 100_000], dtype=float)
k = 10                                   # average local contacts per individual

all_pairs = N**2                         # check every pair: O(N^2)
local = N * k                            # check k neighbours each: O(N)

fig, ax = plt.subplots()
ax.loglog(N, all_pairs, "o-", color=PALETTE[1], lw=2.0, ms=6,
          label="everyone mixes with everyone  ·  O(N²)")
ax.loglog(N, local, "s-", color=PALETTE[2], lw=2.0, ms=6,
          label=f"local contacts (k={k} neighbours)  ·  O(N)")

# annotate the gap at the largest population
xn = N[-1]
ax.annotate("", xy=(xn, all_pairs[-1]), xytext=(xn, local[-1]),
            arrowprops=dict(arrowstyle="<->", color="0.45", lw=1.2))
factor = all_pairs[-1] / local[-1]
ax.text(xn * 0.62, np.sqrt(all_pairs[-1] * local[-1]),
        f"{factor:,.0f}×\nmore work",
        color="0.3", fontsize=9, ha="right", va="center", fontweight="bold")

ax.set_xlabel("population size  N")
ax.set_ylabel("interactions checked per timestep  (log scale)")
ax.set_title("Individual-based epidemic model: the cost of “everyone mixes”")
ax.legend(loc="upper left", fontsize="small")
ax.grid(True, which="both", alpha=0.4)

save(fig, "assets/figures/population-model-scaling.svg")
