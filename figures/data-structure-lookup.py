# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Choosing the container changes the complexity. Doing n membership tests
("is this k-mer / sample / allele already seen?") against a list scans the
whole list each time -- O(n) per lookup, O(n^2) in total. The same tests
against a set or dictionary are O(1) each, O(n) in total. The gap is enormous
and it comes entirely from the data structure, not the algorithm.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

n = np.array([100, 300, 1000, 3000, 10_000, 30_000, 100_000], dtype=float)

list_ops = n * (n / 2)      # n lookups, each scans on average n/2  -> O(n^2)
set_ops = n * 1.0           # n lookups, each O(1)                   -> O(n)

fig, ax = plt.subplots()
ax.loglog(n, list_ops, "o-", color=PALETTE[1], lw=2.0, ms=6,
          label="membership in a list  ·  O(n) per lookup  ·  O(n²) total")
ax.loglog(n, set_ops, "s-", color=PALETTE[2], lw=2.0, ms=6,
          label="membership in a set / dict  ·  O(1) per lookup  ·  O(n) total")

xn = n[-1]
ax.annotate("", xy=(xn, list_ops[-1]), xytext=(xn, set_ops[-1]),
            arrowprops=dict(arrowstyle="<->", color="0.45", lw=1.2))
factor = list_ops[-1] / set_ops[-1]
ax.text(xn * 0.62, np.sqrt(list_ops[-1] * set_ops[-1]),
        f"{factor:,.0f}×\nfewer\noperations",
        color="0.3", fontsize=9, ha="right", va="center", fontweight="bold")

ax.set_xlabel("number of items  n")
ax.set_ylabel("total comparisons for n lookups  (log scale)")
ax.set_title("Same task, different container: list vs. set / dictionary")
ax.legend(loc="upper left", fontsize="small")
ax.grid(True, which="both", alpha=0.4)

save(fig, "assets/figures/data-structure-lookup.svg")
