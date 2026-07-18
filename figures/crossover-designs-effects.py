# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pandas", "statsmodels", "scipy", "matplotlib"]
# ///
"""Estimated crossover effects with 95% intervals. Treatment and period, estimated
within subjects, have narrow intervals; the carryover effect, aliased with the
between-subject sequence contrast, has a wide interval and cannot be pinned down —
the argument for controlling it by washout."""
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

warnings.filterwarnings("ignore")
apply_style()

rng = np.random.default_rng(11)
seqs = {"AB": ("A", "B"), "BA": ("B", "A")}
eff = {"A": 0.0, "B": -3.0}
rows = []
sid = 0
for seq, (t1, t2) in seqs.items():
    for _ in range(12):
        s = rng.normal(0, 5.0)
        for period, t in [(1, t1), (2, t2)]:
            y = 20 + s + 1.0 * (period - 1) + eff[t] + rng.normal(0, 1.0)
            rows.append((sid, seq, period, t, y))
        sid += 1
d = pd.DataFrame(rows, columns=["subject", "seq", "period", "treatment", "y"])

m = smf.mixedlm("y ~ treatment + C(period)", d, groups=d["subject"]).fit()

# carryover is aliased with the between-subject sequence contrast:
subj_mean = d.groupby(["subject", "seq"])["y"].mean().reset_index()
ab = subj_mean.loc[subj_mean.seq == "AB", "y"].values
ba = subj_mean.loc[subj_mean.seq == "BA", "y"].values
carry = ba.mean() - ab.mean()
carry_se = np.sqrt(ab.var(ddof=1) / len(ab) + ba.var(ddof=1) / len(ba))

items = [("treatment B\n(within subject)", m.params["treatment[T.B]"],
          m.bse["treatment[T.B]"], PALETTE[0]),
         ("period 2\n(within subject)", m.params["C(period)[T.2]"],
          m.bse["C(period)[T.2]"], PALETTE[2]),
         ("carryover\n(between subject)", carry, carry_se, PALETTE[1])]

fig, ax = plt.subplots(figsize=(6.6, 3.5))
for i, (label, est, se, col) in enumerate(items):
    y = len(items) - 1 - i
    lo, hi = est - 1.96 * se, est + 1.96 * se
    ax.plot([lo, hi], [y, y], color=col, lw=2.4)
    ax.plot([est], [y], "o", color=col, ms=9)
    ax.annotate(f"{est:.2f}  (±{1.96*se:.2f})", (est, y + 0.16), fontsize=8.2,
                color=INK, ha="center")

ax.axvline(0, color=INK, lw=0.8, ls=":")
ax.set_yticks(range(len(items)))
ax.set_yticklabels([r[0] for r in items][::-1], fontsize=8.6)
ax.set_xlabel("estimated effect")
ax.set_title("Within-subject effects sharp; carryover cannot be pinned down",
             fontsize=9.2)
ax.set_ylim(-0.6, len(items) - 0.2)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/crossover-designs-effects.svg")
