# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Gaussian process prior samples and a regression posterior with a 95% band."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()

rng = np.random.default_rng(0)


def rbf(a, b, ell=1.0, sf2=1.0):
    """RBF (squared-exponential) covariance between input vectors a and b."""
    d2 = (a[:, None] - b[None, :]) ** 2
    return sf2 * np.exp(-0.5 * d2 / ell ** 2)


xs = np.linspace(-5, 5, 200)

# --- GP prior: draw several sample functions from GP(0, k) ---
Kprior = rbf(xs, xs) + 1e-9 * np.eye(xs.size)   # jitter for a stable Cholesky
Lp = np.linalg.cholesky(Kprior)
prior_draws = Lp @ rng.standard_normal((xs.size, 4))

# --- GP posterior given noisy observations ---
X = np.array([-4.0, -2.5, -0.5, 1.0, 3.0])       # training inputs
y = np.array([-1.2, 0.6, 1.4, 0.2, -0.8])        # noisy observations
sn2 = 0.05                                        # noise variance
K = rbf(X, X) + sn2 * np.eye(X.size)
alpha = np.linalg.solve(K, y)
Ks = rbf(xs, X)
mean = Ks @ alpha
cov = rbf(xs, xs) - Ks @ np.linalg.solve(K, Ks.T)
sd = np.sqrt(np.clip(np.diag(cov), 0.0, None))

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.4, 3.8))

for i in range(prior_draws.shape[1]):
    ax0.plot(xs, prior_draws[:, i], color=PALETTE[i % len(PALETTE)], lw=1.4)
ax0.set_title("Prior samples  f ~ GP(0, k)")
ax0.set_xlabel("x")
ax0.set_ylabel("f(x)")

ax1.fill_between(xs, mean - 1.96 * sd, mean + 1.96 * sd,
                 color=PALETTE[0], alpha=0.20, label="95% band")
ax1.plot(xs, mean, color=PALETTE[0], lw=1.8, label="posterior mean")
ax1.plot(X, y, "o", color=INK, ms=6, label="observations")
ax1.set_title("Posterior given data")
ax1.set_xlabel("x")
ax1.set_ylabel("f(x)")
ax1.legend(loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/gaussian-processes.svg")
