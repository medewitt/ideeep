# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Incidence simulated from the renewal equation and its instantaneous growth."""
import numpy as np
from scipy.stats import gamma
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

# Discretize a gamma generation interval (mean 5 days, sd ~2.2 days).
shape, scale = 5.0, 1.0
smax = 20
s = np.arange(1, smax + 1)
cdf = gamma.cdf(np.arange(0, smax + 1), a=shape, scale=scale)
w = np.diff(cdf)
w = w / w.sum()                       # generation-interval weights w_s

# Time-varying R_t: above 1 while the epidemic grows, then falling through 1.
T = 90
days = np.arange(T)
Rt = 0.7 + 1.7 * np.exp(-days / 32.0)

# Renewal equation: I_t = R_t * sum_s I_{t-s} w_s.
I = np.zeros(T)
I[0] = 10.0
for t in range(1, T):
    k = np.arange(1, min(t, smax) + 1)
    I[t] = Rt[t] * np.sum(I[t - k] * w[k - 1])

# Instantaneous growth rate r_t = d/dt log I(t), estimated as a log difference.
r = np.full(T, np.nan)
r[1:] = np.log(I[1:]) - np.log(I[:-1])

peak_day = int(np.argmax(I))

fig, (axT, axB) = plt.subplots(2, 1, figsize=(6.4, 5.6), sharex=True)

axT.plot(days, I, color=PALETTE[0], lw=2.0)
axT.axvline(peak_day, color="0.5", ls=":", lw=1.2)
axT.set_ylabel("incidence $I(t)$")
axT.set_title("Renewal-equation epidemic")
axT.annotate(f"peak day {peak_day}", xy=(peak_day, I[peak_day]),
             xytext=(peak_day + 5, I[peak_day] * 0.85),
             arrowprops=dict(arrowstyle="->", color="0.4"), fontsize="small")

axB.plot(days, r, color=PALETTE[1], lw=2.0)
axB.axhline(0.0, color="0.4", ls="--", lw=1.2)
axB.axvline(peak_day, color="0.5", ls=":", lw=1.2)
axB.set_xlabel("day")
axB.set_ylabel("growth rate $r(t)$")
axB.annotate("$r=0$ at the peak", xy=(peak_day, 0.0),
             xytext=(peak_day + 5, 0.06),
             arrowprops=dict(arrowstyle="->", color="0.4"), fontsize="small")

fig.tight_layout()

print(f"generation interval mean = {(s * w).sum():.2f} days")
print(f"peak day = {peak_day}")

save(fig, "assets/figures/renewal-equation.svg")
