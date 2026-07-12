# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""The latent-variable view of the proportional odds model. Left: an
unobserved continuous variable (here logistic) underlies the ordinal outcome;
fixed cutpoints slice it into ordered categories. A treatment shifts the whole
latent distribution by the same amount beta on the log-odds scale, so *every*
cutpoint sees the same shift -- that single common shift is the proportional
odds assumption, and exp(beta) is the one odds ratio that applies at every
cutpoint. Right: the shift moves probability mass toward the higher
categories, shown as the category probabilities for control vs treated."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# logistic pdf / cdf
def lpdf(z):
    e = np.exp(-z)
    return e / (1 + e) ** 2

def lcdf(z):
    return 1.0 / (1 + np.exp(-z))

beta = 1.3                                  # common log-odds shift (treatment)
cuts = np.array([-2.2, -0.7, 0.7, 2.2])     # 4 cutpoints -> 5 categories
z = np.linspace(-6, 6, 600)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.9))

# ---- left: two shifted latent densities with cutpoints ----
axL.plot(z, lpdf(z), color=PALETTE[0], lw=2.0, label="control")
axL.plot(z, lpdf(z - beta), color=PALETTE[1], lw=2.0,
         label=r"treated (shift $\beta$)")
for c in cuts:
    axL.axvline(c, color=MUTED, lw=0.9, ls="--")
ymax = lpdf(0.0)
axL.annotate("", xy=(beta, ymax * 1.03), xytext=(0, ymax * 1.03),
             arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
axL.text(beta / 2, ymax * 1.08, r"$\beta$", fontsize=11, color=INK, ha="center")
labels = ["1", "2", "3", "4", "5"]
edges = np.r_[-6, cuts, 6]
for lab, a, b in zip(labels, edges[:-1], edges[1:]):
    axL.text((a + b) / 2, -0.028, lab, fontsize=9, color=MUTED, ha="center")
axL.set_ylim(-0.05, ymax * 1.2)
axL.set_title("Latent variable cut into ordered categories", fontsize=10)
axL.set_xlabel("latent scale (log-odds)")
axL.set_ylabel("density")
axL.legend(fontsize=8.2, loc="upper left")

# ---- right: category probabilities control vs treated ----
def cat_probs(shift):
    F = lcdf(cuts - shift)                  # P(Y <= j)
    Fful = np.r_[0.0, F, 1.0]
    return np.diff(Fful)

p0 = cat_probs(0.0)
p1 = cat_probs(beta)
xcat = np.arange(1, 6)
w = 0.38
axR.bar(xcat - w / 2, p0, width=w, color=PALETTE[0], label="control")
axR.bar(xcat + w / 2, p1, width=w, color=PALETTE[1], label="treated")
axR.set_xticks(xcat)
axR.set_title("Category probabilities shift upward", fontsize=10)
axR.set_xlabel("ordinal category")
axR.set_ylabel("probability")
axR.legend(fontsize=8.2, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/proportional-odds.svg")
