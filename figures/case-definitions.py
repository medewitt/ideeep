# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Case definitions: the sensitivity-specificity trade-off, the graded
suspected/probable/confirmed ladder, and the 7-1-7 response-timeliness target.

  (a) Overlapping clinical/laboratory-evidence scores for true cases and
      non-cases, with the three graded cutoffs (suspected, probable,
      confirmed) marking where the definition is drawn.
  (b) As the definition tightens, sensitivity falls and specificity rises;
      broad catches every case but dilutes with non-cases, narrow is pure but
      misses cases.
  (c) The 7-1-7 target: 7 days to detect, 1 day to notify and investigate,
      7 days to mount an effective response. All illustrative.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(717)

# Synthetic "evidence score": non-cases low, true cases high, overlapping.
n = 40000
noncases = rng.normal(0.0, 1.0, n)
cases = rng.normal(3.0, 1.0, n)
SUS, PROB, CONF = 0.5, 2.0, 3.5          # suspected / probable / confirmed cutoffs

fig, (axa, axb, axc) = plt.subplots(1, 3, figsize=(11.8, 3.9))

# --- (a) score distributions with the three cutoffs -----------------------
bins = np.linspace(-4, 7, 60)
axa.hist(noncases, bins=bins, density=True, color=PALETTE[0], alpha=0.55,
         label="non-cases")
axa.hist(cases, bins=bins, density=True, color=PALETTE[1], alpha=0.55,
         label="true cases")
for x, name in [(SUS, "suspected"), (PROB, "probable"), (CONF, "confirmed")]:
    axa.axvline(x, color=INK, lw=1.2, ls="--")
    axa.text(x, 0.44, name, rotation=90, va="top", ha="right",
             fontsize=7.6, color=INK)
axa.set_xlabel("clinical + laboratory evidence")
axa.set_ylabel("density")
axa.set_title("(a) A graded case definition")
axa.legend(fontsize=8, loc="upper left")
axa.set_ylim(0, 0.5)

# --- (b) sensitivity and specificity vs the cutoff ------------------------
cuts = np.linspace(-2, 6, 200)
sens = np.array([(cases >= c).mean() for c in cuts])
spec = np.array([(noncases < c).mean() for c in cuts])
axb.plot(cuts, sens, color=PALETTE[1], lw=2.2, label="sensitivity")
axb.plot(cuts, spec, color=PALETTE[0], lw=2.2, label="specificity")
for x, name in [(SUS, "susp."), (PROB, "prob."), (CONF, "conf.")]:
    axb.axvline(x, color=INK, lw=1.0, ls="--")
axb.text(-1.95, 0.14, "broad:\ncatch every case,\ndilute with non-cases",
         fontsize=7.6, color=MUTED, va="top")
axb.text(3.7, 0.42, "narrow:\npure but\nmisses cases",
         fontsize=7.6, color=MUTED, va="top")
axb.set_xlabel("case-definition cutoff (tighter -> )")
axb.set_ylabel("probability")
axb.set_title("(b) Sensitivity vs specificity")
axb.legend(fontsize=8, loc="center left")
axb.set_ylim(0, 1.05)

# --- (c) the 7-1-7 timeline ------------------------------------------------
axc.set_xlim(0, 16)
axc.set_ylim(0, 1)
axc.axis("off")
axc.set_title("(c) The 7-1-7 target")
segs = [(0, 7, PALETTE[0], "detect", "7 days"),
        (7, 1, PALETTE[3], "notify +\ninvestigate", "1 day"),
        (8, 7, PALETTE[2], "effective\nresponse", "7 days")]
y = 0.55
for x0, w, col, label, dur in segs:
    axc.add_patch(plt.Rectangle((x0, y), w, 0.16, color=col, alpha=0.85))
    axc.text(x0 + w / 2, y + 0.30, label, ha="center", va="bottom",
             fontsize=8.4, color=INK)
    axc.text(x0 + w / 2, y + 0.08, dur, ha="center", va="center",
             fontsize=8.0, color="white", weight="bold")
for x in (0, 7, 8, 15):
    axc.plot([x, x], [y - 0.03, y + 0.19], color=INK, lw=0.8)
for x in (0, 7, 15):
    axc.text(x, y - 0.10, f"day {x}", ha="center", fontsize=7.4, color=MUTED)
axc.text(8, 0.14, "detection speed drives the whole clock",
         ha="center", fontsize=8, color=MUTED, style="italic")

fig.suptitle("A case definition trades sensitivity for specificity; 7-1-7 "
             "puts a clock on the response", fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "assets/figures/case-definitions.svg")
