# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""What each assay class detects across the course of an infection."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

t = np.linspace(0, 40, 500)

def bump(t, center, width, height=1.0):
    return height * np.exp(-0.5 * ((t - center) / width) ** 2)

def logistic(t, mid, k, plateau=1.0):
    return plateau / (1 + np.exp(-k * (t - mid)))

# Pathogen load (RNA/DNA -> PCR; also drives antigen)
load = bump(t, 8, 4.2)
# Antigen tracks high load but needs more of it (narrower, later threshold)
antigen = bump(t, 8, 3.4) ** 1.4
# IgM: transient, rises ~day 10, wanes
igm = bump(t, 16, 5.5, 0.9)
# IgG: rises later, persists
igg = logistic(t, 18, 0.35, 0.95)

fig, ax = plt.subplots(figsize=(7.0, 3.8))
ax.plot(t, load, color=PALETTE[0], lw=2.0, label="pathogen nucleic acid  (PCR / LAMP)")
ax.plot(t, antigen, color=PALETTE[1], lw=2.0, label="antigen  (RAT / ELISA)")
ax.plot(t, igm, color=PALETTE[3], lw=2.0, label="IgM antibody  (serology)")
ax.plot(t, igg, color=PALETTE[2], lw=2.0, label="IgG antibody  (serology)")

ax.axvline(0, color=MUTED, lw=0.8, ls=":")
ax.text(0.3, 1.02, "infection", fontsize=8.5, color=MUTED, rotation=90, va="top")
ax.axvline(4, color=MUTED, lw=0.8, ls=":")
ax.text(4.3, 1.02, "symptom onset", fontsize=8.5, color=MUTED, rotation=90, va="top")

ax.set_xlabel("days since infection")
ax.set_ylabel("relative signal")
ax.set_ylim(0, 1.15)
ax.set_xlim(0, 40)
ax.set_title("The diagnostic window: what turns positive, and when")
ax.legend(loc="upper right", fontsize=8)
save(fig, "assets/figures/diagnostic-window.svg")
