# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Per-capita growth rate of an invading infection vs host density, under
density- vs frequency-dependent transmission."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()

N = np.linspace(0, 400, 400)

# Invasion growth rate r(N) = beta(N) - gamma, with beta(N) the effective
# standard-incidence coefficient. Same parameters as the page's worked example.
gamma = 0.1
bk_dd = 0.002         # density-dependent: beta(N) = bk_dd * N  (rises with N)
bk_fd = 0.3           # frequency-dependent: beta(N) = bk_fd    (flat in N)
r_dd = bk_dd * N - gamma
r_fd = np.full_like(N, bk_fd - gamma)
N_T = gamma / bk_dd   # critical host density = 50

fig, ax = plt.subplots(figsize=(6.2, 3.8))

ax.plot(N, r_dd, color=PALETTE[0], label="density-dependent  $r=\\beta\\kappa N-\\gamma$")
ax.plot(N, r_fd, color=PALETTE[1], label="frequency-dependent  $r=\\beta\\kappa-\\gamma$")

# r = 0 is the invasion boundary; below it the infection dies out.
ax.axhline(0, color=MUTED, lw=0.8, ls=":")
ax.axvline(N_T, color=PALETTE[0], lw=0.8, ls="--")
ax.text(N_T + 8, -0.075, "threshold $N_T=50$", color=PALETTE[0], fontsize=8)
ax.text(300, 0.015, "$r=0$", color=MUTED, fontsize=8)

# Shade the region where the density-dependent pathogen cannot invade.
ax.axvspan(0, N_T, color=PALETTE[0], alpha=0.06)
ax.text(6, -0.085, "fadeout", color=PALETTE[0], fontsize=8)

ax.set_xlim(0, 400)
ax.set_ylim(-0.11, 0.72)
ax.set_xlabel("host density $N$")
ax.set_ylabel("per-capita growth rate $r$  (day$^{-1}$)")
ax.set_title("Invasion growth rate vs. host density")
ax.legend(loc="upper left", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/transmission-modes-growth.svg")
