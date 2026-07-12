# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Riemann vs. Lebesgue integration: slice the domain vs. slice the range."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# A smooth non-negative curve on [0, 4].
def f(x):
    return 0.5 + 2.2 * np.exp(-0.5 * ((x - 1.7) / 0.9) ** 2) \
               + 0.4 * np.exp(-0.5 * ((x - 3.1) / 0.5) ** 2)

x = np.linspace(0, 4, 400)
y = f(x)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5), sharey=True)

# ---- Left: Riemann sum — partition the DOMAIN into vertical strips ----
n = 12
edges = np.linspace(0, 4, n + 1)
mids = 0.5 * (edges[:-1] + edges[1:])
axL.bar(edges[:-1], f(mids), width=4 / n, align="edge",
        color=PALETTE[0], alpha=0.25, edgecolor=PALETTE[0], linewidth=0.8)
axL.plot(x, y, color=INK, lw=1.8)
axL.set_title("Riemann: slice the domain")
axL.set_xlabel("$x$")
axL.set_ylabel("$f(x)$")
axL.annotate(r"width $\Delta x$", xy=(2.0, 0.15), xytext=(2.4, 0.55),
             fontsize=8.5, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))

# ---- Right: Lebesgue — partition the RANGE into horizontal layers ----
axR.plot(x, y, color=INK, lw=1.8)
levels = np.linspace(0, y.max(), 13)
dt = levels[1] - levels[0]
for k, t in enumerate(levels[:-1]):
    axR.fill_between(x, t, t + dt, where=(y > t),
                     color=PALETTE[1], alpha=0.30 if k % 2 else 0.16, linewidth=0)
# Highlight one level set {f > t*} with its measure (a horizontal extent).
tstar = 1.3
mask = y > tstar
xs = x[mask]
axR.hlines(tstar, xs.min(), xs.max(), color=PALETTE[3], lw=2.2)
axR.annotate(r"$\mu(\{f > t\})$", xy=(0.5 * (xs.min() + xs.max()), tstar),
             xytext=(2.35, 1.95), fontsize=9, color=INK,
             arrowprops=dict(arrowstyle="->", color=PALETTE[3], lw=1.1))
axR.set_title("Lebesgue: slice the range")
axR.set_xlabel("$x$")

fig.tight_layout()
save(fig, "assets/figures/lebesgue-integration.svg")
