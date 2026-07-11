# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""The spatial transmission kernel K(d) = (1 + (d/d0)^2)^(-alpha) at
different parameter values.

  (a) Varying the tail exponent alpha at fixed local scale d0: a smaller
      alpha gives a heavier tail, so long-range "sparks" are more likely.
  (b) Varying the local scale d0 at fixed alpha: a larger d0 stretches the
      near-field over which spread is essentially certain.
All curves are normalized to K(0) = 1 and shown on a log axis so the tails
are visible.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

d = np.linspace(0.0, 15.0, 500)
fig, (axa, axb) = plt.subplots(1, 2, figsize=(8.8, 3.7), sharey=True)

# --- (a) vary the tail exponent alpha (d0 fixed) --------------------------
d0 = 0.4
for i, alpha in enumerate([0.5, 1.0, 1.5, 3.0]):
    K = (1.0 + (d / d0) ** 2) ** (-alpha)
    axa.semilogy(d, K, color=PALETTE[i], lw=2.0, label=rf"$\alpha$ = {alpha}")
axa.set_ylim(1e-5, 1.5)
axa.set_xlabel("distance between farms $d$ (km)")
axa.set_ylabel("relative transmission $K(d)$")
axa.set_title(r"(a) Tail exponent $\alpha$  ($d_0 = 0.4$)")
axa.legend(fontsize=8, loc="upper right", title="heavier tail $\\uparrow$")
axa.annotate("smaller $\\alpha$:\nfatter tail, more sparks", xy=(5.5, 7e-2),
             xytext=(1.6, 1.3e-3), fontsize=8, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=INK))

# --- (b) vary the local scale d0 (alpha fixed) ----------------------------
alpha = 1.5
for i, d0 in enumerate([0.2, 0.5, 1.0, 2.0]):
    K = (1.0 + (d / d0) ** 2) ** (-alpha)
    axb.semilogy(d, K, color=PALETTE[i], lw=2.0, label=rf"$d_0$ = {d0}")
axb.set_ylim(1e-5, 1.5)
axb.set_xlabel("distance between farms $d$ (km)")
axb.set_title(r"(b) Local scale $d_0$  ($\alpha = 1.5$)")
axb.legend(fontsize=8, loc="upper right", title="wider near-field $\\uparrow$")

fig.suptitle("The transmission kernel at different parameter values",
             fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "assets/figures/foot-and-mouth-kernel.svg")
