# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""SEIR epidemic model integrated over time."""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

N = 1000.0
beta, sigma, gamma = 0.6, 1 / 3, 1 / 5
I0 = 1.0
R0 = beta / gamma
print(f"SEIR: R0 = beta/gamma = {R0:.2f}")


def rhs(t, y):
    S, E, I, R = y
    inf = beta * S * I / N
    return [-inf, inf - sigma * E, sigma * E - gamma * I, gamma * I]


y0 = [N - I0, 0.0, I0, 0.0]
t = np.linspace(0, 120, 1200)
sol = solve_ivp(rhs, [0, 120], y0, t_eval=t, rtol=1e-8, atol=1e-8)
S, E, I, R = sol.y

fig, ax = plt.subplots()
ax.plot(t, S, color=PALETTE[0], lw=2, label="Susceptible")
ax.plot(t, E, color=PALETTE[4], lw=2, label="Exposed")
ax.plot(t, I, color=PALETTE[1], lw=2, label="Infectious")
ax.plot(t, R, color=PALETTE[2], lw=2, label="Recovered")

# Annotate epidemic peak.
ipk = int(np.argmax(I))
ax.plot(t[ipk], I[ipk], "o", color=PALETTE[1], ms=7)
ax.annotate(f"peak I = {I[ipk]:.0f}\nat t = {t[ipk]:.0f} d",
            xy=(t[ipk], I[ipk]), xytext=(t[ipk] + 12, I[ipk] + 60),
            arrowprops=dict(arrowstyle="->", color="#26323f"), fontsize=9)
print(f"peak infectious {I[ipk]:.1f} at t={t[ipk]:.1f}; final R={R[-1]:.1f}")

ax.set_xlabel("time (days)")
ax.set_ylabel("individuals")
ax.set_title(f"SEIR model ($R_0={R0:.1f}$)")
ax.legend(loc="center right", fontsize=9)

save(fig, "assets/figures/seir-curve.svg")
