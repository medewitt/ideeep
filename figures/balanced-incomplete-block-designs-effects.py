# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pandas", "statsmodels", "scipy", "matplotlib"]
# ///
"""Adjusted treatment (panel) effects from the intra-block analysis of the (7,3,1)
BIBD, each with its 95% interval. The intervals are equal in width across
treatments because every pair of treatments is compared through the same number of
shared blocks — the balance the design is built to guarantee."""
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

warnings.filterwarnings("ignore")
apply_style()

blocks = [(1, 2, 3), (1, 4, 5), (1, 6, 7), (2, 4, 6),
          (2, 5, 7), (3, 4, 7), (3, 5, 6)]
rng = np.random.default_rng(2)
tau = {t: e for t, e in zip(range(1, 8), [0, 1, 2, 1, 3, 2, 1])}
rows = []
for blk, treats in enumerate(blocks):
    shift = rng.normal(0, 2.0)
    for t in treats:
        rows.append((t, blk, 10 + tau[t] + shift + rng.normal(0, 0.6)))
d = pd.DataFrame(rows, columns=["treatment", "block", "y"])
fit = smf.ols("y ~ C(treatment) + C(block)", data=d).fit()

# adjusted treatment effects relative to treatment 1, with CIs
est, lo, hi = [0.0], [0.0], [0.0]
for t in range(2, 8):
    key = f"C(treatment)[T.{t}]"
    ci = fit.conf_int().loc[key]
    est.append(fit.params[key])
    lo.append(ci[0])
    hi.append(ci[1])

fig, ax = plt.subplots(figsize=(6.4, 3.9))
for i in range(7):
    y = 7 - 1 - i
    col = PALETTE[i % len(PALETTE)]
    if i == 0:
        ax.plot([est[0]], [y], "o", color=INK, ms=9)
        ax.annotate("t1 (reference)", (0, y + 0.18), fontsize=8, color=INK,
                    ha="center")
    else:
        ax.plot([lo[i], hi[i]], [y, y], color=col, lw=2.2)
        ax.plot([est[i]], [y], "o", color=col, ms=8)
        ax.annotate(f"{est[i]:.2f}", (est[i], y + 0.18), fontsize=8, color=INK,
                    ha="center")

ax.axvline(0, color=INK, lw=0.8, ls=":")
ax.set_yticks(range(7))
ax.set_yticklabels([f"t{t}" for t in range(1, 8)][::-1], fontsize=8.6)
ax.set_xlabel("adjusted effect vs t1")
ax.set_title("Balanced: equal-width intervals across treatments", fontsize=9.4)
ax.set_ylim(-0.6, 6.6)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/balanced-incomplete-block-designs-effects.svg")
