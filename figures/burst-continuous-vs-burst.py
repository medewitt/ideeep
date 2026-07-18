# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Continuous vs. lytic-burst production: same mean, different extinction.

Deterministic ODEs cannot tell the two apart -- only the lifetime yield R0
matters. But the offspring *distribution* differs: continuous release with an
exponential cell lifetime gives a geometric number of secondary infections
(over-dispersed), while a fixed burst gives a Poisson/binomial number
(under-dispersed). More variance means a higher chance the lineage dies out,
so for the same R0 the continuous mode is easier to extinguish early.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

R0 = np.linspace(1.0, 6.0, 300)

# Continuous production, exponential lifetime -> geometric offspring: q = 1/R0.
q_cont = np.where(R0 > 1, 1.0 / R0, 1.0)

# Fixed burst, each virion independently succeeds -> ~Poisson(R0) offspring:
# q solves q = exp(R0 (q - 1)).
q_burst = np.ones_like(R0)
for i, r in enumerate(R0):
    qi = 0.0
    for _ in range(4000):
        qi = np.exp(r * (qi - 1.0))
    q_burst[i] = qi

fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot(R0, q_cont, color=PALETTE[0], lw=2.4, label="continuous (geometric): $q=1/R_0$")
ax.plot(R0, q_burst, color=PALETTE[1], lw=2.4, label="lytic burst (Poisson)")
ax.fill_between(R0, q_burst, q_cont, color=PALETTE[0], alpha=0.10)

ax.set_xlabel("cellular reproduction number $R_0$")
ax.set_ylabel("probability infection dies out")
ax.set_title("same $R_0$, different early fate")
ax.set_xlim(1, 6)
ax.set_ylim(0, 1.02)
ax.legend(fontsize=9)
ax.annotate("continuous production\nis easier to extinguish",
            xy=(2.0, 0.5), xytext=(3.0, 0.72), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))

fig.tight_layout()
save(fig, "assets/figures/burst-continuous-vs-burst.svg")
