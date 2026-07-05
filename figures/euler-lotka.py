# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Euler-Lotka: from growth rate to R0 through the generation interval."""
import numpy as np
from scipy.stats import gamma as gamma_dist
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
np.random.seed(1834)

fig, (axa, axb, axc) = plt.subplots(1, 3, figsize=(11.4, 3.6))

# --- Panel (a): renewal-equation schematic -------------------------------
r = 0.15
days = np.arange(-10, 1)                       # past days up to today (0)
inc = np.exp(r * days)                          # exponentially growing incidence
shape, mean_gi = 4.0, 6.0
scale = mean_gi / shape
tau = np.arange(1, 11)
g = gamma_dist.pdf(tau, a=shape, scale=scale)
g = g / g.sum()

axa.bar(days[:-1], inc[:-1], width=0.7, color=MUTED, alpha=0.45,
        label="past incidence $i(t-\\tau)$")
axa.bar([0], [inc[-1]], width=0.7, color=PALETTE[1], label="today $i(t)$")
# weighting profile g(tau) laid over the recent past
axg = axa.twinx()
axg.plot(-tau, g, "o-", color=PALETTE[0], lw=1.8, ms=4,
         label="$g(\\tau)$")
axg.set_ylim(0, g.max() * 2.6)
axg.set_yticks([])
axa.set_title("(a) renewal convolution")
axa.set_xlabel("time relative to today (days)")
axa.set_ylabel("incidence")
axa.annotate("$i(t)=R_0\\sum_\\tau i(t-\\tau)\\,g(\\tau)$",
             xy=(0, inc[-1]), xytext=(-10.3, inc[-1] * 1.02),
             fontsize=8.5, color=INK)
h1, l1 = axa.get_legend_handles_labels()
h2, l2 = axg.get_legend_handles_labels()
axa.legend(h1 + h2, l1 + l2, fontsize=7.5, loc="upper left")

# --- Panel (b): R0 vs generation-interval mean at fixed r ----------------
Tg = np.linspace(2, 12, 200)
axb.plot(Tg, np.exp(r * Tg), color=PALETTE[3], lw=2,
         label="fixed delay  $e^{rT_g}$")
axb.plot(Tg, (1 + r * Tg / 4) ** 4, color=PALETTE[2], lw=2,
         label="gamma, shape 4")
axb.plot(Tg, 1 + r * Tg, color=PALETTE[0], lw=2,
         label="exponential  $1+rT_g$")
axb.set_title(f"(b) $R_0$ vs mean interval ($r={r}$)")
axb.set_xlabel("mean generation interval $T_g$ (days)")
axb.set_ylabel("$R_0$")
axb.legend(fontsize=8, loc="upper left")

# --- Panel (c): R0 = 1 / M(-r) for a gamma interval ----------------------
rr = np.linspace(0.0, 0.35, 200)
R0_curve = (1 + rr * scale) ** shape           # gamma MGF, mean 6, shape 4
axc.plot(rr, R0_curve, color=PALETTE[1], lw=2.2)
axc.axhline(1, color=MUTED, lw=0.8, ls=":")
axc.plot([r], [(1 + r * scale) ** shape], "o", color=INK, ms=6)
axc.annotate(f"$r={r}\\Rightarrow R_0={(1 + r * scale) ** shape:.2f}$",
             xy=(r, (1 + r * scale) ** shape),
             xytext=(0.02, 3.4), fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK))
axc.set_title("(c) $R_0 = 1/M(-r)$, gamma $g$")
axc.set_xlabel("growth rate $r$ (per day)")
axc.set_ylabel("$R_0$")

fig.tight_layout()
save(fig, "assets/figures/euler-lotka.svg")
