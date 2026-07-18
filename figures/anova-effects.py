# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "scipy"]
# ///
"""The variance partition and the F-test for the worked ANOVA example. Left: SSB
and SSW stack to SST, and dividing by their degrees of freedom gives the mean
squares whose ratio is F. Right: the F(2,9) reference density with the 5% critical
value at 4.26 and the observed F of 14.0 far into the upper tail."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# worked example
groups = {"A": [8, 9, 7, 8], "B": [10, 11, 12, 11], "C": [9, 8, 10, 9]}
y = np.array([v for vs in groups.values() for v in vs], float)
grand = y.mean()
ssb = sum(len(v) * (np.mean(v) - grand) ** 2 for v in groups.values())
ssw = sum(((np.array(v) - np.mean(v)) ** 2).sum() for v in groups.values())
k, N = len(groups), y.size
df_b, df_w = k - 1, N - k
msb, msw = ssb / df_b, ssw / df_w
F = msb / msw
Fcrit = stats.f.ppf(0.95, df_b, df_w)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.7))

# ---- stacked SS decomposition --------------------------------------------
axL.bar(0, ssb, color=PALETTE[0], width=0.6, label=f"SSB = {ssb:.1f}")
axL.bar(0, ssw, bottom=ssb, color=PALETTE[1], width=0.6, label=f"SSW = {ssw:.1f}")
axL.bar(1, ssb + ssw, color=MUTED, width=0.6, alpha=0.5,
        label=f"SST = {ssb+ssw:.1f}")
axL.text(0, ssb / 2, f"MSB\n={msb:.2f}", ha="center", va="center", fontsize=8,
         color="white")
axL.text(0, ssb + ssw / 2, f"MSW\n={msw:.2f}", ha="center", va="center",
         fontsize=8, color="white")
axL.set_xticks([0, 1])
axL.set_xticklabels(["SSB + SSW", "SST"])
axL.set_ylabel("sum of squares")
axL.set_title(f"Partition  →  $F = {msb:.2f}/{msw:.2f} = {F:.1f}$", fontsize=9.5)
axL.legend(fontsize=7.8, loc="upper right")
axL.grid(axis="x", visible=False)

# ---- F distribution -------------------------------------------------------
xx = np.linspace(0, 16, 400)
axR.plot(xx, stats.f.pdf(xx, df_b, df_w), color=PALETTE[0], lw=2.0)
tail = xx[xx >= Fcrit]
axR.fill_between(tail, stats.f.pdf(tail, df_b, df_w), color=PALETTE[1], alpha=0.35)
axR.axvline(Fcrit, color=PALETTE[1], lw=1.4, ls="--")
axR.axvline(F, color=INK, lw=2.0)
axR.annotate(f"$F_{{crit}} = {Fcrit:.2f}$", xy=(Fcrit, 0.15), xytext=(Fcrit + 1.2,
             0.35), fontsize=8.3, color=PALETTE[1],
             arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.9))
axR.annotate(f"observed\n$F = {F:.1f}$", xy=(F, 0.02), xytext=(F - 4.5, 0.18),
             fontsize=8.3, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
axR.set_xlabel("F")
axR.set_ylabel("density")
axR.set_title("$F_{2,9}$ reference", fontsize=9.5)
axR.set_ylim(0, 0.8)

fig.tight_layout()
save(fig, "assets/figures/anova-effects.svg")
