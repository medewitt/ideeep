# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Simpson's paradox: a trend that reverses when a confounding group is
ignored — the visual heart of why correlation is not causation."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()
rng = np.random.default_rng(1)


def make_group(n, x_mean, intercept):
    x = rng.normal(x_mean, 0.5, n)
    y = intercept - 0.8 * x + rng.normal(0, 0.3, n)   # within-group: negative
    return x, y


def ols(x, y):
    b1 = np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1)
    return y.mean() - b1 * x.mean(), b1


xA, yA = make_group(60, 2.0, 6.0)
xB, yB = make_group(60, 5.0, 10.0)
x = np.concatenate([xA, xB])
y = np.concatenate([yA, yB])

b0A, sA = ols(xA, yA)
b0B, sB = ols(xB, yB)
b0, sAll = ols(x, y)

print(f"within-group A slope       = {sA:+.2f}")
print(f"within-group B slope       = {sB:+.2f}")
print(f"pooled slope (ignore group) = {sAll:+.2f}   <- sign flips!")

fig, ax = plt.subplots()
ax.scatter(xA, yA, color=PALETTE[0], s=20, label="group A")
ax.scatter(xB, yB, color=PALETTE[1], s=20, label="group B")
for xg, b0g, sg, c in [(xA, b0A, sA, PALETTE[0]), (xB, b0B, sB, PALETTE[1])]:
    xr = np.array([xg.min(), xg.max()])
    ax.plot(xr, b0g + sg * xr, color=c, lw=1.6, ls="--")
xr = np.array([x.min(), x.max()])
ax.plot(xr, b0 + sAll * xr, color="#26323f", lw=2.4,
        label=f"pooled slope {sAll:+.2f}")
ax.text(0.03, 0.03,
        f"within groups: {sA:+.1f}, {sB:+.1f}\npooled: {sAll:+.1f}",
        transform=ax.transAxes, fontsize=9, va="bottom",
        bbox=dict(boxstyle="round", fc="white", ec="#c8d0d6"))
ax.set_xlabel("x  (e.g., hours of exercise)")
ax.set_ylabel("y  (e.g., disease risk)")
ax.set_title("Simpson's paradox: the group is a confounder")
ax.legend(loc="upper left", fontsize=9)
save(fig, "assets/figures/simpsons-paradox.svg")
