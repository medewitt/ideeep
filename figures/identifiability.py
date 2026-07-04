# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""A log-likelihood ridge from a non-identified parameter pair.

Counts whose mean depends only on the product beta*N leave the two parameters
unidentified: the log-likelihood is flat along the hyperbola beta*N = ybar.
The contour shows the ridge, and the dashed curve traces it.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1834)
beta_true, N_true = 0.4, 50.0
y = rng.poisson(beta_true * N_true, size=30)
s = y.sum()
n = len(y)
ybar = y.mean()

betas = np.linspace(0.1, 1.0, 240)
Ns = np.linspace(10.0, 200.0, 240)
B, NN = np.meshgrid(betas, Ns)
MU = B * NN
# Poisson log-likelihood (dropping the data-only constant).
LL = s * np.log(MU) - n * MU

fig, ax = plt.subplots()
ax.grid(False)
cs = ax.contourf(B, NN, LL, levels=25, cmap="viridis")
ridge_beta = np.linspace(0.1, 1.0, 200)
ax.plot(ridge_beta, ybar / ridge_beta, color=PALETTE[1], lw=2.2, ls="--",
        label=r"ridge $\beta N=\bar y$")

ax.set_xlabel(r"$\beta$ (transmission rate)")
ax.set_ylabel(r"$N$ (population size)")
ax.set_ylim(10, 200)
ax.set_title(r"Only the product $\beta N$ is identified")
cbar = fig.colorbar(cs, ax=ax)
cbar.set_label("log-likelihood")
ax.legend(loc="upper right", fontsize=9)

save(fig, "assets/figures/identifiability.svg")
