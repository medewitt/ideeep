# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Synthetic age-structured social contact matrix (illustrative, not empirical)."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, INK

apply_style()
rng = np.random.default_rng(1834)

# 16 five-year age bands: 0-4, 5-9, ..., 75+
n = 16
labels = [f"{5 * i}-{5 * i + 4}" for i in range(n - 1)] + ["75+"]
mid = np.arange(n) * 5 + 2.5      # band midpoints in years

M = np.zeros((n, n))
ii, jj = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
ai, aj = mid[ii], mid[jj]

# (a) assortative diagonal: contact own age most
M += 3.0 * np.exp(-((ai - aj) ** 2) / (2 * 6.0 ** 2))

# (b) intense school-age block (~5-19 yr with each other)
school = (ai >= 5) & (ai <= 19) & (aj >= 5) & (aj <= 19)
M[school] += 4.5 * np.exp(-((ai[school] - aj[school]) ** 2) / (2 * 9.0 ** 2))

# (c) parent-child ridges: ~25-40 yr contacting ~0-14 yr (and symmetric)
ridge = np.exp(-((ai - 32) ** 2) / (2 * 7.0 ** 2)) * \
    np.exp(-((aj - 7) ** 2) / (2 * 6.0 ** 2))
M += 2.2 * (ridge + ridge.T)

# (d) mild background contacts
M += 0.4

# enforce approximate reciprocity by symmetrizing
M = (M + M.T) / 2.0

fig, ax = plt.subplots(figsize=(5.2, 4.4))
im = ax.imshow(M, origin="lower", cmap="magma", aspect="equal")

cbar = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
cbar.set_label("mean contacts per day")

ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(labels, rotation=90, fontsize=7)
ax.set_yticklabels(labels, fontsize=7)
ax.set_xlabel("age of contact")
ax.set_ylabel("age of participant")
ax.set_title("Age-structured contact matrix (synthetic)", fontsize=10)
ax.grid(False)

fig.tight_layout()
save(fig, "assets/figures/contact-matrices.svg")
