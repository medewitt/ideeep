# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""What "proportional odds" looks like on the two scales that define it. Left:
the model says the log-odds of exceeding each cutpoint, log odds(Y >= j), is
linear in x with the SAME slope beta for every j -- so the cutpoint lines are
parallel, separated only by their intercepts. Right: on the probability scale
this is a family of cumulative-probability curves P(Y >= j | x) that are
horizontal shifts of one another. A single odds ratio exp(beta) moves you the
same multiplicative distance at every cutpoint; that shared slope is exactly
the assumption a proportional odds check interrogates."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

def lcdf(z):
    return 1.0 / (1 + np.exp(-z))

beta = 0.9
alphas = np.array([2.4, 0.9, -0.9, -2.4])   # intercepts for P(Y >= j), j=2..5
x = np.linspace(-4, 4, 400)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.9))

# ---- left: parallel cumulative-logit lines ----
for a, col, j in zip(alphas, PALETTE, range(2, 6)):
    axL.plot(x, a + beta * x, color=col, lw=2.0, label=fr"$Y \geq {j}$")
axL.axhline(0, color=MUTED, lw=0.8)
axL.set_title(r"Log-odds are parallel (common slope $\beta$)", fontsize=10)
axL.set_xlabel("x")
axL.set_ylabel(r"$\log\,\mathrm{odds}(Y \geq j)$")
axL.legend(fontsize=8, loc="upper left", ncol=2)

# ---- right: parallel cumulative-probability sigmoids ----
for a, col, j in zip(alphas, PALETTE, range(2, 6)):
    axR.plot(x, lcdf(a + beta * x), color=col, lw=2.0, label=fr"$Y \geq {j}$")
axR.set_ylim(0, 1)
axR.set_title(r"Cumulative probabilities are shifts", fontsize=10)
axR.set_xlabel("x")
axR.set_ylabel(r"$P(Y \geq j \mid x)$")
axR.legend(fontsize=8, loc="lower right", ncol=2)

fig.tight_layout()
save(fig, "assets/figures/proportional-odds-parallel.svg")
