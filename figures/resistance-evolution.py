# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Resistant-strain frequency under drug pressure then drug removal."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

cost = 0.05      # fitness cost of resistance when the drug is absent
kill = 0.15      # drug suppression of the sensitive strain
u = 1e-4         # recurrent forward mutation to resistance
p0 = u / cost    # mutation-selection balance baseline
T_on, T_end = 60, 220


def step(p, wR, wS):
    p = p * wR / (p * wR + (1 - p) * wS)   # discrete selection
    return p + u * (1 - p)                 # recurrent mutation input


p = p0
traj = [p]
for t in range(1, T_end + 1):
    if t <= T_on:
        wR, wS = 1.0, 1.0 - kill      # drug present: sensitive suppressed
    else:
        wR, wS = 1.0 - cost, 1.0      # drug removed: resistance costs
    p = step(p, wR, wS)
    traj.append(p)

traj = np.array(traj)
gens = np.arange(T_end + 1)

fig, ax = plt.subplots()
ax.axvspan(0, T_on, color="#eef2f5", zorder=0)
ax.plot(gens, traj, color=PALETTE[1], lw=2.2)
ax.axhline(p0, color=MUTED, ls=":", lw=1.2,
           label=f"mutation-selection baseline $\\approx${p0:.3f}")
ax.axvline(T_on, color=INK, lw=1.0, ls="--")

ax.text(T_on / 2, 1.02, "drug on", ha="center", fontsize=9, color=INK)
ax.text((T_on + T_end) / 2, 1.02, "drug off", ha="center", fontsize=9,
        color=INK)
ax.annotate("rise under selection", xy=(30, 0.55), xytext=(6, 0.82),
            fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK))
ax.annotate("slow decline\nunder fitness cost", xy=(130, 0.3),
            xytext=(150, 0.6), fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK))

ax.set_xlabel("generation")
ax.set_ylabel("resistant frequency $p$")
ax.set_ylim(-0.03, 1.12)
ax.set_xlim(0, T_end)
ax.set_title("Selection for and against resistance")
ax.legend(loc="center right", fontsize=9)

save(fig, "assets/figures/resistance-evolution.svg")
