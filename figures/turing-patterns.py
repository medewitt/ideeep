# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Gray-Scott reaction-diffusion Turing patterns on a periodic grid."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)

N = 128
Du, Dv = 0.16, 0.08
F, k = 0.037, 0.06
dt = 1.0
steps = 6000

u = np.ones((N, N))
v = np.zeros((N, N))

# Central square seed
c = N // 2
r = 10
u[c - r:c + r, c - r:c + r] = 0.5
v[c - r:c + r, c - r:c + r] = 0.25

# Tiny noise
u += 0.01 * rng.standard_normal((N, N))
v += 0.01 * rng.standard_normal((N, N))


def laplacian(a):
    return (
        np.roll(a, 1, axis=0) + np.roll(a, -1, axis=0)
        + np.roll(a, 1, axis=1) + np.roll(a, -1, axis=1)
        - 4 * a
    )


for _ in range(steps):
    Lu = laplacian(u)
    Lv = laplacian(v)
    uvv = u * v * v
    u += dt * (Du * Lu - uvv + F * (1 - u))
    v += dt * (Dv * Lv + uvv - (F + k) * v)

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(v, cmap="magma", interpolation="bilinear")
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Gray-Scott Turing Patterns (v field)")

save(fig, "assets/figures/turing-patterns.svg")
