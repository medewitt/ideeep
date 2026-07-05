# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Life-history theory: the reproductive-effort trade-off, Cole's paradox,
and a life-history invariant."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.4))

# (a) Reproductive-effort trade-off with the fitness-maximizing allocation.
B, Vf, s0 = 4.0, 3.0, 0.9
e = np.linspace(0, 1, 200)
fecundity = B * e                     # current reproduction rises with effort
survival = s0 * (1 - e**2)            # survival to next year falls with effort
fitness = fecundity + Vf * survival   # current + future reproductive value
e_star = e[int(np.argmax(fitness))]
axes[0].plot(e, fecundity, color=PALETTE[1], lw=2, label="fecundity $b(e)$")
axes[0].plot(e, Vf * survival, color=PALETTE[0], lw=2,
             label="survival value $V_f\\,s(e)$")
axes[0].plot(e, fitness, color=INK, lw=2.2, label="fitness $w(e)$")
axes[0].axvline(e_star, color=MUTED, ls="--", lw=1)
axes[0].plot(e_star, fitness.max(), "o", color=INK, ms=6)
axes[0].set_xlabel("reproductive effort $e$")
axes[0].set_ylabel("contribution to fitness")
axes[0].set_title("(a) allocation trade-off")
axes[0].legend(fontsize=7.5, loc="lower center")

# (b) Cole's paradox: iteroparity favored when adult survival is high.
c = 0.5                               # juvenile survival to first breeding
Bi = 3.0                              # iteroparous clutch
Bs = Bi + 1.0                         # semelparous clutch (one extra offspring)
p = np.linspace(0, 1, 200)
lam_semel = np.full_like(p, c * Bs)   # reproduce once, then die
lam_itero = c * Bi + p                # reproduce yearly, adult survives at p
pcross = (c * Bs - c * Bi)            # solve lam_semel = lam_itero
axes[1].plot(p, lam_semel, color=PALETTE[1], lw=2, label="semelparous")
axes[1].plot(p, lam_itero, color=PALETTE[0], lw=2, label="iteroparous")
axes[1].axvline(pcross, color=MUTED, ls="--", lw=1)
axes[1].annotate("iteroparity wins", xy=(0.78, c * Bi + 0.78),
                 fontsize=7.5, color=INK, ha="center")
axes[1].set_xlabel("adult survival $p$")
axes[1].set_ylabel(r"growth rate $\lambda$")
axes[1].set_title("(b) Cole's paradox")
axes[1].legend(fontsize=8, loc="upper left")

# (c) A life-history invariant: age at maturity times mortality is near-constant.
M = np.exp(rng.uniform(np.log(0.05), np.log(2.0), 120))   # adult mortality
K = 1.0                                                    # invariant product
alpha = K / M * np.exp(rng.normal(0, 0.25, M.size))        # age at maturity
axes[2].scatter(M, alpha, s=14, color=PALETTE[2], alpha=0.7, edgecolor="none")
grid = np.logspace(np.log10(0.05), np.log10(2.0), 50)
axes[2].plot(grid, K / grid, color=INK, lw=1.6, label=r"$\alpha\,M = 1$")
axes[2].set_xscale("log")
axes[2].set_yscale("log")
axes[2].set_xlabel("mortality $M$")
axes[2].set_ylabel(r"age at maturity $\alpha$")
axes[2].set_title("(c) life-history invariant")
axes[2].legend(fontsize=8, loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/life-history-theory.svg")
