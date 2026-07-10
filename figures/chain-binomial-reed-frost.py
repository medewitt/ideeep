# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Reed-Frost chain-binomial model in a closed household of six."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)


def reed_frost(n, p, reps, rng):
    """Total ever infected (incl. index) per rep; household size n."""
    q = 1.0 - p
    totals = np.empty(reps, dtype=int)
    for k in range(reps):
        infectious = 1
        susceptible = n - 1
        total = 1
        while infectious > 0 and susceptible > 0:
            escape = q ** infectious
            new = rng.binomial(susceptible, 1.0 - escape)
            susceptible -= new
            total += new
            infectious = new
        totals[k] = total
    return totals


n = 6
reps = 20000

# LEFT: household final-size distribution for two transmission probs
j = np.arange(1, n + 1)
width = 0.4

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5))

for i, (p, col) in enumerate([(0.3, PALETTE[0]), (0.6, PALETTE[1])]):
    totals = reed_frost(n, p, reps, rng)
    dist = np.array([(totals == v).mean() for v in j])
    offset = (i - 0.5) * width
    axL.bar(j + offset, dist, width=width, color=col,
            label=f"p = {p}")

axL.annotate("bimodal at low p:\nmany small + full sweeps", xy=(1, 0.30),
             xytext=(2.4, 0.34), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axL.set_xticks(j)
axL.set_xlabel("total ever infected in household (of 6)")
axL.set_ylabel("probability")
axL.legend(loc="upper center", fontsize=8)

# RIGHT: mean household attack rate vs per-pair transmission prob.
# Fraction infected INCLUDES the index case (total / n).
pgrid = np.linspace(0.0, 0.8, 33)
mean_frac = np.empty_like(pgrid)
for idx, p in enumerate(pgrid):
    totals = reed_frost(n, p, 5000, rng)
    mean_frac[idx] = totals.mean() / n

axR.plot(pgrid, mean_frac, color=PALETTE[2], lw=2.0)
axR.annotate("secondary attack rate rises steeply\n"
             "near the household epidemic threshold",
             xy=(0.35, np.interp(0.35, pgrid, mean_frac)),
             xytext=(0.06, 0.85), fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axR.set_xlim(0, 0.8)
axR.set_ylim(0, 1.0)
axR.set_xlabel("per-pair transmission probability p")
axR.set_ylabel("mean fraction infected in household")

fig.tight_layout()
save(fig, "assets/figures/chain-binomial-reed-frost.svg")
