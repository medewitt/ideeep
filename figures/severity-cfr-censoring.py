# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Real-time CFR estimation under censoring: two naive estimators bracket the
truth, and the delay-corrected estimator (Ghani/Nishiura) tracks it."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (axl, axr) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# ---- Left: the two competing outcome delays.
x = np.arange(0, 61)
# Onset-to-death is shorter than onset-to-recovery, so early in an outbreak
# deaths resolve first and deaths/(deaths+recoveries) overestimates.
f_death = stats.gamma(a=5.0, scale=3.0).pdf(x)      # mean ~15 days
f_recov = stats.gamma(a=8.0, scale=3.0).pdf(x)      # mean ~24 days
f_death /= f_death.sum()
f_recov /= f_recov.sum()

axl.plot(x, f_death, color=PALETTE[1], lw=2, label="onset → death (mean 15 d)")
axl.plot(x, f_recov, color=PALETTE[2], lw=2,
         label="onset → recovery (mean 24 d)")
axl.fill_between(x, f_death, color=PALETTE[1], alpha=0.12)
axl.fill_between(x, f_recov, color=PALETTE[2], alpha=0.12)
axl.set_xlabel("days from symptom onset to outcome")
axl.set_ylabel("probability")
axl.set_title("competing outcome delays", fontsize=10)
axl.legend(loc="upper right", fontsize=7.5)
axl.set_xlim(0, 60)

# ---- Right: three estimators over epidemic time.
days = np.arange(0, 201)
cases = 3000.0 * stats.lognorm(s=0.4, scale=55).pdf(days)   # epidemic wave
true_cfr = 0.015

# Pad the delay kernels to the series length.
fd = np.zeros(len(days)); fd[: len(f_death)] = f_death
fr = np.zeros(len(days)); fr[: len(f_recov)] = f_recov
Fd = np.cumsum(fd)

deaths = true_cfr * np.convolve(cases, fd)[: len(days)]
recov = (1 - true_cfr) * np.convolve(cases, fr)[: len(days)]

cum_c = np.cumsum(cases)
cum_d = np.cumsum(deaths)
cum_r = np.cumsum(recov)

naive = np.divide(cum_d, cum_c, out=np.zeros_like(cum_d), where=cum_c > 0)
resolved = np.divide(cum_d, cum_d + cum_r,
                     out=np.zeros_like(cum_d), where=(cum_d + cum_r) > 0)
# Censoring-corrected: divide deaths by cases with a known (resolved) outcome,
# estimated as cases convolved with the onset-to-death CDF.
known = np.convolve(cases, Fd)[: len(days)]
corrected = np.divide(cum_d, known,
                      out=np.full_like(cum_d, np.nan), where=known > 30)

axr.axhline(true_cfr, color=MUTED, ls="--", lw=1.1, label="true CFR")
axr.plot(days, resolved, color=PALETTE[2], lw=2,
         label="deaths / (deaths + recoveries)")
axr.plot(days, naive, color=PALETTE[1], lw=2, label="deaths / cases (naive)")
axr.plot(days, corrected, color=PALETTE[0], lw=2.2,
         label="censoring-corrected")
axr.set_xlabel("day of the epidemic")
axr.set_ylabel("estimated CFR")
axr.set_ylim(0, 0.06)
axr.set_xlim(0, 200)
axr.annotate("biased high early\n(deaths resolve first)", xy=(35, resolved[35]),
             xytext=(70, 0.048), fontsize=7.5, color=PALETTE[2],
             arrowprops=dict(arrowstyle="->", color=PALETTE[2], lw=0.9))
axr.annotate("biased low early\n(deaths not yet counted)", xy=(35, naive[35]),
             xytext=(78, 0.005), fontsize=7.5, color=PALETTE[1],
             arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.9))
axr.set_title("three estimators over the epidemic", fontsize=10)
axr.legend(loc="upper right", fontsize=7)

fig.tight_layout()
save(fig, "assets/figures/severity-cfr-censoring.svg")
