# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Poisson(lambda=3) probability mass function."""
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

np.random.seed(0)

lam = 3
k = np.arange(0, 13)
pmf = poisson.pmf(k, lam)

fig, ax = plt.subplots()
ax.bar(k, pmf, color=PALETTE[2], width=0.72, label="P(X=k)")
ax.axvline(lam, color=PALETTE[1], linewidth=1.6, linestyle="--",
           label=f"lambda = {lam}")
kmax = int(np.argmax(pmf))
ax.annotate(f"peak k={kmax}\nP={pmf[kmax]:.3f}",
            xy=(kmax, pmf[kmax]), xytext=(kmax + 2, pmf[kmax] * 0.85),
            arrowprops=dict(arrowstyle="->", color="#26323f"))
ax.annotate("mean = variance = 3", xy=(lam, 0.02),
            xytext=(lam + 0.6, 0.20), color=PALETTE[1])

ax.set_xticks(k)
ax.set_xlabel("number of events, k")
ax.set_ylabel("probability")
ax.set_title("Poisson(λ=3) pmf")
ax.legend()

print("mean = variance = 3")
for ki, pi in zip(k, pmf):
    print(f"  k={ki:2d}  P={pi:.4f}")

save(fig, "assets/figures/poisson-pmf.svg")
