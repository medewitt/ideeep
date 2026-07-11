# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Generalized linear models. Left: the inverse link maps the unbounded linear
predictor eta onto the mean's natural range — the identity link is a straight
line, the logit's inverse (a sigmoid) keeps a probability in [0,1], and the
log's inverse (exp) keeps a rate positive. Right: the worked count example —
District B has the larger raw case count (60 vs 30) but, once the log-population
offset is applied, half the incidence rate (0.0015 vs 0.0030), so the offset
flips which district looks worse."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- inverse-link curves --------------------------------------------------
eta = np.linspace(-4, 4, 300)
axL.plot(eta, eta, color=MUTED, lw=1.8, ls="--", label="identity: $\\mu=\\eta$")
axL.plot(eta, 1 / (1 + np.exp(-eta)), color=PALETTE[0], lw=2.0,
         label=r"logit$^{-1}$: sigmoid $\in[0,1]$")
axL.plot(eta, np.exp(eta), color=PALETTE[1], lw=2.0,
         label=r"log$^{-1}$: $e^\eta>0$")
axL.axhline(0, color="#c9d2da", lw=0.8)
axL.axhline(1, color="#c9d2da", lw=0.8, ls=":")
axL.set_xlabel(r"linear predictor $\eta=x^\top\beta$")
axL.set_ylabel(r"mean $\mu=g^{-1}(\eta)$")
axL.set_title("The link maps η onto the mean's range", fontsize=9.5)
axL.set_ylim(-1.5, 4)
axL.legend(fontsize=8, loc="upper left")

# ---- offset flips the ranking ---------------------------------------------
districts = ["A", "B"]
cases = np.array([30, 60])
pop = np.array([10000, 40000])
rate = cases / pop * 1000                 # per 1000 person-years

x = np.arange(2)
axR.bar(x, rate, width=0.55, color=[PALETTE[0], PALETTE[1]])
for i in range(2):
    axR.annotate(f"{rate[i]:.1f} / 1000", (i, rate[i]),
                 textcoords="offset points", xytext=(0, 4), ha="center",
                 fontsize=9, color=INK)
    axR.text(i, 0.12, f"{cases[i]} cases\npop {pop[i]:,}", ha="center",
             fontsize=7.8, color="white", va="bottom")
axR.annotate("more raw cases,\nbut half the rate", xy=(1, rate[1]),
             xytext=(0.3, 2.4), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axR.set_xticks(x)
axR.set_xticklabels([f"District {d}" for d in districts])
axR.set_ylabel("incidence rate (per 1000)")
axR.set_title("Why the population offset matters", fontsize=9.5)
axR.set_ylim(0, 3.4)
axR.grid(axis="x", visible=False)

fig.tight_layout()
save(fig, "assets/figures/generalized-linear-models.svg")
