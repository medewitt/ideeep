# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Two ways to make predictions honest about uncertainty. Left: a reliability
diagram -- an over-confident classifier's predicted probabilities do not match
observed frequencies (curve below the diagonal), while a calibrated model tracks
it. Right: split-conformal prediction bands around a regression, calibrated to
cover 90% of new points with a distribution-free guarantee; the band widens
where the data are noisier.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(2)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.8, 3.9))

# --- left: reliability diagram ---
# true prob p; an overconfident model reports p^0.5-ish pushed toward extremes
p = np.linspace(0.02, 0.98, 12)
overconf = np.clip(p + 0.18 * np.sin(np.pi * (p - 0.5)) - 0.0, 0, 1)
# observed frequency for the overconfident model sits off the diagonal
obs_over = np.clip(1 / (1 + np.exp(-(np.log(p / (1 - p)) * 0.55))), 0, 1)
ax0.plot([0, 1], [0, 1], color=MUTED, lw=1.2, ls="--", label="perfect")
ax0.plot(overconf, obs_over, "o-", color=PALETTE[1], lw=1.8, ms=4,
         label="over-confident")
ax0.plot(p, p + 0.02 * rng.standard_normal(p.size), "s-", color=PALETTE[2],
         lw=1.6, ms=3, label="calibrated")
ax0.set_xlim(0, 1); ax0.set_ylim(0, 1)
ax0.set_title("Reliability diagram", fontsize=10)
ax0.set_xlabel("predicted probability", fontsize=9)
ax0.set_ylabel("observed frequency", fontsize=9)
ax0.legend(loc="upper left", fontsize=8)

# --- right: split-conformal prediction band ---
def f(x):
    return np.sin(x)
xtr = rng.uniform(0, 6, 200)
noise = 0.15 + 0.12 * xtr                          # heteroscedastic noise
ytr = f(xtr) + rng.normal(0, 1, xtr.size) * noise
# a simple mean fit (here the true mean) + conformal residual quantile
xg = np.linspace(0, 6, 200)
resid = np.abs(ytr - f(xtr)) / noise               # normalized residuals
q = np.quantile(resid, 0.9)                          # 90% conformal quantile
band = q * (0.15 + 0.12 * xg)
xte = rng.uniform(0, 6, 120)
yte = f(xte) + rng.normal(0, 1, xte.size) * (0.15 + 0.12 * xte)
inside = np.abs(yte - f(xte)) <= q * (0.15 + 0.12 * xte)
ax1.fill_between(xg, f(xg) - band, f(xg) + band, color=PALETTE[0], alpha=0.18,
                 label="90% conformal band")
ax1.plot(xg, f(xg), color=PALETTE[0], lw=1.8, label="prediction")
ax1.scatter(xte[inside], yte[inside], s=10, color=INK, label="covered")
ax1.scatter(xte[~inside], yte[~inside], s=16, color=PALETTE[1], zorder=3,
            label="missed")
ax1.set_title(f"Conformal prediction ({100*inside.mean():.0f}% covered)",
              fontsize=10)
ax1.set_xlabel("x", fontsize=9)
ax1.set_ylabel("y", fontsize=9)
ax1.legend(loc="upper right", fontsize=7.3)

fig.tight_layout()
save(fig, "assets/figures/uncertainty-calibration-conformal.svg")
