# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "scipy"]
# ///
"""GWAS summary plots. Left: a Manhattan plot of -log10 p across the genome,
where a tower of correlated SNPs rises above the genome-wide line at 5e-8 while
the null variants sit in a noisy band below it. Right: QQ plots contrasting a
well-controlled study (lambda ~ 1, tracking the diagonal until a few true hits
pull away) with a confounded one (lambda >> 1, the whole cloud lifting off the
diagonal early)."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(20260711)

GW = -np.log10(5e-8)          # genome-wide significance line ~7.30

# ---- Manhattan plot -------------------------------------------------------
chrom_sizes = [200, 185, 170, 160, 150, 150, 140, 130, 120, 110]
xs, ys, colors = [], [], []
offset = 0
band = [PALETTE[0], MUTED]
for c, size in enumerate(chrom_sizes):
    pos = np.arange(size) + offset
    logp = -np.log10(rng.uniform(size=size))     # nulls: p ~ Uniform(0,1)
    xs.append(pos)
    ys.append(logp)
    colors += [band[c % 2]] * size
    offset += size + 20

xs = np.concatenate(xs)
ys = np.concatenate(ys)

# a correlated "skyscraper" of SNPs on chromosome 6
tower_center = sum(chrom_sizes[:5]) + 20 * 5 + 75
tower_x = tower_center + np.arange(-8, 9)
tower_y = np.array([2.5, 3.4, 4.6, 6.0, 7.8, 9.3, 10.6, 11.4, 11.8,
                    11.2, 10.3, 8.9, 7.1, 5.4, 4.1, 3.0, 2.3])

fig, (axM, axQ) = plt.subplots(1, 2, figsize=(8.6, 3.6),
                               gridspec_kw={"width_ratios": [1.6, 1]})

axM.scatter(xs, ys, s=4, c=colors, linewidths=0)
axM.scatter(tower_x, tower_y, s=8, color=PALETTE[1], zorder=3)
axM.axhline(GW, ls="--", color=PALETTE[1], lw=1.0)
axM.text(5, GW + 0.25, r"genome-wide significance  $5\times10^{-8}$",
         fontsize=8, color=PALETTE[1])
axM.annotate("tower of correlated\nSNPs — a real signal",
             xy=(tower_center, 11.9), xytext=(tower_center - 640, 9.6),
             fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axM.set_xlabel("genomic position (alternating chromosomes)")
axM.set_ylabel(r"$-\log_{10} p$")
axM.set_title("Manhattan plot", fontsize=10)
axM.set_xticks([])
axM.set_ylim(0, 13)
axM.grid(axis="x", visible=False)

# ---- QQ plots -------------------------------------------------------------
m = 3000
expected = -np.log10((np.arange(1, m + 1) - 0.5) / m)


def qq(inflation, n_hits=6):
    z = rng.normal(0, np.sqrt(inflation), size=m)
    p = 2 * stats.norm.sf(np.abs(z))
    idx = rng.choice(m, n_hits, replace=False)
    p[idx] = 10.0 ** (-rng.uniform(8, 12, n_hits))      # a few genuine hits
    lam = np.median(stats.chi2.isf(p, 1)) / 0.4549
    return -np.log10(np.sort(p)), lam


obs_ok, lam_ok = qq(1.0)
obs_bad, lam_bad = qq(1.35)

lim = max(expected.max(), obs_ok.max(), obs_bad.max()) + 0.5
axQ.plot([0, lim], [0, lim], ls="--", color=MUTED, lw=1.0)
axQ.scatter(expected, obs_bad, s=6, color=PALETTE[1],
            label=fr"confounded, $\lambda={lam_bad:.2f}$")
axQ.scatter(expected, obs_ok, s=6, color=PALETTE[0],
            label=fr"well controlled, $\lambda={lam_ok:.2f}$")
axQ.set_xlabel(r"expected $-\log_{10} p$")
axQ.set_ylabel(r"observed $-\log_{10} p$")
axQ.set_title("QQ plot", fontsize=10)
axQ.set_xlim(0, lim)
axQ.set_ylim(0, lim)
axQ.legend(loc="upper left", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/gwas.svg")
