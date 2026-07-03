# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Lotka-Volterra competition zero-growth isoclines for stable coexistence."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(0)

K1 = K2 = 100.0
a12 = a21 = 0.5

# Interior equilibrium: N1 = (K1 - a12 K2) / (1 - a12 a21), symmetric here.
denom = 1 - a12 * a21
N1_eq = (K1 - a12 * K2) / denom
N2_eq = (K2 - a21 * K1) / denom
print(f"interior equilibrium: N1*={N1_eq:.2f}, N2*={N2_eq:.2f}")

# dN1/dt = 0 isocline: N2 = (K1 - N1) / a12
# dN2/dt = 0 isocline: N2 = K2 - a21 * N1
N1 = np.linspace(0, max(K1, K1 / a12) * 1.02, 200)
iso1 = (K1 - N1) / a12          # N1 zero-growth
iso2 = K2 - a21 * N1            # N2 zero-growth

fig, ax = plt.subplots()
ax.plot(N1, iso1, color=PALETTE[0], lw=2,
        label=r"$dN_1/dt=0$ isocline")
ax.plot(N1, iso2, color=PALETTE[1], lw=2,
        label=r"$dN_2/dt=0$ isocline")

# Equilibrium point.
ax.plot(N1_eq, N2_eq, "o", color=PALETTE[3], ms=9, zorder=5)
ax.annotate(f"coexistence\n({N1_eq:.0f}, {N2_eq:.0f})",
            xy=(N1_eq, N2_eq), xytext=(N1_eq + 22, N2_eq + 30),
            arrowprops=dict(arrowstyle="->", color="#26323f"),
            fontsize=9)


def deriv(N1v, N2v):
    r = 0.4
    dN1 = r * N1v * (K1 - N1v - a12 * N2v) / K1
    dN2 = r * N2v * (K2 - N2v - a21 * N1v) / K2
    return dN1, dN2


# Trajectory arrows converging to the interior equilibrium.
starts = [(140.0, 20.0), (15.0, 150.0), (30.0, 30.0), (160.0, 160.0)]
for (x0, y0) in starts:
    xs, ys = [x0], [y0]
    x, y = x0, y0
    dt = 0.05
    for _ in range(4000):
        dx, dy = deriv(x, y)
        x += dx * dt
        y += dy * dt
        xs.append(x)
        ys.append(y)
    ax.plot(xs, ys, color="#5b6b7a", lw=0.9, alpha=0.7)
    # arrow near the start showing direction of flow
    i = 40
    ax.annotate("", xy=(xs[i + 1], ys[i + 1]), xytext=(xs[i], ys[i]),
                arrowprops=dict(arrowstyle="-|>", color="#5b6b7a", lw=1.4))

ax.set_xlim(0, 205)
ax.set_ylim(0, 205)
ax.set_xlabel(r"$N_1$")
ax.set_ylabel(r"$N_2$")
ax.set_title("Competition isoclines (stable coexistence)")
ax.legend(loc="upper right", fontsize=9)

save(fig, "assets/figures/competition-isoclines.svg")
