# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Eight viruses as eight cellular life-history strategies.

Left: cumulative virions produced by one infected cell over time. The lifetime
yield B = (production rate) x (production window) is reached different ways --
poliovirus fastest, in a lytic burst; influenza fast then lyses; measles and
RSV bud but fuse cells into dying syncytia; dengue buds then the cell dies;
variola (a DNA poxvirus) builds in cytoplasmic factories and releases mainly on
lysis; HIV moderate then the cell dies; and hantavirus slow but non-cytopathic
so the window stays open (persistence). Right: each virus on the burst-size /
mutation-rate plane, with diagonals of constant per-cell mutational output B*mu
-- variola sits far below the RNA viruses, its proofreading DNA polymerase
holding the per-site rate near 1e-6.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.0, 4.0))

# two extra series colours beyond the shared 5-colour PALETTE (kept local so
# the shared style module -- and every other figure -- is left untouched)
RSV_C = "#1f9aa0"    # teal
DENV_C = "#b0436b"   # rose
VARIOLA_C = "#6d4c2f"  # umber -- the one DNA virus

# --- Left: cumulative production, five strategies -------------------------
t = np.linspace(0, 10, 800)   # days


def sat(t, ecl, Bmax, tau):
    return np.where(t > ecl, Bmax * (1 - np.exp(-(t - ecl) / tau)), 0.0)


# influenza: short eclipse, fast build, cell lyses ~1 day
flu = np.ma.masked_where(t > 1.0, sat(t, 0.25, 5e3, 0.25))
# HIV: longer eclipse, large yield, infected cell dies ~2.2 days
hiv = np.ma.masked_where(t > 2.2, sat(t, 1.0, 5e4, 0.4))
# hantavirus: slow, non-cytopathic -> window stays open for the whole plot
han = np.where(t > 1.0, 2e3 * (t - 1.0), 0.0)
# poliovirus: fast lytic cycle, large burst released at lysis ~7 h
polio = np.ma.masked_where(t > 0.3, sat(t, 0.1, 3e4, 0.06))
# measles: buds but cytopathic (syncytia); moderate yield, cell dies ~3 days
mea = np.ma.masked_where(t > 3.0, sat(t, 0.5, 1e3, 0.6))
# RSV: budding but strongly syncytial; low-infectivity yield, cell dies ~2.5 days
rsv = np.ma.masked_where(t > 2.5, sat(t, 0.5, 8e2, 0.5))
# dengue: budding through the secretory pathway, apoptotic; cell dies ~3 days
denv = np.ma.masked_where(t > 3.2, sat(t, 0.7, 5e3, 0.6))
# variola: large dsDNA poxvirus, cytoplasmic factories; released mainly on lysis ~2 days
var_ = np.ma.masked_where(t > 2.0, sat(t, 0.3, 1e4, 0.5))

axL.plot(t, flu, color=PALETTE[1], lw=2.3, label="influenza (lyses)")
axL.plot(t, hiv, color=PALETTE[0], lw=2.3, label="HIV (cell dies)")
axL.plot(t, han, color=PALETTE[2], lw=2.3, label="hantavirus (persists)")
axL.plot(t, polio, color=PALETTE[3], lw=2.3, label="poliovirus (lytic burst)")
axL.plot(t, mea, color=PALETTE[4], lw=2.3, label="measles (syncytia)")
axL.plot(t, rsv, color=RSV_C, lw=2.3, label="RSV (syncytia)")
axL.plot(t, denv, color=DENV_C, lw=2.3, label="dengue (cell dies)")
axL.plot(t, var_, color=VARIOLA_C, lw=2.3, label="variola (DNA, lyses)")
axL.plot(1.0, sat(np.array([1.0]), 0.25, 5e3, 0.25)[0], "o", color=PALETTE[1], ms=6)
axL.plot(2.2, sat(np.array([2.2]), 1.0, 5e4, 0.4)[0], "o", color=PALETTE[0], ms=6)
axL.plot(0.3, sat(np.array([0.3]), 0.1, 3e4, 0.06)[0], "o", color=PALETTE[3], ms=6)
axL.plot(3.0, sat(np.array([3.0]), 0.5, 1e3, 0.6)[0], "o", color=PALETTE[4], ms=6)
axL.plot(2.5, sat(np.array([2.5]), 0.5, 8e2, 0.5)[0], "o", color=RSV_C, ms=6)
axL.plot(3.2, sat(np.array([3.2]), 0.7, 5e3, 0.6)[0], "o", color=DENV_C, ms=6)
axL.plot(2.0, sat(np.array([2.0]), 0.3, 1e4, 0.5)[0], "o", color=VARIOLA_C, ms=6)
axL.annotate("no lysis:\nwindow stays open", xy=(9.4, 2e3 * 8.4), xytext=(4.9, 7e4),
             fontsize=7.6, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
axL.set_yscale("log")
axL.set_xlabel("time since infection (days)")
axL.set_ylabel("cumulative virions per cell")
axL.set_title("$B$ = rate $\\times$ window")
axL.set_xlim(0, 10)
axL.set_ylim(1, 2e5)
axL.legend(fontsize=7, loc="lower right", ncol=2, columnspacing=1.0,
           handlelength=1.4, labelspacing=0.3)

# --- Right: burst size vs mutation rate, constant-B*mu diagonals ----------
B_lo, B_hi = 1e1, 1e5
mu_lo, mu_hi = 3e-7, 1e-3   # floor lowered to fit variola's DNA-virus mutation rate
axR.set_xscale("log")
axR.set_yscale("log")
axR.set_xlim(B_lo, B_hi)
axR.set_ylim(mu_lo, mu_hi)

diag_labels = []
for Bmu in (1e-2, 1e-1, 1.0, 10.0):
    axR.plot([B_lo, B_hi], [Bmu / B_lo, Bmu / B_hi], color=MUTED, lw=0.8, ls=":")
    # anchor each label on the visible segment of its own diagonal, so no label
    # is pushed off the top of the plot the way a fixed left-edge anchor would be
    b0, b1 = max(B_lo, Bmu / mu_hi), min(B_hi, Bmu / mu_lo)
    bl = np.exp(0.5 * np.log(b0) + 0.5 * np.log(b1))
    t = axR.text(bl, Bmu / bl, f"$B\\mu={Bmu:g}$", fontsize=6.8, color=MUTED,
                 rotation_mode="anchor", ha="center", va="bottom")
    diag_labels.append(t)

pts = [("HIV",        5e4, 2.5e-5, PALETTE[0], (6, 6)),
       ("influenza",  3e3, 2.0e-4, PALETTE[1], (-4, 8)),
       ("hantavirus", 5e2, 1.0e-5, PALETTE[2], (8, -4)),
       ("poliovirus", 3e4, 2.0e-4, PALETTE[3], (-10, 8)),
       ("measles",    1e3, 1.0e-4, PALETTE[4], (-16, 7)),
       ("RSV",        8e2, 6.0e-5, RSV_C, (8, -3)),
       ("dengue",     5e3, 1.2e-4, DENV_C, (7, 3)),
       ("variola",    1e4, 1.5e-6, VARIOLA_C, (8, -3))]
for name, b, mu, color, (dx, dy) in pts:
    axR.plot(b, mu, "o", color=color, ms=9)
    axR.annotate(name, xy=(b, mu), xytext=(dx, dy), textcoords="offset points",
                 fontsize=8.5, color=INK)

axR.set_xlabel("burst size $B$ (virions/cell)")
axR.set_ylabel(r"per-site mutation rate $\mu$")
axR.set_title("per-cell mutational output")

fig.tight_layout()

# rotate each constant-B*mu label to match its diagonal's on-screen slope,
# measured after tight_layout so it tracks the final axes aspect ratio
fig.canvas.draw()
p0 = axR.transData.transform((B_lo, 1.0 / B_lo))
p1 = axR.transData.transform((B_hi, 1.0 / B_hi))
diag_deg = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
for t in diag_labels:
    t.set_rotation(diag_deg)

save(fig, "assets/figures/burst-three-viruses.svg")
