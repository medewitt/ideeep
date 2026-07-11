# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "scikit-learn", "statsmodels"]
# ///
"""Controlling population stratification with PCA. Left: the two simulated
subpopulations separate along the leading principal component of the genome-wide
genotypes, so PC1 is the axis of ancestry. Right: a candidate SNP with no true
effect looks strongly (spuriously) associated when tested alone, but adding the
top PCs as covariates collapses the association back toward null — the p-value
falls from far past the genome-wide line to non-significant."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import statsmodels.api as sm  # noqa: F401 (kept parallel to the page; not required)
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(42)

n = 600
pop = np.array([0] * 300 + [1] * 300)                 # 0 = A, 1 = B
G = np.column_stack([
    rng.binomial(2, np.where(pop == 0, rng.uniform(.5, .8), rng.uniform(.1, .4)))
    for _ in range(200)]).astype(float)
snp = rng.binomial(2, np.where(pop == 0, 0.7, 0.2)).astype(float)
y = (pop == 0).astype(float) + rng.normal(size=n)     # trait differs by pop only

Zs = (G - G.mean(0)) / G.std(0)
pcs = PCA(n_components=2, svd_solver="full").fit_transform(Zs)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- PC1 vs PC2 -----------------------------------------------------------
for p, col, lab in [(0, PALETTE[0], "population A"), (1, PALETTE[1], "population B")]:
    axL.scatter(pcs[pop == p, 0], pcs[pop == p, 1], s=10, color=col + "aa",
                linewidths=0, label=lab)
axL.set_xlabel("PC1  (axis of ancestry)")
axL.set_ylabel("PC2")
axL.set_title("Leading PCs are the axes of ancestry", fontsize=9.5)
axL.legend(fontsize=8.3, loc="upper right")

# ---- before/after p-value -------------------------------------------------
def pval(X):
    fit = sm.OLS(y, sm.add_constant(X)).fit()
    return fit.pvalues[1]

p_raw = pval(snp)
p_adj = pval(np.column_stack([snp, pcs]))
gw = -np.log10(5e-8)
vals = [-np.log10(p_raw), -np.log10(p_adj)]
axR.bar([0, 1], vals, width=0.55, color=[PALETTE[1], PALETTE[0]])
axR.axhline(gw, ls="--", color=MUTED, lw=1.2)
axR.text(1.4, gw + 0.3, "genome-wide 5×10⁻⁸", fontsize=7.6, color=MUTED,
         ha="right")
for x, pv in [(0, p_raw), (1, p_adj)]:
    axR.annotate(f"p = {pv:.2g}", (x, -np.log10(pv)),
                 textcoords="offset points", xytext=(0, 4), ha="center",
                 fontsize=8.5, color=INK)
axR.set_xticks([0, 1])
axR.set_xticklabels(["SNP alone\n(spurious)", "SNP + PCs\n(adjusted)"],
                    fontsize=8.5)
axR.set_ylabel(r"$-\log_{10} p$ for the SNP")
axR.set_title("PCs absorb the spurious association", fontsize=9.5)
axR.set_ylim(0, max(vals) * 1.2)
axR.grid(axis="x", visible=False)

fig.tight_layout()
save(fig, "assets/figures/population-stratification.svg")
