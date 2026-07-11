# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""A two-state Markov chain. Left: the transition diagram for the weather chain
(Sunny, Rainy) with its four one-step probabilities. Right: two long
simulations started from opposite states both have their running frequency of
Sunny converge to the stationary probability pi_1 = 4/7 ~ 0.571, illustrating
that an irreducible aperiodic chain forgets its starting point."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(42)

P = np.array([[0.7, 0.3], [0.4, 0.6]])

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.6),
                               gridspec_kw={"width_ratios": [1, 1.15]})

# ---- transition diagram ---------------------------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 10)
axL.axis("off")
axL.set_title("Transition diagram", fontsize=10)

sunny = (2.6, 5.0)
rainy = (7.4, 5.0)
for c, lab, col in [(sunny, "Sunny", PALETTE[4]), (rainy, "Rainy", PALETTE[0])]:
    axL.add_patch(Circle(c, 1.25, facecolor=col + "22", edgecolor=col, lw=2.0))
    axL.text(*c, lab, ha="center", va="center", fontsize=10, color=INK)

# S -> R (top) and R -> S (bottom)
axL.add_patch(FancyArrowPatch((3.7, 5.6), (6.3, 5.6), arrowstyle="-|>",
              mutation_scale=15, color=MUTED, lw=1.6,
              connectionstyle="arc3,rad=-0.3"))
axL.text(5.0, 7.0, "0.3", fontsize=9, color=INK, ha="center")
axL.add_patch(FancyArrowPatch((6.3, 4.4), (3.7, 4.4), arrowstyle="-|>",
              mutation_scale=15, color=MUTED, lw=1.6,
              connectionstyle="arc3,rad=-0.3"))
axL.text(5.0, 3.0, "0.4", fontsize=9, color=INK, ha="center")
# self-loops
axL.add_patch(FancyArrowPatch((1.9, 6.0), (1.9, 4.0), arrowstyle="-|>",
              mutation_scale=13, color=PALETTE[4], lw=1.5,
              connectionstyle="arc3,rad=1.4"))
axL.text(0.15, 5.0, "0.7", fontsize=9, color=PALETTE[4], ha="center")
axL.add_patch(FancyArrowPatch((8.1, 4.0), (8.1, 6.0), arrowstyle="-|>",
              mutation_scale=13, color=PALETTE[0], lw=1.5,
              connectionstyle="arc3,rad=1.4"))
axL.text(9.85, 5.0, "0.6", fontsize=9, color=PALETTE[0], ha="center")
axL.text(5.0, 1.2, r"$\pi=(4/7,\,3/7)\approx(0.571,\,0.429)$", fontsize=9,
         color=INK, ha="center")

# ---- convergence of running frequency -------------------------------------
n = 4000


def run_chain(start):
    x = np.empty(n, dtype=int)
    x[0] = start
    for t in range(1, n):
        x[t] = rng.choice(2, p=P[x[t - 1]])
    return np.cumsum(x == 0) / np.arange(1, n + 1)   # running freq of Sunny


axR.plot(run_chain(0), color=PALETTE[4], lw=1.4, label="started Sunny")
axR.plot(run_chain(1), color=PALETTE[0], lw=1.4, label="started Rainy")
axR.axhline(4 / 7, ls="--", color=INK, lw=1.2)
axR.text(n, 4 / 7 + 0.015, r"$\pi_1=4/7$", fontsize=8.5, color=INK, ha="right")
axR.set_xlabel("step")
axR.set_ylabel("running frequency of Sunny")
axR.set_title("Convergence to the stationary distribution", fontsize=10)
axR.set_xlim(0, n)
axR.set_ylim(0.3, 0.8)
axR.legend(fontsize=8.5, loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/markov-chains.svg")
