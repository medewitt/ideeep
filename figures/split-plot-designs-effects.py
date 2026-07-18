# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pandas", "statsmodels", "scipy", "matplotlib"]
# ///
"""Estimated effects from the split-plot model with 95% intervals. The whole-plot
(irrigation) effect carries a wide interval because it is measured against
between-field variation; the sub-plot (variety) effect and the interaction carry
narrow intervals because they are measured within fields."""
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

warnings.filterwarnings("ignore")
apply_style()

rng = np.random.default_rng(7)
rows = []
for irr in (-1, 1):
    for rep in range(3):
        field = f"{irr}_{rep}"
        u = rng.normal(0, 2.0)
        for var in (-1, 1):
            y = 20 + 3 * irr + 2 * var + 1 * irr * var + u + rng.normal(0, 0.7)
            rows.append((field, irr, var, y))
d = pd.DataFrame(rows, columns=["field", "irrigation", "variety", "resp"])
m = smf.mixedlm("resp ~ irrigation * variety", d, groups=d["field"]).fit()

terms = [("irrigation", "irrigation\n(whole-plot)", PALETTE[1]),
         ("variety", "variety\n(sub-plot)", PALETTE[0]),
         ("irrigation:variety", "irrigation × variety\n(sub-plot)", PALETTE[2])]

fig, ax = plt.subplots(figsize=(6.4, 3.6))
for i, (key, label, col) in enumerate(terms):
    est = m.params[key]
    se = m.bse[key]
    lo, hi = est - 1.96 * se, est + 1.96 * se
    y = len(terms) - 1 - i
    ax.plot([lo, hi], [y, y], color=col, lw=2.4)
    ax.plot([est], [y], "o", color=col, ms=9)
    ax.annotate(f"{est:.2f}  (±{1.96*se:.2f})", (est, y + 0.16), fontsize=8.2,
                color=INK, ha="center")

ax.axvline(0, color=INK, lw=0.8, ls=":")
ax.set_yticks(range(len(terms)))
ax.set_yticklabels([label for _, label, _ in terms][::-1], fontsize=8.6)
ax.set_xlabel("estimated effect (coefficient)")
ax.set_title("Wide whole-plot vs narrow sub-plot intervals", fontsize=9.5)
ax.set_ylim(-0.6, len(terms) - 0.2)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/split-plot-designs-effects.svg")
