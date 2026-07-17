# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Time-varying transmission with a linear Kalman filter: a local-linear-trend
model on log-incidence recovers the growth rate, and hence a time-varying R_t."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(8)

T = 50
w = np.array([0.25, 0.35, 0.25, 0.15])          # generation-interval weights
L = len(w)
t = np.arange(T)
R_true = np.where(t < 16, 1.5, np.where(t < 30, 0.75, 1.2))

# Simulate incidence via the renewal equation, observe 50% of it.
I = np.zeros(T)
I[:L] = [30, 40, 55, 70]
for k in range(L, T):
    I[k] = rng.poisson(R_true[k] * np.sum(w * I[k - L:k][::-1]))
cases = rng.poisson(0.5 * I)
y = np.log(np.maximum(cases, 1.0))

# Local-linear-trend Kalman filter: state = [level, slope = growth rate r_t].
A = np.array([[1., 1.], [0., 1.]])
H = np.array([1., 0.])
Q = np.diag([1e-3, 8e-3])
Rm = 0.15
x = np.array([y[L], 0.0])
P = np.eye(2) * 0.5
r_hat = np.zeros(T)
r_sd = np.zeros(T)
for k in range(T):
    x = A @ x
    P = A @ P @ A.T + Q                          # predict
    innov = y[k] - H @ x
    Sk = H @ P @ H + Rm
    K = P @ H / Sk                               # gain
    x = x + K * innov
    P = (np.eye(2) - np.outer(K, H)) @ P         # update
    r_hat[k], r_sd[k] = x[1], np.sqrt(P[1, 1])


def r_to_R(r):
    """Growth rate -> reproduction number via the discretized renewal relation."""
    return 1.0 / np.sum(w * np.exp(-r * np.arange(1, L + 1)))


R_est = np.array([r_to_R(r) for r in r_hat])
R_lo = np.clip([r_to_R(r) for r in r_hat - r_sd], 0.5, 1.85)   # +/- 1 SD
R_hi = np.clip([r_to_R(r) for r in r_hat + r_sd], 0.5, 1.85)
k0 = L + 4                                       # drop the filter warm-up

fig, (axl, axr) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# ---- Left: observed cases and the filtered growth rate.
weeks = np.arange(1, T + 1)
axl.bar(weeks, cases, color=PALETTE[0], alpha=0.5, width=0.75,
        label="reported cases")
axl.set_xlabel("week")
axl.set_ylabel("cases")
axl.set_title("observed incidence", fontsize=10)
ax2 = axl.twinx()
ax2.axhline(0, color=MUTED, lw=0.8, ls=":")
ax2.plot(weeks[L:], r_hat[L:], color=PALETTE[1], lw=2, label="growth rate $r_t$")
ax2.set_ylabel("growth rate $r_t$", color=PALETTE[1])
ax2.tick_params(axis="y", labelcolor=PALETTE[1])
ax2.spines["right"].set_visible(True)
ax2.grid(False)
axl.legend(loc="upper left", fontsize=8)
ax2.legend(loc="upper right", fontsize=8)

# ---- Right: implied time-varying reproduction number.
axr.axhline(1.0, color=MUTED, lw=0.8, ls=":")
axr.fill_between(weeks[k0:], R_lo[k0:], R_hi[k0:], color=PALETTE[0],
                 alpha=0.18, label="$\\pm1$ SD")
axr.step(weeks, R_true, where="mid", color=PALETTE[1], lw=2, label="true $R_t$")
axr.plot(weeks[k0:], R_est[k0:], color=INK, lw=2, label="Kalman $R_t$")
axr.set_xlabel("week")
axr.set_ylabel("reproduction number $R_t$")
axr.set_title("recovered transmission", fontsize=10)
axr.set_ylim(0.4, 2.0)
axr.legend(loc="lower right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/kalman-time-varying-rt.svg")
