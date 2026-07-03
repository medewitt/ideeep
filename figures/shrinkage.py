# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Partial-pooling shrinkage: noisy group means pulled toward the grand mean."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()
rng = np.random.default_rng(7)

# ~12 small areas: true disease rates drawn around a grand mean, varied sample sizes
J = 12
mu = 5.0           # grand mean rate (per 1000)
tau = 1.6          # between-group SD
sigma = 3.0        # within-group observation SD (per single count-scale unit)

true = rng.normal(mu, tau, size=J)
n = rng.integers(3, 60, size=J)          # sample sizes: some tiny, some large
raw = true + rng.normal(0, sigma / np.sqrt(n))   # no-pooling estimates (noisy)

grand = raw.mean()
# empirical-Bayes shrinkage weight: reliability of each group's estimate
se2 = sigma**2 / n                        # sampling variance of each raw mean
w = tau**2 / (tau**2 + se2)               # weight on the data (0..1)
shrunk = grand + w * (raw - grand)        # pull toward grand mean

# print a few raw vs shrunken values
order = np.argsort(n)
print("grand mean =", round(grand, 3))
print(" n   raw     shrunk   weight")
for i in order[[0, 1, -2, -1]]:
    print(f"{n[i]:3d}  {raw[i]:6.2f}  {shrunk[i]:6.2f}  {w[i]:.2f}")

fig, ax = plt.subplots(figsize=(6.2, 4.2))
ax.axhline(grand, ls="--", color="#5b6b7a", lw=1.0)
ax.text(2.06, grand, "grand mean", va="center", ha="left", color="#5b6b7a", fontsize=9)

for i in range(J):
    ax.annotate("", xy=(2, shrunk[i]), xytext=(1, raw[i]),
                arrowprops=dict(arrowstyle="->", color="#b0b8c0", lw=1.0))
ax.scatter(np.ones(J), raw, s=20 + n * 3, color=PALETTE[0], zorder=3, label="no pooling (raw)")
ax.scatter(np.full(J, 2), shrunk, s=20 + n * 3, color=PALETTE[1], zorder=3, label="partial pooling")

ax.set_xlim(0.6, 2.7)
ax.set_xticks([1, 2])
ax.set_xticklabels(["raw\nestimate", "shrunken\nestimate"])
ax.set_ylabel("estimated rate (per 1000)")
ax.set_title("Shrinkage toward the grand mean (marker size = sample size)")
ax.legend(loc="upper right")
ax.grid(axis="x", visible=False)
save(fig, "assets/figures/shrinkage.svg")
