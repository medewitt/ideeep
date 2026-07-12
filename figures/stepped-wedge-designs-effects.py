# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pandas", "statsmodels", "scipy", "matplotlib"]
# ///
"""Left: the estimated stepped-wedge intervention effect with its 95% interval,
recovered after adjusting for calendar time. Right: the fitted period effects — the
secular trend the design must separate from the rollout, so a naive before/after
estimate is inflated by exactly this trend."""
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

warnings.filterwarnings("ignore")
apply_style()

rng = np.random.default_rng(5)
n_clusters, n_periods = 5, 5
switch = {c: c + 1 for c in range(n_clusters)}
rows = []
for c in range(n_clusters):
    u = rng.normal(0, 1.5)
    for p in range(n_periods):
        X = int(p >= switch[c])
        y = 10 + 0.4 * p + 2.0 * X + u + rng.normal(0, 1.0)
        rows.append((c, p, X, y))
d = pd.DataFrame(rows, columns=["cluster", "period", "treatment", "y"])
m = smf.mixedlm("y ~ treatment + C(period)", d, groups=d["cluster"]).fit()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.5),
                               gridspec_kw={"width_ratios": [1, 1.2]})

# ---- intervention effect --------------------------------------------------
est, se = m.params["treatment"], m.bse["treatment"]
axL.plot([est - 1.96 * se, est + 1.96 * se], [0, 0], color=PALETTE[1], lw=2.8)
axL.plot([est], [0], "o", color=PALETTE[1], ms=11)
axL.axvline(2.0, color=INK, lw=0.8, ls=":")
axL.annotate("true = 2", (2.0, 0.35), fontsize=8, color=INK, ha="center")
axL.annotate(f"{est:.2f}  (±{1.96*se:.2f})", (est, -0.32), fontsize=8.6,
             color=INK, ha="center")
axL.set_yticks([])
axL.set_ylim(-0.7, 0.7)
axL.set_xlabel("intervention effect")
axL.set_title("Adjusted treatment effect", fontsize=9.5)
axL.grid(axis="y", visible=False)

# ---- fitted period (secular) trend ----------------------------------------
per = [0.0] + [m.params[f"C(period)[T.{p}]"] for p in range(1, n_periods)]
axR.plot(range(1, n_periods + 1), per, color=PALETTE[0], lw=2.0, marker="o", ms=6,
         label="fitted period effect")
axR.plot(range(1, n_periods + 1), [0.4 * p for p in range(n_periods)],
         color=MUTED, lw=1.4, ls="--", label="true trend")
axR.set_xlabel("time period")
axR.set_ylabel("effect vs period 1")
axR.set_title("Secular trend to remove", fontsize=9.5)
axR.legend(fontsize=8)
axR.set_xticks(range(1, n_periods + 1))

fig.tight_layout()
save(fig, "assets/figures/stepped-wedge-designs-effects.svg")
