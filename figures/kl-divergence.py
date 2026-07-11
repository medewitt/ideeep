# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""KL divergence: asymmetry and its consequence. Left: two Gaussians and the
two directions of KL, which differ -- KL is not a distance. Right: approximating
a bimodal target with a single Gaussian. Minimizing the forward KL(p||q) spreads
q to cover both modes (mean-seeking); minimizing the reverse KL(q||p), as
variational inference does, locks q onto one mode (mode-seeking).
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()


def gauss(x, m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))


def kl_gauss(m0, s0, m1, s1):
    return np.log(s1 / s0) + (s0 ** 2 + (m0 - m1) ** 2) / (2 * s1 ** 2) - 0.5


fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.6, 3.9))

# --- left: two Gaussians, asymmetric KL ---
x = np.linspace(-6, 8, 400)
m0, s0, m1, s1 = 0.0, 1.0, 2.0, 1.6
ax0.plot(x, gauss(x, m0, s0), color=PALETTE[0], lw=2, label="$p = \\mathcal{N}(0,1)$")
ax0.fill_between(x, gauss(x, m0, s0), color=PALETTE[0], alpha=0.12)
ax0.plot(x, gauss(x, m1, s1), color=PALETTE[1], lw=2,
         label="$q = \\mathcal{N}(2,1.6^2)$")
ax0.fill_between(x, gauss(x, m1, s1), color=PALETTE[1], alpha=0.12)
ax0.set_title("KL is asymmetric")
ax0.set_xlabel("x")
ax0.set_ylabel("density")
ax0.legend(loc="upper right", fontsize=8)
ax0.text(-5.8, 0.34, f"$D_{{KL}}(p\\,\\|\\,q) = {kl_gauss(m0,s0,m1,s1):.2f}$",
         fontsize=9, color=INK)
ax0.text(-5.8, 0.30, f"$D_{{KL}}(q\\,\\|\\,p) = {kl_gauss(m1,s1,m0,s0):.2f}$",
         fontsize=9, color=INK)

# --- right: forward vs reverse KL fit of a single Gaussian to a bimodal target ---
xt = np.linspace(-6, 6, 400)
target = 0.5 * gauss(xt, -2.2, 0.55) + 0.5 * gauss(xt, 2.2, 0.7)   # mixture
# forward KL(p||q): moment-matching -> mean and variance of the mixture
mean_t = 0.5 * (-2.2) + 0.5 * (2.2)
var_t = 0.5 * (0.55 ** 2 + 2.2 ** 2) + 0.5 * (0.7 ** 2 + 2.2 ** 2) - mean_t ** 2
fwd = gauss(xt, mean_t, np.sqrt(var_t))
rev = gauss(xt, 2.2, 0.7)                                          # locks onto a mode
ax1.plot(xt, target, color=INK, lw=2, label="target $p$ (bimodal)")
ax1.plot(xt, fwd, color=PALETTE[0], lw=2, ls="--",
         label="forward KL: covers both")
ax1.plot(xt, rev, color=PALETTE[1], lw=2, ls="--",
         label="reverse KL: one mode")
ax1.set_title("Forward vs reverse KL")
ax1.set_xlabel("x")
ax1.set_ylabel("density")
ax1.legend(loc="upper left", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/kl-divergence.svg")
