# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "scipy"]
# ///
"""What a p-value is. Left: the two-sided p-value for the worked example is the
tail mass of a standard normal beyond +/-2.1, which totals about 0.0357. Right:
when the null hypothesis is true, an exact test's p-value is Uniform(0,1) — a
histogram of 10,000 simulated null p-values is flat, and the shaded p <= 0.05
region contains about 5% of them, which is exactly why testing at alpha gives a
Type I error rate of alpha."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(7)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- two-sided tails ------------------------------------------------------
z = np.linspace(-4, 4, 400)
dens = stats.norm.pdf(z)
axL.plot(z, dens, color=PALETTE[0], lw=2.0)
zc = 2.1
axL.fill_between(z, 0, dens, where=np.abs(z) >= zc, color=PALETTE[1] + "55")
axL.axvline(zc, color=PALETTE[1], lw=1.0)
axL.axvline(-zc, color=PALETTE[1], lw=1.0)
p_two = 2 * stats.norm.sf(zc)
axL.annotate(f"both tails beyond ±2.1\n$p=2\\,\\mathrm{{P}}(Z\\geq2.1)\\approx{p_two:.4f}$",
             xy=(2.7, stats.norm.pdf(2.7)), xytext=(-1.4, 0.28), fontsize=8.2,
             color=INK, arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axL.set_xlabel("test statistic $z$")
axL.set_ylabel("density under $H_0$")
axL.set_title("A two-sided p-value is tail mass", fontsize=10)
axL.set_ylim(0, 0.43)

# ---- uniform p-values under H0 --------------------------------------------
m = 10000
x = rng.normal(0, 1, size=(m, 30))          # H0 true: mean 0
tstat = x.mean(axis=1) / (x.std(axis=1, ddof=1) / np.sqrt(30))
pvals = 2 * stats.t.sf(np.abs(tstat), df=29)

axR.hist(pvals, bins=20, range=(0, 1), color=PALETTE[0] + "cc",
         edgecolor="white", linewidth=0.4)
axR.axhline(m / 20, ls="--", color=MUTED, lw=1.1)
axR.text(0.5, m / 20 + 30, "flat: Uniform(0,1)", fontsize=8.5, color=MUTED,
         ha="center")
axR.axvspan(0, 0.05, color=PALETTE[1] + "33", zorder=0)
frac = (pvals <= 0.05).mean()
axR.annotate(f"$p\\leq0.05$: {frac*100:.1f}% of tests\n= Type I error rate $\\alpha$",
             xy=(0.05, m / 20), xytext=(0.18, m / 20 * 1.7), fontsize=8.2,
             color=PALETTE[1],
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axR.set_xlabel("p-value under $H_0$")
axR.set_ylabel("count (10,000 tests)")
axR.set_title("Under $H_0$ the p-value is uniform", fontsize=10)
axR.set_xlim(0, 1)

fig.tight_layout()
save(fig, "assets/figures/p-values.svg")
