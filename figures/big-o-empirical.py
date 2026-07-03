# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Measuring complexity by simulation: time real code as the input grows.

You don't have to *derive* an algorithm's complexity -- you can *measure*
it. Run the code on inputs of growing size, record the wall-clock time, and
plot it on log-log axes. On log-log axes a power law time ~ n^k becomes a
straight line whose slope is the exponent k: a single loop (linear) has
slope ~1, an all-pairs double loop (quadratic) has slope ~2.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()


def timeit(fn, arg, repeats=3):
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(arg)
        best = min(best, time.perf_counter() - t0)
    return best


def linear_sum(data):
    """O(n): touch every element once."""
    total = 0.0
    for x in data:
        total += x
    return total


def all_pairs(data):
    """O(n²): compare every element with every other -- e.g. a distance
    matrix or all-vs-all sequence comparison."""
    n = len(data)
    acc = 0.0
    for i in range(n):
        di = data[i]
        for j in range(n):
            acc += abs(di - data[j])
    return acc


rng = np.random.default_rng(0)

lin_n = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
quad_n = [100, 200, 400, 800, 1600, 3200]

lin_t = [timeit(linear_sum, rng.random(n).tolist()) for n in lin_n]
quad_t = [timeit(all_pairs, rng.random(n).tolist()) for n in quad_n]

# fit slopes on log-log axes: log t = k * log n + c  ->  k is the exponent
lin_k = np.polyfit(np.log(lin_n), np.log(lin_t), 1)[0]
quad_k = np.polyfit(np.log(quad_n), np.log(quad_t), 1)[0]

fig, ax = plt.subplots()
ax.loglog(lin_n, lin_t, "o-", color=PALETTE[4], lw=1.8, ms=6,
          label=f"single loop  (measured slope ≈ {lin_k:.1f}  → O(n))")
ax.loglog(quad_n, quad_t, "s-", color=PALETTE[1], lw=1.8, ms=6,
          label=f"all-pairs loop  (measured slope ≈ {quad_k:.1f}  → O(n²))")

ax.set_xlabel("input size  n  (log scale)")
ax.set_ylabel("time in seconds  (log scale)")
ax.set_title("Diagnosing complexity by measurement")
ax.legend(loc="upper left", fontsize="small")
ax.grid(True, which="both", alpha=0.4)

save(fig, "assets/figures/big-o-empirical.svg")
