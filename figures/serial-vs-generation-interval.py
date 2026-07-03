# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Generation interval (infection-to-infection) vs serial interval (onset-to-onset)."""
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# Infector timeline
inf_A_infection = 0.0
inf_A_incubation = 4.0
inf_A_onset = inf_A_infection + inf_A_incubation      # = 4

# Infectee timeline
generation = 5.0                                       # infection-to-infection
inf_B_infection = inf_A_infection + generation         # = 5
inf_B_incubation = 2.0                                 # shorter incubation
inf_B_onset = inf_B_infection + inf_B_incubation       # = 7
serial = inf_B_onset - inf_A_onset                     # = 3

fig, ax = plt.subplots(figsize=(7.0, 3.8))
ax.grid(False)
ax.set_yticks([])
for spine in ("left", "top", "right"):
    ax.spines[spine].set_visible(False)

yA, yB = 2.0, 0.6

for y, lab in [(yA, "infector"), (yB, "infectee")]:
    ax.axhline(y, xmin=0.06, xmax=0.98, color="#c9d3db", lw=2, zorder=0)
    ax.text(-0.4, y, lab, ha="right", va="center", fontsize=9.5, color=INK)

def event(t, y, color, label, dy):
    ax.plot(t, y, "o", color=color, ms=9, zorder=3)
    ax.text(t, y + dy, label, ha="center", va="bottom" if dy > 0 else "top",
            fontsize=8.5, color=color)

event(inf_A_infection, yA, PALETTE[1], "infection", 0.18)
event(inf_A_onset, yA, PALETTE[0], "onset", 0.18)
event(inf_B_infection, yB, PALETTE[1], "infection", 0.18)
event(inf_B_onset, yB, PALETTE[0], "onset", 0.18)

# Generation interval: infection A -> infection B
ax.annotate("", xy=(inf_B_infection, 1.35), xytext=(inf_A_infection, 1.35),
            arrowprops=dict(arrowstyle="<->", color=PALETTE[1], lw=1.6))
ax.text((inf_A_infection + inf_B_infection) / 2, 1.44,
        f"generation interval = {generation:.0f} d", ha="center", va="bottom",
        fontsize=9, color=PALETTE[1])

# Serial interval: onset A -> onset B
ax.annotate("", xy=(inf_B_onset, 1.35), xytext=(inf_A_onset, 1.35),
            arrowprops=dict(arrowstyle="<->", color=PALETTE[0], lw=1.6))
ax.text((inf_A_onset + inf_B_onset) / 2, 1.22,
        f"serial interval = {serial:.0f} d", ha="center", va="top",
        fontsize=9, color=PALETTE[0])

# Guide lines linking the two lanes
for t in (inf_A_infection, inf_A_onset, inf_B_infection, inf_B_onset):
    ax.plot([t, t], [yB, yA], ls=":", lw=0.7, color=MUTED, zorder=0)

ax.set_xlim(-1.4, 9)
ax.set_ylim(0.0, 2.7)
ax.set_xlabel("calendar time (days)")
ax.set_title("Generation interval vs serial interval")
save(fig, "assets/figures/serial-vs-generation-interval.svg")
