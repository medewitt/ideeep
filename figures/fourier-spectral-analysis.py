# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Fourier decomposition and periodogram of a seasonal incidence series."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# --- Synthetic monthly incidence over 12 years (144 months) ---
t = np.arange(144)
baseline = 100.0
annual = 40.0 * np.sin(2 * np.pi * t / 12.0)
biennial = 18.0 * np.sin(2 * np.pi * t / 24.0 + 0.6)
noise = rng.normal(0.0, 6.0, size=t.size)

observed = baseline + annual + biennial + noise
fit = baseline + annual + biennial

# --- Periodogram of the detrended (mean-removed) series ---
detrended = observed - observed.mean()
coef = np.fft.rfft(detrended)
power = np.abs(coef) ** 2
freq = np.fft.rfftfreq(144, d=1.0)  # cycles per month

# Drop the zero-frequency (mean) term, then convert to period in months.
freq = freq[1:]
power = power[1:]
period = 1.0 / freq

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# LEFT: time series with waveform reconstruction.
axL.plot(t, observed, color=INK, lw=0.8, marker="o", ms=2.5,
         alpha=0.8, label="observed")
axL.plot(t, fit, color=PALETTE[1], lw=2.0, label="annual + biennial fit")
axL.set_xlabel("time (months)")
axL.set_ylabel("monthly incidence")
axL.set_xlim(0, 143)
axL.set_title("Seasonal waveform")
axL.legend(loc="upper right", fontsize="x-small")

# RIGHT: power spectrum versus period.
axR.plot(period, power, color=PALETTE[0], lw=1.4, marker="o", ms=3.5)
axR.set_xlabel("period (months)")
axR.set_ylabel("spectral power")
axR.set_xlim(2, 40)
axR.set_title("Power spectrum")

# Annotate the two dominant peaks.
p_annual = power[np.argmin(np.abs(period - 12.0))]
p_biennial = power[np.argmin(np.abs(period - 24.0))]
axR.annotate("annual (12 mo)", xy=(12.0, p_annual),
             xytext=(15.0, p_annual * 0.85), fontsize="x-small",
             color=PALETTE[0],
             arrowprops=dict(arrowstyle="->", color=PALETTE[0], lw=0.8))
axR.annotate("biennial (24 mo)", xy=(24.0, p_biennial),
             xytext=(26.0, p_biennial + p_annual * 0.25),
             fontsize="x-small", color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))

fig.tight_layout()

save(fig, "assets/figures/fourier-spectral-analysis.svg")
