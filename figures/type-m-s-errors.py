# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "scipy"]
# ///
"""Design analysis of Gelman & Carlin (2014). Everything is driven by one
number, d = (true effect) / (standard error). Left: the exaggeration ratio
(Type M) — the factor by which a statistically significant estimate overstates
the true effect, on average — climbs steeply as power falls, exceeding 2 well
before power drops to 0.2. Right: the Type S (sign) error rate — the chance a
significant estimate points the wrong way — rises from ~0 at high power toward
0.5 as power approaches the significance level. Two worked examples (a
continuous-outcome trial and a binary-outcome case-control study) are marked;
the dashed line marks the conventional 80% power target, where both errors are
small."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

ZC = norm.ppf(0.975)          # two-sided alpha = 0.05 critical value


def design(d):
    """Power, Type S, Type M for standardized true effect d = effect / SE."""
    p_hi = norm.cdf(d - ZC)                 # significant, correct sign
    p_lo = norm.cdf(-ZC - d)                # significant, wrong sign
    power = p_hi + p_lo
    type_s = p_lo / power
    num = d * (p_hi - p_lo) + norm.pdf(ZC - d) + norm.pdf(ZC + d)
    type_m = num / (d * power)
    return power, type_s, type_m


d = np.linspace(0.02, 4.0, 600)
power, type_s, type_m = np.vectorize(design)(d)

# Two worked examples from the page.
d_cont, d_bin = 0.50, 0.618
ex = {
    "continuous trial": (d_cont, PALETTE[1]),
    "binary case-control": (d_bin, PALETTE[3]),
}

fig, (axM, axS) = plt.subplots(1, 2, figsize=(8.6, 3.7))

# ---- Type M (exaggeration ratio) vs power ---------------------------------
axM.plot(power, type_m, color=PALETTE[0], lw=2.0)
axM.axhline(1, color=MUTED, ls=":", lw=1.0)
axM.axvline(0.8, color=MUTED, ls="--", lw=1.0)
axM.text(0.8, 7.4, "80%\npower", fontsize=7.8, color=MUTED, ha="center", va="top")
for name, (dv, col) in ex.items():
    pw, _, tm = design(dv)
    axM.scatter([pw], [tm], color=col, s=34, zorder=5)
    axM.annotate(name, xy=(pw, tm), xytext=(pw + 0.06, tm + 0.7),
                 fontsize=7.8, color=col)
axM.set_xlabel("power")
axM.set_ylabel("exaggeration ratio  (Type M)")
axM.set_title("Significant estimates overstate the effect", fontsize=10)
axM.set_xlim(0, 1)
axM.set_ylim(0, 8)

# ---- Type S (sign error) vs power -----------------------------------------
axS.plot(power, 100 * type_s, color=PALETTE[0], lw=2.0)
axS.axvline(0.8, color=MUTED, ls="--", lw=1.0)
for name, (dv, col) in ex.items():
    pw, ts, _ = design(dv)
    axS.scatter([pw], [100 * ts], color=col, s=34, zorder=5)
    axS.annotate(name, xy=(pw, 100 * ts), xytext=(pw + 0.05, 100 * ts + 2.0),
                 fontsize=7.8, color=col)
axS.set_xlabel("power")
axS.set_ylabel("wrong-sign rate  (Type S, %)")
axS.set_title("...and can point the wrong way", fontsize=10)
axS.set_xlim(0, 1)
axS.set_ylim(0, 50)

fig.tight_layout()
save(fig, "assets/figures/type-m-s-errors.svg")
