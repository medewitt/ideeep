# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Why a few latents can stand in for the whole field. Left: the eigenvalue
(Karhunen-Loeve) spectrum of the spatial prior's covariance falls off fast, so
the first six modes already capture almost all of the prior's variance -- the
cumulative curve crosses 99% by mode six. Right: those leading modes are smooth
spatial basis functions; a draw from the prior is a weighted sum of them, so
six independent coefficients encode the entire 25-dimensional correlated field.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

s = np.linspace(0, 1, 25)
K = np.exp(-0.5 * (s[:, None] - s[None, :]) ** 2 / 0.15 ** 2) + 1e-9 * np.eye(25)
vals, vecs = np.linalg.eigh(K)
order = np.argsort(vals)[::-1]
vals, vecs = vals[order], vecs[:, order]

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.6, 3.7))

k = np.arange(1, 26)
ax0.bar(k, vals, color=PALETTE[0], alpha=0.55, label="eigenvalue")
ax0.set_ylabel("eigenvalue (variance)", color=PALETTE[0], fontsize=9)
ax0.set_xlabel("mode")
ax0.set_title("KL spectrum: a few modes carry the variance", fontsize=10)
ax0.axvline(6.5, color=MUTED, lw=1.1, ls="--")
ax0.text(7, vals.max() * 0.8, "keep 6", fontsize=8.5, color=INK)
ax0b = ax0.twinx()
cum = np.cumsum(vals) / vals.sum()
ax0b.plot(k, cum, "o-", color=PALETTE[1], ms=3, lw=1.6)
ax0b.set_ylabel("cumulative variance", color=PALETTE[1], fontsize=9)
ax0b.set_ylim(0, 1.02)
ax0b.text(9, cum[5] - 0.10, f"{cum[5]*100:.1f}% by mode 6", fontsize=8,
          color=PALETTE[1])

for i in range(4):
    ax1.plot(s, vecs[:, i] * np.sqrt(vals[i]), color=PALETTE[i % len(PALETTE)],
             lw=2, label=f"mode {i + 1}")
ax1.axhline(0, color=INK, lw=0.7)
ax1.set_title("The leading spatial modes (columns of $B$)", fontsize=10)
ax1.set_xlabel("location  $s$")
ax1.set_ylabel("basis function")
ax1.legend(fontsize=8, ncol=2)

fig.tight_layout()
save(fig, "assets/figures/prior-encoding-vae-encoding.svg")
