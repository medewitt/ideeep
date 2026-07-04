# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Within-host virus dynamics with a B-cell (antibody) and T-cell (CTL)
immune response, in the style of Nowak & May. Two regimes: a strong immune
response that clears the virus, and a weak response that settles to a
persistent set point."""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()

# Scaled parameters (arbitrary within-host units).
lam, d = 1.0, 0.1        # target-cell supply and turnover
beta = 1.0               # infection of target cells by virus
a = 0.5                  # baseline death of infected cells
k, u = 5.0, 3.0          # virion production and clearance
p = 1.0                  # extra killing of infected cells by CTL
q = 1.0                  # neutralization of virus by antibody
b, h = 0.3, 0.3          # decay of CTL and antibody effectors


def rhs(t, y, c, g):
    x, yi, v, z, w = y
    dx = lam - d * x - beta * x * v
    dyi = beta * x * v - a * yi - p * yi * z
    dv = k * yi - u * v - q * v * w
    dz = c * yi * z - b * z        # CTL proliferation on infected cells
    dw = g * v * w - h * w         # antibody proliferation on virus
    return [dx, dyi, dv, dz, dw]


x0 = lam / d                        # uninfected steady state = 10
y0 = [x0, 0.0, 1e-2, 1e-3, 1e-3]    # small viral seed, primed effectors
t = np.linspace(0, 120, 1600)

# Strong immune response clears the virus to a low set point; without an
# effective adaptive response (c = g = 0) the virus persists at the
# target-cell-limited set point.
strong = solve_ivp(rhs, [0, 120], y0, args=(10.0, 10.0),
                   method="LSODA", t_eval=t, rtol=1e-8, atol=1e-10, max_step=0.5)
weak = solve_ivp(rhs, [0, 120], y0, args=(0.0, 0.0),
                 method="LSODA", t_eval=t, rtol=1e-8, atol=1e-10, max_step=0.5)

fig, (axv, axi) = plt.subplots(1, 2, figsize=(8.4, 3.8))

eps = 1e-8
axv.plot(t, np.log10(strong.y[2] + eps), color=PALETTE[2], lw=2,
         label="strong response (clearance)")
axv.plot(t, np.log10(weak.y[2] + eps), color=PALETTE[1], lw=2,
         label="weak response (persistence)")
axv.set_xlabel("time (days)")
axv.set_ylabel(r"viral load $\log_{10} v$")
axv.set_title("Viral load")
axv.legend(loc="upper right", fontsize=8)

axi.plot(t, strong.y[3], color=PALETTE[3], lw=2, label="T cells (CTL) $z$")
axi.plot(t, strong.y[4], color=PALETTE[0], lw=2, label="B cells / antibody $w$")
axi.plot(t, strong.y[2], color=MUTED, lw=1.5, ls="--", label="virus $v$")
axi.set_xlabel("time (days)")
axi.set_ylabel("effector / virus level")
axi.set_title("Immune effectors (clearance case)")
axi.legend(loc="upper right", fontsize=8)

print(f"strong: final viral load v = {strong.y[2][-1]:.2e}")
print(f"weak:   final viral load v = {weak.y[2][-1]:.2e}")

fig.tight_layout()
save(fig, "assets/figures/within-host-dynamics.svg")
