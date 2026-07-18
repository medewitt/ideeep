# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "statsmodels", "matplotlib"]
# ///
"""Reading the force of infection off an age-seroprevalence survey. Seroprevalence
rises with age as susceptibles accumulate exposure; the simple catalytic model,
seroprevalence = 1 - exp(-lambda * age), fits a constant annual force of infection.
Here the fit recovers lambda near 0.1 per year - a mean age at infection of about
ten years. Points are observed seroprevalence by age (area proportional to sample
size)."""
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(9)
ages = np.arange(1, 46)
nper = rng.integers(20, 45, len(ages))
pos = rng.binomial(nper, 1 - np.exp(-0.10 * ages))
m = sm.GLM(np.column_stack([pos, nper - pos]), np.ones((len(ages), 1)),
           family=sm.families.Binomial(sm.families.links.CLogLog()),
           offset=np.log(ages)).fit()
lam = np.exp(m.params[0])

fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.scatter(ages, pos / nper, s=12 + 1.6 * nper, color=PALETTE[0], alpha=0.6,
           edgecolor=INK, linewidth=0.4, zorder=3, label="observed seroprevalence")
aa = np.linspace(0, 45, 200)
ax.plot(aa, 1 - np.exp(-lam * aa), color=PALETTE[1], lw=2.4,
        label=f"catalytic fit  (λ = {lam:.3f}/yr)")
ax.axhline(0.5, color=INK, lw=0.7, ls=":")
ax.axvline(1 / lam, color=INK, lw=0.7, ls=":")
ax.annotate(f"mean age at infection\n1/λ ≈ {1/lam:.0f} yr", xy=(1 / lam, 0.2),
            xytext=(16, 0.12), fontsize=8.4, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
ax.set_xlabel("age (years)")
ax.set_ylabel("proportion seropositive")
ax.set_title("Age-seroprevalence and the catalytic model", fontsize=9.8)
ax.set_xlim(0, 45)
ax.set_ylim(0, 1.02)
ax.legend(fontsize=8.4, loc="lower right")
fig.tight_layout()
save(fig, "assets/figures/serocatalytic-curve.svg")
