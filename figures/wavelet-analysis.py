# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Wavelet power spectrum (scalogram) of a signal whose dominant period shifts
from annual to biennial — time-resolved periodicity a Fourier spectrum misses."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(0)

n, dt = 416, 1.0                                   # weekly series, ~8 years
t = np.arange(n)
sig = np.zeros(n)
sig[:208] = np.sin(2 * np.pi * t[:208] / 52)       # annual cycle
sig[208:] = np.sin(2 * np.pi * t[208:] / 104)      # biennial cycle
x = sig + rng.normal(0, 0.4, n)


def cwt_morlet(x, dt, periods, w0=6.0):
    xh = np.fft.fft(x - x.mean())
    omega = 2 * np.pi * np.fft.fftfreq(len(x), d=dt)
    scales = periods * (w0 + np.sqrt(2 + w0 ** 2)) / (4 * np.pi)
    W = np.empty((len(scales), len(x)), complex)
    for i, s in enumerate(scales):
        norm = np.sqrt(2 * np.pi * s / dt) * np.pi ** -0.25
        W[i] = np.fft.ifft(xh * norm * np.exp(-0.5 * (s * omega - w0) ** 2) * (omega > 0))
    return np.abs(W) ** 2


periods = np.geomspace(8, 200, 80)
power = cwt_morlet(x, dt, periods)

# cone of influence: periods above this curve are edge-contaminated
edge = np.minimum(t, n - 1 - t)
coi = 1.033 * np.sqrt(2) * dt * np.maximum(edge, 1e-6)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 4.6), sharex=True,
                               gridspec_kw={"height_ratios": [1, 2.4]})

# ---- Top: the raw non-stationary signal.
ax1.plot(t, x, color=PALETTE[0], lw=0.9)
ax1.axvline(208, color=INK, ls="--", lw=1.0)
ax1.set_ylabel("signal")
ax1.set_title("a signal whose period doubles halfway through", fontsize=10)
ax1.set_yticks([-2, 0, 2])

# ---- Bottom: the wavelet power spectrum (scalogram).
pcm = ax2.pcolormesh(t, periods, power, cmap="viridis", shading="gouraud",
                     rasterized=True)
ax2.set_yscale("log")
ax2.set_ylim(periods[0], periods[-1])
for pr in (52, 104):
    ax2.axhline(pr, color="white", ls=":", lw=0.8, alpha=0.7)
ax2.axvline(208, color="white", ls="--", lw=1.0, alpha=0.8)
ax2.fill_between(t, coi, periods[-1], color=INK, alpha=0.30, lw=0)   # COI
ax2.plot(t, coi, color=INK, lw=0.6, alpha=0.5)
ax2.set_ylabel("period (weeks)")
ax2.set_xlabel("week")
ax2.set_title("wavelet power: the ridge tracks 52 → 104 weeks", fontsize=10)
ax2.text(150, 52, "annual", color="white", fontsize=8, va="bottom")
ax2.text(300, 104, "biennial", color="white", fontsize=8, va="bottom")
cb = fig.colorbar(pcm, ax=ax2, pad=0.015, aspect=18)
cb.set_label("power", fontsize=8)
cb.ax.tick_params(labelsize=7)

fig.tight_layout()
save(fig, "assets/figures/wavelet-analysis.svg")
