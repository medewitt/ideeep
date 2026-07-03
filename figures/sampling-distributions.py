# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Sampling distribution of the mean narrows as sample size n grows."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)

mu, sigma = 10.0, 4.0
n_reps = 20000
sample_sizes = [5, 20, 80]

fig, ax = plt.subplots()

for i, n in enumerate(sample_sizes):
    samples = rng.normal(mu, sigma, size=(n_reps, n))
    means = samples.mean(axis=1)
    se = sigma / np.sqrt(n)
    ax.hist(means, bins=60, density=True, alpha=0.5,
            color=PALETTE[i % len(PALETTE)],
            label=f"n = {n}  (SE = {se:.2f})")

ax.axvline(mu, color="0.3", ls="--", lw=1.2)
ax.set_xlabel("sample mean")
ax.set_ylabel("density")
ax.set_title("Sampling distribution of the mean")
ax.annotate(r"spread = standard error $\sigma/\sqrt{n}$",
            xy=(0.02, 0.95), xycoords="axes fraction",
            va="top", ha="left", fontsize="small")
ax.legend(loc="upper right", fontsize="small")

save(fig, "assets/figures/sampling-distributions.svg")
