# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
#     "scipy",
# ]
# ///
"""Back-calculation: recover infections from cases via deconvolution."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# Delay pmf (e.g. incubation period), discretised over 0..21 days.
days = np.arange(0, 22)
shape, scale = 5.0, 1.6
cdf = gamma.cdf(days + 1, a=shape, scale=scale)
pmf = np.diff(np.concatenate(([0.0], cdf)))
pmf = pmf / pmf.sum()

# Latent infection incidence: a smooth epidemic bump over 120 days.
t = np.arange(0, 120)
infections = 900 * np.exp(-0.5 * ((t - 42) / 12.0) ** 2)

# Observed cases = infections convolved with the delay pmf.
cases_full = np.convolve(infections, pmf)
cases = cases_full[: len(t)]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.4))

# Left: the delay distribution.
axL.bar(days, pmf, color=PALETTE[2], width=0.85, edgecolor="white",
        linewidth=0.4)
axL.set_xlabel("delay: infection → observation (days)")
axL.set_ylabel("probability")
axL.set_title("delay distribution")
axL.set_xlim(-0.6, 21.6)

# Right: latent infections and resulting observed cases.
axR.fill_between(t, cases, color=PALETTE[0], alpha=0.18)
axR.plot(t, cases, color=PALETTE[0], lw=2.0, label="observed cases")
axR.plot(t, infections, color=PALETTE[1], lw=2.0, label="infections")
axR.set_xlabel("day")
axR.set_ylabel("count")
axR.set_title("infections vs observed cases")
axR.set_xlim(0, 119)
axR.legend(loc="upper right")

axR.annotate(
    "back-calculation recovers infections\n(earlier, sharper) from cases"
    "\n(later, smoother)",
    xy=(48, 640), xytext=(72, 430),
    fontsize=8.5, color=INK, ha="left",
    arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1),
)

fig.tight_layout()
save(fig, "assets/figures/back-calculation.svg")
