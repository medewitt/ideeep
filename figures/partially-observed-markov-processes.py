# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Fitting a mechanistic POMP: a noisily observed stochastic SIR, and the
particle-filter log-likelihood profile that locates the transmission rate."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gammaln, logsumexp
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

N = 50_000          # population
gamma = 1.0         # weekly recovery rate
rho = 0.4           # reporting probability
n_weeks = 30
beta_true = 1.5     # weekly transmission rate (R0 = beta/gamma = 1.5)


def simulate(beta, rng):
    """One realization of the stochastic SIR process; returns true weekly
    incidence and its binomially under-reported case counts."""
    S, I = N - 20, 20
    inc = np.zeros(n_weeks)
    for k in range(n_weeks):
        new_inf = rng.binomial(S, 1.0 - np.exp(-beta * I / N))
        new_rec = rng.binomial(I, 1.0 - np.exp(-gamma))
        S -= new_inf
        I += new_inf - new_rec
        inc[k] = new_inf
    reports = rng.binomial(inc.astype(int), rho)
    return inc, reports


def pf_loglik(beta, reports, rng, n_part=1500):
    """Bootstrap particle filter: unbiased estimate of the log-likelihood of
    the reported series under transmission rate beta."""
    S = np.full(n_part, N - 20, dtype=float)
    I = np.full(n_part, 20, dtype=float)
    loglik = 0.0
    for k in range(n_weeks):
        new_inf = rng.binomial(S.astype(int), 1.0 - np.exp(-beta * I / N))
        new_rec = rng.binomial(I.astype(int), 1.0 - np.exp(-gamma))
        S = S - new_inf
        I = I + new_inf - new_rec
        obs = reports[k]
        # observation density: reports ~ Binomial(new_inf, rho), in log space.
        with np.errstate(divide="ignore", invalid="ignore"):
            logw = np.where(
                new_inf >= obs,
                obs * np.log(rho) + (new_inf - obs) * np.log(1 - rho)
                + gammaln(new_inf + 1) - gammaln(obs + 1)
                - gammaln(new_inf - obs + 1),
                -np.inf,
            )
        total = logsumexp(logw)
        if not np.isfinite(total):     # filter collapse: beta effectively ruled out
            return -np.inf
        loglik += total - np.log(n_part)
        w = np.exp(logw - total)
        idx = rng.choice(n_part, size=n_part, p=w)
        S, I = S[idx], I[idx]
    return loglik


rng = np.random.default_rng(20260712)
inc, reports = simulate(beta_true, rng)

# Profile the particle-filter log-likelihood over a grid of beta, averaging a
# few filter replicates per grid point to smooth the Monte-Carlo noise.
betas = np.linspace(1.35, 1.68, 15)
ll = np.array([
    np.mean([pf_loglik(b, reports, np.random.default_rng(1000 + j * 7 + r))
             for r in range(4)])
    for j, b in enumerate(betas)
])
mle = betas[np.argmax(ll)]

fig, (axl, axr) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# ---- Left: the mechanistic process and its noisy shadow.
weeks = np.arange(1, n_weeks + 1)
axl.plot(weeks, inc, color=PALETTE[1], lw=2, label="true incidence")
axl.bar(weeks, reports, color=PALETTE[0], alpha=0.55, width=0.7,
        label="reported cases")
axl.set_xlabel("week")
axl.set_ylabel("new infections")
axl.set_title("process + observation", fontsize=10)
axl.annotate("only a fraction $\\rho$ of\ninfections are reported",
             xy=(weeks[np.argmax(inc)], inc.max()),
             xytext=(1.5, inc.max() * 0.62), fontsize=7, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axl.legend(loc="upper right", fontsize=8)

# ---- Right: particle-filter log-likelihood profile locating beta.
axr.plot(betas, ll, color=PALETTE[0], lw=2, marker="o", ms=3)
axr.axvline(beta_true, color=INK, ls=":", lw=1.2, label=f"truth = {beta_true}")
axr.axvline(mle, color=PALETTE[2], ls="--", lw=1.4,
            label=f"MLE $\\approx$ {mle:.2f}")
axr.set_xlabel(r"transmission rate $\beta$")
axr.set_ylabel("particle-filter log-likelihood")
axr.set_title("likelihood slice", fontsize=10)
axr.legend(loc="lower center", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/partially-observed-markov-processes.svg")
