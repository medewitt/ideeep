# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Hilbert-space (HSGP) approximation of a Gaussian process:
the first Laplacian eigenfunctions on [-L, L] and sample paths drawn from
the finite basis-function expansion f(x) = sum_j sqrt(S(sqrt(lam_j))) phi_j(x) beta_j."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()
rng = np.random.default_rng(0)

# Domain and (squared-exponential) kernel hyperparameters
L = 3.0        # boundary half-width, L = c * S
ell = 0.6      # lengthscale
sigma = 1.0    # marginal standard deviation

x = np.linspace(-L, L, 400)


def sqrt_lam(j):
    # sqrt of the j-th Laplacian eigenvalue: sqrt(lam_j) = j*pi / (2L)
    return j * np.pi / (2 * L)


def phi(j, x):
    # sine eigenfunction phi_j(x) = sqrt(1/L) sin(sqrt(lam_j) (x + L))
    return np.sqrt(1.0 / L) * np.sin(sqrt_lam(j) * (x + L))


def S_rbf(w):
    # RBF (squared-exponential) spectral density in 1D
    return sigma**2 * np.sqrt(2 * np.pi) * ell * np.exp(-0.5 * (w * ell) ** 2)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.0))

# Panel 1: first four Laplacian eigenfunctions
for j in range(1, 5):
    ax1.plot(x, phi(j, x), color=PALETTE[(j - 1) % len(PALETTE)], label=f"j = {j}")
ax1.set_xlabel("x")
ax1.set_ylabel(r"$\phi_j(x)$")
ax1.set_title("Laplacian eigenfunctions on [-L, L]")
ax1.legend(title="basis", ncol=2)

# Panel 2: sample paths from the HSGP prior
m = 30
j = np.arange(1, m + 1)
Phi = np.stack([phi(k, x) for k in j])                 # (m, len(x))
sd = np.sqrt(S_rbf(sqrt_lam(j)))                        # (m,) spectral weights
for c in range(3):
    beta = rng.standard_normal(m)                       # beta_j ~ N(0, 1)
    f = (sd[:, None] * Phi * beta[:, None]).sum(axis=0)
    ax2.plot(x, f, color=PALETTE[c], lw=1.6, alpha=0.9)
ax2.axhline(0.0, color=MUTED, lw=0.8, ls="--")
ax2.set_xlabel("x")
ax2.set_ylabel("f(x)")
ax2.set_title(f"HSGP prior draws (m = {m})")

fig.tight_layout()
save(fig, "assets/figures/hilbert-space-gp.svg")
