# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Binomial(n=10, p=0.3) probability mass function."""
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

np.random.seed(0)

n, p = 10, 0.3
k = np.arange(0, n + 1)
pmf = binom.pmf(k, n, p)
mean = n * p

fig, ax = plt.subplots()
ax.bar(k, pmf, color=PALETTE[0], width=0.72, label="P(X=k)")
ax.axvline(mean, color=PALETTE[1], linewidth=1.6, linestyle="--",
           label=f"mean np = {mean:g}")
kmax = int(np.argmax(pmf))
ax.annotate(f"peak at k={kmax}\nP={pmf[kmax]:.3f}",
            xy=(kmax, pmf[kmax]), xytext=(kmax + 1.5, pmf[kmax] * 0.9),
            arrowprops=dict(arrowstyle="->", color="#26323f"))
ax.annotate(f"mean np = {mean:g}", xy=(mean, 0.02),
            xytext=(mean + 0.4, 0.24), color=PALETTE[1])

ax.set_xticks(k)
ax.set_xlabel("number of successes, k")
ax.set_ylabel("probability")
ax.set_title("Binomial(n=10, p=0.3) pmf")
ax.legend()

print(f"mean np = {mean:g}")
print(f"peak at k={kmax}, P={pmf[kmax]:.4f}")
for ki, pi in zip(k, pmf):
    print(f"  k={ki:2d}  P={pi:.4f}")

save(fig, "assets/figures/binomial-pmf.svg")
