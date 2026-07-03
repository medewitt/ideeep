# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""OLS fit of development rate vs temperature, with residual segments."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(1)
n = 40
x = rng.uniform(15, 35, n)
true_intercept, true_slope = 0.02, 0.03
y = true_intercept + true_slope * x + rng.normal(0, 0.08, n)

# OLS fit
slope, intercept = np.polyfit(x, y, 1)
yfit = intercept + slope * x
print(f"true slope = {true_slope}, fitted slope = {slope:.4f}")
print(f"fitted intercept = {intercept:.4f}")

xline = np.linspace(15, 35, 100)
yline = intercept + slope * xline

fig, ax = plt.subplots()
ax.scatter(x, y, color=PALETTE[0], s=28, alpha=0.8, rasterized=True,
           label="observations", zorder=3)
ax.plot(xline, yline, color=PALETTE[1], lw=2,
        label=f"OLS fit (slope={slope:.3f})", zorder=4)

# a few residual segments
order = np.argsort(x)
for i in order[::8]:
    ax.plot([x[i], x[i]], [y[i], yfit[i]], color=PALETTE[3], ls="--",
            lw=1, zorder=2)

ax.annotate(f"fitted slope = {slope:.3f}",
            xy=(28, intercept + slope * 28),
            xytext=(16, 1.05),
            arrowprops=dict(arrowstyle="->", color="#26323f"))

ax.set_xlabel("temperature (°C)")
ax.set_ylabel("development rate")
ax.set_title("Linear regression fit with residuals")
ax.legend(loc="upper left")

save(fig, "assets/figures/linear-regression-fit.svg")
