# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""A state-space model fit by a particle filter: cloud and filtered posterior."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# ---- Simulate a latent state (log-incidence) and noisy observations.
n_steps = 40
t = np.arange(n_steps)
# Smooth rise-and-fall latent trajectory plus a small random-walk wobble.
base = 3.0 + 2.4 * np.exp(-0.5 * ((t - 18) / 8.0) ** 2)
wobble = np.cumsum(rng.normal(0, 0.06, n_steps))
x_true = base + wobble

obs_sd = 0.35
y_obs = x_true + rng.normal(0, obs_sd, n_steps)

# ---- Bootstrap particle filter over the latent state.
n_part = 400
proc_sd = 0.18
particles = rng.normal(x_true[0], 0.4, n_part)
cloud = np.zeros((n_steps, n_part))
post_mean = np.zeros(n_steps)
lo = np.zeros(n_steps)
hi = np.zeros(n_steps)

for k in range(n_steps):
    if k > 0:                                  # propagate: random-walk prior
        particles = particles + rng.normal(0, proc_sd, n_part)
    # weight by Gaussian observation likelihood, then resample.
    w = np.exp(-0.5 * ((y_obs[k] - particles) / obs_sd) ** 2)
    w = w / w.sum()
    idx = rng.choice(n_part, size=n_part, p=w)
    particles = particles[idx]
    cloud[k] = particles
    post_mean[k] = particles.mean()
    lo[k], hi[k] = np.percentile(particles, [5, 95])

fig, (axl, axr) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# ---- Left: particle cloud tracking the latent state.
for k in range(0, n_steps, 2):
    show = rng.choice(n_part, size=150, replace=False)
    axl.scatter(np.full(150, t[k]), cloud[k][show], s=5, alpha=0.06,
                color=PALETTE[0], edgecolors="none")
axl.plot(t, x_true, color=PALETTE[1], lw=2, label="true state")
axl.scatter(t, y_obs, s=14, color=INK, zorder=5, label="observations")
axl.set_xlabel("time step")
axl.set_ylabel("latent state (log incidence)")
axl.set_title("particle cloud", fontsize=10)
axl.annotate("particles approximate the filtering\n"
             "distribution; resampling concentrates them",
             xy=(18, x_true[18]), xytext=(2, 6.4), fontsize=7,
             color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axl.legend(loc="lower right", fontsize=8)

# ---- Right: filtered estimate vs truth vs observations.
axr.fill_between(t, lo, hi, color=PALETTE[0], alpha=0.22,
                 label="90% band")
axr.plot(t, x_true, color=PALETTE[1], lw=2, label="truth")
axr.scatter(t, y_obs, s=14, color=INK, zorder=5, label="observations")
axr.plot(t, post_mean, color=PALETTE[0], lw=2, label="filtered mean")
axr.set_xlabel("time step")
axr.set_ylabel("latent state")
axr.set_title("filtered posterior", fontsize=10)
axr.legend(loc="lower right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/state-space-particle-filter.svg")
