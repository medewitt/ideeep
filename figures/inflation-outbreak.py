# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""The inflationary effect: reddened (autocorrelated) noise in a sink's growth
rate produces outbreak-like abundance far above the deterministic baseline,
while white noise of the same variance leaves the long-run mean unchanged."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

lam_bar = 0.8      # mean local growth rate (< 1: a sink)
sigma = 0.18       # SD of the growth-rate fluctuations
phi_red = 0.72     # lag-1 autocorrelation of the reddened environment
I = 10.0           # constant immigration per step
T = 120_000        # long run for stable mean estimates
burn = 3000
win = 360          # width of the displayed window


def ar1(phi, n, rng):
    """Standardized AR(1): zero mean, unit variance, lag-1 autocorr = phi."""
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + np.sqrt(1 - phi**2) * rng.standard_normal()
    return x


def simulate(phi, seed):
    rng = np.random.default_rng(seed)
    z = ar1(phi, T, rng)
    lam = np.clip(lam_bar + sigma * z, 0.0, None)
    N = np.empty(T)
    N[0] = I / (1 - lam_bar)
    for t in range(1, T):
        N[t] = lam[t - 1] * N[t - 1] + I
    return lam, N


lam_w, N_w = simulate(0.0, seed=0)       # white noise (iid)
lam_r, N_r = simulate(phi_red, seed=0)   # reddened (positively autocorrelated) noise
baseline = I / (1 - lam_bar)             # deterministic equilibrium = 50

mean_w = N_w[burn:].mean()
mean_r = N_r[burn:].mean()

# centre the displayed window on a *representative* outbreak (peak in a typical
# band, not the rare global maximum) so the baseline stays legible
seg = N_r[burn:burn + 60_000]
cands = np.where((seg > 300) & (seg < 650))[0]
peak = burn + int(cands[len(cands) // 2])
lo = max(burn, peak - win // 2)
window = slice(lo, lo + win)
ymax = 1.18 * N_r[window].max()

fig, (axg, axn) = plt.subplots(2, 1, figsize=(9.6, 6.4), sharex=True,
                               gridspec_kw={"height_ratios": [1, 1.5]})
t = np.arange(T)[window]

# Top: the growth-rate environment
axg.plot(t, lam_r[window], color=PALETTE[1], lw=1.0, label=f"reddened  (autocorr = {phi_red})")
axg.plot(t, lam_w[window], color=MUTED, lw=0.8, alpha=0.7, label="white  (iid)")
axg.axhline(lam_bar, color=INK, lw=1.0, ls="--")
axg.axhline(1.0, color=PALETTE[2], lw=1.0, ls=":")
axg.text(t[0], lam_bar - 0.10, r"mean $\bar\lambda=0.8$", color=INK, fontsize=9)
axg.text(t[0], 1.02, r"replacement $\lambda=1$", color=PALETTE[2], fontsize=9)
axg.set_ylabel("growth rate  $\\lambda_t$")
axg.set_title("Local growth rate fluctuates around a sub-replacement mean")
axg.legend(loc="upper right", fontsize=9, ncol=2)

# Bottom: abundance
axn.plot(t, N_r[window], color=PALETTE[1], lw=1.2,
         label=f"reddened noise   mean $\\approx$ {mean_r:.0f}")
axn.plot(t, N_w[window], color=MUTED, lw=1.0, alpha=0.85,
         label=f"white noise   mean $\\approx$ {mean_w:.0f}")
axn.axhline(baseline, color=INK, lw=1.2, ls="--",
            label=f"deterministic  $I/(1-\\bar\\lambda)$ = {baseline:.0f}")
axn.set_ylim(0, ymax)
axn.set_ylabel("abundance  $N_t$")
axn.set_xlabel("time  $t$")
axn.set_title("Positive autocorrelation inflates the mean and drives outbreaks")
axn.legend(loc="upper right", fontsize=9)

fig.suptitle("The inflationary effect in an immigration-fed sink", fontweight="bold")
fig.tight_layout()
save(fig, "assets/figures/inflation-outbreak.svg")
