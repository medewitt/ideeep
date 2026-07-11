# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""One outbreak, counted three ways: the case definition decides the shape of
the epidemic curve and the size of the count.

  (a) The same true incidence, counted under a broad (suspected) definition
      -- high sensitivity but padded with false positives, so the curve is
      taller and broader -- and under a narrow (confirmed) definition -- high
      specificity but low sensitivity and delayed by laboratory confirmation,
      so the curve is lower and shifted later.
  (b) The resulting totals: the broad definition over-counts, the narrow one
      under-counts, and only the true curve is the epidemic itself. All
      illustrative.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(2007)

t = np.arange(0, 71)
shape = t ** 4 * np.exp(-t / 5.0)              # gamma-like epidemic wave
true = 1000 * shape / shape.sum()

# Broad / suspected: near-perfect sensitivity, but false positives from
# co-circulating look-alike illness broaden and inflate the curve.
false_pos = 16 * np.exp(-0.5 * ((t - 34) / 20) ** 2) + 1.5
suspected = rng.poisson(0.98 * true + false_pos).astype(float)

# Narrow / confirmed: high specificity, but low sensitivity and a laboratory
# confirmation delay shift the curve down and to the right.
LAB_DELAY = 7
conf_mean = np.zeros_like(true)
conf_mean[LAB_DELAY:] = 0.45 * true[:-LAB_DELAY]
confirmed = rng.poisson(conf_mean).astype(float)

fig, (axa, axb) = plt.subplots(1, 2, figsize=(10.8, 3.9),
                               gridspec_kw={"width_ratios": [2.1, 1]})

# --- (a) the three epidemic curves ----------------------------------------
axa.plot(t, true, color=INK, lw=2.4, label="true infections")
axa.plot(t, suspected, color=PALETTE[1], lw=1.8, label="suspected (broad)")
axa.plot(t, confirmed, color=PALETTE[0], lw=1.8, label="confirmed (narrow)")
axa.fill_between(t, true, confirmed, color=PALETTE[0], alpha=0.08)
axa.set_xlabel("day of the outbreak")
axa.set_ylabel("cases counted per day")
axa.set_title("(a) The same outbreak, counted three ways")
axa.legend(fontsize=8, loc="upper right")
axa.annotate("broad: taller,\npadded with\nfalse positives", xy=(24, suspected[24]),
             xytext=(40, 46), fontsize=8, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=INK))
axa.annotate("narrow: lower and\nlab-delayed", xy=(30, confirmed[30]),
             xytext=(43, 20), fontsize=8, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=INK))

# --- (b) totals ------------------------------------------------------------
totals = [true.sum(), suspected.sum(), confirmed.sum()]
labels = ["true", "suspected", "confirmed"]
cols = [INK, PALETTE[1], PALETTE[0]]
axb.bar(labels, totals, color=cols, width=0.62)
axb.axhline(true.sum(), color=INK, lw=1.0, ls=":")
for i, v in enumerate(totals):
    axb.text(i, v + 12, f"{v:.0f}", ha="center", fontsize=8.5, color=INK)
axb.set_ylabel("total cases counted")
axb.set_title("(b) The denominator shifts too")
axb.set_ylim(0, max(totals) * 1.18)

fig.suptitle("The case definition decides the shape of the epidemic curve",
             fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "assets/figures/case-definition-epicurve.svg")
