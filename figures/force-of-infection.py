# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Force of infection: catalytic seroprevalence and age-varying FOI."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# LEFT: age-seroprevalence with fitted catalytic model
lam = 0.12  # constant force of infection per year
ages = np.linspace(0, 60, 300)
sero = 1.0 - np.exp(-lam * ages)

axL.plot(ages, sero, color=INK, lw=2.0, label="catalytic model")

n = 60
sample_ages = np.arange(2, 56, 3)
p_true = 1.0 - np.exp(-lam * sample_ages)
obs = rng.binomial(n, p_true) / n
axL.plot(sample_ages, obs, "o", color=PALETTE[0], ms=5,
         label="observed seroprevalence")

axL.annotate("catalytic model:  1 − e^(−λa)", xy=(30, 1 - np.exp(-lam * 30)),
             xytext=(12, 0.9), fontsize=9, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axL.set_xlim(0, 60)
axL.set_ylim(0, 1.0)
axL.set_xlabel("age (years)")
axL.set_ylabel("proportion seropositive")
axL.legend(loc="lower right", fontsize=8)

# RIGHT: piecewise-constant force of infection by age band
edges = [0, 5, 15, 45, 65]     # band boundaries (years)
foi = [0.05, 0.20, 0.08, 0.04]  # per year, school-age peak

x = np.array(edges, dtype=float)
y = np.array(foi + [foi[-1]], dtype=float)  # repeat last for step "post"
axR.step(x, y, where="post", color=PALETTE[3], lw=2.0)
axR.fill_between(x, 0, y, step="post", color=PALETTE[3], alpha=0.15)

axR.annotate("average age at infection ≈ 1/λ̄", xy=(10, 0.20),
             xytext=(20, 0.16), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axR.set_xlim(0, 65)
axR.set_ylim(0, 0.24)
axR.set_xlabel("age (years)")
axR.set_ylabel("force of infection λ (per year)")

fig.tight_layout()
save(fig, "assets/figures/force-of-infection.svg")
