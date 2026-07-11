# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Polygenic scores. Left: because a PGS sums many small independent allele
effects, its distribution across a population is approximately Gaussian by the
central limit theorem, and disease cases are shifted toward the high-score
right tail (so the top of the distribution carries elevated risk). Right: a
score trained in one ancestry transfers poorly — predictive accuracy is highest
in the (over-represented) European training ancestry and markedly lower in
others."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(7)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- PGS distribution, cases in the right tail ----------------------------
N = 40000
m = 400                                   # many small-effect SNPs
betas = rng.normal(0, 1, m) / np.sqrt(m)
X = rng.binomial(2, 0.3, size=(N, m)).astype(float)
pgs = X @ betas
pgs = (pgs - pgs.mean()) / pgs.std()      # standardize
# liability = PGS + noise; cases are the high-liability individuals
liability = pgs + rng.normal(0, 1.0, N)
case = liability > np.quantile(liability, 0.85)

bins = np.linspace(-4, 4, 41)
axL.hist(pgs, bins=bins, color=PALETTE[0] + "aa", edgecolor="white",
         linewidth=0.3, label="whole population")
axL.hist(pgs[case], bins=bins, color=PALETTE[1] + "cc", edgecolor="white",
         linewidth=0.3, label="disease cases")
axL.axvline(pgs.mean(), ls="--", color=MUTED, lw=1.0)
axL.annotate("cases shifted\ninto the right tail", xy=(1.6, 250),
             xytext=(1.1, 1700), fontsize=8, color=PALETTE[1],
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axL.text(-3.9, 2600, "≈ Gaussian\n(CLT over many SNPs)", fontsize=8,
         color=INK)
axL.set_xlabel("standardized polygenic score")
axL.set_ylabel("individuals")
axL.set_title("A PGS is an approximately normal risk axis", fontsize=9.5)
axL.legend(fontsize=8, loc="upper right")

# ---- transferability by ancestry ------------------------------------------
anc = ["European\n(training)", "South Asian", "East Asian", "African"]
r2 = [0.10, 0.065, 0.055, 0.032]
cols = [PALETTE[0], PALETTE[2], PALETTE[4], PALETTE[1]]
axR.bar(range(4), r2, color=cols, width=0.62)
for i, v in enumerate(r2):
    axR.annotate(f"{v:.3f}", (i, v), textcoords="offset points",
                 xytext=(0, 4), ha="center", fontsize=8.5, color=INK)
axR.set_xticks(range(4))
axR.set_xticklabels(anc, fontsize=7.6)
axR.set_ylabel(r"predictive $R^2$ in test set")
axR.set_title("Accuracy drops across ancestries", fontsize=9.5)
axR.set_ylim(0, 0.12)
axR.grid(axis="x", visible=False)

fig.tight_layout()
save(fig, "assets/figures/polygenic-scores.svg")
