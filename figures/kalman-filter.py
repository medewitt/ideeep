# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""The Kalman filter on a local-level model: it tracks a noisy hidden state and
its Kalman gain / posterior variance settle to a steady state."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(0)

n = 60
x_true = np.cumsum(rng.normal(0, 0.3, n)) + 5.0     # latent random walk
y = x_true + rng.normal(0, 1.0, n)                  # noisy observation

q, r = 0.09, 1.0                                    # process / obs variance
xhat, P = y[0], 1.0
xf = np.zeros(n)
sd = np.zeros(n)
gain = np.zeros(n)
for t in range(n):
    xp, Pp = xhat, P + q                            # predict
    K = Pp / (Pp + r)                               # Kalman gain
    xhat = xp + K * (y[t] - xp)                     # update
    P = (1 - K) * Pp
    xf[t], sd[t], gain[t] = xhat, np.sqrt(P), K

t = np.arange(n)
fig, (axl, axr) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# ---- Left: filtered estimate vs truth vs noisy observations.
axl.fill_between(t, xf - 1.96 * sd, xf + 1.96 * sd, color=PALETTE[0],
                 alpha=0.20, label="95% band")
axl.scatter(t, y, s=14, color=INK, alpha=0.6, label="observations")
axl.plot(t, x_true, color=PALETTE[1], lw=2, label="true state")
axl.plot(t, xf, color=PALETTE[0], lw=2, label="filtered mean")
axl.set_xlabel("time step")
axl.set_ylabel("state")
axl.set_title("filtering a noisy signal", fontsize=10)
axl.legend(loc="upper left", fontsize=8)

# ---- Right: Kalman gain and posterior SD converge to a steady state.
axr.plot(t, gain, color=PALETTE[2], lw=2, label="Kalman gain $K_t$")
axr.plot(t, sd, color=PALETTE[3], lw=2, label="posterior SD")
axr.set_xlabel("time step")
axr.set_ylabel("value")
axr.set_title("gain reaches steady state", fontsize=10)
axr.annotate("recursion forgets the\nprior within a few steps",
             xy=(5, gain[5]), xytext=(23, 0.55), fontsize=7, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axr.legend(loc="upper right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/kalman-filter.svg")
