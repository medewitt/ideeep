# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Linkage disequilibrium. Left: D decays geometrically, D_t = D_0 (1-c)^t, so
tightly linked loci (small c) retain LD for many generations while unlinked loci
(c = 0.5) lose half of any remaining D each generation. Right: the worked
example's haplotype frequencies (observed) sit away from the product of allele
frequencies (expected under independence), and that gap is D = 0.15."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- geometric decay ------------------------------------------------------
D0 = 0.15
t = np.arange(0, 21)
for c, col in zip([0.01, 0.1, 0.5], [PALETTE[0], PALETTE[2], PALETTE[1]]):
    axL.plot(t, D0 * (1 - c) ** t, color=col, lw=1.9, marker="o", ms=3,
             label=fr"$c={c}$")
axL.set_xlabel("generations $t$")
axL.set_ylabel(r"linkage disequilibrium $D_t$")
axL.set_title(r"Decay under recombination  $D_t=D_0(1-c)^t$", fontsize=10)
axL.legend(title="recombination fraction", fontsize=8.5, title_fontsize=8.5)
axL.set_ylim(0, 0.16)

# ---- observed vs expected haplotype frequencies ---------------------------
labels = ["AB", "Ab", "aB", "ab"]
observed = np.array([0.4, 0.1, 0.1, 0.4])
pA, pB = 0.5, 0.5
expected = np.array([pA * pB, pA * (1 - pB), (1 - pA) * pB, (1 - pA) * (1 - pB)])

x = np.arange(4)
w = 0.38
axR.bar(x - w / 2, observed, width=w, color=PALETTE[0], label="observed")
axR.bar(x + w / 2, expected, width=w, color=MUTED,
        label=r"expected $p_A p_B$ (independence)")

# annotate the AB departure = D
axR.annotate("", xy=(0 - w / 2, 0.40), xytext=(0 - w / 2, 0.25),
             arrowprops=dict(arrowstyle="<->", color=PALETTE[1], lw=1.3))
axR.text(0.15, 0.325, r"$D=p_{AB}-p_Ap_B$" + "\n$=0.40-0.25=0.15$",
         fontsize=8.5, color=PALETTE[1], va="center")
axR.text(3.0, 0.44, r"$r^2=0.36$", fontsize=9, color=INK, ha="center")

axR.set_xticks(x)
axR.set_xticklabels([f"$p_{{{l}}}$" for l in labels])
axR.set_ylabel("haplotype frequency")
axR.set_title("Departure from independence", fontsize=10)
axR.set_ylim(0, 0.52)
axR.legend(fontsize=8.5, loc="upper left")
axR.grid(axis="x", visible=False)

fig.tight_layout()
save(fig, "assets/figures/linkage-disequilibrium.svg")
