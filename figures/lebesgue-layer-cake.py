# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""What the layer-cake code computes: the mean infectious period is the area
under the survival curve, E[T] = ∫ S(t) dt = 1/gamma, for S(t) = e^{-gamma t}."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

gamma = 0.4
mean = 1 / gamma                       # = 2.5, the value the code prints
t = np.linspace(0, 14, 700)
S = np.exp(-gamma * t)

fig, ax = plt.subplots(figsize=(6.6, 3.8))

# The integral E[T] = ∫ S(t) dt is the shaded area under the survival curve.
ax.fill_between(t, S, color=PALETTE[0], alpha=0.18, linewidth=0)
ax.plot(t, S, color=PALETTE[0], lw=2.0, label=r"$S(t)=\Pr(T>t)=e^{-\gamma t}$")

# The layer-cake reading: each height t contributes the level-set measure
# mu({T > t}) = S(t). Draw a few horizontal layers to make that concrete.
for tt in (0.6, 1.4, 2.4, 3.6):
    s = np.exp(-gamma * tt)
    ax.hlines(s, 0, tt, color=MUTED, lw=0.8, ls=":")
    ax.plot([tt], [s], "o", color=PALETTE[1], ms=4, zorder=4)

# Mean marker.
ax.axvline(mean, color=PALETTE[1], lw=1.4, ls="--")
ax.annotate(r"mean $=1/\gamma=2.5$", xy=(mean, np.exp(-gamma * mean)),
            xytext=(mean + 0.5, 0.62), fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=1.1))
ax.annotate(r"$\mathbb{E}[T]=\int_0^\infty S(t)\,dt$" "\n" r"$=$ shaded area $=2.5$",
            xy=(1.6, 0.28), xytext=(4.6, 0.42), fontsize=10, color=INK)

ax.set_xlim(0, 14)
ax.set_ylim(0, 1.02)
ax.set_xlabel("time since infection $t$ (days)")
ax.set_ylabel("survival $S(t)$")
ax.set_title("Mean infectious period as area under the survival curve")
ax.legend(loc="upper right")

save(fig, "assets/figures/lebesgue-layer-cake.svg")
