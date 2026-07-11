# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Global sensitivity analysis. Left: Sobol indices for the worked model
Y = X1 + X2 + X1*X2 — each input's first-order index S_i = 0.491 sits just below
its total-effect index S_Ti = 0.509, and the small gap S_Ti - S_i is that
input's share of the pure interaction term (about 1.8% of variance). Right: a
Morris screening plot places each input by its mean absolute elementary effect
(importance) against its spread (nonlinearity/interaction), separating
negligible inputs near the origin from influential ones."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- Sobol first-order vs total -------------------------------------------
Si = 27 / 55       # 0.491
STi = 28 / 55      # 0.509
x = np.arange(2)
w = 0.36
axL.bar(x - w / 2, [Si, Si], width=w, color=PALETTE[0],
        label=r"first-order $S_i$")
axL.bar(x + w / 2, [Si, Si], width=w, color=PALETTE[1] + "55",
        label="_none")
axL.bar(x + w / 2, [STi - Si, STi - Si], width=w, bottom=[Si, Si],
        color=PALETTE[1], label=r"interaction $S_{Ti}-S_i$")
axL.bar(x + w / 2, [Si, Si], width=w, color=PALETTE[1] + "55",
        label=r"total-effect $S_{Ti}$")
axL.set_xticks(x)
axL.set_xticklabels(["$X_1$", "$X_2$"])
axL.set_ylabel("share of output variance")
axL.set_title("Sobol indices  ($S_i=0.491$, $S_{Ti}=0.509$)", fontsize=9.5)
axL.set_ylim(0, 0.6)
axL.legend(fontsize=7.6, loc="upper center")
axL.grid(axis="x", visible=False)
axL.annotate("gap = interaction\n(≈1.8%)", xy=(1 + w / 2, 0.5),
             xytext=(0.7, 0.55), fontsize=7.6, color=PALETTE[1])

# ---- Morris mu* vs sigma ---------------------------------------------------
labels = ["β (transmission)", "γ (recovery)", "reporting", "seasonality",
          "waning", "import rate"]
mustar = [0.92, 0.61, 0.14, 0.40, 0.09, 0.05]
sigma = [0.55, 0.20, 0.05, 0.42, 0.06, 0.03]
axR.scatter(mustar, sigma, s=55, color=PALETTE[0], zorder=5)
for lab, mx, sy in zip(labels, mustar, sigma):
    axR.annotate(lab, (mx, sy), textcoords="offset points", xytext=(5, 3),
                 fontsize=7, color=INK)
axR.axvspan(0, 0.2, color=MUTED + "18", zorder=0)
axR.text(0.1, 0.55, "negligible\n(can fix)", fontsize=7.5, color=MUTED,
         ha="center")
axR.set_xlabel(r"$\mu^*$  (overall importance)")
axR.set_ylabel(r"$\sigma$  (nonlinearity / interaction)")
axR.set_title("Morris screening", fontsize=9.5)
axR.set_xlim(0, 1.05)
axR.set_ylim(0, 0.65)

fig.tight_layout()
save(fig, "assets/figures/sensitivity-analysis.svg")
