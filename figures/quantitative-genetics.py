# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "scipy"]
# ///
"""The breeder's equation R = h^2 S. Left: selecting the tallest plants
(selected mean 60 cm, so the selection differential S = 10) shifts the offspring
mean only a fraction h^2 of the way — with h^2 = 0.5 the response is R = 5 cm
(offspring mean 55), not the full 10. Right: the response is governed by the
slope of offspring on mid-parent, which equals h^2, so a high-heritability trait
(steep, h^2=0.5) responds five times as much as a low one (flat, h^2=0.1)."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- selection and response -----------------------------------------------
mu, sd = 50.0, 6.0
h2 = 0.5
x = np.linspace(30, 70, 400)
parent = stats.norm.pdf(x, mu, sd)
sel_mean = 60.0
S = sel_mean - mu                       # 10
R = h2 * S                              # 5
offspring = stats.norm.pdf(x, mu + R, sd)

axL.plot(x, parent, color=PALETTE[0], lw=2.0, label="parents (mean 50)")
axL.plot(x, offspring, color=PALETTE[2], lw=2.0,
         label=f"offspring (mean {mu+R:.0f})")
# shade selected upper tail
thr = mu + 0.84 * sd
axL.fill_between(x, 0, parent, where=x >= thr, color=PALETTE[1] + "40")
for m, col, lab in [(mu, PALETTE[0], "50"), (sel_mean, PALETTE[1], "S: 60"),
                    (mu + R, PALETTE[2], "55")]:
    axL.axvline(m, color=col, lw=1.0, ls="--")
axL.annotate("selected\nparents\n(mean 60)", xy=(60, 0.01), xytext=(61, 0.045),
             fontsize=7.6, color=PALETTE[1])
axL.annotate(r"$R=h^2S=0.5\times10=5$", xy=(mu + R, 0.05), xytext=(31, 0.062),
             fontsize=8.2, color=INK)
axL.set_xlabel("stem height (cm)")
axL.set_ylabel("density")
axL.set_title("Selection differential and response", fontsize=10)
axL.set_ylim(0, 0.075)
axL.legend(fontsize=7.8, loc="upper right")

# ---- offspring on mid-parent, slope = h^2 ---------------------------------
n = 300
midparent = rng.normal(0, 1, n)
for h2v, col in [(0.5, PALETTE[0]), (0.1, PALETTE[3])]:
    off = h2v * midparent + rng.normal(0, np.sqrt(1 - h2v**2) * 0.7, n)
    axR.scatter(midparent, off, s=6, color=col + "70", linewidths=0)
    xx = np.array([-2.5, 2.5])
    axR.plot(xx, h2v * xx, color=col, lw=2.0, label=fr"$h^2={h2v}$ (slope)")
axR.set_xlabel("mid-parent breeding value (sd)")
axR.set_ylabel("offspring value (sd)")
axR.set_title("Response slope = $h^2$", fontsize=10)
axR.set_xlim(-2.6, 2.6)
axR.set_ylim(-2.6, 2.6)
axR.legend(fontsize=8.3, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/quantitative-genetics.svg")
