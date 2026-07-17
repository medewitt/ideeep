# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Time-varying transmission as a POMP: log R_t is a latent random walk, and a
particle filter recovers its trajectory from noisily reported incidence."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
from scipy.special import logsumexp
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

n_weeks, rho = 40, 0.6
w = np.array([0.30, 0.40, 0.20, 0.10])      # generation-interval weights
L = len(w)

# True time-varying reproduction number: 1.6 -> 0.7 (control) -> 1.15 (rebound).
t = np.arange(n_weeks)
R_true = np.where(t < 14, 1.6, np.where(t < 26, 0.7, 1.15))

# Simulate latent incidence via the renewal equation, then under-report it.
rng = np.random.default_rng(3)
I = np.zeros(n_weeks)
I[:L] = [20, 25, 30, 35]
for k in range(L, n_weeks):
    lam = R_true[k] * np.sum(w * I[k - L:k][::-1])
    I[k] = rng.poisson(lam)
reports = rng.binomial(I.astype(int), rho)


def filt(n_part=6000, sigma=0.15, seed=4):
    """Particle filter tracking (recent incidence, log R_t) with a Gaussian
    random walk on log R_t; returns the filtered R_t mean and 90% band."""
    r = np.random.default_rng(seed)
    logR = r.normal(np.log(1.5), 0.3, n_part)
    Ihist = np.tile(I[:L], (n_part, 1)).astype(float)
    est = np.array(R_true, dtype=float)
    lo = np.array(R_true, dtype=float)
    hi = np.array(R_true, dtype=float)
    for k in range(L, n_weeks):
        logR = logR + r.normal(0, sigma, n_part)
        lam = np.exp(logR) * (Ihist[:, ::-1] * w).sum(1)
        Ik = r.poisson(np.maximum(lam, 1e-6))
        logw = binom.logpmf(reports[k], Ik, rho)
        wt = np.exp(logw - logsumexp(logw))
        est[k] = np.sum(wt * np.exp(logR))
        idx = r.choice(n_part, n_part, p=wt)
        logR = logR[idx]
        Ihist = np.column_stack([Ihist[idx, 1:], Ik[idx]])
        lo[k], hi[k] = np.percentile(np.exp(logR), [5, 95])
    return est, lo, hi


est, lo, hi = filt()

fig, (axl, axr) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# ---- Left: latent incidence and its under-reported observation.
weeks = np.arange(1, n_weeks + 1)
axl.plot(weeks, I, color=PALETTE[1], lw=2, label="latent infections")
axl.bar(weeks, reports, color=PALETTE[0], alpha=0.55, width=0.7,
        label="reported cases")
axl.set_xlabel("week")
axl.set_ylabel("new infections")
axl.set_title("observed incidence", fontsize=10)
axl.legend(loc="upper right", fontsize=8)

# ---- Right: recovered time-varying reproduction number.
axr.axhline(1.0, color=MUTED, lw=0.8, ls=":")
axr.fill_between(weeks[L:], lo[L:], hi[L:], color=PALETTE[0], alpha=0.22,
                 label="90% band")
axr.step(weeks, R_true, where="mid", color=PALETTE[1], lw=2,
         label="true $R_t$")
axr.plot(weeks[L:], est[L:], color=PALETTE[0], lw=2, label="filtered $R_t$")
axr.set_xlabel("week")
axr.set_ylabel("reproduction number $R_t$")
axr.set_title("recovered transmission", fontsize=10)
axr.annotate("control brings\n$R_t$ below 1", xy=(20, 0.7), xytext=(24, 1.35),
             fontsize=7, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axr.legend(loc="upper right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/pomp-time-varying-transmission.svg")
