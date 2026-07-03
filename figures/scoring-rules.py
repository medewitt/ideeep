# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Propriety: the expected Brier and log scores are both minimized when the
forecaster reports the true probability, so honesty is optimal."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

p = 0.7                                   # true probability of the event
q = np.linspace(1e-3, 1 - 1e-3, 500)      # the probability the forecaster reports
brier = p * (1 - q) ** 2 + (1 - p) * q ** 2
logscore = -(p * np.log(q) + (1 - p) * np.log(1 - q))

print(f"true probability p = {p}")
print(f"Brier expected penalty minimized at q = {q[np.argmin(brier)]:.3f}")
print(f"log-score expected penalty minimized at q = {q[np.argmin(logscore)]:.3f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.6))
for ax, y, name in ((ax1, brier, "Brier score"), (ax2, logscore, "Logarithmic score")):
    ax.plot(q, y, color=PALETTE[0], lw=2)
    ax.axvline(p, color=PALETTE[1], ls="--")
    ax.scatter([p], [y[np.argmin(np.abs(q - p))]], color=PALETTE[1], zorder=5)
    ax.set_xlabel("reported probability $q$")
    ax.set_ylabel("expected penalty")
    ax.set_title(name)
    ax.annotate("minimized at\n$q = p = 0.7$", xy=(p, y.min()),
                xytext=(0.12, 0.72), textcoords="axes fraction", fontsize=9,
                arrowprops=dict(arrowstyle="->", color="#26323f"))
fig.suptitle("Proper scores reward honest probabilities", y=1.03)
save(fig, "assets/figures/scoring-rules.svg")
