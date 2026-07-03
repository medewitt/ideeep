# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Bernoulli log-likelihood and the MLE for k=7 successes in n=10."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

k, n = 7, 10
p = np.linspace(1e-3, 1 - 1e-3, 500)
loglik = k * np.log(p) + (n - k) * np.log(1 - p)

p_hat = k / n  # = 0.7
loglik_hat = k * np.log(p_hat) + (n - k) * np.log(1 - p_hat)
print(f"MLE p_hat = k/n = {p_hat}")
print(f"log-likelihood at MLE = {loglik_hat:.4f}")

fig, ax = plt.subplots()
ax.plot(p, loglik, color=PALETTE[0], lw=2, label=r"$\ell(p)$")
ax.axvline(p_hat, color=PALETTE[1], lw=1.5, ls="--")
ax.plot([p_hat], [loglik_hat], "o", color=PALETTE[1], ms=8, zorder=5)

ax.annotate(r"MLE $\hat{p} = 0.7$", xy=(p_hat, loglik_hat),
            xytext=(p_hat - 0.42, loglik_hat - 3),
            arrowprops=dict(arrowstyle="->", color="#26323f"))

ax.set_ylim(loglik_hat - 12, loglik_hat + 1)
ax.set_xlabel("p (success probability)")
ax.set_ylabel(r"log-likelihood  $\ell(p)$")
ax.set_title(f"Bernoulli log-likelihood (k={k}, n={n})")
ax.legend(loc="lower center")

save(fig, "assets/figures/likelihood.svg")
