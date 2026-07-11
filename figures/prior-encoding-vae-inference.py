# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""The output of PriorVAE inference. Using the encoded prior (here the linear
Karhunen-Loeve decoder from the page), the model recovers a smooth latent field
from a handful of noisy observations: the posterior mean tracks the true field,
and the 95% credible band widens between observations and narrows where data
pin it down. Sampling six independent latents in place of a correlated
25-dimensional field is what makes this fast and well-mixing.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(0)

s = np.linspace(0, 1, 25)
K = np.exp(-0.5 * (s[:, None] - s[None, :]) ** 2 / 0.15 ** 2) + 1e-9 * np.eye(25)
vals, vecs = np.linalg.eigh(K)
idx = np.argsort(vals)[::-1][:6]
B = vecs[:, idx] * np.sqrt(vals[idx])          # 25 x 6 linear decoder (KL modes)

f_true = B @ rng.standard_normal(6)             # the field to recover
sigma = 0.1
y = f_true + sigma * rng.standard_normal(25)    # noisy observations

# closed-form linear-Gaussian posterior over z ~ N(0, I) with y ~ N(Bz, sigma^2)
Sig = np.linalg.inv(B.T @ B / sigma ** 2 + np.eye(6))
mu = Sig @ B.T @ y / sigma ** 2
f_hat = B @ mu
band = 1.96 * np.sqrt(np.diag(B @ Sig @ B.T))
rmse = np.sqrt(np.mean((f_hat - f_true) ** 2))

fig, ax = plt.subplots(figsize=(7.4, 3.7))
ax.fill_between(s, f_hat - band, f_hat + band, color=PALETTE[0], alpha=0.18,
                label="95% credible band")
ax.plot(s, f_true, color=INK, lw=2, label="true field")
ax.plot(s, f_hat, color=PALETTE[0], lw=2, ls="--", label="posterior mean")
ax.scatter(s, y, s=24, color=PALETTE[1], zorder=3, label="noisy observations")
ax.set_title(f"PriorVAE inference: field recovered from 6 latents "
             f"(RMSE {rmse:.3f})", fontsize=10.5)
ax.set_xlabel("location  $s$")
ax.set_ylabel("latent field  $f(s)$")
ax.legend(loc="upper right", fontsize=8, ncol=2)

fig.tight_layout()
save(fig, "assets/figures/prior-encoding-vae-inference.svg")
