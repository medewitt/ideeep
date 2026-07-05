# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Modern coexistence theory: the stabilizing-equalizing plane and the
storage effect.

Panel (a) draws the coexistence region in the niche-overlap by fitness-ratio
plane: species coexist when the fitness ratio sits between the niche overlap
and its reciprocal. Panel (b) simulates a two-species lottery model and shows
that each species has a positive low-density growth rate only when population
growth is buffered by adult survival.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.9))

# Panel (a): coexistence region  rho < k_j/k_i < 1/rho.
ax = axes[0]
rho = np.linspace(0.001, 1.0, 300)
ax.fill_between(rho, rho, 1.0 / rho, color=PALETTE[2], alpha=0.18)
ax.plot(rho, rho, color=PALETTE[0], lw=2, label=r"$k_j/k_i=\rho$")
ax.plot(rho, 1.0 / rho, color=PALETTE[1], lw=2, label=r"$k_j/k_i=1/\rho$")
ax.axhline(1.0, color=MUTED, ls=":", lw=1)
ax.set_yscale("log")
ax.set_ylim(0.25, 4.0)
ax.set_xlim(0, 1)
ax.set_xlabel(r"niche overlap $\rho$  (1 = identical niches)")
ax.set_ylabel(r"fitness ratio $k_j/k_i$")
ax.set_title("(a) stabilizing vs equalizing", fontsize=10)
ax.text(0.35, 1.0, "coexistence", color=PALETTE[2], fontsize=10,
        ha="center", va="center", weight="bold")
ax.text(0.82, 2.7, "exclusion", color=MUTED, fontsize=9.5, ha="center")
ax.legend(fontsize=8.5, loc="lower left")

# Panel (b): storage effect via a two-species lottery model.
# B_i(t) is environment-driven per-capita reproduction; species respond to
# negatively correlated environments. Adult survival (1 - delta) buffers growth.
T = 20000
sig = 1.0
z = rng.standard_normal((T, 2))
z[:, 1] = -0.8 * z[:, 0] + np.sqrt(1 - 0.8**2) * z[:, 1]
B = np.exp(sig * z - 0.5 * sig**2)  # lognormal, mean 1


def invasion_rate(delta, inv, res):
    ratio = B[:, inv] / B[:, res]
    lam = (1.0 - delta) + delta * ratio
    return np.mean(np.log(lam))


labels = ["buffered\n(delta=0.1)", "unbuffered\n(delta=1.0)"]
r_sp1 = [invasion_rate(0.1, 0, 1), invasion_rate(1.0, 0, 1)]
r_sp2 = [invasion_rate(0.1, 1, 0), invasion_rate(1.0, 1, 0)]
x = np.arange(2)
ax = axes[1]
ax.bar(x - 0.2, r_sp1, width=0.4, color=PALETTE[0], label="species 1 rare")
ax.bar(x + 0.2, r_sp2, width=0.4, color=PALETTE[1], label="species 2 rare")
ax.axhline(0.0, color=INK, lw=1)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("low-density growth rate $\\bar r_i$")
ax.set_title("(b) the storage effect", fontsize=10)
ax.legend(fontsize=8.5)

fig.tight_layout()
save(fig, "assets/figures/coexistence-theory.svg")
