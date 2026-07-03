# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""How to measure asynchrony. Left: the phase (Kuramoto) picture -- each local
epidemic is a clock hand; the length of their vector sum, the order parameter r,
measures phase coherence (r = 1 fully synchronous, r ~ 0 asynchronous). Right:
as local epidemics are spread across the seasonal cycle, both the community
synchrony index phi (Loreau & de Mazancourt) and the mean pairwise correlation
of incidence fall from 1 toward their asynchronous floors."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(1)
n = 8

fig = plt.figure(figsize=(11, 4.8))
axL = fig.add_subplot(1, 2, 1, projection="polar")
axR = fig.add_subplot(1, 2, 2)

# ---- Left: Kuramoto order parameter for two phase configurations ----
def order_parameter(phases):
    z = np.mean(np.exp(1j * phases))
    return np.abs(z), np.angle(z)

configs = [
    (rng.uniform(-0.35, 0.35, n), PALETTE[1], "coherent"),
    (rng.uniform(0, 2 * np.pi, n), PALETTE[0], "incoherent"),
]
for phases, color, name in configs:
    r, psi = order_parameter(phases)
    axL.plot(phases, np.ones(n), "o", color=color, ms=8, alpha=0.9)
    axL.annotate("", xy=(psi, r), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=color, lw=2.2))
    axL.text(psi, r + 0.12, f"{name}\n$r$ = {r:.2f}", color=color,
             ha="center", fontsize=9)
axL.set_rmax(1.25)
axL.set_rticks([0.5, 1.0])
axL.set_title("Phase coherence:\nKuramoto order parameter $r$", fontsize=10, pad=14)

# ---- Right: synchrony index and mean correlation vs phase spread ----
steps_per_yr = 26
T = steps_per_yr * 20
t = np.arange(T)
spreads = np.linspace(0.0, 1.0, 25)   # 0 = identical phase, 1 = evenly spread
phi_vals, corr_vals = [], []

base_phases = np.linspace(0, 2 * np.pi, n, endpoint=False)
for s in spreads:
    phases = s * base_phases
    # stylized recurrent local epidemics: seasonal wave + noise, non-negative
    series = np.empty((T, n))
    for i in range(n):
        wave = 1 + np.cos(2 * np.pi * t / steps_per_yr + phases[i])
        series[:, i] = np.clip(wave + rng.normal(0, 0.15, T), 0, None)
    sd = series.std(axis=0)
    phi = series.sum(axis=1).var() / sd.sum() ** 2
    C = np.corrcoef(series.T)
    mean_corr = (C.sum() - n) / (n * (n - 1))
    phi_vals.append(phi)
    corr_vals.append(mean_corr)

axR.plot(spreads, phi_vals, color=PALETTE[0], lw=2.2,
         label="synchrony index  $\\varphi$")
axR.plot(spreads, corr_vals, color=PALETTE[3], lw=2.2,
         label="mean pairwise corr.  $\\bar\\rho$")
axR.axhline(1 / n, color=INK, ls=":", lw=1.0)
axR.text(0.02, 1 / n + 0.03, r"$\varphi$ floor $= 1/n$", color=INK, fontsize=8.5)
axR.set_xlabel("phase spread  (0 = synchronous $\\to$ 1 = evenly staggered)")
axR.set_ylabel("synchrony")
axR.set_title("Two synchrony measures fall as epidemics spread out",
              fontsize=10)
axR.legend(loc="upper right", fontsize=9)
axR.set_ylim(-0.15, 1.05)

fig.suptitle("Measuring asynchrony across space", fontweight="bold")
fig.tight_layout()
save(fig, "assets/figures/asynchrony-measures.svg")
