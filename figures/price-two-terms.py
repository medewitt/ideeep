# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Schematic of the two-term Price decomposition.

The change in the mean of a trait z from one generation to the next splits
exactly into a SELECTION term (the covariance between fitness w and trait z)
and a TRANSMISSION term (the fitness-weighted change of trait between
ancestors and their descendants, e.g. mutation bias):

    wbar * dzbar = Cov(w, z) + E(w * dz).

Left: selection as a covariance -- ancestors with a higher trait leave more
descendants, so the fitness-weighted mean shifts up. Right: a waterfall that
adds the selection and transmission contributions to reach the total change."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.0, 4.2),
                               gridspec_kw={"width_ratios": [1.05, 1.0]})

# ---- Left: selection as a covariance between fitness and trait ----
rng = np.random.default_rng(3)
z = np.array([1.0, 1.6, 2.1, 2.6, 3.1, 3.5, 4.0, 4.6])
w = 0.9 + 0.7 * (z - z.mean()) + rng.normal(0, 0.25, z.size)   # fitness rises with trait
w = np.clip(w, 0.2, None)

axL.scatter(z, w, s=90, color=PALETTE[0], zorder=3, edgecolor="white", linewidth=1.1)
b, a = np.polyfit(z, w, 1)
zz = np.linspace(z.min() - 0.2, z.max() + 0.2, 50)
axL.plot(zz, a + b * zz, color=PALETTE[1], lw=2.0, zorder=2,
         label=f"slope $=\\mathrm{{Cov}}(w,z)/\\mathrm{{Var}}(z)>0$")
axL.axhline(w.mean(), color=MUTED, lw=0.8, ls=":")
axL.set_title("Selection: $\\mathrm{Cov}(w, z)$", fontsize=11)
axL.set_xlabel("ancestor trait  $z_i$")
axL.set_ylabel("fitness  $w_i$  (number of descendants)")
axL.legend(fontsize=8.5, loc="upper left")
axL.annotate("higher-trait ancestors\nleave more descendants",
             xy=(4.0, a + b * 4.0), xytext=(1.6, 2.4), fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))

# ---- Right: waterfall from parental mean to offspring mean ----
zbar = 2.5                     # parental mean trait
sel = 0.55                     # selection contribution  Cov(w,z)/wbar
trans = -0.15                  # transmission / mutation bias  E(w dz)/wbar
zprime = zbar + sel + trans

axR.set_xlim(0, 4)
axR.set_ylim(zbar - 0.6, zbar + 0.9)
bar_kw = dict(width=0.55, edgecolor=INK, linewidth=1.0)

axR.bar(0.5, zbar, color="#c9d4dd", **bar_kw)
axR.bar(1.5, sel, bottom=zbar, color=PALETTE[0], **bar_kw)
axR.bar(2.5, trans, bottom=zbar + sel, color=PALETTE[3], **bar_kw)
axR.bar(3.5, zprime, color="#c9d4dd", **bar_kw)

# connector lines
for x0, y0 in [(0.5, zbar), (1.5, zbar + sel), (2.5, zbar + sel + trans)]:
    axR.plot([x0 + 0.275, x0 + 0.725], [y0, y0], color=MUTED, lw=0.9, ls="--")

axR.annotate(f"$+\\,\\mathrm{{Cov}}(w,z)/\\bar w$", xy=(1.5, zbar + sel + 0.03),
             ha="center", va="bottom", fontsize=8.5, color=PALETTE[0])
axR.annotate(f"$+\\,\\mathbb{{E}}(w\\,\\Delta z)/\\bar w$", xy=(2.5, zbar + sel + 0.02),
             ha="center", va="top", fontsize=8.5, color=PALETTE[3])
axR.axhline(zbar, color=MUTED, lw=0.7, ls=":")

axR.set_xticks([0.5, 1.5, 2.5, 3.5])
axR.set_xticklabels(["parental\n$\\bar z$", "selection", "transmission", "offspring\n$\\bar z'$"],
                    fontsize=9)
axR.set_ylabel("mean trait")
axR.set_title("$\\bar z' - \\bar z = \\Delta\\bar z$  (two contributions)", fontsize=11)
axR.grid(axis="x", visible=False)

fig.suptitle("The Price equation partitions trait change into selection + transmission",
             fontweight="bold")
fig.tight_layout()
save(fig, "assets/figures/price-two-terms.svg")
