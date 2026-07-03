# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Maximizing a concave quadratic: f(x) = -(x-3)^2 + 5."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

np.random.seed(0)

x = np.linspace(-1, 7, 400)
f = -(x - 3) ** 2 + 5
xstar, fstar = 3.0, 5.0

fig, ax = plt.subplots()
ax.plot(x, f, color=PALETTE[0], linewidth=2.0, label="f(x) = -(x-3)² + 5")
# flat tangent at the maximum
ax.plot([xstar - 2, xstar + 2], [fstar, fstar], color=PALETTE[1],
        linewidth=1.6, linestyle="--", label="tangent f'(3)=0")
ax.plot([xstar], [fstar], "o", color=PALETTE[1], markersize=8)
ax.annotate("f'(3)=0, f''<0 → maximum\nf(3)=5",
            xy=(xstar, fstar), xytext=(xstar + 0.4, fstar - 2.4),
            color="#26323f",
            arrowprops=dict(arrowstyle="->", color="#26323f"))

ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title("Optimization: a concave maximum")
ax.legend(loc="lower center")

print(f"maximum at x* = {xstar:g}, f(x*) = {fstar:g}")
print("f'(3) = 0, f'' = -2 < 0 -> maximum")

save(fig, "assets/figures/optimization-max.svg")
