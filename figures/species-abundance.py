# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "scipy"]
# ///
"""Species-abundance distributions. Left: a rank-abundance curve from a neutral
community (J=500, immigration m=0.1 from a 50-species metacommunity) is steep
even though every species is ecologically identical — a few species dominate and
a long tail sits near one individual, the log-series-like shape neutral drift
produces. Right: the two classic SAD forms binned by log2 abundance — Fisher's
log-series (singletons the richest class, a monotone decline) versus Preston's
log-normal (an interior bell-shaped mode revealed only in well-sampled
communities)."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(11)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- neutral community -> rank-abundance ----------------------------------
S_meta, J, m = 50, 500, 0.1
meta_p = rng.dirichlet(np.ones(S_meta) * 0.3)
local = rng.choice(S_meta, size=J, p=meta_p)
for _ in range(60000):
    die = rng.integers(J)
    if rng.random() < m:
        local[die] = rng.choice(S_meta, p=meta_p)
    else:
        local[die] = local[rng.integers(J)]
counts = np.sort(np.bincount(local, minlength=S_meta))[::-1]
counts = counts[counts > 0]
axL.semilogy(np.arange(1, len(counts) + 1), counts, color=PALETTE[0], lw=1.8,
             marker="o", ms=4)
axL.annotate("a few dominant species", xy=(1, counts[0]), xytext=(4, counts[0]),
             fontsize=8, color=INK, va="center")
axL.annotate("long tail of rare species", xy=(len(counts) - 1, 1),
             xytext=(3, 1.7), fontsize=8, color=MUTED)
axL.set_xlabel("species rank (most → least common)")
axL.set_ylabel("abundance (log scale)")
axL.set_title("Neutral drift → a steep rank-abundance curve", fontsize=9.3)

# ---- log-series vs log-normal SADs ----------------------------------------
ls = stats.logser.rvs(0.97, size=3000, random_state=rng)
ln = np.round(np.exp(rng.normal(3.0, 1.4, 3000))).astype(int)
ln = ln[ln >= 1]
bins = np.arange(0, 12)
ls_oct = np.floor(np.log2(ls)).astype(int)
ln_oct = np.floor(np.log2(ln)).astype(int)
h_ls = np.bincount(ls_oct, minlength=12)[:12]
h_ln = np.bincount(ln_oct, minlength=12)[:12]
w = 0.4
axR.bar(bins - w / 2, h_ls / h_ls.sum(), width=w, color=PALETTE[1],
        label="log-series")
axR.bar(bins + w / 2, h_ln / h_ln.sum(), width=w, color=PALETTE[2],
        label="log-normal")
axR.set_xlabel(r"abundance class ($\log_2$ individuals)")
axR.set_ylabel("fraction of species")
axR.set_title("Two classic SAD shapes", fontsize=9.3)
axR.legend(fontsize=8.3, loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/species-abundance.svg")
