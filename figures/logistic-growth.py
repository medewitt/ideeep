# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Exponential vs. logistic growth curves."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

r, K, N0 = 0.6, 100.0, 2.0
t = np.linspace(0, 20, 400)
exp = N0 * np.exp(r * t)
logi = K / (1 + (K - N0) / N0 * np.exp(-r * t))

fig, ax = plt.subplots()
ax.plot(t, exp, "--", color=PALETTE[1], label="exponential  $rN$")
ax.plot(t, logi, color=PALETTE[0], label=r"logistic  $rN(1-N/K)$")
ax.axhline(K, color="#9aa7b3", lw=0.8, ls=":")
ax.text(0.3, K + 2, "carrying capacity $K$", color="#5b6b7a", fontsize=9)
ax.set_ylim(0, 130)
ax.set_xlabel("time $t$")
ax.set_ylabel("population $N(t)$")
ax.set_title("Exponential vs. logistic growth")
ax.legend(loc="upper left")
save(fig, "assets/figures/logistic-growth.svg")
