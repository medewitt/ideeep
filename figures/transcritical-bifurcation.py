# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Transcritical bifurcation diagram for dx/dt = r x - x^2."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

r = np.linspace(-1, 1, 400)

# Equilibria: x* = 0 and x* = r.
# f(x) = r x - x^2, f'(x) = r - 2x.
# Branch x*=0: f'(0) = r  -> stable when r<0, unstable when r>0.
# Branch x*=r: f'(r) = -r -> stable when r>0, unstable when r<0.
r_neg = r[r <= 0]
r_pos = r[r >= 0]

fig, ax = plt.subplots()

# x* = 0 branch
ax.plot(r_neg, np.zeros_like(r_neg), color=PALETTE[0], lw=2.4,
        label="stable")
ax.plot(r_pos, np.zeros_like(r_pos), color=PALETTE[1], lw=2.0, ls="--",
        label="unstable")

# x* = r branch
ax.plot(r_pos, r_pos, color=PALETTE[0], lw=2.4)
ax.plot(r_neg, r_neg, color=PALETTE[1], lw=2.0, ls="--")

# Bifurcation point at origin.
ax.plot(0, 0, "o", color=PALETTE[3], ms=9, zorder=5)
ax.annotate("transcritical bifurcation\n(e.g., the $R_0=1$ epidemic threshold)",
            xy=(0, 0), xytext=(-0.95, 0.55), fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#26323f"))

print("branches exchange stability at r=0; equilibria x*=0 and x*=r")

ax.set_xlabel("parameter $r$")
ax.set_ylabel("equilibrium $x^*$")
ax.set_title(r"Transcritical bifurcation: $\dot{x}=rx-x^2$")
ax.legend(loc="lower right", fontsize=9)

save(fig, "assets/figures/transcritical-bifurcation.svg")
