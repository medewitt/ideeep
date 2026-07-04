# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Density- vs frequency-dependent transmission: contact rate and R0 vs host density."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()

N = np.linspace(0, 1000, 400)

# contact rate C(N): density-dependent rises with N, frequency-dependent flat
kappa = 0.01
C_dd = kappa * N
C_fd = np.full_like(N, 5.0)

# R0(N): density-dependent scales with N (threshold at N_T), frequency-dependent flat
gamma = 0.1
beta_dd = 0.002       # per individual per day
beta_fd = 0.3         # per day
R0_dd = beta_dd * N / gamma
R0_fd = np.full_like(N, beta_fd / gamma)
N_T = gamma / beta_dd  # critical host density = 50

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.4))

ax1.plot(N, C_dd, color=PALETTE[0], label="density-dependent  $C=\\kappa N$")
ax1.plot(N, C_fd, color=PALETTE[1], label="frequency-dependent  $C=\\kappa$")
ax1.set_xlabel("host density $N$")
ax1.set_ylabel("contact rate $C(N)$")
ax1.set_title("Contacts per individual")
ax1.legend(loc="upper left", fontsize=8)

ax2.plot(N, R0_dd, color=PALETTE[0], label="density-dependent")
ax2.plot(N, R0_fd, color=PALETTE[1], label="frequency-dependent")
ax2.axhline(1, color=MUTED, lw=0.8, ls=":")
ax2.axvline(N_T, color=PALETTE[0], lw=0.8, ls="--")
ax2.text(N_T + 15, 6, "threshold $N_T$", color=PALETTE[0], fontsize=8)
ax2.text(620, 1.3, "$R_0=1$", color=MUTED, fontsize=8)
ax2.set_ylim(0, 8)
ax2.set_xlabel("host density $N$")
ax2.set_ylabel("$R_0$")
ax2.set_title("Invasion vs. density")
ax2.legend(loc="upper right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/transmission-modes.svg")
