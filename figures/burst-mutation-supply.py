# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Burst size as a mutational lottery: the supply of variation per cell.

Each of the B progeny genomes is copied with some per-site error rate mu, so
the expected number of progeny carrying a given point mutation is B*mu and the
chance the burst contains at least one such variant is 1 - (1 - mu)^B. Burst
size and mutation rate enter only through their product B*mu -- the per-cell
mutational output -- so a large burst is a large draw from sequence space.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

B = np.logspace(0, 4.5, 500)   # burst size, 1 .. ~30000

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.9, 3.5))

# Left: probability the burst contains >=1 copy of a specific escape mutation.
for mu, color in zip([1e-5, 1e-4, 1e-3], PALETTE[:3]):
    P = 1.0 - (1.0 - mu) ** B
    axL.plot(B, P, color=color, lw=2.2, label=fr"$\mu = 10^{{{int(np.log10(mu))}}}$")
axL.set_xscale("log")
axL.set_xlabel("burst size $B$")
axL.set_ylabel(r"P(escape variant in burst)")
axL.set_title("one site: $1-(1-\\mu)^B$")
axL.set_ylim(-0.02, 1.03)
axL.legend(fontsize=8.5, loc="upper left")

# Right: expected mutant progeny per cell, B * mu, on log-log axes.
for mu, color in zip([1e-5, 1e-4, 1e-3], PALETTE[:3]):
    axR.plot(B, B * mu, color=color, lw=2.2)
axR.axhline(1.0, color=MUTED, lw=1.0, ls="--")
axR.set_xscale("log")
axR.set_yscale("log")
axR.set_xlabel("burst size $B$")
axR.set_ylabel(r"expected mutants per cell $B\mu$")
axR.set_title("the per-cell mutational output")
axR.annotate("one mutant\nper cell", xy=(3e3, 1.0), xytext=(1.3e2, 3.0),
             fontsize=8.0, color=INK)

fig.tight_layout()
save(fig, "assets/figures/burst-mutation-supply.svg")
