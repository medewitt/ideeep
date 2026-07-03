# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Why biologists meet imaginary numbers: a complex eigenvalue a + bi turns
into a (here damped) oscillation, e^{at} cos(bt) — the math behind population
cycles."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

a, b = -0.15, 1.0                 # eigenvalue lambda = a + b*i
t = np.linspace(0, 30, 600)
signal = np.exp(a * t) * np.cos(b * t)     # real part of e^{lambda t}
period = 2 * np.pi / b

print(f"eigenvalue lambda = {a} + {b}i")
print(f"decay rate (real part) a = {a}  -> a < 0 means the cycle damps out")
print(f"angular frequency (imag part) b = {b}  -> period = 2*pi/b = {period:.2f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.6))

# Left: the complex plane
ax1.axhline(0, color="#c0c8cf", lw=0.8)
ax1.axvline(0, color="#c0c8cf", lw=0.8)
ax1.scatter([a], [b], color=PALETTE[1], zorder=5, s=45)
ax1.annotate(rf"$\lambda = {a} + {b}i$", (a, b),
             textcoords="offset points", xytext=(8, 6), fontsize=10)
ax1.set_xlim(-1, 1)
ax1.set_ylim(-1.6, 1.6)
ax1.set_xlabel("real part  (growth / decay)")
ax1.set_ylabel("imaginary part  (frequency)")
ax1.set_title("A complex eigenvalue")

# Right: the resulting oscillation
ax2.plot(t, signal, color=PALETTE[0], label=r"$\mathrm{Re}(e^{\lambda t})=e^{at}\cos(bt)$")
ax2.plot(t, np.exp(a * t), color=PALETTE[1], ls="--", lw=1, label=r"envelope $e^{at}$")
ax2.plot(t, -np.exp(a * t), color=PALETTE[1], ls="--", lw=1)
ax2.axhline(0, color="#c0c8cf", lw=0.8)
ax2.set_xlabel("time")
ax2.set_ylabel("state")
ax2.set_title("...is a damped oscillation")
ax2.legend(loc="upper right", fontsize=9)
save(fig, "assets/figures/complex-oscillation.svg")
