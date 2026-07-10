# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Final epidemic size, herd immunity threshold, and overshoot."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# LEFT: final size Z(R0), herd immunity threshold, and overshoot
r0 = np.linspace(1.01, 4.0, 300)


def final_size(rr):
    return brentq(lambda z: 1.0 - np.exp(-rr * z) - z, 1e-9, 1 - 1e-9)


Z = np.array([final_size(rr) for rr in r0])
H = 1.0 - 1.0 / r0

axL.fill_between(r0, H, Z, color=PALETTE[1], alpha=0.15)
axL.plot(r0, Z, color=PALETTE[1], lw=2.0, label="final size Z(∞)")
axL.plot(r0, H, color=PALETTE[0], lw=2.0,
         label="herd immunity threshold 1 − 1/R0")
axL.annotate("overshoot", xy=(2.5, 0.5 * (final_size(2.5) + (1 - 1 / 2.5))),
             xytext=(2.7, 0.42), fontsize=9, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axL.set_xlim(1.0, 4.0)
axL.set_ylim(0, 1.0)
axL.set_xlabel("basic reproduction number R0")
axL.set_ylabel("fraction of population")
axL.legend(loc="lower right", fontsize=8)

# RIGHT: SIR time course with overshoot past the threshold
R0 = 2.5
gamma = 1.0
beta = R0 * gamma
I0 = 1e-3


def sir(t, y):
    S, I, R = y
    return [-beta * S * I, beta * S * I - gamma * I, gamma * I]


sol = solve_ivp(sir, (0, 20), [1 - I0, I0, 0.0],
                dense_output=True, rtol=1e-8, atol=1e-10)
t = np.linspace(0, 20, 400)
S, I, R = sol.sol(t)

thresh = 1.0 / R0
Sinf = S[-1]

axR.plot(t, S, color=PALETTE[0], lw=2.0, label="S(t)")
axR.plot(t, I, color=PALETTE[1], lw=2.0, label="I(t)")
axR.plot(t, R, color=PALETTE[2], lw=2.0, label="R(t)")
axR.axhline(thresh, ls="--", color=MUTED, lw=1.0,
            label="herd immunity threshold S = 1/R0")
axR.axhline(Sinf, ls=":", color=INK, lw=1.0)

axR.annotate("", xy=(18, Sinf), xytext=(18, thresh),
             arrowprops=dict(arrowstyle="<->", color=INK, lw=0.9))
axR.annotate("overshoot:\nS(∞) falls past 1/R0", xy=(18, 0.5 * (Sinf + thresh)),
             xytext=(9.5, 0.55), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
tpeak = t[np.argmax(I)]
axR.annotate("I peaks when S = 1/R0", xy=(tpeak, thresh),
             xytext=(tpeak + 1.0, 0.78), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axR.set_xlim(0, 20)
axR.set_ylim(0, 1.0)
axR.set_xlabel("time (1/gamma units)")
axR.set_ylabel("fraction of population")
axR.legend(loc="center right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/final-size-and-herd-immunity.svg")
