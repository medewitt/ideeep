# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""A renewal-equation epidemic: incidence and the effective reproduction number R_t."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(3)

# --- Generation interval: discretized Gamma with mean ~5 days ---
shape, scale = 2.5, 2.0          # mean = shape*scale = 5 days
smax = 20
s = np.arange(1, smax + 1)
# Discretize via difference of the Gamma CDF at integer boundaries.
from math import gamma as _g
def gamma_cdf(x, k, th):
    # regularized lower incomplete gamma via series (adequate for small x/th)
    if x <= 0:
        return 0.0
    a = k
    xx = x / th
    term = 1.0 / a
    total = term
    n = 1
    while n < 500:
        term *= xx / (a + n)
        total += term
        if term < 1e-12:
            break
        n += 1
    return (xx ** a) * np.exp(-xx) * total / _g(a)

cdf = np.array([gamma_cdf(x, shape, scale) for x in np.arange(0, smax + 1)])
w = np.diff(cdf)
w = w / w.sum()                  # generation-interval weights w_s

# --- True time-varying R_t: starts >1, declines through 1 ---
T = 80
days = np.arange(T)
Rt_true = 0.7 + 1.6 * np.exp(-days / 30.0)   # ~2.3 down toward ~0.7

# --- Renewal equation: I_t = R_t * sum_s I_{t-s} w_s ---
I = np.zeros(T)
I[0] = 10.0
for t in range(1, T):
    lam = 0.0
    for k in range(1, min(t, smax) + 1):
        lam += I[t - k] * w[k - 1]
    I[t] = Rt_true[t] * lam

# --- Simple back-out estimate of R_t = I_t / sum_s I_{t-s} w_s ---
Rt_est = np.full(T, np.nan)
for t in range(1, T):
    lam = sum(I[t - k] * w[k - 1] for k in range(1, min(t, smax) + 1))
    if lam > 0:
        Rt_est[t] = I[t] / lam

peak_day = int(np.argmax(I))

fig, (axT, axB) = plt.subplots(2, 1, figsize=(6.6, 6.0), sharex=True)

axT.plot(days, I, color=PALETTE[0], lw=2.0)
axT.axvline(peak_day, color="0.5", ls=":", lw=1.2)
axT.set_ylabel("incidence (new cases)")
axT.set_title("Renewal-equation epidemic")
axT.annotate(f"peak day {peak_day}", xy=(peak_day, I[peak_day]),
             xytext=(peak_day + 4, I[peak_day] * 0.9),
             arrowprops=dict(arrowstyle="->", color="0.4"), fontsize="small")

axB.plot(days, Rt_true, color=PALETTE[1], lw=2.0, label="true $R_t$")
axB.plot(days, Rt_est, color=PALETTE[2], lw=1.3, ls="--", label="estimated $R_t$")
axB.axhline(1.0, color="0.4", ls="--", lw=1.2)
axB.axvline(peak_day, color="0.5", ls=":", lw=1.2)
axB.set_ylim(0, 2.6)
axB.set_xlabel("day")
axB.set_ylabel("$R_t$")
axB.legend(loc="upper right")

fig.tight_layout()

print(f"generation interval mean = {(s * w).sum():.2f} days")
print(f"peak day = {peak_day}")
for t in [5, 20, peak_day, 60]:
    print(f"day {t:2d}: R_t true = {Rt_true[t]:.2f}, est = {Rt_est[t]:.2f}, I = {I[t]:.1f}")

save(fig, "assets/figures/rt-epidemic.svg")
