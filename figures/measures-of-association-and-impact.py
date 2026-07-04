# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""A 2x2 table with its measures, and when the odds ratio departs from the risk ratio."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axt, axr) = plt.subplots(1, 2, figsize=(8.2, 4.0),
                               gridspec_kw={"width_ratios": [1.05, 1.0]})

# ---- Left: 2x2 contingency table ----
axt.set_xlim(0, 3)
axt.set_ylim(0, 3)
axt.axis("off")
axt.grid(False)

a, b, c, d = 300, 700, 100, 900
cells = {(1, 2): ("a", a, PALETTE[1]), (2, 2): ("b", b, "#c9d3db"),
         (1, 1): ("c", c, PALETTE[1]), (2, 1): ("d", d, "#c9d3db")}
for (col, row), (lab, val, color) in cells.items():
    axt.add_patch(Rectangle((col, row), 1, 1, facecolor=color, alpha=0.85,
                            edgecolor="white", lw=2))
    axt.text(col + 0.5, row + 0.5, f"{lab} = {val}", ha="center", va="center",
             fontsize=10, color=INK)

axt.text(1.5, 3.15, "Case", ha="center", fontsize=9.5, color=INK)
axt.text(2.5, 3.15, "Non-case", ha="center", fontsize=9.5, color=INK)
axt.text(0.9, 2.5, "Exposed", ha="right", va="center", fontsize=9.5, color=INK)
axt.text(0.9, 1.5, "Unexposed", ha="right", va="center", fontsize=9.5, color=INK)
axt.set_title("A 2x2 table")

RR = (a / (a + b)) / (c / (c + d))
OR = (a * d) / (b * c)
RD = a / (a + b) - c / (c + d)
axt.text(1.5, 0.55, f"RR = {RR:.2f}   OR = {OR:.2f}   RD = {RD:.2f}",
         ha="center", fontsize=9.5, color=INK)

# ---- Right: OR inflates above RR as the outcome becomes common ----
p0 = np.linspace(0.001, 0.45, 300)
rr_fixed = 2.0
p1 = rr_fixed * p0
odds_ratio = (p1 / (1 - p1)) / (p0 / (1 - p0))

axr.plot(p0, odds_ratio, color=PALETTE[1], lw=2, label="odds ratio")
axr.axhline(rr_fixed, color=PALETTE[0], lw=2, ls="--", label="risk ratio = 2")
axr.set_xlabel("baseline risk in unexposed")
axr.set_ylabel("ratio measure")
axr.set_title("OR approximates RR only when risk is low")
axr.legend(loc="upper left", fontsize=9)

save(fig, "assets/figures/measures-of-association-and-impact.svg")
