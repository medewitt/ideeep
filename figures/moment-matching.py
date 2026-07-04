# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Moment matching: fit a gamma to a skewed sample by equating the sample
mean and variance to the gamma's, and contrast with a moment-matched normal
that shares the same two moments but misses the skew."""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, MUTED

apply_style()
rng = np.random.default_rng(7)

# A right-skewed sample (e.g. an incubation-period distribution)
sample = rng.gamma(shape=2.5, scale=1.6, size=400)

# Method-of-moments estimates from the first two moments
m = sample.mean()
v = sample.var()                      # population (MLE-style) variance
shape = m**2 / v                      # alpha = mean^2 / var
rate = m / v                          # beta  = mean / var
scale = 1.0 / rate

xs = np.linspace(0, sample.max() * 1.05, 400)
gamma_pdf = stats.gamma.pdf(xs, a=shape, scale=scale)
normal_pdf = stats.norm.pdf(xs, loc=m, scale=np.sqrt(v))

fig, ax = plt.subplots(figsize=(7.0, 4.0))
ax.hist(sample, bins=30, density=True, color=PALETTE[0], alpha=0.45,
        edgecolor="white", linewidth=0.3, label="sample")
ax.plot(xs, gamma_pdf, color=PALETTE[1], lw=2.0,
        label=f"gamma (α={shape:.2f}, β={rate:.2f})")
ax.plot(xs, normal_pdf, color=PALETTE[3], lw=2.0, ls="--",
        label="normal (same μ, σ²)")

ax.axvline(m, color=MUTED, lw=1.0, ls=":")
ax.annotate(r"matched $\mu,\ \sigma^2$", xy=(m, ax.get_ylim()[1] * 0.92),
            xytext=(m + 1.0, ax.get_ylim()[1] * 0.92), color=MUTED, fontsize=9)

ax.set_xlabel("value")
ax.set_ylabel("density")
ax.set_title("Moment matching: gamma captures the skew, normal does not")
ax.legend()

save(fig, "assets/figures/moment-matching.svg")
