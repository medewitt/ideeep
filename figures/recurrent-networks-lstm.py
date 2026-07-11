# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""What a recurrent network is for. Left: a sequence model reads a weekly
incidence series one step at a time and rolls its hidden state forward to
forecast the coming weeks. Right: the LSTM cell, whose forget / input / output
gates let a long-term cell state survive across many steps -- the mechanism
that lets it remember a seasonal signal an ordinary RNN would wash out.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(1)

# --- left: a seasonal incidence series with a held-out forecast horizon ---
weeks = np.arange(104)
season = 30 * (1 + np.sin(2 * np.pi * (weeks - 8) / 52))
trend = 0.15 * weeks
signal = season + trend + 8
obs = signal + rng.normal(0, 3, weeks.size)
cut = 84
# a seasonal + trend fit on the observed weeks, rolled forward over the horizon
# (illustrative of the role a trained recurrent model plays)
def design(w):
    return np.c_[np.ones_like(w), w, np.sin(2 * np.pi * w / 52),
                 np.cos(2 * np.pi * w / 52)]
beta, *_ = np.linalg.lstsq(design(weeks[:cut]), obs[:cut], rcond=None)
fcast = design(weeks[cut:]) @ beta

fig = plt.figure(figsize=(9.6, 3.9))
ax0 = fig.add_axes([0.06, 0.15, 0.44, 0.74])
ax0.plot(weeks[:cut], obs[:cut], color=INK, lw=1.4, label="observed")
ax0.plot(weeks[cut:], fcast, color=PALETTE[1], lw=2.2, label="forecast")
ax0.plot(weeks[cut:], obs[cut:], "o", color=INK, ms=3, alpha=0.5,
         label="later truth")
ax0.axvline(cut, color=MUTED, lw=0.9, ls=":")
ax0.set_title("Sequence model forecasting incidence")
ax0.set_xlabel("week")
ax0.set_ylabel("cases")
ax0.legend(loc="upper left", fontsize=8)

# --- right: LSTM cell schematic ---
ax1 = fig.add_axes([0.55, 0.05, 0.43, 0.9])
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")
ax1.add_patch(FancyBboxPatch((0.8, 1.2), 8.4, 7.4, boxstyle="round,pad=0.1",
              linewidth=1.6, edgecolor=INK, facecolor="#2f6f9f10"))
ax1.text(5, 9.2, "LSTM cell", ha="center", fontsize=11, color=INK,
         fontweight="bold")

# cell-state conveyor belt across the top
ax1.add_patch(FancyArrowPatch((0.4, 7.3), (9.6, 7.3), arrowstyle="-|>",
              mutation_scale=16, color=PALETTE[2], lw=2.4))
ax1.text(0.2, 7.7, r"$c_{t-1}$", ha="left", fontsize=9, color=INK)
ax1.text(9.8, 7.7, r"$c_t$", ha="right", fontsize=9, color=INK)

# hidden state along the bottom
ax1.add_patch(FancyArrowPatch((0.4, 2.1), (9.6, 2.1), arrowstyle="-|>",
              mutation_scale=16, color=PALETTE[0], lw=2.0))
ax1.text(0.2, 1.5, r"$h_{t-1}$", ha="left", fontsize=9, color=INK)
ax1.text(9.8, 1.5, r"$h_t$", ha="right", fontsize=9, color=INK)

gates = [(2.6, "forget", PALETTE[1]), (5.0, "input", PALETTE[2]),
         (7.4, "output", PALETTE[3])]
for gx, name, col in gates:
    ax1.add_patch(Circle((gx, 4.7), 0.72, edgecolor=col, facecolor=col + "22",
                  linewidth=1.8))
    ax1.text(gx, 4.7, r"$\sigma$", ha="center", va="center", fontsize=11,
             color=INK)
    ax1.text(gx, 3.5, name, ha="center", fontsize=8.5, color=INK)
    ax1.add_patch(FancyArrowPatch((gx, 5.42), (gx, 7.28), arrowstyle="-|>",
                  mutation_scale=11, color=col, lw=1.4))
    ax1.add_patch(FancyArrowPatch((gx, 2.15), (gx, 3.98), arrowstyle="-",
                  color="0.6", lw=1.0, ls=":"))

save(fig, "assets/figures/recurrent-networks-lstm.svg")
