# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Definite integral as area under f(x)=x^2 from 0 to 1."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

x = np.linspace(0, 1, 400)
f = lambda t: t**2
area = 1 / 3  # analytic value of int_0^1 x^2 dx

print(f"area = int_0^1 x^2 dx = 1/3 = {area:.6f}")

fig, ax = plt.subplots()
ax.plot(x, f(x), color=PALETTE[0], lw=2, label=r"$f(x)=x^2$")
ax.fill_between(x, 0, f(x), color=PALETTE[0], alpha=0.25,
                label="area under curve")

ax.annotate(r"area = $\int_0^1 x^2\,dx = \frac{1}{3} \approx 0.333$",
            xy=(0.6, f(0.6) / 2), xytext=(0.05, 0.7),
            arrowprops=dict(arrowstyle="->", color="#26323f"))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title("Definite integral as area")
ax.legend(loc="upper left")

save(fig, "assets/figures/integral-area.svg")
