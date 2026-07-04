# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Bolker-Pacala spatial moment equations for a plant population.

Integrates the closed mean-density and spatial-covariance equations
(Eqs. 6-7) for a locally dispersing, locally competing plant, and
contrasts the depressed spatial equilibrium with mean-field logistic
growth. Left: mean density and average covariance over time. Right:
the equilibrium spatial covariance c*(r), the second moment the
equations predict.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()

# Parameters: fecundity f, background death mu, competition alpha,
# competition/dispersal inverse scales lam_u, lam_d (Laplacian kernels).
f, mu, alpha, lam = 0.8, 0.4, 0.02, 3.0
K = (f - mu) / alpha            # mean-field carrying capacity = 20

L, dr, dt, T = 8.0, 0.04, 0.006, 220.0
r = np.arange(-L, L + dr / 2, dr)
U = 0.5 * lam * np.exp(-lam * np.abs(r)); U /= U.sum() * dr   # competition
D = 0.5 * lam * np.exp(-lam * np.abs(r)); D /= D.sum() * dr   # dispersal
U0 = 0.5 * lam                  # self-competition U(0)
mu_p = mu + alpha * U0          # mortality including self-competition


def conv(a, k):                 # discrete convolution of two lag functions
    return dr * np.convolve(a, k, mode="same")


# --- spatial moment equations (start from a near-Poisson low density) ---
n, c = 2.0, np.zeros_like(r)
ts, ns, cbars = [], [], []
for s in range(int(T / dt)):
    cbar = dr * np.sum(U * c)               # competition-weighted covariance
    if s % int(1 / dt) == 0:
        ts.append(s * dt); ns.append(n); cbars.append(cbar)
    dn = n * (f - mu - alpha * n) - alpha * U0 * n - alpha * cbar
    dc = 2 * (-mu_p * c + f * (conv(c, D) + n * D)
              - alpha * n * (conv(c, U) + n * U + c) - alpha * U * c)
    n += dt * dn; c += dt * dc
ts, ns, cbars = np.array(ts), np.array(ns), np.array(cbars)

# --- mean-field logistic for comparison (no spatial structure) ---
rgrow = f - mu
tmf = np.linspace(0, T, 400)
nmf = K / (1 + (K / 2.0 - 1) * np.exp(-rgrow * tmf))

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 4.0))

# Left: mean density (both models) and average covariance over time.
tmax = 60
axL.plot(tmf[tmf <= tmax], nmf[tmf <= tmax], color=MUTED, ls="--",
         label="mean-field logistic")
axL.plot(ts[ts <= tmax], ns[ts <= tmax], color=PALETTE[0], lw=2.2,
         label="spatial moment eq.")
axL.axhline(K, color=MUTED, lw=0.8, ls=":")
axL.annotate("$K = 20$", xy=(tmax * 0.62, K + 0.4), color=MUTED)
axL.annotate(f"$n^* \\approx {ns[-1]:.1f}$", xy=(tmax * 0.62, ns[-1] - 1.6),
             color=PALETTE[0])
axL.set_xlabel("Time")
axL.set_ylabel("Mean density $n$")
axL.set_ylim(0, 22)
axL.set_title("Clustering depresses the mean")
axL.legend(loc="lower right")

axLc = axL.twinx()
axLc.plot(ts[ts <= tmax], cbars[ts <= tmax], color=PALETTE[1], lw=1.6)
axLc.set_ylabel("Average covariance $\\bar c$", color=PALETTE[1])
axLc.tick_params(axis="y", colors=PALETTE[1])
axLc.grid(False)
axLc.set_ylim(0, max(cbars) * 1.25)

# Right: the equilibrium spatial covariance c*(r).
mask = np.abs(r) <= 2.2
axR.axhline(0, color=MUTED, lw=0.8, ls="--", label="mean-field ($c=0$)")
axR.plot(r[mask], c[mask], color=PALETTE[0], lw=2.2, label="moment eq. $c^*(r)$")
axR.set_xlabel("Spatial lag $r$")
axR.set_ylabel("Covariance density $c^*(r)$")
axR.set_title("Positive covariance = clustering")
axR.legend(loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/spatial-moment-equations.svg")
