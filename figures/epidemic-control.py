# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Speed and strength of epidemic control: controllability, peaks, timing."""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
np.random.seed(1834)

fig, (axa, axb, axc) = plt.subplots(1, 3, figsize=(11.4, 3.7))

# --- Panel (a): Fraser controllability region ------------------------------
theta = np.linspace(0.001, 0.99, 400)
R0_boundary = 1.0 / theta                              # boundary R0 = 1/theta
axa.plot(theta, R0_boundary, color=PALETTE[1], lw=2.2)
axa.fill_between(theta, 1, R0_boundary, color=PALETTE[2], alpha=0.20)
axa.fill_between(theta, R0_boundary, 10, color=PALETTE[1], alpha=0.12)
axa.set_ylim(1, 10)
axa.set_xlim(0, 1)
axa.text(0.12, 2.4, "controllable by\nsymptom isolation", fontsize=8,
         color=INK)
axa.text(0.55, 7.2, "not controllable\n(too much pre-symptomatic\ntransmission)",
         fontsize=8, color=INK)
for name, R0, th in [("SARS-CoV-1", 2.5, 0.11),
                     ("SARS-CoV-2", 2.5, 0.50)]:
    axa.plot(th, R0, "o", color=INK, ms=6)
    axa.annotate(name, xy=(th, R0), xytext=(th + 0.03, R0 + 0.5),
                 fontsize=7.5, color=INK)
axa.set_title("(a) Fraser controllability")
axa.set_xlabel(r"pre-symptomatic fraction $\theta$")
axa.set_ylabel("$R_0$")

# --- Panel (b): speed vs strength, same final size, different peak ---------
N = 1.0
R0 = 1.8


def sir(gamma, beta):
    def rhs(t, y):
        S, I, R = y
        inf = beta * S * I
        return [-inf, inf - gamma * I, gamma * I]
    t = np.linspace(0, 300, 3000)
    sol = solve_ivp(rhs, [0, 300], [N - 1e-4, 1e-4, 0.0],
                    t_eval=t, rtol=1e-8, atol=1e-10)
    return t, sol.y


for gamma, col, lab in [(1 / 3, PALETTE[1], "fast (short interval)"),
                        (1 / 10, PALETTE[0], "slow (long interval)")]:
    t, (S, I, R) = sir(gamma, R0 * gamma)
    axb.plot(t, I, color=col, lw=2,
             label=f"{lab}, final size {R[-1]:.2f}")
axb.set_title(f"(b) same $R_0={R0}$, different speed")
axb.set_xlabel("time (days)")
axb.set_ylabel("prevalence $I$")
axb.legend(fontsize=7.5, loc="upper right")

# --- Panel (c): reactive vs proactive control on a fast outbreak ----------
R0f, gamma_f = 2.5, 1 / 4
beta0 = R0f * gamma_f
trigger = 0.02                                        # cumulative-incidence trigger
control_factor = 0.45                                 # beta multiplier once active


def sir_controlled(mode):
    def rhs(t, y):
        S, I, R = y
        cum = 1.0 - S                                 # cumulative incidence
        if mode == "proactive":
            beta = beta0 * control_factor
        elif mode == "reactive" and cum >= trigger:
            beta = beta0 * control_factor
        else:
            beta = beta0
        inf = beta * S * I
        return [-inf, inf - gamma_f * I, gamma_f * I]
    t = np.linspace(0, 160, 2000)
    sol = solve_ivp(rhs, [0, 160], [N - 1e-4, 1e-4, 0.0],
                    t_eval=t, rtol=1e-8, atol=1e-10)
    return t, sol.y


for mode, col in [("none", MUTED), ("reactive", PALETTE[1]),
                  ("proactive", PALETTE[2])]:
    t, (S, I, R) = sir_controlled(mode)
    axc.plot(t, I, color=col, lw=2,
             label=f"{mode} (final {R[-1]:.2f})")
axc.set_title("(c) reactive vs proactive")
axc.set_xlabel("time (days)")
axc.set_ylabel("prevalence $I$")
axc.legend(fontsize=7.5, loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/epidemic-control.svg")
