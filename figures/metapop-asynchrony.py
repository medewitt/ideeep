# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Spatial asynchrony and metapopulation persistence, in a stochastic TSIR
(measles-type) metapopulation of small towns, each below the critical community
size. When local epidemics are synchronous their troughs align, the pathogen
fades out everywhere at once, and the metapopulation goes globally extinct. When
they are asynchronous, a town at its epidemic peak reseeds a neighbour that has
just faded out — the rescue effect — and the pathogen persists regionally
(Bartlett 1957; Bolker & Grenfell 1995; Grenfell & Bolker 1998)."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

n = 5                 # towns
N = 120_000           # population per town (below measles CCS ~ 250-500k)
steps_per_yr = 26     # biweekly generations
years = 16
T = steps_per_yr * years
R0 = 17.0
delta = 0.15          # seasonal forcing amplitude
birth = 0.03          # per-capita birth rate per year
m = 0.006             # movement coupling between towns
S0 = int(N / R0 * 1.15)
I0 = 60
SEED = 1


def run(phases, seed):
    rng = np.random.default_rng(seed)
    S = np.full(n, S0, float)
    Inf = np.full(n, I0, float)
    hist = np.empty((T, n))
    for t in range(T):
        beta = R0 * (1 + delta * np.cos(2 * np.pi * t / steps_per_yr + phases))
        imports = m * (Inf.sum() - Inf)            # infecteds arriving from elsewhere
        lam = beta * (S / N) * (Inf + imports)     # expected new cases
        newI = rng.poisson(np.clip(lam, 0, None))
        newI = np.minimum(newI, S)                 # cannot infect more than S
        S = S + birth / steps_per_yr * N - newI
        Inf = newI.astype(float)
        hist[t] = Inf
    return hist


def first_sustained_fadeout(gl, run_len=4):
    """Year of the first run of >= run_len consecutive zero-incidence
    generations (a true fadeout, not a between-epidemic trough)."""
    run = 0
    for t, v in enumerate(gl <= 0):
        run = run + 1 if v else 0
        if run >= run_len:
            return (t - run_len + 1) / steps_per_yr
    return None


def synchrony_index(hist):
    """Loreau & de Mazancourt community synchrony phi in [1/n, 1]."""
    sd = hist.std(axis=0)
    total_var = hist.sum(axis=1).var()
    return total_var / (sd.sum() ** 2)


phases_sync = np.zeros(n)
phases_async = np.linspace(0, 2 * np.pi, n, endpoint=False)

H_sync = run(phases_sync, seed=SEED)
H_async = run(phases_async, seed=SEED)
phi_sync = synchrony_index(H_sync)
phi_async = synchrony_index(H_async)

t_yr = np.arange(T) / steps_per_yr

fig, axes = plt.subplots(2, 2, figsize=(11, 6.6), sharex=True)

for col, (H, title, phi) in enumerate([
        (H_sync, "Synchronous towns", phi_sync),
        (H_async, "Asynchronous towns", phi_async)]):
    ax_local, ax_global = axes[0, col], axes[1, col]
    for i in range(n):
        ax_local.plot(t_yr, H[:, i], color=PALETTE[i % len(PALETTE)], lw=0.9, alpha=0.9)
    ax_local.set_title(f"{title}\nsynchrony $\\varphi$ = {phi:.2f}", fontsize=10)
    if col == 0:
        ax_local.set_ylabel("local cases")

    gcolor = PALETTE[2] if col else PALETTE[1]
    gl = H.sum(axis=1)
    ax_global.fill_between(t_yr, gl, color=gcolor, alpha=0.30)
    ax_global.plot(t_yr, gl, color=gcolor, lw=1.1)
    te = first_sustained_fadeout(gl)
    if te is not None:
        ax_global.axvline(te, color=PALETTE[1], ls="--", lw=1.4)
        ax_global.text(te + 0.2, gl.max() * 0.78,
                       f"global fadeout\n$\\approx$ year {te:.0f}",
                       color=PALETTE[1], fontsize=9)
    else:
        ax_global.text(0.97, 0.92, "persists (rescue)", transform=ax_global.transAxes,
                       ha="right", va="top", color=PALETTE[2], fontsize=10,
                       fontweight="bold")
    ax_global.set_xlabel("year")
    if col == 0:
        ax_global.set_ylabel("regional cases\n(all towns)")

fig.suptitle("Asynchrony sustains a pathogen that no single town can hold",
             fontweight="bold")
fig.tight_layout()
save(fig, "assets/figures/metapop-asynchrony.svg")
