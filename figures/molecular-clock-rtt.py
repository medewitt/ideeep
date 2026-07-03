# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Root-to-tip regression estimating substitution rate and tMRCA."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(7)

rate = 1e-3          # subs/site/year
tMRCA = 2015.0       # a few years before first sample
n = 60

dates = rng.uniform(2018.0, 2023.0, n)
noise = rng.normal(0, 6e-4, n)
dist = rate * (dates - tMRCA) + noise
dist = np.clip(dist, 0, None)

# Linear fit: distance = slope * date + intercept.
slope, intercept = np.polyfit(dates, dist, 1)
x_int = -intercept / slope  # date where distance = 0 -> estimated tMRCA
xs = np.linspace(tMRCA - 0.5, dates.max() + 0.3, 100)

fig, ax = plt.subplots()
ax.scatter(dates, dist, s=26, color=PALETTE[0], alpha=0.75,
           edgecolor="none", rasterized=True, label="tips")
ax.plot(xs, slope * xs + intercept, color=PALETTE[1], lw=2,
        label="regression")

ax.axhline(0, color="#b0b8c0", lw=0.8)
ax.plot(x_int, 0, "o", color=PALETTE[3], ms=8, zorder=5)
ax.annotate(f"tMRCA $\\approx$ {x_int:.2f}\n(x-intercept)",
            xy=(x_int, 0), xytext=(x_int + 0.3, dist.max() * 0.35),
            arrowprops=dict(arrowstyle="->", color="#26323f"), fontsize=9)
ax.annotate(f"slope = rate\n$\\approx$ {slope:.2e} subs/site/yr",
            xy=(dates.mean(), slope * dates.mean() + intercept),
            xytext=(dates.min() + 0.2, dist.max() * 0.85), fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#26323f"))

print(f"true rate={rate:.2e}, estimated slope={slope:.3e} subs/site/yr")
print(f"true tMRCA={tMRCA}, estimated tMRCA={x_int:.2f}")

ax.set_xlabel("sampling date (year)")
ax.set_ylabel("root-to-tip distance (subs/site)")
ax.set_title("Molecular clock: root-to-tip regression")
ax.legend(loc="upper left", fontsize=9)

save(fig, "assets/figures/molecular-clock-rtt.svg")
