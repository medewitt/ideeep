# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""The three-term continuous-time Price equation in a two-strain epidemic.

We simulate the Day, Parsons, Lambert & Gandon (2020) evolutionary-epidemiology
model: two pathogen strains differing in virulence v (the rate at which an
infection ends) and, through a transmission-virulence trade-off, in transmission
rate beta. Strains mutate on transmission (probability tau) and compete within
hosts via superinfection (rate sigma, the more virulent strain winning).

Tracking mean virulence vbar across the infected population, its change obeys

    dvbar/dt = cov[v, r] + E[b*dv] + E[dv^s/dt],   r_i = beta_i S - (mu + v_i),

i.e. SELECTION (net between-host spread), MUTATION on transmission, and
WITHIN-HOST change. Each term depends on S and I, so evolution and the epidemic
feed back on one another -- and short-term selection can run opposite to the
long-term direction."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# ---- two strains on a transmission-virulence trade-off  beta = a*sqrt(v) ----
mu = 0.02
a = 6.0
v1, v2 = 0.80, 0.40                 # strain 1 more virulent, strain 2 less
beta1, beta2 = a * np.sqrt(v1), a * np.sqrt(v2)
tau1 = tau2 = 0.01                  # mutation probability on transmission
sigma = 0.6                         # superinfection efficacy
rho12, rho21 = 1.0, 0.0             # the MORE virulent strain (1) wins within-host


def h_of(I1, I2):
    h1 = beta1 * I1 * (1 - tau1) + beta2 * I2 * tau2      # rate type-1 propagules generated
    h2 = beta2 * I2 * (1 - tau2) + beta1 * I1 * tau1
    return h1, h2


def rhs(t, y):
    S, I1, I2 = y
    h1, h2 = h_of(I1, I2)
    dS = mu * (1 - S) - (beta1 * I1 + beta2 * I2) * S
    dI1 = h1 * S - (mu + v1) * I1 + sigma * h1 * I2 * rho12 - sigma * h2 * I1 * rho21
    dI2 = h2 * S - (mu + v2) * I2 + sigma * h2 * I1 * rho21 - sigma * h1 * I2 * rho12
    return [dS, dI1, dI2]


y0 = [0.99, 5e-3, 5e-3]
t_end = 300.0
sol = solve_ivp(rhs, (0, t_end), y0, t_eval=np.linspace(0, t_end, 6000),
                rtol=1e-10, atol=1e-13, method="LSODA")
t, S, I1, I2 = sol.t, sol.y[0], sol.y[1], sol.y[2]
I = I1 + I2
p = I1 / I                                        # frequency of strain 1
vbar = p * v1 + (1 - p) * v2                       # mean virulence

# ---- the three Price terms (trait = virulence) ----
b1, b2 = beta1 * S, beta2 * S
r1, r2 = b1 - (mu + v1), b2 - (mu + v2)
h1, h2 = h_of(I1, I2)
T_sel = p * (1 - p) * (v1 - v2) * (r1 - r2)                                  # cov[v, r]
T_mut = p * b1 * tau1 * (v2 - v1) + (1 - p) * b2 * tau2 * (v1 - v2)          # E[b dv]
T_wh = (v1 - v2) * (sigma * h1 * (1 - p) * rho12 - sigma * h2 * p * rho21)   # E[dv^s/dt]
T_sum = T_sel + T_mut + T_wh
dvbar_fd = np.gradient(vbar, t)                    # finite-difference truth

fig, axes = plt.subplots(2, 2, figsize=(11.6, 7.2))

# A: epidemic dynamics
axA = axes[0, 0]
axA.plot(t, S, color=PALETTE[4], lw=1.8, label="$S$ (susceptible)")
axA.plot(t, I1, color=PALETTE[1], lw=1.8, label="$I_1$ (virulent)")
axA.plot(t, I2, color=PALETTE[2], lw=1.8, label="$I_2$ (mild)")
axA.set_title("A. Epidemic then endemic", fontsize=10.5)
axA.set_xlabel("time"); axA.set_ylabel("density")
axA.legend(fontsize=8, loc="center right")

# B: mean virulence + frequency (transient vs long term)
axB = axes[0, 1]
axB.plot(t, vbar, color=INK, lw=2.0)
axB.axhline(v1, color=PALETTE[1], lw=0.8, ls=":"); axB.axhline(v2, color=PALETTE[2], lw=0.8, ls=":")
imax = np.argmax(vbar)
axB.scatter([t[imax]], [vbar[imax]], color=PALETTE[1], zorder=5)
axB.annotate("transient peak\n(more virulent)", xy=(t[imax], vbar[imax]),
             xytext=(t[imax] + 40, vbar[imax] - 0.02), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axB.annotate("long-term\n(milder wins)", xy=(t[-1], vbar[-1]),
             xytext=(t[-1] - 120, v2 + 0.06), fontsize=8, color=PALETTE[2],
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axB.set_title("B. Mean virulence $\\bar v(t)$: transient $\\neq$ long term", fontsize=10.5)
axB.set_xlabel("time"); axB.set_ylabel("mean virulence  $\\bar v$")

# C: the three terms and their sum vs the truth
axC = axes[1, 0]
axC.axhline(0, color=MUTED, lw=0.8)
axC.plot(t, T_sel, color=PALETTE[0], lw=1.6, label="selection  $\\mathrm{cov}[v,r]$")
axC.plot(t, T_mut * 50, color=PALETTE[3], lw=1.4, label="mutation  $\\mathbb{E}[b\\Delta v]\\times 50$")
axC.plot(t, T_wh, color=PALETTE[4], lw=1.4, label="within-host  $\\mathbb{E}[\\dot v^{\\,s}]$")
axC.plot(t, T_sum, color=INK, lw=2.4, alpha=0.35, label="sum of three")
axC.plot(t, dvbar_fd, color="black", lw=0.9, ls="--", label="$d\\bar v/dt$ (numeric)")
axC.set_xlim(0, 120)
axC.set_title("C. Three terms sum exactly to $d\\bar v/dt$", fontsize=10.5)
axC.set_xlabel("time"); axC.set_ylabel("contribution to $d\\bar v/dt$")
axC.legend(fontsize=7.5, loc="upper right")

# D: eco-evolutionary feedback -- selection sign follows S
axD = axes[1, 1]
sel_coef = (beta1 - beta2) * S - (v1 - v2)          # r1 - r2
axD.axhline(0, color=MUTED, lw=0.9)
axD.plot(t, sel_coef, color=PALETTE[0], lw=1.8, label="$r_1-r_2=(\\beta_1-\\beta_2)S-(v_1-v_2)$")
Scross = (v1 - v2) / (beta1 - beta2)
axD.fill_between(t, 0, sel_coef, where=(sel_coef > 0), color=PALETTE[1], alpha=0.18)
axD.fill_between(t, 0, sel_coef, where=(sel_coef < 0), color=PALETTE[2], alpha=0.18)
axD.set_xlim(0, 120)
axD.set_title(f"D. Epi-evolutionary feedback: sign flips as $S$ falls past {Scross:.2f}",
              fontsize=10.5)
axD.set_xlabel("time"); axD.set_ylabel("selection on virulence")
axD.legend(fontsize=7.5, loc="upper right")
axDt = axD.twinx()
axDt.plot(t, S, color=PALETTE[4], lw=1.2, ls=":")
axDt.set_ylabel("$S$", color=PALETTE[4])
axDt.tick_params(axis="y", labelcolor=PALETTE[4])
axDt.grid(False)

fig.suptitle("A two-strain epidemic through the lens of Price's equation "
             "(Day et al. 2020)", fontweight="bold")
fig.tight_layout()
save(fig, "assets/figures/price-sir-three-terms.svg")

# console check: the three terms reconstruct dvbar/dt
interior = (t > 1) & (t < t_end - 1)
err = np.max(np.abs(T_sum[interior] - dvbar_fd[interior]))
print("max |sum of three terms - dvbar/dt| =", float(err))
print("peak mean virulence:", round(float(vbar.max()), 4), "at t =", round(float(t[np.argmax(vbar)]), 1))
print("final mean virulence:", round(float(vbar[-1]), 4), " (v2 =", v2, ")")
