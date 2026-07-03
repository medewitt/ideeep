# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Law of large numbers: running average of fair die rolls converging to 3.5."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)

n = 2000
n_seq = 5
true_mean = 3.5

fig, ax = plt.subplots()

x = np.arange(1, n + 1)
for i in range(n_seq):
    rolls = rng.integers(1, 7, size=n)
    running = np.cumsum(rolls) / x
    ax.plot(x, running, color=PALETTE[i % len(PALETTE)], lw=1.3,
            alpha=0.85, label=f"sequence {i + 1}")

ax.axhline(true_mean, color="0.3", ls="--", lw=1.5,
           label=f"true mean = {true_mean}")

ax.set_xscale("log")
ax.set_xlabel("number of rolls (n)")
ax.set_ylabel("running average")
ax.set_title("Law of large numbers: fair die rolls")
ax.set_ylim(1, 6)
ax.legend(loc="upper right", fontsize="small")

save(fig, "assets/figures/law-of-large-numbers.svg")
