# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Coalescent genealogy for n=6 lineages with waiting times T_k."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

n = 6

# Simulate coalescent waiting times. With k lineages the time to the next
# coalescence is Exp(rate = k(k-1)/2) in units of Ne generations.
times = {}
t = 0.0
for k in range(n, 1, -1):
    rate = k * (k - 1) / 2.0
    dt = rng.exponential(1.0 / rate)
    t += dt
    times[k] = (t - dt, t)          # (start, end) of interval with k lineages

# Each active lineage is a dict with its current x position and the time it
# last became active (bottom y of its vertical segment).
tips_x = np.arange(n, dtype=float)   # tip positions 0..n-1
lineages = [{"x": x, "y0": 0.0} for x in tips_x]

fig, ax = plt.subplots(figsize=(6.4, 4.0))

# Perform n-1 coalescence events, from k=n down to k=2. At each event merge
# two randomly chosen adjacent lineages and continue the parent upward.
for k in range(n, 1, -1):
    t_event = times[k][1]
    order = np.argsort([lin["x"] for lin in lineages])
    lineages = [lineages[i] for i in order]
    i = int(rng.integers(0, len(lineages) - 1))   # adjacent pair (i, i+1)
    left, right = lineages[i], lineages[i + 1]

    # Draw the two vertical branches up to the coalescence time.
    for lin in (left, right):
        ax.plot([lin["x"], lin["x"]], [lin["y0"], t_event],
                color=INK, lw=1.6, solid_capstyle="round")
    # Horizontal join.
    ax.plot([left["x"], right["x"]], [t_event, t_event],
            color=INK, lw=1.6, solid_capstyle="round")

    parent_x = 0.5 * (left["x"] + right["x"])
    parent = {"x": parent_x, "y0": t_event}
    lineages = lineages[:i] + [parent] + lineages[i + 2:]

# The single remaining lineage is the MRCA.
mrca = lineages[0]
t_mrca = times[2][1]
ax.plot(mrca["x"], t_mrca, "o", color=PALETTE[1], ms=8, zorder=5)
ax.annotate("MRCA", (mrca["x"], t_mrca), xytext=(6, 4),
            textcoords="offset points", fontsize=9, color=PALETTE[1])

# Annotate the interval boundaries T_k on the right margin.
x_r = n - 0.4
for k in range(n, 1, -1):
    y0, y1 = times[k]
    ax.plot([x_r, x_r], [y0, y1], color=MUTED, lw=1.0)
    ax.plot([x_r - 0.06, x_r + 0.06], [y0, y0], color=MUTED, lw=1.0)
    ax.plot([x_r - 0.06, x_r + 0.06], [y1, y1], color=MUTED, lw=1.0)
    ax.annotate(f"$T_{{{k}}}$", (x_r + 0.12, 0.5 * (y0 + y1)),
                va="center", fontsize=9, color=MUTED)

ax.annotate("deepest interval $T_2$ (2 lineages)\nis the longest",
            (x_r, 0.5 * (times[2][0] + times[2][1])),
            xytext=(-2.3, times[2][1] * 0.92), fontsize=8, color=MUTED,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
ax.annotate("recent intervals (many\nlineages) are short",
            (x_r, times[n][1] * 0.5),
            xytext=(-2.3, times[2][0] * 0.35), fontsize=8, color=MUTED,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))

ax.set_xticks(tips_x)
ax.set_xticklabels([f"sample {i + 1}" for i in range(n)], fontsize=8,
                   rotation=30, ha="right")
ax.set_ylabel(r"time into the past ($\times N_e$ generations)")
ax.set_ylim(0, t_mrca * 1.12)
ax.set_xlim(-0.6, n + 0.4)
ax.grid(axis="x", visible=False)
ax.set_title("Coalescent genealogy of n = 6 lineages")

save(fig, "assets/figures/coalescent-theory.svg")
