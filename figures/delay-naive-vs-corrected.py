# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Ignoring right truncation biases a fitted delay distribution toward short delays."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(3)

# True incubation-period distribution: lognormal (meanlog, sdlog)
mu, sigma = 1.6, 0.5
true = stats.lognorm(s=sigma, scale=np.exp(mu))

# Simulate infections during a still-growing epidemic and right-truncate:
# an event is observed only if infection_time + delay <= T.
T = 30.0
n = 4000
infection_time = rng.uniform(0, T, n)
delay = true.rvs(n, random_state=rng)
seen = infection_time + delay <= T
obs = delay[seen]

# Naive fit: fit a lognormal to the observed (truncated) delays, ignoring T.
s_hat, _, scale_hat = stats.lognorm.fit(obs, floc=0)
naive = stats.lognorm(s=s_hat, scale=scale_hat)

x = np.linspace(0, 20, 400)
fig, ax = plt.subplots(figsize=(6.6, 3.8))
ax.hist(obs, bins=30, density=True, color="#c9d3db", alpha=0.8,
        label="observed (right-truncated) sample")
ax.plot(x, true.pdf(x), color=PALETTE[2], lw=2.2,
        label="true / truncation-aware fit")
ax.plot(x, naive.pdf(x), color=PALETTE[1], lw=2.2, ls="--",
        label="naïve fit (ignores truncation)")

ax.axvline(true.mean(), color=PALETTE[2], lw=0.9, ls=":")
ax.axvline(naive.mean(), color=PALETTE[1], lw=0.9, ls=":")
ax.text(true.mean() + 0.2, ax.get_ylim()[1] * 0.92,
        f"true mean ≈ {true.mean():.1f} d", color=PALETTE[2], fontsize=8.5)
ax.text(naive.mean() - 0.2, ax.get_ylim()[1] * 0.80,
        f"naïve ≈ {naive.mean():.1f} d", color=PALETTE[1], fontsize=8.5, ha="right")

ax.set_xlabel("incubation period (days)")
ax.set_ylabel("density")
ax.set_title("Right truncation biases the naïve fit short")
ax.legend(loc="upper right", fontsize=8.5)
ax.set_xlim(0, 20)
save(fig, "assets/figures/delay-naive-vs-corrected.svg")
