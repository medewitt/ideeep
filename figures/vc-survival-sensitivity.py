# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Why mosquito survival is the dominant lever on transmission. Vectorial capacity
depends on daily survival p through p^n / (-ln p), where n is the extrinsic
incubation period, so it climbs steeply with p: the mosquito must survive the
whole incubation period to transmit. The field estimate (p about 0.87) sits on the
steep part of the curve, which is why interventions that shorten mosquito life -
bed nets, indoor spraying - cut capacity so effectively."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(11)
hbr = rng.poisson(6, size=80).mean()          # human biting rate (bites/person/night)
a = 0.9 / 3.0                                  # biting rate on humans per day
n_eip = 11


def V(p):
    return hbr * a * p**n_eip / (-np.log(p))


pp = np.linspace(0.70, 0.96, 300)
p_field = (78 / 120) ** (1 / 3.0)              # daily survival from parity

fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.plot(pp, V(pp), color=PALETTE[0], lw=2.4)
for p0, col in [(0.80, PALETTE[1]), (p_field, INK), (0.90, PALETTE[2])]:
    ax.plot([p0, p0], [0, V(p0)], color=col, lw=1.0, ls=":")
    ax.scatter([p0], [V(p0)], s=55, color=col, zorder=5)
ax.annotate(f"field estimate\np ≈ {p_field:.2f},  V ≈ {V(p_field):.1f}",
            xy=(p_field, V(p_field)), xytext=(0.735, 5.6), fontsize=8.4, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
ax.annotate(f"p = 0.90 → V ≈ {V(0.90):.1f}", xy=(0.90, V(0.90)),
            xytext=(0.80, 7.3), fontsize=8.2, color=PALETTE[2],
            arrowprops=dict(arrowstyle="->", color=PALETTE[2], lw=0.9))
ax.annotate(f"p = 0.80 → V ≈ {V(0.80):.1f}", xy=(0.80, V(0.80)),
            xytext=(0.83, 1.4), fontsize=8.2, color=PALETTE[1],
            arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=0.9))
ax.set_xlabel("daily survival probability  $p$")
ax.set_ylabel("vectorial capacity  $V$")
ax.set_title("A 10-point drop in survival collapses capacity", fontsize=9.6)
ax.set_ylim(0, 8)
fig.tight_layout()
save(fig, "assets/figures/vc-survival-sensitivity.svg")
