# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""ABC rejection sampling for a one-parameter model."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# Generative model: theta ~ Uniform(0, 10); S = theta + N(0, 0.8).
# Observed summary statistic and acceptance tolerance.
s_obs = 6.5
epsilon = 0.5

n = 1500
theta = rng.uniform(0.0, 10.0, size=n)
s_sim = theta + rng.normal(0.0, 0.8, size=n)
accepted = np.abs(s_sim - s_obs) < epsilon

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# --- LEFT: prior draws, simulated summaries, and the acceptance band ---
axL.axhspan(s_obs - epsilon, s_obs + epsilon, color=PALETTE[0],
            alpha=0.12, lw=0.0, zorder=0)
axL.axhline(s_obs, color=INK, lw=1.2, zorder=1)

axL.scatter(theta[~accepted], s_sim[~accepted], s=10, color="#c9d3db",
            alpha=0.5, edgecolors="none", label="rejected", zorder=2)
axL.scatter(theta[accepted], s_sim[accepted], s=12, color=PALETTE[0],
            alpha=0.9, edgecolors="none", label="accepted", zorder=3)

axL.text(0.3, 13.0, "accept if\n|S(sim) - S(obs)| < epsilon",
         fontsize="x-small", color=MUTED, ha="left", va="top")
axL.annotate(f"S(obs) = {s_obs}", xy=(9.7, s_obs), xytext=(9.7, s_obs + 1.6),
             fontsize="x-small", color=INK, ha="right",
             arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))

axL.set_xlabel("parameter theta (from prior)")
axL.set_ylabel("simulated summary statistic S")
axL.set_xlim(0, 10)
axL.set_ylim(-1, 14)
axL.set_title("ABC rejection sampling")
axL.legend(loc="lower right", fontsize="x-small")

# --- RIGHT: prior vs ABC posterior over theta ---
prior_density = 1.0 / 10.0  # Uniform(0, 10)
axR.hlines(prior_density, 0, 10, color=MUTED, lw=1.4, label="prior")

axR.hist(theta[accepted], bins=18, range=(0, 10), density=True,
         color=PALETTE[0], alpha=0.75, edgecolor="white", lw=0.4,
         label="ABC posterior")

axR.axvline(s_obs, color=MUTED, lw=1.2, ls="--")
axR.text(s_obs + 0.2, axR.get_ylim()[1] * 0.92, "target",
         fontsize="x-small", color=MUTED, ha="left", va="top")

axR.set_xlabel("parameter theta")
axR.set_ylabel("density")
axR.set_xlim(0, 10)
axR.set_title("prior updated to ABC posterior")
axR.legend(loc="upper left", fontsize="x-small")

fig.tight_layout()

print(f"accepted {accepted.sum()} of {n} draws "
      f"(rate {accepted.mean():.3f})")

save(fig, "assets/figures/approximate-bayesian-computation.svg")
