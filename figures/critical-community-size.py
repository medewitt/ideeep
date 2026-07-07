# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Critical community size, stochastic fade-out, and epidemic burnout.

Three panels from a discrete-time stochastic SIR with vital dynamics
(demographic stochasticity via Poisson/binomial event draws):
(a) fraction of time with zero cases versus population size, with the
    critical community size band marked;
(b) one small-population run that fades out in the post-epidemic trough
    versus one large-population run that persists;
(c) probability that the first major epidemic burns out (goes extinct)
    rather than settling to endemicity, as a function of R0.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

GAMMA = 1 / 13.0          # recovery rate (13-day infectious period)


def step(S, I, R, N, beta, gamma, mu, rng):
    """One-day tau-leap update of the stochastic SIR with demography."""
    lam = beta * I / N
    ninf = rng.binomial(S.astype(int), 1 - np.exp(-lam))
    nrec = rng.binomial(I.astype(int), 1 - np.exp(-gamma))
    births = rng.poisson(mu * N, S.shape)
    pd = 1 - np.exp(-mu)
    dS = rng.binomial(S.astype(int), pd)
    dI = rng.binomial(I.astype(int), pd)
    dR = rng.binomial(R.astype(int), pd)
    S = np.maximum(S - ninf + births - dS, 0)
    I = np.maximum(I + ninf - nrec - dI, 0)
    R = np.maximum(R + nrec - dR, 0)
    return S, I, R


def run_endemic(N, beta, gamma, mu, days, n_runs, rng, burn=2 * 365):
    """Seed near the endemic equilibrium; track trough fade-out."""
    R0 = beta / gamma
    Istar = max(1, int(round(mu * N * (1 - 1 / R0) / (gamma + mu))))
    S = np.full(n_runs, int(round(N / R0)), dtype=float)
    I = np.full(n_runs, Istar, dtype=float)
    R = np.full(n_runs, N, dtype=float) - S - I
    zero_days = np.zeros(n_runs)
    trace = np.zeros((days, n_runs))
    for t in range(days):
        S, I, R = step(S, I, R, N, beta, gamma, mu, rng)
        trace[t] = I
        if t >= burn:
            zero_days += I == 0
    return zero_days / (days - burn), trace


def run_burnout(N, R0, gamma, mu, days, n_runs, rng):
    """Single introduction; among take-offs, did infection go extinct?"""
    beta = R0 * gamma
    S = np.full(n_runs, N - 1, dtype=float)
    I = np.ones(n_runs)
    R = np.zeros(n_runs)
    thr = max(50.0, 5e-4 * N)
    reached = np.zeros(n_runs, bool)
    zero_after = np.zeros(n_runs, bool)
    for _ in range(days):
        S, I, R = step(S, I, R, N, beta, gamma, mu, rng)
        reached |= I >= thr
        zero_after |= reached & (I == 0)
    return reached, zero_after & reached


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11.6, 3.7))

# ---- Panel (a): fade-out frequency vs population size (measles demography).
rng = np.random.default_rng(1834)
beta = 15 * GAMMA                      # R0 = 15
mu = 1 / (50 * 365)                    # ~50-year host lifespan
Ns = np.array([2e3, 5e3, 1e4, 3e4, 7e4, 1.5e5,
               2.5e5, 4e5, 7e5, 1.2e6], dtype=int)
frac_zero = np.array([run_endemic(N, beta, GAMMA, mu, 20 * 365, 25, rng)[0].mean()
                      for N in Ns])
ax1.axvspan(2.5e5, 3.0e5, color=PALETTE[1], alpha=0.15)
ax1.plot(Ns, frac_zero, "o-", color=PALETTE[0], lw=2)
ax1.set_xscale("log")
ax1.set_xlabel("population size $N$")
ax1.set_ylabel("fraction of time with zero cases")
ax1.set_title("(a) stochastic fade-out")
ax1.text(2.7e5, 0.86, "measles CCS\n$\\approx$ 250–300k", color=PALETTE[1],
         ha="center", fontsize=8)

# ---- Panel (b): one small vs one large run.
rng = np.random.default_rng(7)
_, tr_small = run_endemic(50_000, beta, GAMMA, mu, 12 * 365, 1, rng)
_, tr_large = run_endemic(500_000, beta, GAMMA, mu, 12 * 365, 1, rng)
yrs = np.arange(12 * 365) / 365.0
ax2.plot(yrs, tr_large[:, 0], color=PALETTE[0], lw=1.2,
         label="$N=5\\times10^5$ (persists)")
ax2.plot(yrs, tr_small[:, 0], color=PALETTE[1], lw=1.2,
         label="$N=5\\times10^4$ (fades out)")
fade = np.argmax(tr_small[:, 0] == 0)
if tr_small[fade, 0] == 0:
    ax2.plot(yrs[fade], 0, "v", color=PALETTE[1], ms=9)
    ax2.text(yrs[fade], 40, "fade-out", color=PALETTE[1], fontsize=8, ha="center")
ax2.set_xlabel("time (years)")
ax2.set_ylabel("infectious individuals $I$")
ax2.set_title("(b) trough that empties vs persists")
ax2.legend(loc="upper right", fontsize=8)

# ---- Panel (c): burnout probability vs R0 (faster-turnover host).
rng = np.random.default_rng(1834)
mu_c = 1 / (8 * 365)                   # 8-year lifespan: comparable timescales
R0s = np.array([2, 3, 4, 6, 8, 10, 12, 14, 16, 20])
pb = []
for R0 in R0s:
    to, bo = run_burnout(2_000_000, R0, GAMMA, mu_c, 15 * 365, 200, rng)
    pb.append(bo.sum() / max(to.sum(), 1))
ax3.plot(R0s, pb, "o-", color=PALETTE[3], lw=2)
ax3.set_xlabel("basic reproduction number $R_0$")
ax3.set_ylabel("P(burnout | major epidemic)")
ax3.set_title("(c) epidemic burnout")
ax3.set_ylim(-0.03, 1.03)
ax3.text(11, 0.75, "more transmissible\n$\\Rightarrow$ persists", color=MUTED,
         fontsize=8, ha="center")

fig.tight_layout()
save(fig, "assets/figures/critical-community-size.svg")
