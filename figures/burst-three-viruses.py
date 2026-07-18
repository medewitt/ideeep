# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""HIV, influenza, and hantavirus as three cellular life-history strategies.

Left: cumulative virions produced by one infected cell over time. The lifetime
yield B = (production rate) x (production window) is reached three different
ways -- influenza fast then lyses, HIV moderate then the cell dies, hantavirus
slow but non-cytopathic so the window stays open (persistence). Right: each
virus on the burst-size / mutation-rate plane, with diagonals of constant
per-cell mutational output B*mu.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.0, 4.0))

# --- Left: cumulative production, three strategies ------------------------
t = np.linspace(0, 10, 800)   # days


def sat(t, ecl, Bmax, tau):
    return np.where(t > ecl, Bmax * (1 - np.exp(-(t - ecl) / tau)), 0.0)


# influenza: short eclipse, fast build, cell lyses ~1 day
flu = np.ma.masked_where(t > 1.0, sat(t, 0.25, 5e3, 0.25))
# HIV: longer eclipse, large yield, infected cell dies ~2.2 days
hiv = np.ma.masked_where(t > 2.2, sat(t, 1.0, 5e4, 0.4))
# hantavirus: slow, non-cytopathic -> window stays open for the whole plot
han = np.where(t > 1.0, 2e3 * (t - 1.0), 0.0)

axL.plot(t, flu, color=PALETTE[1], lw=2.3, label="influenza (lyses)")
axL.plot(t, hiv, color=PALETTE[0], lw=2.3, label="HIV (cell dies)")
axL.plot(t, han, color=PALETTE[2], lw=2.3, label="hantavirus (persists)")
axL.plot(1.0, sat(np.array([1.0]), 0.25, 5e3, 0.25)[0], "o", color=PALETTE[1], ms=6)
axL.plot(2.2, sat(np.array([2.2]), 1.0, 5e4, 0.4)[0], "o", color=PALETTE[0], ms=6)
axL.annotate("no lysis:\nwindow stays open", xy=(9.4, 2e3 * 8.4), xytext=(4.6, 6e4),
             fontsize=7.6, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
axL.set_yscale("log")
axL.set_xlabel("time since infection (days)")
axL.set_ylabel("cumulative virions per cell")
axL.set_title("$B$ = rate $\\times$ window")
axL.set_xlim(0, 10)
axL.set_ylim(1, 2e5)
axL.legend(fontsize=8, loc="lower right")

# --- Right: burst size vs mutation rate, constant-B*mu diagonals ----------
B_lo, B_hi = 1e1, 1e5
mu_lo, mu_hi = 3e-6, 1e-3
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
    bl = np.exp(0.62 * np.log(b0) + 0.38 * np.log(b1))
    t = axR.text(bl, Bmu / bl, f"$B\\mu={Bmu:g}$", fontsize=6.8, color=MUTED,
                 rotation_mode="anchor", ha="center", va="bottom")
    diag_labels.append(t)

pts = [("HIV",        5e4, 2.5e-5, PALETTE[0], (6, 6)),
       ("influenza",  3e3, 2.0e-4, PALETTE[1], (-4, 8)),
       ("hantavirus", 5e2, 1.0e-5, PALETTE[2], (8, -4))]
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
