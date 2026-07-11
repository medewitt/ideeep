# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Heritability from twins. Left: identical (MZ) twins correlate more strongly
than fraternal (DZ) twins, and because DZ pairs share only half the additive
variance, doubling the gap gives Falconer's estimate h^2 = 2(r_MZ - r_DZ) =
2(0.80-0.50) = 0.60. Right: the ACE variance decomposition that follows
(h^2=0.60, c^2=0.20, e^2=0.20), alongside a lower SNP-heritability bar whose gap
to the twin estimate is the 'missing heritability'."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

r_mz, r_dz = 0.80, 0.50
h2 = 2 * (r_mz - r_dz)      # 0.60
c2 = 2 * r_dz - r_mz        # 0.20
e2 = 1 - r_mz               # 0.20

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- twin correlations ----------------------------------------------------
axL.bar([0, 1], [r_mz, r_dz], width=0.5, color=[PALETTE[0], PALETTE[2]])
axL.annotate("", xy=(1, r_mz), xytext=(1, r_dz),
             arrowprops=dict(arrowstyle="<->", color=PALETTE[1], lw=1.4))
axL.text(1.32, (r_mz + r_dz) / 2, r"gap $=0.30$" + "\n" +
         r"$h^2=2\times0.30=0.60$", fontsize=8.5, color=PALETTE[1],
         va="center")
axL.plot([1, 1], [r_mz, r_mz], marker="_")
axL.axhline(r_mz, xmin=0.08, xmax=0.5, ls=":", color=MUTED, lw=1.0)
for x, v, lab in [(0, r_mz, "MZ (identical)"), (1, r_dz, "DZ (fraternal)")]:
    axL.annotate(f"{v:.2f}", (x, v), textcoords="offset points",
                 xytext=(0, 4), ha="center", fontsize=9, color=INK)
axL.set_xticks([0, 1])
axL.set_xticklabels(["MZ", "DZ"])
axL.set_ylabel("within-pair trait correlation")
axL.set_title("Falconer's twin comparison", fontsize=10)
axL.set_ylim(0, 1.0)
axL.grid(axis="x", visible=False)

# ---- ACE decomposition + SNP-heritability ---------------------------------
snp_h2 = 0.42                 # illustrative: below twin h^2
axR.bar([0], [h2], width=0.55, color=PALETTE[0], label=r"additive $h^2$")
axR.bar([0], [c2], width=0.55, bottom=h2, color=PALETTE[2],
        label=r"shared env. $c^2$")
axR.bar([0], [e2], width=0.55, bottom=h2 + c2, color=MUTED,
        label=r"unique env. $e^2$")
axR.bar([1], [snp_h2], width=0.55, color=PALETTE[0] + "99")
axR.annotate("", xy=(1, h2), xytext=(1, snp_h2),
             arrowprops=dict(arrowstyle="<->", color=PALETTE[1], lw=1.3))
axR.text(1.05, (h2 + snp_h2) / 2, "missing\nheritability", fontsize=8,
         color=PALETTE[1], va="center")
axR.axhline(h2, ls=":", color=MUTED, lw=1.0)
axR.set_xticks([0, 1])
axR.set_xticklabels(["twin\ndecomposition", "SNP-$h^2$"], fontsize=8.5)
axR.set_ylabel("share of phenotypic variance")
axR.set_title("Variance components", fontsize=10)
axR.set_ylim(0, 1.0)
axR.legend(fontsize=7.8, loc="upper right")
axR.grid(axis="x", visible=False)

fig.tight_layout()
save(fig, "assets/figures/heritability.svg")
