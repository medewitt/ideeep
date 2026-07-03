# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""Ross-Macdonald R0 shows squared dependence on the mosquito biting rate."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE
apply_style()

rng = np.random.default_rng(1)

# Fixed parameters.
m = 10.0      # mosquitoes per host
b = 0.5       # transmission efficiency vector -> host
c = 0.5       # transmission efficiency host -> vector
mu = 0.1      # mosquito mortality rate
gamma = 0.1   # host recovery rate

a = np.linspace(0.0, 0.6, 400)

# True Ross-Macdonald: R0 proportional to a^2.
R0 = m * a**2 * b * c / (mu * gamma)

# Hypothetical linear dependence (a to the first power), scaled to match
# the true curve at a reference biting rate.
a_ref = 0.4
k = m * a_ref**2 * b * c / (mu * gamma) / a_ref   # slope so both meet at a_ref
R0_linear = k * a

fig, ax = plt.subplots()
ax.plot(a, R0, color=PALETTE[0], linewidth=2.2,
        label=r"Ross-Macdonald  $R_0 \propto a^2$")
ax.plot(a, R0_linear, color=PALETTE[1], linewidth=2.0, linestyle="--",
        label=r"hypothetical linear  $R_0 \propto a$")

ax.axhline(1.0, color="0.4", linewidth=1.2, linestyle=":",
           label=r"epidemic threshold $R_0=1$")

# Annotate the fourfold effect of halving the biting rate.
a_hi = 0.4
a_lo = 0.2
R0_hi = m * a_hi**2 * b * c / (mu * gamma)
R0_lo = m * a_lo**2 * b * c / (mu * gamma)
ax.scatter([a_hi, a_lo], [R0_hi, R0_lo], color=PALETTE[0], zorder=5, s=30)
ax.annotate(
    "halving $a$\ncuts $R_0$ fourfold\n"
    fr"({R0_hi:.0f} $\rightarrow$ {R0_lo:.0f})",
    xy=(a_lo, R0_lo), xytext=(0.22, R0_hi * 0.75),
    arrowprops=dict(arrowstyle="->", color="0.3"),
    fontsize="small")

ax.set_xlabel("Biting rate $a$ (bites per mosquito per day)")
ax.set_ylabel("Basic reproduction number $R_0$")
ax.set_xlim(0, 0.6)
ax.set_ylim(0, None)
ax.set_title("Vector-borne transmission:\n"
             r"$R_0 = m\,a^2\,b\,c / (\mu\,\gamma)$ scales with the "
             "square of biting rate")
ax.legend(loc="upper left", fontsize="small")

save(fig, "assets/figures/vector-borne.svg")
