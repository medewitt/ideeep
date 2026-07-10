# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
#     "scipy",
# ]
# ///
"""Superspreading: overdispersed offspring distributions and transmission concentration."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

R = 2.0                       # mean secondary cases (reproduction number)
x = np.arange(0, 13)          # 0..12 secondary cases

# Poisson(mean R) vs Negative Binomial(mean R, dispersion k)
pois = stats.poisson.pmf(x, R)


def nb_pmf(k, mean=R):
    """NB parameterised by mean R and dispersion k (var = R + R^2/k)."""
    p = k / (k + mean)
    return stats.nbinom.pmf(x, k, p)


nb = nb_pmf(0.3)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.4))

# --- LEFT: offspring distribution ------------------------------------------
w = 0.4
axL.bar(x - w / 2, pois, width=w, color=PALETTE[0], label="Poisson (k → ∞)")
axL.bar(x + w / 2, nb, width=w, color=PALETTE[1], label="Neg. binomial (k = 0.3)")

axL.annotate("most infections\ncause none",
             xy=(0.2, nb[0]), xytext=(2.6, 0.5),
             fontsize=8.5, color=MUTED, ha="left",
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axL.annotate("superspreading\nevents",
             xy=(8, nb[8] + 0.006), xytext=(6.4, 0.24),
             fontsize=8.5, color=MUTED, ha="left",
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

axL.set_xlabel("secondary cases from one infection")
axL.set_ylabel("probability")
axL.set_title("Offspring distribution (both mean R = 2)", fontsize=10)
axL.set_xticks(x[::2])
axL.legend(loc="upper right", fontsize=8.5)
axL.grid(axis="x", visible=False)

# --- RIGHT: Lorenz-type concentration curve --------------------------------
N = 200_000


def lorenz(k):
    """Cumulative share of transmission vs cumulative share of cases."""
    draws = nb_pmf(k)  # reuse mean R; simulate offspring counts
    p = k / (k + R)
    counts = stats.nbinom.rvs(k, p, size=N, random_state=rng)
    counts = np.sort(counts)[::-1]          # most infectious first
    cum_t = np.cumsum(counts) / counts.sum()
    cum_c = np.arange(1, N + 1) / N
    cum_t = np.concatenate([[0.0], cum_t])
    cum_c = np.concatenate([[0.0], cum_c])
    return cum_c, cum_t


ks = [0.1, 0.3, 1.0]
for k, col in zip(ks, PALETTE):
    cc, ct = lorenz(k)
    axR.plot(cc, ct, color=col, lw=1.8, label=f"k = {k}")

axR.plot([0, 1], [0, 1], ls="--", color=MUTED, lw=1.0,
         label="homogeneous (k → ∞)")

# top 20% cause ~97% of transmission for k = 0.1
axR.axvline(0.2, color="#d8dee4", lw=0.8, zorder=0)
axR.annotate("k = 0.1: top 20% of cases\ncause ~97% of transmission",
             xy=(0.2, 0.965), xytext=(0.32, 0.55),
             fontsize=8.5, color=INK, ha="left",
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

axR.set_xlabel("cumulative share of cases (ranked)")
axR.set_ylabel("cumulative share of transmission")
axR.set_title("Transmission concentration", fontsize=10)
axR.set_xlim(0, 1)
axR.set_ylim(0, 1)
axR.legend(loc="lower right", fontsize=8.5)

fig.tight_layout()
save(fig, "assets/figures/superspreading.svg")
