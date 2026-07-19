# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Viruses as cellular life-history strategies (colour = strategy, not identity).

Colour encodes the *strategy* a virus uses to exploit the cell -- lytic burst,
acute budding, syncytial (bud then fuse the cell into a dying syncytium), or
persistent (non-cytopathic) -- rather than one hue per virus, so the figure
stays legible as viruses are added; individuals are read from direct labels
and the accompanying table.

Left: cumulative virions produced by one infected cell over time. The lifetime
yield B = (production rate) x (production window) is reached different ways --
poliovirus fastest, in a lytic burst; the acute budders (HIV, influenza,
dengue) build then kill the cell; the syncytial paramyxo/pneumoviruses
(measles, mumps, RSV, and the henipaviruses Nipah and Hendra) fuse cells into
dying syncytia; variola (a DNA poxvirus) builds in cytoplasmic factories and is
freed on lysis; and hantavirus persists, so its window stays open. Right: each
virus on the burst-size / mutation-rate plane, with diagonals of constant
per-cell mutational output B*mu; variola sits far below the RNA viruses, its
proofreading DNA polymerase holding the per-site rate near 1e-6.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 4.2))

# Colour encodes life-history STRATEGY, not virus identity, so the figure
# scales to any number of viruses: individuals are read from direct labels and
# the table, while colour groups them by how they exploit the cell.
STRAT = {
    "lytic":      (PALETTE[1], "lytic burst"),          # released at lysis (Poisson offspring)
    "acute":      (PALETTE[0], "acute budding"),         # continuous budding, cell dies
    "syncytial":  (PALETTE[3], "syncytial (fuse + die)"),
    "persistent": (PALETTE[2], "persistent"),            # non-cytopathic, window stays open
}


def sat(t, ecl, Bmax, tau):
    return np.where(t > ecl, Bmax * (1 - np.exp(-(t - ecl) / tau)), 0.0)


# name, strategy, production model (left panel), burst B, per-site mu (right panel)
#   "sat" model = (eclipse, Bmax, tau, t_death);  "lin" model = (rate, t_start)
VIRUSES = [
    ("HIV",        "acute",      ("sat", 1.00, 5e4, 0.40, 2.2),  5e4,   2.5e-5),
    ("influenza",  "acute",      ("sat", 0.25, 5e3, 0.25, 1.0),  3e3,   2.0e-4),
    ("dengue",     "acute",      ("sat", 0.70, 5e3, 0.60, 3.2),  5e3,   1.2e-4),
    ("hantavirus", "persistent", ("lin", 2e3, 1.0),              5e2,   1.0e-5),
    ("poliovirus", "lytic",      ("sat", 0.10, 3e4, 0.06, 0.3),  3e4,   2.0e-4),
    ("variola",    "lytic",      ("sat", 0.30, 1e4, 0.50, 2.0),  1e4,   1.5e-6),
    ("measles",    "syncytial",  ("sat", 0.50, 1e3, 0.60, 3.0),  1e3,   1.0e-4),
    ("mumps",      "syncytial",  ("sat", 0.50, 1.5e3, 0.55, 2.8), 1.7e3, 1.8e-4),
    ("RSV",        "syncytial",  ("sat", 0.50, 8e2, 0.50, 2.5),  8e2,   6.0e-5),
    ("Nipah",      "syncytial",  ("sat", 0.50, 7e3, 0.60, 2.5),  7e3,   8.0e-5),
    ("Hendra",     "syncytial",  ("sat", 0.50, 3.5e3, 0.60, 2.3), 3.5e3, 6.0e-5),
]

# --- Left: cumulative production over time, coloured by strategy -----------
t = np.linspace(0, 10, 800)   # days
for name, strat, model, B, mu in VIRUSES:
    color = STRAT[strat][0]
    if model[0] == "sat":
        _, ecl, Bmax, tau, td = model
        axL.plot(t, np.ma.masked_where(t > td, sat(t, ecl, Bmax, tau)),
                 color=color, lw=1.8, alpha=0.95)
        axL.plot(td, sat(np.array([td]), ecl, Bmax, tau)[0], "o", color=color, ms=5)
    else:
        _, rate, t0 = model
        axL.plot(t, np.where(t > t0, rate * (t - t0), 0.0), color=color, lw=1.8)

# direct labels for a few landmark curves (the rest read from the right panel)
for name, x, y, dx, dy in [("poliovirus", 0.30, 3e4, 5, 5),
                           ("HIV", 2.20, 5e4, 5, 3),
                           ("variola", 2.00, 1e4, 5, 2),
                           ("Nipah", 2.50, 5e3, 5, 1)]:
    axL.annotate(name, xy=(x, y), xytext=(dx, dy), textcoords="offset points",
                 fontsize=7.0, color=INK)

axL.annotate("hantavirus:\nno lysis, window stays open", xy=(9.4, 2e3 * 8.4),
             xytext=(4.2, 6.5e4), fontsize=7.2, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
axL.set_yscale("log")
axL.set_xlabel("time since infection (days)")
axL.set_ylabel("cumulative virions per cell")
axL.set_title("$B$ = rate $\\times$ window")
axL.set_xlim(0, 10)
axL.set_ylim(1, 2e5)
handles = [Line2D([0], [0], color=c, lw=2.6) for c, _ in STRAT.values()]
axL.legend(handles, [lab for _, lab in STRAT.values()], fontsize=7.4,
           loc="lower right", title="life-history strategy", title_fontsize=7.4)

# --- Right: burst size vs mutation rate, coloured by strategy --------------
B_lo, B_hi = 1e1, 1e5
mu_lo, mu_hi = 3e-7, 1e-3   # floor lowered to fit variola's DNA-virus mutation rate
axR.set_xscale("log")
axR.set_yscale("log")
axR.set_xlim(B_lo, B_hi)
axR.set_ylim(mu_lo, mu_hi)

diag_labels = []
for Bmu in (1e-2, 1e-1, 1.0, 10.0):
    axR.plot([B_lo, B_hi], [Bmu / B_lo, Bmu / B_hi], color=MUTED, lw=0.8, ls=":")
    b0, b1 = max(B_lo, Bmu / mu_hi), min(B_hi, Bmu / mu_lo)
    bl = np.exp(0.5 * np.log(b0) + 0.5 * np.log(b1))
    diag_labels.append(axR.text(bl, Bmu / bl, f"$B\\mu={Bmu:g}$", fontsize=6.6,
                       color=MUTED, rotation_mode="anchor", ha="center", va="bottom"))

# per-virus label offsets (pt); leader=True draws a thin line in the dense cluster
LABELS = {
    "HIV":        (10, -3, "left",  False),
    "influenza":  (2, 11, "center", False),
    "dengue":     (11, 3, "left",  False),
    "hantavirus": (9, -3, "left",  False),
    "poliovirus": (-8, 2, "right", False),
    "variola":    (9, -2, "left",  False),
    "measles":    (-40, 0, "right", True),
    "mumps":      (-8, 9, "right", False),
    "RSV":        (-14, -18, "right", True),
    "Nipah":      (16, -14, "left",  True),
    "Hendra":     (-4, -18, "center", True),
}
for name, strat, model, B, mu in VIRUSES:
    color = STRAT[strat][0]
    axR.plot(B, mu, "o", color=color, ms=8.5)
    dx, dy, ha, leader = LABELS[name]
    axR.annotate(name, xy=(B, mu), xytext=(dx, dy), textcoords="offset points",
                 fontsize=7.6, color=INK, ha=ha,
                 arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6) if leader else None)

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
for tl in diag_labels:
    tl.set_rotation(diag_deg)

save(fig, "assets/figures/burst-three-viruses.svg")
