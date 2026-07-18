# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pandas", "statsmodels", "scipy", "matplotlib"]
# ///
"""The condition effect estimated two ways from the same repeated-measures data.
The between-subjects analysis (wide interval) carries person-to-person variability
in its error; the within-subject repeated-measures analysis (narrow interval)
removes it, sharpening the same estimate."""
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

warnings.filterwarnings("ignore")
apply_style()

rng = np.random.default_rng(3)
n_subj = 12
subj_level = rng.normal(0, 4.0, n_subj)
tau = {"c1": 0.0, "c2": 2.0, "c3": 3.0}
rows = []
for i in range(n_subj):
    for c, t in tau.items():
        rows.append((i, c, 10 + subj_level[i] + t + rng.normal(0, 1.0)))
d = pd.DataFrame(rows, columns=["subject", "condition", "y"])

within = smf.mixedlm("y ~ condition", d, groups=d["subject"]).fit()
between = smf.ols("y ~ condition", d).fit()

key = "condition[T.c3]"
rows_fp = [("within-subject\n(repeated measures)", within.params[key],
            within.bse[key], PALETTE[0]),
           ("between-subjects\n(ignores pairing)", between.params[key],
            between.bse[key], PALETTE[1])]

fig, ax = plt.subplots(figsize=(6.4, 3.2))
for i, (label, est, se, col) in enumerate(rows_fp):
    y = len(rows_fp) - 1 - i
    lo, hi = est - 1.96 * se, est + 1.96 * se
    ax.plot([lo, hi], [y, y], color=col, lw=2.6)
    ax.plot([est], [y], "o", color=col, ms=10)
    ax.annotate(f"{est:.2f}  (±{1.96*se:.2f})", (est, y + 0.18), fontsize=8.4,
                color=INK, ha="center")

ax.axvline(3.0, color=INK, lw=0.8, ls=":")
ax.annotate("true effect = 3", (3.0, 1.45), fontsize=8, color=INK, ha="center")
ax.set_yticks(range(len(rows_fp)))
ax.set_yticklabels([r[0] for r in rows_fp][::-1], fontsize=8.8)
ax.set_xlabel("estimated condition-3 effect")
ax.set_title("Same estimate, very different precision", fontsize=9.5)
ax.set_ylim(-0.6, 1.7)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/repeated-measures-effects.svg")
