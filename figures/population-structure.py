# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Population structure and F_ST. Left: the Wahlund effect — pooling two
subpopulations (p1=0.7, p2=0.3) gives a pooled expected heterozygosity
H_T = 0.50 that exceeds the within-subpopulation mean H_S = 0.42; the shaded gap
is the heterozygosity lost to structure, and F_ST = (H_T-H_S)/H_T = 0.16. Right:
F_ST rises from 0 as the allele-frequency difference between two equal
subpopulations grows, shown against Wright's interpretive bands."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- Wahlund bar ----------------------------------------------------------
HS, HT = 0.42, 0.50
axL.bar([0], [HT], width=0.5, color=MUTED, label=r"$H_T$ pooled")
axL.bar([1], [HS], width=0.5, color=PALETTE[0], label=r"$H_S$ within")
# shade the deficit on the H_S bar up to H_T
axL.bar([1], [HT - HS], width=0.5, bottom=HS, color=PALETTE[1] + "44",
        hatch="//", edgecolor=PALETTE[1], label="lost to structure")
axL.annotate(r"$F_{ST}=\dfrac{H_T-H_S}{H_T}=\dfrac{0.08}{0.50}=0.16$",
             xy=(1, (HS + HT) / 2), xytext=(-0.35, 0.20), fontsize=8.8,
             color=INK)
axL.set_xticks([0, 1])
axL.set_xticklabels(["pooled\n$H_T=0.50$", "within\n$H_S=0.42$"], fontsize=8.5)
axL.set_ylabel("expected heterozygosity")
axL.set_title("The Wahlund heterozygote deficit", fontsize=10)
axL.set_ylim(0, 0.58)
axL.legend(fontsize=8, loc="upper right")
axL.grid(axis="x", visible=False)

# ---- F_ST vs allele-frequency difference ----------------------------------
d = np.linspace(0, 1, 200)             # |p1 - p2|, equal subpops
p1 = 0.5 + d / 2
p2 = 0.5 - d / 2
HS_d = 0.5 * (2 * p1 * (1 - p1) + 2 * p2 * (1 - p2))
HT_d = 2 * 0.5 * 0.5 * np.ones_like(d)  # pbar = 0.5 always here
FST_d = (HT_d - HS_d) / HT_d

bands = [(0, 0.05, "little", "#eef2f5"), (0.05, 0.15, "moderate", "#e3ebf1"),
         (0.15, 0.25, "great", "#d6e2ea"), (0.25, 1.0, "very great", "#c7d8e4")]
for lo, hi, lab, col in bands:
    axR.axhspan(lo, hi, color=col, zorder=0)
    axR.text(0.02, (lo + min(hi, 1.0)) / 2, lab, fontsize=7, color=MUTED,
             va="center")
axR.plot(d, FST_d, color=PALETTE[0], lw=2.0)
axR.scatter([0.4], [0.16], s=45, color=PALETTE[1], zorder=5)
axR.annotate("worked example\n$|p_1-p_2|=0.4,\\ F_{ST}=0.16$", xy=(0.4, 0.16),
             xytext=(0.44, 0.05), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axR.set_xlabel(r"allele-frequency difference $|p_1-p_2|$")
axR.set_ylabel(r"$F_{ST}$")
axR.set_title("How structure maps to $F_{ST}$", fontsize=10)
axR.set_xlim(0, 1)
axR.set_ylim(0, 1)
axR.grid(False)

fig.tight_layout()
save(fig, "assets/figures/population-structure.svg")
