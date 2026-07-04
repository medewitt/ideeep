# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""How demographic stochasticity reweights the Price equation (Day et al. 2020).

In a finite population the covariance term of Price's equation acquires a
'measure of fitness' b - d - (b+d)/(AI): expected fitness b-d PENALIZED by the
variance in fitness b+d, scaled by the number of infected hosts AI. Equivalently
(their eq. 5.2), selection on the birth (transmission) component is multiplied by
(1 - 1/AI) and selection on the death (virulence) component by (1 + 1/AI).

Left: those two weights versus AI -- selection on transmission is weakened,
selection on virulence is strengthened. Right: the consequence on a
transmission-virulence trade-off. Two strains chosen to be DETERMINISTICALLY
NEUTRAL (equal net fitness) differ in turnover b+d; the milder strain has lower
fitness variance, so drift favours it, and the bias grows as AI shrinks -- drift
drives the evolution of lower virulence."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.2, 4.4))

# ---- Left: the birth/death weights (1 -/+ 1/AI) ----
AI = np.linspace(3, 200, 400)
axL.axhline(1.0, color=MUTED, lw=0.9, ls="--", label="deterministic (weight 1)")
axL.plot(AI, 1 - 1 / AI, color=PALETTE[0], lw=2.0,
         label="transmission / birth:  $1-\\dfrac{1}{AI}$")
axL.plot(AI, 1 + 1 / AI, color=PALETTE[1], lw=2.0,
         label="virulence / death:  $1+\\dfrac{1}{AI}$")
axL.fill_between(AI, 1 - 1 / AI, 1, color=PALETTE[0], alpha=0.12)
axL.fill_between(AI, 1, 1 + 1 / AI, color=PALETTE[1], alpha=0.12)
axL.set_xlabel("number of infected hosts  $AI$")
axL.set_ylabel("weight on the selection term")
axL.set_title("Drift weakens selection on transmission,\nstrengthens it on virulence",
              fontsize=10.5)
axL.legend(fontsize=8.5, loc="center right")
axL.set_ylim(0.5, 1.7)

# ---- Right: consequence on a virulence-transmission trade-off ----
mu, a = 0.02, 6.0
vH, vL = 0.80, 0.40                          # high- and low-virulence strains
bH_rate, bL_rate = a * np.sqrt(vH), a * np.sqrt(vL)   # transmission via trade-off
Sneutral = (vH - vL) / (bH_rate - bL_rate)   # S where the two strains have EQUAL net fitness
bH, bL = bH_rate * Sneutral, bL_rate * Sneutral       # births
dH, dL = mu + vH, mu + vL                              # deaths
# deterministic net fitnesses are equal by construction:
rH, rL = bH - dH, bL - dL                     # ~ equal

AIr = np.linspace(4, 300, 400)
# stochastic fitness measure b - d - (b+d)/AI for each strain; selection favouring L:
sL = (bL - dL - (bL + dL) / AIr)
sH = (bH - dH - (bH + dH) / AIr)
sel_diff = sL - sH                            # > 0 means the milder strain L is favoured

axR.axhline(0, color=MUTED, lw=0.9)
axR.plot(AIr, sel_diff, color=PALETTE[2], lw=2.2)
axR.fill_between(AIr, 0, sel_diff, color=PALETTE[2], alpha=0.15)
axR.set_xlabel("number of infected hosts  $AI$")
axR.set_ylabel("stochastic selection for the milder strain")
axR.set_title("Deterministically neutral strains:\ndrift favours the milder one", fontsize=10.5)
axR.annotate(f"variance in fitness\n$b+d$: {bH+dH:.2f} (virulent) vs {bL+dL:.2f} (mild)",
             xy=(60, sel_diff[np.argmin(np.abs(AIr - 60))]),
             xytext=(90, sel_diff.max() * 0.6), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axR.text(0.97, 0.06, "net fitness $b-d$ equal for both strains",
         transform=axR.transAxes, ha="right", fontsize=8, color=MUTED, style="italic")

fig.suptitle("Demographic stochasticity reweights Price's equation toward lower virulence",
             fontweight="bold")
fig.tight_layout()
save(fig, "assets/figures/price-drift-virulence.svg")

print("S (neutral) =", round(float(Sneutral), 4))
print("net fitness rH, rL =", round(float(rH), 5), round(float(rL), 5), " (equal by design)")
print("fitness variance b+d: virulent =", round(float(bH + dH), 3),
      " mild =", round(float(bL + dL), 3))
print("selection for mild at AI=20:", round(float((bL - dL - (bL + dL) / 20) -
                                                  (bH - dH - (bH + dH) / 20)), 4))
