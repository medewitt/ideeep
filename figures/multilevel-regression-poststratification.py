# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Multilevel regression and poststratification: shrinkage then reweighting."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.6))

# --- LEFT: partial pooling / shrinkage -------------------------------------
J = 8
mu = 0.40                                   # grand-mean prevalence
tau = 0.10                                  # between-cell SD
n = np.array([12, 18, 30, 45, 70, 120, 260, 500])   # cell sample sizes
true = mu + rng.normal(0, tau, size=J)
raw = true + rng.normal(0, 0.5 / np.sqrt(n))        # noisy no-pooling estimate

grand = mu
se = 0.5 / np.sqrt(n)                        # standard error of raw estimate
w = tau ** 2 / (tau ** 2 + se ** 2)          # reliability weight
pooled = grand + w * (raw - grand)           # pull toward grand mean

xc = np.arange(J)
axL.axhline(grand, ls="--", color=MUTED, lw=1.0)
axL.text(J - 1, grand + 0.006, "grand mean", ha="right", va="bottom",
         color=MUTED, fontsize=8.5)

# arrows: raw -> pooled (shrinkage)
for i in range(J):
    axL.annotate("", xy=(xc[i], pooled[i]), xytext=(xc[i], raw[i]),
                 arrowprops=dict(arrowstyle="->", color="#b0b8c0", lw=0.9))

axL.errorbar(xc, raw, yerr=1.96 * se, fmt="o", ms=4, color=MUTED,
             ecolor=MUTED, elinewidth=1.0, capsize=2,
             label="no pooling (95% CI)", zorder=3)
axL.scatter(xc, pooled, s=32, color=PALETTE[0], zorder=4,
            label="partial pooling")

axL.annotate("small cells\nshrink most",
             xy=(0, pooled[0]), xytext=(1.4, 0.72),
             fontsize=8.5, color=INK, ha="left",
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

axL.set_xticks(xc)
axL.set_xticklabels([f"{ni}" for ni in n], fontsize=8)
axL.set_xlabel("cell (sample size n)")
axL.set_ylabel("estimated prevalence")
axL.set_title("Shrinkage in the model", fontsize=10)
axL.legend(loc="lower right", fontsize=8.5)
axL.grid(axis="x", visible=False)

# --- RIGHT: poststratification ---------------------------------------------
K = 6
rates = np.array([0.28, 0.55, 0.42, 0.66, 0.35, 0.50])   # modeled cell rates
share = np.array([0.30, 0.10, 0.22, 0.06, 0.20, 0.12])   # population share
share = share / share.sum()

ps = np.sum(rates * share)               # poststratified estimate

left = np.concatenate([[0.0], np.cumsum(share)])[:-1]
axR.bar(left, rates, width=share, align="edge", color=PALETTE[2],
        edgecolor="white", linewidth=0.8, alpha=0.9)

for i in range(K):
    axR.text(left[i] + share[i] / 2, rates[i] + 0.015,
             f"{share[i]*100:.0f}%", ha="center", va="bottom",
             color=MUTED, fontsize=7.5)

axR.axhline(ps, color=PALETTE[1], lw=1.6)
axR.annotate("poststratified estimate",
             xy=(0.5, ps), xytext=(0.30, ps + 0.14),
             fontsize=8.5, color=PALETTE[1], ha="left",
             arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.9))

axR.set_xlim(0, 1)
axR.set_ylim(0, 0.8)
axR.set_xlabel("population share")
axR.set_ylabel("modeled rate")
axR.set_title("Poststratify to the population", fontsize=10)
axR.grid(axis="x", visible=False)

fig.tight_layout()
save(fig, "assets/figures/multilevel-regression-poststratification.svg")
