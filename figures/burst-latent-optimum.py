# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""The latent-period / burst-size trade-off and the phage fitness optimum.

Left: intracellular progeny accumulate after the eclipse period, rising then
saturating as host resources run out. Right: phage population growth rate
r(L) = ln B(L) / (T_a + L) peaks at an intermediate latent period, and the
optimum shifts to shorter lysis times when hosts are abundant (small search
time T_a). This is the marginal-value-theorem view of lysis timing.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# --- Intracellular accumulation B(L) -------------------------------------
eclipse = 15.0           # min, no progeny released before this
Bmax = 250.0             # saturating yield (host resources finite)
kappa = 50.0             # accumulation time-scale
L = np.linspace(0, 160, 600)


def burst(L):
    out = np.where(L > eclipse, Bmax * (1.0 - np.exp(-(L - eclipse) / kappa)), 0.0)
    return out


B = burst(L)
# early linear approximation B ~ p (L - eclipse), slope from the initial rate
p0 = Bmax / kappa
lin = np.clip(p0 * (L - eclipse), 0, None)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.9, 3.5))

axL.plot(L, B, color=PALETTE[0], lw=2.2, label="burst size $B(L)$")
axL.plot(L, lin, color=PALETTE[1], lw=1.4, ls="--", label="linear approx.")
axL.axvline(eclipse, color=MUTED, lw=1.0, ls=":")
axL.annotate("eclipse", xy=(eclipse, 170), xytext=(eclipse + 4, 168),
             fontsize=8.5, color=INK)
axL.set_xlabel("latent period $L$ (min)")
axL.set_ylabel("progeny per cell")
axL.set_title("intracellular accumulation")
axL.set_xlim(0, 160)
axL.set_ylim(0, 265)
axL.legend(fontsize=8.5, loc="lower right")

# --- Fitness r(L) = ln B(L) / (T_a + L) ----------------------------------
Lp = np.linspace(eclipse + 0.5, 160, 800)
Bp = burst(Lp)
for Ta, color, lab in [(3.0, PALETTE[2], "abundant hosts ($T_a=3$)"),
                       (60.0, PALETTE[3], "scarce hosts ($T_a=60$)")]:
    r = np.log(Bp) / (Ta + Lp)
    axR.plot(Lp, r, color=color, lw=2.2, label=lab)
    j = int(np.argmax(r))
    axR.plot(Lp[j], r[j], "o", color=color, ms=6)
    axR.axvline(Lp[j], color=color, lw=0.8, ls=":")

axR.set_xlabel("latent period $L$ (min)")
axR.set_ylabel("phage growth rate $r(L)$")
axR.set_title("an intermediate optimum")
axR.set_xlim(0, 160)
axR.legend(fontsize=8.5, loc="upper right")
axR.annotate("shorter optimal lysis\nwhen hosts are dense",
             xy=(22, 0.135), xytext=(52, 0.075), fontsize=8.0, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))

fig.tight_layout()
save(fig, "assets/figures/burst-latent-optimum.svg")
