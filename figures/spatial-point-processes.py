# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Three spatial point patterns: CSR, an inhomogeneous Poisson trend, and a
clustered log-Gaussian Cox process (LGCP)."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(20240704)

# A light single-hue colormap for the intensity backgrounds (on-brand blue).
shade = LinearSegmentedColormap.from_list("shade", ["#ffffff", PALETTE[0]])


def homogeneous_ppp(lam, rng):
    """Complete spatial randomness on the unit square: N ~ Poisson(lam), points uniform."""
    n = rng.poisson(lam)
    return rng.uniform(0, 1, size=(n, 2))


def thin(pts, prob, rng):
    """Independently retain each point with probability prob(x, y)."""
    keep = rng.uniform(size=len(pts)) < prob(pts[:, 0], pts[:, 1])
    return pts[keep]


# Common grid for drawing the intensity fields as background shading.
g = np.linspace(0, 1, 200)
GX, GY = np.meshgrid(g, g)

# ---- Panel 1: homogeneous Poisson (CSR) ---------------------------------
csr = homogeneous_ppp(120, rng)

# ---- Panel 2: inhomogeneous Poisson with a smooth spatial trend ----------
# lambda(s) = lam0 * exp(a*x + b*y), simulated by thinning a dense CSR.
a, b = 2.6, 1.4
inh_field = np.exp(a * GX + b * GY)
dense = homogeneous_ppp(700, rng)
inh = thin(dense, lambda x, y: np.exp(a * x + b * y) / np.exp(a + b), rng)

# ---- Panel 3: log-Gaussian Cox process (clustered) -----------------------
# log lambda(s) = mu + sigma * Z(s), Z a smooth Gaussian random field built by
# filtering white noise in the Fourier domain (a squared-exponential-like GRF).
n = 200
white = rng.standard_normal((n, n))
freq = np.fft.fftfreq(n)
FX, FY = np.meshgrid(freq, freq)
scale = 0.045  # controls the correlation length of the field
spec = np.exp(-0.5 * (FX**2 + FY**2) / scale**2)
field = np.real(np.fft.ifft2(np.fft.fft2(white) * spec))
field = (field - field.mean()) / field.std()
sigma = 1.3
loglam = np.log(600.0) + sigma * field  # mu chosen so counts are comparable
lam_grid = np.exp(loglam)
lgcp_field = lam_grid

# Sample the LGCP by thinning a homogeneous PP at the field's maximum rate.
lam_max = lam_grid.max()
cand = homogeneous_ppp(lam_max, rng)
ix = np.clip((cand[:, 0] * (n - 1)).astype(int), 0, n - 1)
iy = np.clip((cand[:, 1] * (n - 1)).astype(int), 0, n - 1)
accept = rng.uniform(size=len(cand)) < lam_grid[iy, ix] / lam_max
lgcp = cand[accept]

fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.9))

# Panel 1
ax = axes[0]
ax.scatter(csr[:, 0], csr[:, 1], s=14, color=PALETTE[0], alpha=0.85,
           edgecolor="white", linewidth=0.4)
ax.set_title("Homogeneous Poisson (CSR)\nconstant $\\lambda$", fontsize=10)

# Panel 2
ax = axes[1]
ax.imshow(inh_field, origin="lower", extent=(0, 1, 0, 1), cmap=shade,
          alpha=0.55, aspect="auto")
ax.scatter(inh[:, 0], inh[:, 1], s=14, color=PALETTE[1], alpha=0.9,
           edgecolor="white", linewidth=0.4)
ax.set_title("Inhomogeneous Poisson\nsmooth trend $\\lambda(s)$", fontsize=10)

# Panel 3
ax = axes[2]
ax.imshow(lgcp_field, origin="lower", extent=(0, 1, 0, 1), cmap=shade,
          alpha=0.6, aspect="auto")
ax.scatter(lgcp[:, 0], lgcp[:, 1], s=14, color=PALETTE[3], alpha=0.9,
           edgecolor="white", linewidth=0.4)
ax.set_title("Log-Gaussian Cox process\nrandom $\\lambda(s)$, clustered", fontsize=10)

for ax in axes:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_edgecolor(MUTED)
        spine.set_linewidth(0.7)

fig.suptitle("Same expected count, different spatial structure", color=INK, fontsize=12)
fig.tight_layout()
save(fig, "assets/figures/spatial-point-processes.svg")
