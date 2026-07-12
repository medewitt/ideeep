# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pandas", "statsmodels", "scipy", "matplotlib"]
# ///
"""Estimated Latin-square treatment effects (relative to A) with 95% intervals,
after the row and column blocking factors have been partitioned out. Blocking on
both directions shrinks the error term, so the treatment contrasts are estimated
against clean residual variation."""
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

warnings.filterwarnings("ignore")
apply_style()

letters = ["A", "B", "C", "D"]
square = [[letters[(j + i) % 4] for j in range(4)] for i in range(4)]
rng = np.random.default_rng(4)
row_eff = rng.normal(0, 2.0, 4)
col_eff = rng.normal(0, 1.5, 4)
tau = {"A": 0.0, "B": 1.5, "C": 3.0, "D": 2.0}
rows = []
for i in range(4):
    for j in range(4):
        t = square[i][j]
        y = 20 + row_eff[i] + col_eff[j] + tau[t] + rng.normal(0, 0.6)
        rows.append((i, j, t, y))
d = pd.DataFrame(rows, columns=["row", "col", "treatment", "y"])
fit = smf.ols("y ~ C(row) + C(col) + treatment", data=d).fit()

items = [("A (reference)", 0.0, None, None, INK)]
for L in ["B", "C", "D"]:
    key = f"treatment[T.{L}]"
    ci = fit.conf_int().loc[key]
    items.append((L, fit.params[key], ci[0], ci[1], PALETTE[letters.index(L)]))

fig, ax = plt.subplots(figsize=(6.4, 3.4))
for i, (label, est, lo, hi, col) in enumerate(items):
    y = len(items) - 1 - i
    if lo is not None:
        ax.plot([lo, hi], [y, y], color=col, lw=2.4)
    ax.plot([est], [y], "o", color=col, ms=9)
    tru = {"A (reference)": 0.0, "B": 1.5, "C": 3.0, "D": 2.0}[label]
    note = f"{est:.2f}  (true {tru:g})" if lo is not None else "reference"
    ax.annotate(note, (est, y + 0.16), fontsize=8.2, color=INK, ha="center")

ax.axvline(0, color=INK, lw=0.8, ls=":")
ax.set_yticks(range(len(items)))
ax.set_yticklabels([r[0] for r in items][::-1], fontsize=8.8)
ax.set_xlabel("treatment effect vs A (row & column removed)")
ax.set_title("Treatment contrasts against reduced error", fontsize=9.4)
ax.set_ylim(-0.6, len(items) - 0.2)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/latin-square-designs-effects.svg")
