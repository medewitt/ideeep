# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Hardy-Weinberg equilibrium. Left: the genotype frequencies are the terms of
(p+q)^2 — f(AA)=p^2, f(Aa)=2pq, f(aa)=q^2 — with the heterozygote frequency
peaking at 0.5 when p=0.5. Right: starting from three arbitrary genotype
distributions, the heterozygote frequency jumps to the Hardy-Weinberg value 2pq
after a single generation of random mating and stays there, regardless of where
it began."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- HWE proportion curves ------------------------------------------------
p = np.linspace(0, 1, 300)
axL.plot(p, p**2, color=PALETTE[0], lw=2.0, label=r"$f(AA)=p^2$")
axL.plot(p, 2 * p * (1 - p), color=PALETTE[1], lw=2.0, label=r"$f(Aa)=2pq$")
axL.plot(p, (1 - p)**2, color=PALETTE[2], lw=2.0, label=r"$f(aa)=q^2$")
axL.axvline(0.5, ls="--", color=MUTED, lw=1.0)
axL.scatter([0.5], [0.5], s=36, color=PALETTE[1], zorder=5)
axL.annotate("heterozygotes\npeak at 0.5", xy=(0.5, 0.5), xytext=(0.56, 0.62),
             fontsize=8.5, color=INK)
axL.set_xlabel("allele frequency $p$")
axL.set_ylabel("genotype frequency")
axL.set_title("Hardy–Weinberg proportions", fontsize=10)
axL.set_xlim(0, 1)
axL.set_ylim(0, 1.02)
axL.legend(fontsize=8.5, loc="upper center")

# ---- convergence in one generation ----------------------------------------
def het_trajectory(fAA, fAa, faa, gens=6):
    p = fAA + 0.5 * fAa            # allele frequency (constant under random mating)
    het = [fAa]
    for _ in range(gens):
        het.append(2 * p * (1 - p))   # HW heterozygosity from gen 1 onward
    return np.array(het)

starts = [(0.9, 0.0, 0.1), (0.0, 0.4, 0.6), (0.3, 0.6, 0.1)]
cols = [PALETTE[0], PALETTE[2], PALETTE[3]]
t = np.arange(0, 7)
for (fAA, fAa, faa), col in zip(starts, cols):
    axR.plot(t, het_trajectory(fAA, fAa, faa), color=col, lw=1.8, marker="o",
             ms=4, label=fr"start ({fAA:g}, {fAa:g}, {faa:g})")
axR.set_xlabel("generation")
axR.set_ylabel("heterozygote frequency $f(Aa)$")
axR.set_title("Equilibrium reached in one generation", fontsize=10)
axR.set_ylim(0, 0.55)
axR.legend(fontsize=7.8, title="initial (AA, Aa, aa)", title_fontsize=7.8,
           loc="upper right")

fig.tight_layout()
save(fig, "assets/figures/hardy-weinberg.svg")
