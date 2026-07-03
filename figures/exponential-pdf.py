# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Exponential pdf for waiting time between events."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

np.random.seed(0)

lam = 0.5
x = np.linspace(0, 12, 400)
pdf = lam * np.exp(-lam * x)
mean = 1 / lam

fig, ax = plt.subplots()
ax.plot(x, pdf, color=PALETTE[0], linewidth=2.0,
        label=r"$\lambda e^{-\lambda x},\ \lambda=0.5$")
ax.fill_between(x, pdf, color=PALETTE[0], alpha=0.12)
ax.axvline(mean, color=PALETTE[1], linewidth=1.6, linestyle="--",
           label=f"mean = 1/λ = {mean:g}")
ax.annotate(r"mean = 1/$\lambda$ = 2",
            xy=(mean, lam * np.exp(-1)),
            xytext=(mean + 1.5, 0.30), color=PALETTE[1],
            arrowprops=dict(arrowstyle="->", color=PALETTE[1]))

ax.set_xlabel("waiting time between infectious contacts")
ax.set_ylabel("probability density")
ax.set_title("Exponential waiting time (λ=0.5)")
ax.legend()

print(f"lambda = {lam}")
print(f"mean = 1/lambda = {mean:g}")
print(f"pdf(0) = {pdf[0]:.4f}")

save(fig, "assets/figures/exponential-pdf.svg")
