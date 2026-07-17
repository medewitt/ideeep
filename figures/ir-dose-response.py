# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "statsmodels", "matplotlib"]
# ///
"""Insecticide dose-response for a susceptible and a resistant mosquito strain.
Mortality is fit against log dose with a logit model; the concentration killing
50% (LC50) is read off each curve. The resistant strain's curve is shifted about
tenfold to the right - the resistance ratio - so a dose that kills nearly all
susceptible mosquitoes barely dents the resistant population."""
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(5)
doses = np.array([0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5])
ld = np.log10(doses)


def sim(lc50, slope, n=100):
    p = 1 / (1 + np.exp(-slope * (ld - np.log10(lc50))))
    return rng.binomial(n, p), np.full(len(doses), n)


def fit(deaths, n):
    X = sm.add_constant(ld)
    m = sm.GLM(np.c_[deaths, n - deaths], X,
               family=sm.families.Binomial(sm.families.links.Logit())).fit()
    b0, b1 = m.params
    lc50 = 10 ** (-b0 / b1)
    return b0, b1, lc50


ds, ns = sim(0.02, 4.0)
dr, nr = sim(0.20, 4.0)
b0s, b1s, lc50_s = fit(ds, ns)
b0r, b1r, lc50_r = fit(dr, nr)

fig, ax = plt.subplots(figsize=(6.4, 4.2))
xx = np.linspace(ld.min() - 0.3, ld.max() + 0.3, 200)
for (d, n, b0, b1, lc, col, lab) in [
        (ds, ns, b0s, b1s, lc50_s, PALETTE[0], "susceptible"),
        (dr, nr, b0r, b1r, lc50_r, PALETTE[1], "resistant")]:
    ax.scatter(10**ld, d / n * 100, s=34, color=col, edgecolor="white",
               linewidth=0.4, zorder=3)
    ax.plot(10**xx, 100 / (1 + np.exp(-(b0 + b1 * xx))), color=col, lw=2.2,
            label=f"{lab} (LC50 {lc:.3f})")
    ax.plot([lc, lc], [0, 50], color=col, lw=1.0, ls=":")

ax.axhline(50, color=MUTED, lw=0.9, ls="--")
ax.annotate(f"resistance ratio\nRR50 ≈ {lc50_r/lc50_s:.0f}×",
            xy=(lc50_s, 50), xytext=(0.03, 20), fontsize=8.6, color=INK,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
ax.annotate("", xy=(lc50_r, 50), xytext=(lc50_s, 50),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.set_xscale("log")
ax.set_xlabel("insecticide concentration (%, log scale)")
ax.set_ylabel("mortality (%)")
ax.set_title("Dose-response and the resistance ratio", fontsize=9.8)
ax.legend(fontsize=8.4, loc="lower right")
ax.set_ylim(0, 105)
fig.tight_layout()
save(fig, "assets/figures/ir-dose-response.svg")
