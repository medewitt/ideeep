# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Two-tailed z-test: standard normal null with rejection regions beyond +/-1.96."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE

apply_style()

z = np.linspace(-4, 4, 800)
pdf = stats.norm.pdf(z)

zcrit = 1.96  # alpha = 0.05, two-tailed
zobs = 2.3
pval = 2 * (1 - stats.norm.cdf(zobs))
print(f"critical values = +/-{zcrit}, alpha = 0.05")
print(f"observed z = {zobs}, two-tailed p-value = {pval:.4f}")

fig, ax = plt.subplots()
ax.plot(z, pdf, color=PALETTE[0], lw=2, label="null: N(0,1)")

right = z >= zcrit
left = z <= -zcrit
ax.fill_between(z[right], 0, pdf[right], color=PALETTE[1], alpha=0.4)
ax.fill_between(z[left], 0, pdf[left], color=PALETTE[1], alpha=0.4,
                label="rejection region")

ax.axvline(zobs, color=PALETTE[3], lw=2, ls="--")
ax.annotate(f"observed z = {zobs}", xy=(zobs, stats.norm.pdf(zobs)),
            xytext=(2.6, 0.28),
            arrowprops=dict(arrowstyle="->", color="#26323f"))
ax.annotate("rejection region", xy=(2.7, 0.01), xytext=(1.4, 0.12),
            color=PALETTE[1],
            arrowprops=dict(arrowstyle="->", color=PALETTE[1]))

ax.set_xlabel("z")
ax.set_ylabel("density")
ax.set_title(r"Two-tailed test ($\alpha=0.05$, $z_{crit}=\pm1.96$)")
ax.legend(loc="upper left")

save(fig, "assets/figures/hypothesis-test.svg")
