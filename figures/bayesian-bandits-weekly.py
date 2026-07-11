# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Week-by-week adaptive allocation of 100 tests over 8 weeks, four sites.

Week 1 is an even warm start (25 each). Weeks 2-8 guarantee every site a
floor of 5 tests, then hand out the remaining 80 by Thompson sampling on
the running Beta posteriors. Left panel: where the 100 tests go each week
(stacked to 100). Right panel: each site's posterior-mean positivity
tightening toward the truth, with site C's 90% credible band shaded.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# --- simulation (identical to the executed page block) --------------------
rng = np.random.default_rng(1)
theta = np.array([0.05, 0.15, 0.22, 0.08])     # true positivity, sites A-D
sites = ["A", "B", "C", "D"]
K, weeks, weekly, floor = 4, 8, 100, 5
flex = weekly - floor * K                       # 80 tests steered by the bandit

a = np.ones(K)
b = np.ones(K)
alloc_hist = np.zeros((weeks, K), dtype=int)
mean_hist = np.zeros((weeks, K))
lo_hist = np.zeros((weeks, K))
hi_hist = np.zeros((weeks, K))

for w in range(weeks):
    if w == 0:
        alloc = np.full(K, weekly // K)         # even warm start: 25 each
    else:
        alloc = np.full(K, floor)               # guaranteed floor
        draws = rng.beta(a[None, :], b[None, :], size=(flex, K))
        picks = draws.argmax(axis=1)            # Thompson for the flexible 80
        for k in range(K):
            alloc[k] += int((picks == k).sum())
    pos = np.array([rng.binomial(int(alloc[k]), theta[k]) for k in range(K)])
    a += pos
    b += alloc - pos
    alloc_hist[w] = alloc
    mean_hist[w] = a / (a + b)
    lo_hist[w] = stats.beta.ppf(0.05, a, b)
    hi_hist[w] = stats.beta.ppf(0.95, a, b)

print("week " + " ".join(f"{s:>4}" for s in sites))
for w in range(weeks):
    print(f"  {w+1:>2} " + " ".join(f"{alloc_hist[w, k]:>4d}" for k in range(K)))

# --- figure ---------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.9))
wk = np.arange(1, weeks + 1)

bottom = np.zeros(weeks)
for k in range(K):
    ax1.bar(wk, alloc_hist[:, k], bottom=bottom, width=0.72,
            color=PALETTE[k], label=f"site {sites[k]}")
    bottom += alloc_hist[:, k]
ax1.set_xticks(wk)
ax1.set_ylim(0, 100)
ax1.set_xlabel("week")
ax1.set_ylabel("tests allocated (of 100)")
ax1.set_title("Where the 100 tests go each week")
ax1.legend(loc="upper center", ncol=4, fontsize=8,
           bbox_to_anchor=(0.5, -0.18))
ax1.annotate("even\nwarm start", xy=(1, 100), xytext=(1.1, 60),
             fontsize=8, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))

for k in range(K):
    ax2.plot(wk, mean_hist[:, k], color=PALETTE[k], lw=2, marker="o", ms=3,
             label=f"site {sites[k]}")
    ax2.axhline(theta[k], color=PALETTE[k], lw=1, ls=":")
ax2.fill_between(wk, lo_hist[:, 2], hi_hist[:, 2], color=PALETTE[2],
                 alpha=0.15, lw=0)
ax2.set_xticks(wk)
ax2.set_xlim(1, weeks)
ax2.set_xlabel("week")
ax2.set_ylabel("posterior mean positivity")
ax2.set_title("Belief about each site sharpens")
ax2.annotate("site C 90% band", xy=(6, hi_hist[5, 2]), xytext=(3.4, 0.30),
             fontsize=8, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))

fig.tight_layout()
save(fig, "assets/figures/bayesian-bandits-weekly.svg")
