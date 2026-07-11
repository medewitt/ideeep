# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""What a spatial prior is. Three draws from a Gaussian-process prior over a 2D
grid are smooth, spatially correlated random fields -- the kind of surface a
disease-mapping model places over space before seeing data. The right panel
shows the engine: the correlation between two locations decays with the
distance between them, and the lengthscale sets how quickly (how smooth the
fields are).
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(1)

g = 28
xs = np.linspace(0, 1, g)
XX, YY = np.meshgrid(xs, xs)
pts = np.c_[XX.ravel(), YY.ravel()]
ell = 0.15
d2 = ((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1)
K = np.exp(-0.5 * d2 / ell ** 2) + 1e-8 * np.eye(len(pts))
L = np.linalg.cholesky(K)

fig = plt.figure(figsize=(9.8, 3.2))
for i in range(3):
    ax = fig.add_axes([0.015 + i * 0.235, 0.10, 0.215, 0.74])
    f = (L @ rng.standard_normal(len(pts))).reshape(g, g)
    im = ax.imshow(f, cmap="RdBu_r", origin="lower", extent=[0, 1, 0, 1],
                   vmin=-2.6, vmax=2.6)
    ax.set_title(f"prior draw {i + 1}", fontsize=9.5, color=INK)
    ax.set_xticks([]); ax.set_yticks([])

ax = fig.add_axes([0.75, 0.17, 0.225, 0.66])
dd = np.linspace(0, 0.6, 100)
for l, c in [(0.08, PALETTE[0]), (0.15, PALETTE[1]), (0.30, PALETTE[2])]:
    ax.plot(dd, np.exp(-0.5 * dd ** 2 / l ** 2), color=c, lw=2,
            label=f"$\\ell={l}$")
ax.set_title("correlation vs distance", fontsize=9.5)
ax.set_xlabel("distance between locations", fontsize=8.5)
ax.set_ylabel("correlation", fontsize=8.5)
ax.legend(fontsize=8, title="lengthscale")

fig.suptitle("A spatial prior: smooth, correlated random fields over space",
             fontsize=11, color=INK, y=0.99)
save(fig, "assets/figures/prior-encoding-vae-spatial.svg")
