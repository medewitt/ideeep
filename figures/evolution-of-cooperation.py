# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Network reciprocity. Left: cooperation is favoured on a graph roughly when
b/c > <k>, so with a fixed benefit-to-cost ratio b/c = 3 the outcome flips with
connectivity — a sparse graph (<k>=2) lies in the cooperation region while a
denser one (<k>=4) does not. Right: the same contrast as neighbourhoods — on the
sparse graph a cooperator cluster is mutually supported and persists, while on
the dense graph each cooperator has more defector neighbours diluting the local
advantage, and defection takes over."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

COOP, DEF = PALETTE[2], PALETTE[1]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.8),
                               gridspec_kw={"width_ratios": [1, 1.1]})

# ---- b/c vs <k> threshold plane -------------------------------------------
k = np.linspace(0, 7, 100)
axL.fill_between(k, k, 8, color=COOP + "22", zorder=0)
axL.fill_between(k, 0, k, color=DEF + "18", zorder=0)
axL.plot(k, k, color=INK, lw=1.5)
axL.text(1.2, 6.4, "cooperation\nfavoured\n$b/c>\\langle k\\rangle$",
         fontsize=8.5, color=COOP)
axL.text(4.6, 1.3, "defection\nwins", fontsize=8.5, color=DEF)
axL.scatter([2], [3], s=70, color=COOP, zorder=5, edgecolor="white")
axL.annotate(r"$\langle k\rangle=2$, $b/c=3$ ✓", xy=(2, 3), xytext=(2.2, 4.2),
             fontsize=8, color=INK)
axL.scatter([4], [3], s=70, color=DEF, zorder=5, edgecolor="white")
axL.annotate(r"$\langle k\rangle=4$, $b/c=3$ ✗", xy=(4, 3), xytext=(4.1, 3.4),
             fontsize=8, color=INK)
axL.axhline(3, ls=":", color=MUTED, lw=1.0)
axL.set_xlabel(r"mean degree $\langle k\rangle$")
axL.set_ylabel(r"benefit-to-cost ratio $b/c$")
axL.set_title("Same $b/c$, opposite outcomes", fontsize=9.5)
axL.set_xlim(0, 7)
axL.set_ylim(0, 8)
axL.grid(False)

# ---- two neighbourhood snapshots ------------------------------------------
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.axis("off")
axR.set_title("Cluster persists (sparse) vs invaded (dense)", fontsize=9.5)


def node(x, y, coop, r=0.42):
    axR.add_patch(Circle((x, y), r, facecolor=(COOP if coop else DEF),
                  edgecolor="white", lw=1.0, zorder=5))


# sparse ring (top): degree 2, contiguous cooperator cluster survives
axR.text(2.5, 9.3, "sparse ⟨k⟩=2", ha="center", fontsize=8.5, color=COOP)
ang = np.linspace(0, 2 * np.pi, 9)[:-1] + np.pi / 2
cx, cy, R = 2.5, 6.7, 1.7
xs, ys = cx + R * np.cos(ang), cy + R * np.sin(ang)
for i in range(8):
    j = (i + 1) % 8
    axR.plot([xs[i], xs[j]], [ys[i], ys[j]], color=MUTED, lw=0.8, zorder=1)
coop_mask = [True, True, True, True, False, False, False, False]
for i in range(8):
    node(xs[i], ys[i], coop_mask[i])

# dense graph (bottom): degree ~4, cooperators surrounded -> invaded
axR.text(7.2, 9.3, "dense ⟨k⟩=4", ha="center", fontsize=8.5, color=DEF)
cx2, cy2 = 7.2, 6.7
xs2, ys2 = cx2 + R * np.cos(ang), cy2 + R * np.sin(ang)
for i in range(8):
    for d in (1, 2):                     # each node linked to 2 on each side
        j = (i + d) % 8
        axR.plot([xs2[i], xs2[j]], [ys2[i], ys2[j]], color=MUTED, lw=0.6,
                 zorder=1)
coop_mask2 = [True, False, False, True, False, False, True, False]
for i in range(8):
    node(xs2[i], ys2[i], coop_mask2[i])

axR.scatter([], [], color=COOP, label="cooperator")
axR.scatter([], [], color=DEF, label="defector")
axR.legend(fontsize=8, loc="lower center", ncol=2)

fig.tight_layout()
save(fig, "assets/figures/evolution-of-cooperation.svg")
