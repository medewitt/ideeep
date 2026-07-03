# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""The covariance view of the inflationary effect in a metapopulation.

A seasonally forced SIR metapopulation with the local epidemics out of phase
across patches, coupled by movement of infectious hosts. We track the local
per-capita growth rate of cases r_i(t) = beta_i(t) S_i/N - gamma (the log
change in cases), and decompose the growth of total regional prevalence using
the Price-equation identity

    (1/Ibar) dIbar/dt = mean_i r_i(t) + cov_i( r_i(t), nu_i(t) ),   nu_i = I_i/Ibar,

so the spatial covariance between local growth and local relative prevalence is
the instantaneous inflationary contribution (Kortessis et al. 2025, eq. 4). We
also show Roy, Holt & Barfield's (2005, eq. 2) temporal covariance cov_t(r_i,I_i)
per patch, and the ANOVA-style space/time/spatiotemporal variance decomposition
of r (Kortessis et al. 2025, box 1)."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# ---- model ----
n = 4                       # patches
N = 1.0                     # each patch normalized to unit population
gamma = 26.0                # recovery rate (~2-week infectious period), per year
mu = 1 / 50.0               # birth/death rate, per year
R0 = 8.0 * (1 + 0.12 * np.linspace(-1, 1, n))           # mild spatial heterogeneity in R0
beta0 = R0 * (gamma + mu)
delta = 0.12 * (1 + 0.5 * np.cos(np.linspace(0, np.pi, n)))   # and in seasonal amplitude
m = 2.0                     # movement (mixing) rate of infectious hosts, per year
phases = np.linspace(0, 2 * np.pi, n, endpoint=False)   # staggered seasonal phase


def beta(t):
    return beta0 * (1 + delta * np.cos(2 * np.pi * t + phases))


def rhs(t, y):
    S, I, _R = y[:n], y[n:2 * n], y[2 * n:]
    b = beta(t)
    infection = b * S * I / N
    move = m * (I.mean() - I)             # diffusive coupling of infectives (conserves total)
    dS = mu * N - infection - mu * S
    dI = infection - gamma * I - mu * I + move
    dR = gamma * I - mu * _R
    return np.concatenate([dS, dI, dR])


# initial conditions: endemic-ish, seeded slightly differently per patch
S0 = np.full(n, 1 / R0)
I0 = 1e-3 * (1 + 0.2 * np.cos(phases))
y0 = np.concatenate([S0, I0, N - S0 - I0])

t_end = 60.0
sol = solve_ivp(rhs, (0, t_end), y0, t_eval=np.linspace(0, t_end, 12000),
                rtol=1e-9, atol=1e-12, method="LSODA")

burn = sol.t >= (t_end - 12)          # analyse the last 12 years (post-transient)
t = sol.t[burn]
S = sol.y[:n, burn]
I = sol.y[n:2 * n, burn]

beta_mat = beta0[:, None] * (1 + delta[:, None] * np.cos(2 * np.pi * t[None, :] + phases[:, None]))
r = beta_mat * S / N - gamma          # per-capita growth rate of cases, patch x time
Ibar = I.mean(axis=0)
nu = I / Ibar                          # relative prevalence
rbar = r.mean(axis=0)
cov_space = (r * nu).mean(axis=0) - rbar          # cov_i(r_i, nu_i) at each time
metapop_growth = rbar + cov_space                 # = (1/Ibar) dIbar/dt

# temporal covariance per patch (Roy et al. eq. 2), cov_t(r_i, I_i)
cov_time = np.array([np.cov(r[i], I[i])[0, 1] for i in range(n)])

# box 1 variance decomposition of r(x,t)
r_tilde = r.mean(axis=1)               # time-average per patch  -> spatial pattern
r_bar_t = r.mean(axis=0)               # space-average per time  -> temporal pattern
var_S = r_tilde.var()                                  # pure spatial variance
var_T = r_bar_t.var()                                  # pure temporal variance
var_ST = r.var(axis=0).mean() - r_tilde.var()          # spatiotemporal (interaction)

# inflationary effect (eq. 4): E_t[cov_space] minus reference (growth fixed at time means)
Aref = np.diag(r_tilde) + (m / n) * (np.ones((n, n)) - n * np.eye(n)) / 1.0
# reference relative density = leading eigenvector of constant-growth+movement operator
w, V = np.linalg.eig(Aref)
lead = V[:, np.argmax(w.real)].real
nu_ref = lead / lead.mean()
cov_ref = ((r_tilde * nu_ref).mean() - r_tilde.mean())
infl_effect = cov_space.mean() - cov_ref

# ---- figure ----
fig, axes = plt.subplots(2, 2, figsize=(11.4, 7.0))
tt = t - t[0]

win = tt >= (tt.max() - 6)   # show the last 6 years for legibility

# A: local growth rate r_i(t) for all patches
axA = axes[0, 0]
for i in range(n):
    axA.plot(tt[win], r[i][win], color=PALETTE[i % len(PALETTE)], lw=1.0, label=f"patch {i+1}")
axA.plot(tt[win], rbar[win], color=INK, lw=1.8, ls="--", label="spatial mean")
axA.axhline(0, color=MUTED, lw=0.8)
axA.set_title("A. Local growth rate of cases  $r_i(t)=\\beta_i(t)S_i/N-\\gamma$", fontsize=10)
axA.set_xlabel("year"); axA.set_ylabel("$r_i$  (log change in cases / yr)")
axA.legend(fontsize=7.5, ncol=3, loc="lower center")

# B: covariance in space over time (the instantaneous inflation)
axB = axes[0, 1]
axB.fill_between(tt[win], cov_space[win], color=PALETTE[2], alpha=0.35)
axB.plot(tt[win], cov_space[win], color=PALETTE[2], lw=1.4)
axB.axhline(0, color=MUTED, lw=0.8)
axB.axhline(cov_space.mean(), color=PALETTE[1], lw=1.4, ls="--",
            label=f"time mean = {cov_space.mean():.2f} > 0")
axB.set_title("B. Covariance in space  $\\mathrm{cov}_i\\,(r_i(t),\\,\\nu_i(t))$", fontsize=10)
axB.set_xlabel("year"); axB.set_ylabel("spatial covariance")
axB.set_ylim(0, None)
axB.legend(fontsize=8, loc="lower right")

# C: covariance in time, per patch (Roy et al. eq. 2)
axC = axes[1, 0]
axC.bar(np.arange(1, n + 1), cov_time, color=PALETTE[0], alpha=0.85)
axC.axhline(0, color=MUTED, lw=0.8)
axC.set_title("C. Covariance in time  $\\mathrm{cov}_t\\,(r_i,\\,I_i)$  per patch", fontsize=10)
axC.set_xlabel("patch"); axC.set_ylabel("temporal covariance")
axC.set_xticks(np.arange(1, n + 1))

# D: variance decomposition + inflationary effect
axD = axes[1, 1]
labels = ["$\\sigma^2_S$\n(space)", "$\\sigma^2_T$\n(time)", "$\\sigma^2_{ST}$\n(spatio-\ntemporal)"]
vals = [var_S, var_T, var_ST]
bars = axD.bar(labels, vals, color=[PALETTE[3], PALETTE[4], PALETTE[2]], alpha=0.85)
axD.set_title(f"D. Variance of $r$ (box 1) — inflationary effect (eq. 4) = {infl_effect:.2f}",
              fontsize=10)
axD.set_ylabel("variance of $r$")
for b, v in zip(bars, vals):
    axD.text(b.get_x() + b.get_width() / 2, v, f"{v:.2f}", ha="center", va="bottom", fontsize=9)

fig.suptitle("The inflationary effect as a growth-rate covariance in a metapopulation",
             fontweight="bold")
fig.tight_layout()
save(fig, "assets/figures/inflation-covariance.svg")

# console check (not shown on the page)
print("mean metapop growth check: max|rbar+cov - (1/Ibar)dIbar/dt| computed via finite diff")
dIbar = np.gradient(Ibar, t)
print("  max abs diff:", float(np.max(np.abs(metapop_growth - dIbar / Ibar))))
print("infl effect (E_t cov_space - reference):", round(float(infl_effect), 4))
print("mean cov_space:", round(float(cov_space.mean()), 4), " cov_ref:", round(float(cov_ref), 4))
