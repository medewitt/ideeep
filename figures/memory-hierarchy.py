# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""The memory hierarchy: why *where* your data sits dominates speed. Each level
away from the CPU is much bigger but dramatically slower -- cache is tiny and
near-instant, RAM is ~100x slower, disk is ~100,000x slower again. Vectorized
code and cache-friendly access patterns win because they keep the CPU working
from the fast, nearby levels instead of waiting on distant memory.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save

apply_style()

# level, approximate latency in nanoseconds, rough size, colour
levels = [
    ("CPU register", 0.3,    "~1 KB",   "#2f6f9f"),
    ("L1 cache",     1.0,    "~64 KB",  "#3f8f5b"),
    ("L2 cache",     4.0,    "~1 MB",   "#3f8f5b"),
    ("L3 cache",     15.0,   "~32 MB",  "#3f8f5b"),
    ("RAM",          100.0,  "~16 GB",  "#b0842f"),
    ("SSD",          100_000.0,   "~1 TB",  "#c1531f"),
    ("network / spinning disk", 10_000_000.0, "≫ 1 TB", "#b0332f"),
]

names = [x[0] for x in levels]
lat = np.array([x[1] for x in levels])
sizes = [x[2] for x in levels]
colors = [x[3] for x in levels]

y = np.arange(len(levels))[::-1]        # CPU at the top

fig, ax = plt.subplots(figsize=(6.8, 4.0))
ax.barh(y, lat, color=colors, height=0.62, log=True)

for yi, l, sz in zip(y, lat, sizes):
    ax.text(l * 1.6, yi, sz, va="center", ha="left", fontsize=8.5,
            color="#26323f")

ax.set_yticks(y)
ax.set_yticklabels(names, fontsize=9)
ax.set_xlabel("time to fetch one item  (nanoseconds, log scale)")
ax.set_xlim(0.1, 3e8)
ax.set_title("The memory hierarchy: closer is smaller, but far faster")
ax.grid(axis="y", visible=False)

ax.annotate("~100× slower\nthan cache", xy=(100, y[4]), xytext=(2500, y[4] + 0.1),
            fontsize=8, color="#8a6a1f",
            arrowprops=dict(arrowstyle="->", color="#b0842f", lw=1.0))

save(fig, "assets/figures/memory-hierarchy.svg")
