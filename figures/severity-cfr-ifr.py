# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Delay bias in the naive CFR and the severity under-ascertainment pyramid."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (axl, axr) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# ---- Left: naive vs delay-adjusted CFR over epidemic time.
days = np.arange(0, 121)
# Rising-then-falling epidemic bump: lognormal-shaped incidence over ~120 d.
cases = 2200.0 * stats.lognorm(s=0.42, scale=45).pdf(days)

true_cfr = 0.02
# Onset-to-death delay: gamma, mean ~15 d (shape 5, scale 3).
delay_x = np.arange(0, 61)
delay_pmf = stats.gamma(a=5.0, scale=3.0).pdf(delay_x)
delay_pmf = delay_pmf / delay_pmf.sum()

# Deaths lag cases through the onset-to-death delay.
deaths = true_cfr * np.convolve(cases, delay_pmf)[: len(days)]

# Naive CFR divides cumulative deaths by cumulative cases (biased low while
# incidence rises, because those deaths have not yet occurred).
cum_cases = np.cumsum(cases)
cum_deaths = np.cumsum(deaths)
naive_cfr = np.divide(cum_deaths, cum_cases,
                      out=np.zeros_like(cum_deaths), where=cum_cases > 0)

# Delay-adjusted CFR divides cumulative deaths by the number of cases whose
# outcome has already resolved: cases convolved with the delay CDF (the
# probability the outcome is known by day t). This recovers the true CFR.
delay_cdf = np.cumsum(delay_pmf)
resolved = np.convolve(cases, delay_cdf)[: len(days)]
adj_cfr = np.divide(cum_deaths, resolved,
                    out=np.full_like(cum_deaths, np.nan), where=resolved > 5)
# Mild estimation noise so the adjusted line reads as a real estimate that
# hovers on the truth rather than sitting exactly on the dashed line. Only
# shown once enough cases have resolved for the estimate to be meaningful.
se = np.sqrt(np.maximum(adj_cfr * (1 - adj_cfr), 1e-9) / np.maximum(resolved, 1))
adj_noisy = adj_cfr + rng.normal(0, 1, len(days)) * se * 0.6
adj_noisy[resolved <= 900] = np.nan

axl.axhline(true_cfr, color=MUTED, ls="--", lw=1.1, label="true CFR")
axl.plot(days, naive_cfr, color=PALETTE[1], lw=2, label="naive CFR(t)")
axl.plot(days, adj_noisy, color=PALETTE[0], lw=2, label="delay-adjusted")
axl.set_xlabel("day")
axl.set_ylabel("estimated CFR")
axl.set_xlim(0, 120)
axl.set_ylim(0, true_cfr * 1.6)
axl.annotate("naive CFR biased low\nwhile incidence rises",
             xy=(30, naive_cfr[30]), xytext=(46, 0.006), fontsize=7.5,
             color=PALETTE[1],
             arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.9))
axl.legend(loc="lower right", fontsize=8)
axl.set_title("delay bias in the naive CFR", fontsize=10)

# ---- Right: severity / under-ascertainment pyramid (funnel).
tiers = ["infections", "symptomatic", "detected cases",
         "hospitalized", "deaths"]
counts = np.array([100000, 50000, 15000, 3000, 1000], dtype=float)
ypos = np.arange(len(tiers))[::-1]        # deaths at the bottom
widths = counts / counts.max()            # normalized funnel widths
colors = [PALETTE[0], PALETTE[0], PALETTE[2], PALETTE[4], PALETTE[1]]

axr.barh(ypos, widths, left=(1 - widths) / 2, height=0.62,
         color=colors, edgecolor="white", linewidth=0.8)
# Labels sit to the right of the funnel so narrow bars never clip them.
for y, lab, n in zip(ypos, tiers, counts):
    axr.text(1.08, y, f"{lab}: {int(n):,}", ha="left", va="center",
             fontsize=8, color=INK)

ifr = counts[-1] / counts[0]
cfr = counts[-1] / counts[2]
axr.text(0.0, -1.05,
         f"IFR = deaths / infections = {ifr * 100:.1f}%\n"
         f"CFR = deaths / detected = {cfr * 100:.1f}%",
         ha="left", va="center", fontsize=8, color=INK)

axr.set_xlim(0, 2.3)
axr.set_ylim(-1.6, len(tiers) - 0.3)
axr.set_xticks([])
axr.set_yticks([])
axr.grid(False)
for spine in axr.spines.values():
    spine.set_visible(False)
axr.set_title("under-ascertainment pyramid", fontsize=10)

fig.tight_layout()
save(fig, "assets/figures/severity-cfr-ifr.svg")
