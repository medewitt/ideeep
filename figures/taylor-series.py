# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Successive Taylor (Maclaurin) polynomials converging to sin(x)."""
import math
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

x = np.linspace(-2 * np.pi, 2 * np.pi, 800)

# Maclaurin partial sums of sin: T1, T3, T5, T7 (odd-degree terms only)
def taylor_sin(x, degree):
    total = np.zeros_like(x)
    for k in range((degree + 1) // 2):
        n = 2 * k + 1
        total += (-1) ** k * x ** n / math.factorial(n)
    return total

fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color="#26323f", lw=2.2, label=r"$\sin x$")
for i, deg in enumerate([1, 3, 5, 7]):
    ax.plot(x, taylor_sin(x, deg), color=PALETTE[i], lw=1.3, ls="--",
            label=f"degree {deg}")
ax.set_ylim(-2.2, 2.2)
ax.set_xlabel("$x$")
ax.set_ylabel("value")
ax.set_title(r"Taylor polynomials of $\sin x$ about $0$")
ax.legend(loc="upper center", ncol=3, fontsize=9)
save(fig, "assets/figures/taylor-series.svg")
