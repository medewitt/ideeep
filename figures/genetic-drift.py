# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""Wright-Fisher genetic drift trajectories showing fixation and loss."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE
apply_style()

rng = np.random.default_rng(1)

N = 50            # diploid individuals
two_N = 2 * N     # gene copies
p0 = 0.5
generations = 120
replicates = 30

fig, ax = plt.subplots()

n_fixed = 0
n_lost = 0
for _ in range(replicates):
    p = p0
    traj = [p]
    for _g in range(generations):
        count = rng.binomial(two_N, p)
        p = count / two_N
        traj.append(p)
    traj = np.array(traj)
    final = traj[-1]
    if final >= 1.0:
        color = PALETTE[1]
        n_fixed += 1
    elif final <= 0.0:
        color = PALETTE[2]
        n_lost += 1
    else:
        color = PALETTE[0]
    ax.plot(np.arange(generations + 1), traj, color=color,
            linewidth=0.9, alpha=0.5)

ax.axhline(p0, linestyle="--", color="0.4", linewidth=1.2,
           label=f"initial frequency $p_0={p0}$")

# Proxy legend handles for the outcome colors.
ax.plot([], [], color=PALETTE[1], linewidth=1.5,
        label=f"fixation ($p=1$): {n_fixed}")
ax.plot([], [], color=PALETTE[2], linewidth=1.5,
        label=f"loss ($p=0$): {n_lost}")
ax.plot([], [], color=PALETTE[0], linewidth=1.5,
        label="segregating")

ax.set_xlabel("Generation")
ax.set_ylabel("Allele frequency $p$")
ax.set_ylim(-0.02, 1.02)
ax.set_xlim(0, generations)
ax.set_title(f"Genetic drift in a finite population (2N={two_N}):\n"
             "random walk to fixation or loss")
ax.legend(loc="center right", fontsize="small")

save(fig, "assets/figures/genetic-drift.svg")
