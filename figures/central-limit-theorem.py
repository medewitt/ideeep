# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""The sampling distribution of the mean becomes normal as n grows,
even from a skewed (exponential) parent population."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()
rng = np.random.default_rng(1)

parent_mean = 1.0            # Exponential(rate=1): mean 1, sd 1 (right-skewed)
reps = 20000
ns = [1, 5, 30]

fig, axes = plt.subplots(1, 3, figsize=(8.4, 3.0), sharey=True)
for ax, n in zip(axes, ns):
    means = rng.exponential(scale=parent_mean, size=(reps, n)).mean(axis=1)
    ax.hist(means, bins=40, density=True, color=PALETTE[0], alpha=0.65,
            edgecolor="white", linewidth=0.3)
    # normal approximation with matching mean/sd
    mu, sd = parent_mean, parent_mean / np.sqrt(n)
    xs = np.linspace(means.min(), means.max(), 200)
    ax.plot(xs, np.exp(-0.5 * ((xs - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi)),
            color=PALETTE[1], lw=1.6)
    ax.set_title(f"n = {n}")
    ax.set_xlabel(r"$\bar{X}$")
axes[0].set_ylabel("density")
fig.suptitle("Central limit theorem: sample means from a skewed parent", y=1.02)
save(fig, "assets/figures/central-limit-theorem.svg")
