# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""A worked selection-differential example that verifies the Price identity.

A small population of eight ancestral lineages, each with a trait z (say a
pathogen replication rate) and a realized fitness w (number of descendants).
Descendants also carry a small, systematic transmission bias dz (mutation).
Left: a genealogy strip -- ancestors on top at their trait z, descendants
below (count = w), nudged by dz. Right: the exact bookkeeping showing that
Cov(w, z) + E(w*dz) equals wbar * (zbar' - zbar)."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(7)

# ---- a small population ----
z = np.array([2.0, 2.5, 3.0, 3.0, 3.5, 4.0, 4.5, 5.0])       # ancestor trait
w = np.array([1,   2,   1,   3,   3,   4,   4,   5])          # descendants (fitness)
dz = np.full(z.size, -0.12)                                   # transmission bias (mutation)

n = z.size
wbar, zbar = w.mean(), z.mean()
# descendant mean trait: fitness-weighted parent trait shifted by dz
zbar_prime = (w * (z + dz)).sum() / w.sum()
dzbar = zbar_prime - zbar

cov_wz = ((w - wbar) * (z - zbar)).mean()          # selection term
trans = (w * dz).mean()                            # transmission term
lhs = wbar * dzbar

fig = plt.figure(figsize=(11.2, 4.4))
gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0], wspace=0.25)

# ---- Left: genealogy strip ----
axG = fig.add_subplot(gs[0, 0])
cmap = plt.cm.viridis
norm = plt.Normalize(z.min(), z.max())
for i in range(n):
    col = PALETTE[0]
    # ancestor marker (top)
    axG.scatter(z[i], 1.0, s=140, color=col, edgecolor="white", linewidth=1.2, zorder=4)
    # descendants (bottom), spread horizontally around z_i + dz_i
    xs = z[i] + dz[i] + np.linspace(-0.12, 0.12, w[i]) if w[i] > 1 else np.array([z[i] + dz[i]])
    axG.scatter(xs, np.full_like(xs, 0.0), s=42, color=PALETTE[1], alpha=0.9, zorder=4)
    for x in xs:
        axG.plot([z[i], x], [0.96, 0.04], color=MUTED, lw=0.6, alpha=0.6, zorder=2)

axG.axvline(zbar, color=PALETTE[0], lw=1.6, ls="--", zorder=3)
axG.axvline(zbar_prime, color=PALETTE[1], lw=1.6, ls="--", zorder=3)
axG.annotate("", xy=(zbar_prime, 1.28), xytext=(zbar, 1.28),
             arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
axG.text((zbar + zbar_prime) / 2, 1.35, f"$\\Delta\\bar z = {dzbar:+.3f}$",
         ha="center", va="bottom", fontsize=10, color=INK)
axG.text(zbar, -0.28, f"ancestors $\\bar z={zbar:.2f}$", ha="center", color=PALETTE[0], fontsize=9)
axG.text(zbar_prime, -0.42, f"descendants $\\bar z'={zbar_prime:.2f}$", ha="center",
         color=PALETTE[1], fontsize=9)
axG.set_ylim(-0.55, 1.55)
axG.set_yticks([0, 1]); axG.set_yticklabels(["descendants", "ancestors"], fontsize=9)
axG.set_xlabel("trait  $z$")
axG.set_title("Ancestors leave $w_i$ descendants, nudged by mutation $\\Delta z_i$", fontsize=10.5)
axG.grid(axis="y", visible=False)

# ---- Right: the identity as a bar chart ----
axB = fig.add_subplot(gs[0, 1])
parts = [cov_wz, trans]
labels = ["$\\mathrm{Cov}(w,z)$\nselection", "$\\mathbb{E}(w\\,\\Delta z)$\ntransmission"]
colors = [PALETTE[0], PALETTE[3]]
axB.bar([0, 1], parts, color=colors, edgecolor=INK, width=0.6)
axB.bar([2.4], [lhs], color="#c9d4dd", edgecolor=INK, width=0.6)
axB.axhline(0, color=MUTED, lw=0.8)
for x, val in zip([0, 1, 2.4], parts + [lhs]):
    axB.text(x, val + (0.03 if val >= 0 else -0.03), f"{val:+.3f}",
             ha="center", va="bottom" if val >= 0 else "top", fontsize=9)
axB.set_xticks([0, 1, 2.4])
axB.set_xticklabels(labels + ["$\\bar w\\,\\Delta\\bar z$\n(total)"], fontsize=9)
axB.set_ylabel("contribution")
axB.set_title(f"$\\mathrm{{Cov}}(w,z)+\\mathbb{{E}}(w\\Delta z) = \\bar w\\,\\Delta\\bar z$"
              f"\n${cov_wz:.3f}{trans:+.3f} = {lhs:.3f}$", fontsize=10)
axB.grid(axis="x", visible=False)

fig.suptitle("The Price equation is an exact identity, checked on eight lineages",
             fontweight="bold")
fig.tight_layout()
save(fig, "assets/figures/price-selection-differential.svg")

# console check
print("Cov(w,z) =", round(cov_wz, 6), " E(w dz) =", round(trans, 6))
print("sum =", round(cov_wz + trans, 6), " wbar*dzbar =", round(lhs, 6),
      " match:", np.isclose(cov_wz + trans, lhs))
