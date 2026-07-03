# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""The natural history of one infection: latent, incubation, and infectious periods."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# Example timeline (days since infection)
t_infection = 0.0
t_infectious_start = 2.0   # end of latent period
t_onset = 3.0              # end of incubation period (symptoms)
t_infectious_end = 8.0     # recovery / no longer infectious

fig, ax = plt.subplots(figsize=(7.0, 3.6))
ax.grid(False)
ax.set_yticks([])
for spine in ("left", "top", "right"):
    ax.spines[spine].set_visible(False)

# Two lanes: infectiousness (top) and symptoms (bottom)
y_inf, y_sym = 1.0, 0.0

# Infectious period bar
ax.barh(y_inf, t_infectious_end - t_infectious_start, left=t_infectious_start,
        height=0.34, color=PALETTE[1], alpha=0.85, label="infectious period")
# Latent period bar (not yet infectious)
ax.barh(y_inf, t_infectious_start - t_infection, left=t_infection,
        height=0.34, color="#c9d3db", label="latent period")

# Symptomatic period bar
ax.barh(y_sym, t_infectious_end - t_onset, left=t_onset,
        height=0.34, color=PALETTE[0], alpha=0.85, label="symptomatic")
# Incubation period bar (pre-symptomatic)
ax.barh(y_sym, t_onset - t_infection, left=t_infection,
        height=0.34, color="#c9d3db", label="incubation period")

# Pre-symptomatic transmission window
ax.axvspan(t_infectious_start, t_onset, color=PALETTE[3], alpha=0.18)
ax.text((t_infectious_start + t_onset) / 2, 1.72, "pre-symptomatic\ntransmission",
        ha="center", va="bottom", fontsize=8.5, color=PALETTE[3])

# Event markers
for t, lab in [(t_infection, "infection"), (t_onset, "symptom onset")]:
    ax.plot([t, t], [-0.45, 1.55], ls=":", lw=1.0, color=MUTED, zorder=0)
    ax.text(t, -0.62, lab, ha="center", va="top", fontsize=9, color=INK)

# Lane labels
ax.text(-0.25, y_inf, "transmission", ha="right", va="center", fontsize=9.5, color=INK)
ax.text(-0.25, y_sym, "disease", ha="right", va="center", fontsize=9.5, color=INK)

# Period annotations
ax.text(1.0, y_inf, "latent", ha="center", va="center", fontsize=8.5, color=MUTED)
ax.text(5.0, y_inf, "infectious", ha="center", va="center", fontsize=8.5, color="white")
ax.text(1.5, y_sym, "incubation", ha="center", va="center", fontsize=8.5, color=MUTED)
ax.text(5.5, y_sym, "symptomatic", ha="center", va="center", fontsize=8.5, color="white")

ax.set_xlim(-1.6, 9)
ax.set_ylim(-1.0, 2.1)
ax.set_xlabel("time since infection (days)")
ax.set_title("The natural history of one infection")
save(fig, "assets/figures/epi-intervals-timeline.svg")
