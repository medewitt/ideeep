# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""The variational autoencoder as a surveillance anomaly detector. Left: the
encoder squeezes each observation to a low-dimensional latent code and the
decoder rebuilds it; a smooth latent space clusters normal weeks together.
Right: normal weeks reconstruct with small error, but an aberrant week (a
spike the model has never seen) reconstructs badly -- the reconstruction error
becomes an outbreak alarm.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(2)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.6, 3.9))

# --- left: encoder/decoder funnel with a 2D latent bottleneck ---
ax0.set_xlim(0, 10)
ax0.set_ylim(0, 10)
ax0.axis("off")
ax0.add_patch(Polygon([(0.6, 1.2), (0.6, 8.8), (4.2, 6.2), (4.2, 3.8)],
              closed=True, facecolor=PALETTE[0] + "22", edgecolor=PALETTE[0],
              linewidth=1.6))
ax0.add_patch(Polygon([(9.4, 1.2), (9.4, 8.8), (5.8, 6.2), (5.8, 3.8)],
              closed=True, facecolor=PALETTE[2] + "22", edgecolor=PALETTE[2],
              linewidth=1.6))
ax0.add_patch(plt.Rectangle((4.4, 3.9), 1.2, 2.2, facecolor=PALETTE[1] + "33",
              edgecolor=PALETTE[1], linewidth=1.6))
ax0.text(2.2, 5.0, "encoder\n$q(z\\mid x)$", ha="center", va="center",
         fontsize=9.5, color=INK)
ax0.text(5.0, 5.0, "$z$", ha="center", va="center", fontsize=12, color=INK)
ax0.text(7.8, 5.0, "decoder\n$p(x\\mid z)$", ha="center", va="center",
         fontsize=9.5, color=INK)
ax0.text(0.6, 9.3, "input $x$", ha="left", fontsize=9, color=INK)
ax0.text(9.4, 9.3, "reconstruction $\\hat{x}$", ha="right", fontsize=9,
         color=INK)
ax0.text(5.0, 2.6, "latent\n(mean $\\mu$, sd $\\sigma$)", ha="center",
         fontsize=8, color=MUTED)
ax0.set_title("Encode → sample $z$ → decode")

# --- right: reconstruction-error distributions, normal vs aberrant ---
normal_err = rng.gamma(2.0, 0.5, 600)
aberrant_err = rng.gamma(6.0, 0.9, 40) + 3.5
thr = 4.0
bins = np.linspace(0, 12, 40)
ax1.hist(normal_err, bins=bins, color=PALETTE[0], alpha=0.65,
         label="normal weeks")
ax1.hist(aberrant_err, bins=bins, color=PALETTE[1], alpha=0.8,
         label="aberrant weeks")
ax1.axvline(thr, color=INK, lw=1.6, ls="--")
ax1.text(thr + 0.2, ax1.get_ylim()[1] * 0.85, "alarm\nthreshold",
         fontsize=8.5, color=INK)
ax1.set_title("Reconstruction error flags anomalies")
ax1.set_xlabel("reconstruction error  $\\|x-\\hat{x}\\|$")
ax1.set_ylabel("count")
ax1.legend(loc="upper right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/variational-autoencoders.svg")
