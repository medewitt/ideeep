# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Derivative as instantaneous rate of change: tangent to f(x)=x^2 at x0=1.5."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

x = np.linspace(-1, 3, 400)
f = lambda t: t**2
fp = lambda t: 2 * t

x0 = 1.5
y0 = f(x0)
slope = fp(x0)  # = 3
tangent = y0 + slope * (x - x0)

print(f"x0 = {x0}, f(x0) = {y0}, slope f'(x0) = {slope}")

fig, ax = plt.subplots()
ax.plot(x, f(x), color=PALETTE[0], lw=2, label=r"$f(x)=x^2$")
ax.plot(x, tangent, color=PALETTE[1], lw=2, ls="--",
        label=f"tangent at x={x0}")
ax.plot([x0], [y0], "o", color=PALETTE[1], ms=8, zorder=5)

ax.annotate(r"slope = $f'(1.5) = 3$", xy=(x0, y0),
            xytext=(x0 - 1.7, y0 + 3.5),
            arrowprops=dict(arrowstyle="->", color="#26323f"))

ax.set_ylim(-1, f(3) + 1)
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title("Derivative: instantaneous rate of change")
ax.legend(loc="upper left")

save(fig, "assets/figures/derivative-tangent.svg")
