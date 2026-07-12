# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Multi-rate data fusion with a Kalman filter: frequent, noisy wastewater and
sparse, weekly case counts share one latent incidence state."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(2)

D = 84                                              # days
m0 = (np.cumsum(rng.normal(0, 0.06, D)) + np.log(800)
      + 0.7 * np.sin(2 * np.pi * np.arange(D) / 45))
latent = np.exp(m0)                                 # true daily incidence
ww = 0.002 * latent * np.exp(rng.normal(0, 0.45, D))  # daily wastewater (noisy)
cases = np.full(D, np.nan)
for d in range(0, D, 7):                            # cases reported weekly only
    cases[d] = rng.poisson(0.4 * latent[d])

# Kalman filter on latent log-incidence m_t (random walk), two measurements:
#   log(wastewater) = log(0.002) + m + noise   (every day)
#   log(cases)      = log(0.40)  + m + noise   (weekly)
q, r1, r2 = 0.06 ** 2, 0.45 ** 2, 0.12 ** 2
c1, c2 = np.log(0.002), np.log(0.40)


def run(use_cases):
    m, P = np.log(800), 1.0
    est = np.zeros(D)
    for d in range(D):
        P += q                                     # predict (random walk)
        K = P / (P + r1)                           # update: wastewater
        m += K * (np.log(ww[d]) - (c1 + m))
        P = (1 - K) * P
        if use_cases and not np.isnan(cases[d]) and cases[d] > 0:
            K = P / (P + r2)                       # update: weekly cases
            m += K * (np.log(cases[d]) - (c2 + m))
            P = (1 - K) * P
        est[d] = np.exp(m)
    return est


fused = run(True)
days = np.arange(D)
obs_days = ~np.isnan(cases)

fig, (axl, axr) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# ---- Left: the two surveillance streams on their own scales.
axl.scatter(days, ww, s=12, color=PALETTE[2], alpha=0.7, label="wastewater (daily)")
axl.set_xlabel("day")
axl.set_ylabel("wastewater signal", color=PALETTE[2])
axl.tick_params(axis="y", labelcolor=PALETTE[2])
axl.set_title("two reporting rates", fontsize=10)
ax2 = axl.twinx()
ax2.scatter(days[obs_days], cases[obs_days], s=45, color=PALETTE[1],
            marker="D", zorder=5, label="cases (weekly)")
ax2.set_ylabel("reported cases", color=PALETTE[1])
ax2.tick_params(axis="y", labelcolor=PALETTE[1])
ax2.grid(False)
axl.legend(loc="upper left", fontsize=8)
ax2.legend(loc="upper right", fontsize=8)

# ---- Right: the fused latent incidence estimate.
axr.plot(days, latent, color=PALETTE[1], lw=2, label="true incidence")
axr.plot(days, ww / 0.002, color=MUTED, lw=0.8, alpha=0.7,
         label="wastewater alone")
axr.plot(days, fused, color=PALETTE[0], lw=2, label="Kalman fusion")
for d in days[obs_days]:
    axr.axvline(d, color=PALETTE[1], lw=0.5, ls=":", alpha=0.4)
axr.set_xlabel("day")
axr.set_ylabel("daily incidence")
axr.set_title("fused nowcast", fontsize=10)
axr.legend(loc="upper left", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/kalman-nowcast-fusion.svg")
