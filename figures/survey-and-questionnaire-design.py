# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Survey and questionnaire design: three ways a badly built instrument
reads the wrong number even from a perfect sample.

  (a) Social-desirability bias: the reported prevalence of a stigmatized
      behaviour climbs toward the truth as the mode gives the respondent
      more privacy.
  (b) Acquiescence ("yea-saying"): agreement to a claim and to its logical
      reversal should be complementary; the excess is acquiescence, which a
      balanced (positively- and negatively-keyed) scale cancels.
  (c) A double-barreled item measures two things at once, so its item-total
      correlation is low and it drags a scale's reliability (Cronbach's
      alpha) down. All synthetic, for illustration.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(717)


def cronbach_alpha(items):
    """items: (n_respondents, k_items) -> alpha."""
    k = items.shape[1]
    item_var = items.var(axis=0, ddof=1).sum()
    total_var = items.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_var / total_var)


fig, (axa, axb, axc) = plt.subplots(1, 3, figsize=(11.6, 3.9))

# --- (a) social desirability by mode --------------------------------------
p_true = 0.36
modes = ["face-to-\nface", "telephone", "self-admin.\n(ACASI)",
         "indirect\n(RRT)"]
reported = np.array([0.19, 0.25, 0.31, 0.345])
bars = axa.bar(modes, reported, color=PALETTE[0], width=0.66)
axa.axhline(p_true, color=PALETTE[1], lw=1.6, ls="--")
axa.text(3.05, p_true + 0.007, "true prevalence", color=PALETTE[1],
         fontsize=8, ha="right")
axa.set_ylim(0, 0.44)
axa.set_ylabel("reported prevalence")
axa.set_title("(a) Social-desirability bias")
axa.annotate("more privacy\n-> less under-reporting", xy=(0, 0.205),
             xytext=(0.15, 0.36), fontsize=8, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=INK))

# --- (b) acquiescence ------------------------------------------------------
# "agree" to a claim vs "agree" to its reversal; without yea-saying these
# would be complementary (sum to 1). The overlap above 1 is acquiescence.
pos_agree = 0.66
neg_agree = 0.44                       # would be 1 - 0.66 = 0.34 if unbiased
labels = ["claim\n(pos. worded)", "reversal\n(neg. worded)"]
axb.bar(labels, [pos_agree, neg_agree], color=[PALETTE[2], PALETTE[3]],
        width=0.6)
axb.axhline(1 - pos_agree, color=INK, lw=1.2, ls=":")
axb.text(0.03, 0.44, "if unbiased,\nreversal = 0.34", transform=axb.transAxes,
         fontsize=8, color=INK, va="top")
axb.annotate("acquiescence\n(+0.10)", xy=(1, neg_agree),
             xytext=(0.42, 0.66), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK))
axb.set_ylim(0, 1.0)
axb.set_ylabel("proportion agreeing")
axb.set_title("(b) Acquiescence from wording")

# --- (c) a double-barreled item degrades reliability -----------------------
n, k = 600, 6
theta = rng.normal(size=n)                      # latent attitude
phi = rng.normal(size=n)                        # unrelated second construct
clean = np.stack([theta + rng.normal(0, 0.85, n) for _ in range(k - 1)], 1)
barreled = 0.25 * theta + 0.65 * phi + rng.normal(0, 0.9, n)  # two constructs
items = np.column_stack([clean, barreled])
labels_c = [f"Q{i+1}" for i in range(k - 1)] + ["Q6*\n(2-in-1)"]
# corrected item-total correlation (item vs sum of the others)
itc = []
for j in range(k):
    rest = items.sum(1) - items[:, j]
    itc.append(np.corrcoef(items[:, j], rest)[0, 1])
itc = np.array(itc)
cols = [PALETTE[0]] * (k - 1) + [PALETTE[1]]
axc.bar(labels_c, itc, color=cols, width=0.68)
axc.set_ylim(0, 0.9)
axc.set_ylabel("item-total correlation")
axc.set_title("(c) A double-barreled item")
a_with = cronbach_alpha(items)
a_without = cronbach_alpha(items[:, :k - 1])
axc.text(-0.35, 0.87, rf"$\alpha$ = {a_with:.2f} with Q6", ha="left",
         fontsize=8.6, color=PALETTE[1])
axc.text(-0.35, 0.81, rf"$\alpha$ = {a_without:.2f} without Q6", ha="left",
         fontsize=8.6, color=PALETTE[2])
axc.annotate("measures two things\n-> low item-total r", xy=(5, itc[-1] + 0.02),
             xytext=(4.55, 0.55), fontsize=8, color=MUTED, ha="center",
             arrowprops=dict(arrowstyle="->", color=INK))

fig.suptitle("Wording and mode decide what a survey measures, even with a "
             "perfect sample", fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "assets/figures/survey-and-questionnaire-design.svg")
