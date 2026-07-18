# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""The shape of the seroprevalence curve encodes the force of infection. A constant
force of infection gives a smooth exponential approach to full seropositivity
(right); a force of infection concentrated in childhood makes seroprevalence climb
steeply early and then flatten, leaving a kink that marks where transmission fell.
Age-structured serosurveys are read backwards through this mapping to recover when
and in whom infection happens."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
ages = np.linspace(0, 45, 400)


def seroprev(foi_fn):
    da = ages[1] - ages[0]
    cum = np.cumsum(foi_fn(ages)) * da
    return 1 - np.exp(-cum)


const = lambda a: np.full_like(a, 0.10)
twophase = lambda a: np.where(a < 12, 0.20, 0.03)     # high childhood transmission

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.8))

axL.step(ages, const(ages), where="post", color=PALETTE[0], lw=2.2,
         label="constant  λ = 0.10")
axL.step(ages, twophase(ages), where="post", color=PALETTE[1], lw=2.2,
         label="age-varying (high < 12 yr)")
axL.set_xlabel("age (years)")
axL.set_ylabel("force of infection  λ(a)")
axL.set_title("Force of infection", fontsize=9.6)
axL.set_ylim(0, 0.24)
axL.legend(fontsize=8.2, loc="upper right")

axR.plot(ages, seroprev(const), color=PALETTE[0], lw=2.4, label="constant FOI")
axR.plot(ages, seroprev(twophase), color=PALETTE[1], lw=2.4, label="age-varying FOI")
axR.annotate("kink where\ntransmission dropped", xy=(12, seroprev(twophase)[np.argmin(np.abs(ages-12))]),
             xytext=(16, 0.45), fontsize=8.2, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
axR.set_xlabel("age (years)")
axR.set_ylabel("proportion seropositive")
axR.set_title("Resulting seroprevalence", fontsize=9.6)
axR.set_ylim(0, 1.02)
axR.legend(fontsize=8.2, loc="lower right")
fig.tight_layout()
save(fig, "assets/figures/serocatalytic-foi.svg")
