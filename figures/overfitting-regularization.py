# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""The central tension of machine learning. Left: three polynomial fits to the
same noisy data -- too simple (underfit, high bias), about right, and too
flexible (overfit, high variance, chasing the noise). Right: as model
complexity grows, training error falls monotonically but held-out validation
error is U-shaped, bottoming out at the sweet spot; the gap between the curves
is overfitting.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(0)


def truth(x):
    return np.sin(1.5 * x)


xtr = np.sort(rng.uniform(0, 4, 18))
ytr = truth(xtr) + rng.normal(0, 0.25, xtr.size)
xte = np.sort(rng.uniform(0, 4, 200))
yte = truth(xte) + rng.normal(0, 0.25, xte.size)
xg = np.linspace(0, 4, 250)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.6, 3.9))

# --- left: under / good / over fit ---
ax0.plot(xg, truth(xg), color=MUTED, lw=1.4, ls=":", label="true function")
ax0.scatter(xtr, ytr, s=22, color=INK, zorder=3, label="training data")
for deg, col, name in [(1, PALETTE[1], "degree 1 (underfit)"),
                       (4, PALETTE[2], "degree 4 (good)"),
                       (15, PALETTE[3], "degree 15 (overfit)")]:
    coef = np.polyfit(xtr, ytr, deg)
    ax0.plot(xg, np.polyval(coef, xg), color=col, lw=1.8, label=name)
ax0.set_ylim(-2.2, 2.2)
ax0.set_title("Under-, well-, and over-fitting")
ax0.set_xlabel("x")
ax0.set_ylabel("y")
ax0.legend(loc="lower left", fontsize=7.3)

# --- right: train vs validation error against complexity ---
degrees = np.arange(1, 16)
train_mse, val_mse = [], []
for d in degrees:
    coef = np.polyfit(xtr, ytr, d)
    train_mse.append(np.mean((np.polyval(coef, xtr) - ytr) ** 2))
    val_mse.append(np.mean((np.polyval(coef, xte) - yte) ** 2))
val_mse = np.clip(val_mse, None, 2.0)
ax1.plot(degrees, train_mse, "o-", color=PALETTE[0], lw=1.8, ms=4,
         label="training error")
ax1.plot(degrees, val_mse, "s-", color=PALETTE[1], lw=1.8, ms=4,
         label="validation error")
best = degrees[int(np.argmin(val_mse))]
ax1.axvline(best, color=MUTED, lw=1.0, ls="--")
ax1.text(best + 0.3, 1.6, f"sweet spot\n(degree {best})", fontsize=8, color=INK)
ax1.set_ylim(0, 2.05)
ax1.set_title("Training vs validation error")
ax1.set_xlabel("model complexity (polynomial degree)")
ax1.set_ylabel("mean squared error")
ax1.legend(loc="upper center", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/overfitting-regularization.svg")
