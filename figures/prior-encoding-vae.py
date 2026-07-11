# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""PriorVAE: encode a slow spatial prior into a fast neural one. Left: draws
from a Gaussian-process prior over a spatial field -- smooth, correlated
surfaces that are expensive to sample inside an MCMC loop. Right: the PriorVAE
recipe -- train a VAE offline to reproduce those draws, then plug the frozen
decoder into Bayesian inference so a handful of independent latent variables
stand in for the full correlated field.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(3)

# --- left: GP prior draws over a 1D spatial transect ---
s = np.linspace(0, 1, 120)
d2 = (s[:, None] - s[None, :]) ** 2
K = np.exp(-0.5 * d2 / 0.12 ** 2) + 1e-9 * np.eye(s.size)
L = np.linalg.cholesky(K)
draws = L @ rng.standard_normal((s.size, 6))

fig = plt.figure(figsize=(9.8, 3.9))
ax0 = fig.add_axes([0.06, 0.15, 0.40, 0.72])
for i in range(draws.shape[1]):
    ax0.plot(s, draws[:, i], color=PALETTE[i % len(PALETTE)], lw=1.5,
             alpha=0.9)
ax0.set_title("Draws from the spatial prior  $f\\sim\\mathcal{GP}$")
ax0.set_xlabel("location  $s$")
ax0.set_ylabel("latent field  $f(s)$")

# --- right: the PriorVAE workflow ---
ax1 = fig.add_axes([0.52, 0.02, 0.46, 0.96])
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")


def box(x, y, w, h, text, color, fs=8.8):
    ax1.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                  linewidth=1.6, edgecolor=color, facecolor=color + "18"))
    ax1.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fs, color=INK)


box(1.4, 8.1, 7.2, 1.5, "① sample many draws from\nthe GP / ICAR prior",
    PALETTE[0])
box(1.4, 5.6, 7.2, 1.5, "② train a VAE to reconstruct\nthe draws (offline, once)",
    PALETTE[3])
box(1.4, 3.1, 7.2, 1.5, "③ freeze the decoder\n$f \\approx g_\\theta(z)$",
    PALETTE[2])
box(1.4, 0.6, 7.2, 1.5,
    "④ MCMC over $z\\sim\\mathcal{N}(0,I)$\nas the prior — fast & smooth",
    PALETTE[1])
for y0 in (8.05, 5.55, 3.05):
    ax1.add_patch(FancyArrowPatch((5.0, y0), (5.0, y0 - 0.45),
                  arrowstyle="-|>", mutation_scale=14, color="0.45", lw=1.6))

save(fig, "assets/figures/prior-encoding-vae.svg")
