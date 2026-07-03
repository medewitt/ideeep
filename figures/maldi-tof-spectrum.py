# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""A MALDI-TOF mass spectrum: the protein 'fingerprint' used for microbial ID."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(5)

mz = np.linspace(2000, 12000, 4000)

# Characteristic ribosomal-protein peaks (m/z, relative intensity)
peaks = [(2800, 0.35), (3200, 0.55), (4300, 0.9), (5100, 0.5),
         (6300, 1.0), (7200, 0.4), (9000, 0.7), (10300, 0.45)]

signal = np.zeros_like(mz)
for center, height in peaks:
    width = 12 + center * 0.0016
    signal += height * np.exp(-0.5 * ((mz - center) / width) ** 2)
signal += rng.normal(0, 0.006, mz.size).clip(0)        # faint baseline noise

fig, ax = plt.subplots(figsize=(7.0, 3.6))
ax.plot(mz, signal, color=PALETTE[0], lw=0.9)
ax.fill_between(mz, signal, color=PALETTE[0], alpha=0.12)
for center, height in peaks:
    if height >= 0.6:
        ax.annotate(f"{center}", (center, height), xytext=(0, 4),
                    textcoords="offset points", ha="center", fontsize=7.5, color=MUTED)
ax.grid(False)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_xlabel("m/z  (mass-to-charge ratio, Da)")
ax.set_title("MALDI-TOF spectrum — a species fingerprint")
save(fig, "assets/figures/maldi-tof-spectrum.svg")
