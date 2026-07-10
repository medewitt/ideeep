# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Floquet theory for the Mathieu equation.

Left: the Ince-Strutt stability chart. For the Mathieu equation
x'' + (delta + 2*eps*cos(2t)) x = 0 we integrate the fundamental matrix over
one period T = pi to form the monodromy matrix, then shade where the zero
solution is unstable. Because the undamped equation is Hamiltonian, det = 1
and the multipliers are reciprocal, so instability is exactly |trace(M)| > 2;
the unstable tongues emanate from delta = n^2. Right: a bounded (stable) and a
growing (unstable) solution, one point drawn from each region. No RNG; the grid
integration is a fixed-step RK4 vectorised across the whole (delta, eps) grid.
"""
import numpy as np
import matplotlib.pyplot as plt

from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

T = np.pi                      # forcing period of cos(2t)


def trace_monodromy(delta, eps, n_steps=600):
    """Trace of the monodromy matrix over one period, vectorised on a grid.

    Integrates Y' = A(t) Y, Y(0) = I, with A = [[0, 1], [-q(t), 0]] and
    q(t) = delta + 2*eps*cos(2t). delta, eps are arrays of the same shape.
    """
    dt = T / n_steps
    # fundamental matrix components, identity at t = 0
    y11 = np.ones_like(delta); y12 = np.zeros_like(delta)
    y21 = np.zeros_like(delta); y22 = np.ones_like(delta)

    def deriv(t, a11, a12, a21, a22):
        q = delta + 2.0 * eps * np.cos(2.0 * t)
        return a21, a22, -q * a11, -q * a12

    for k in range(n_steps):
        t = k * dt
        k1 = deriv(t, y11, y12, y21, y22)
        k2 = deriv(t + dt/2, y11 + dt/2*k1[0], y12 + dt/2*k1[1],
                   y21 + dt/2*k1[2], y22 + dt/2*k1[3])
        k3 = deriv(t + dt/2, y11 + dt/2*k2[0], y12 + dt/2*k2[1],
                   y21 + dt/2*k2[2], y22 + dt/2*k2[3])
        k4 = deriv(t + dt, y11 + dt*k3[0], y12 + dt*k3[1],
                   y21 + dt*k3[2], y22 + dt*k3[3])
        y11 = y11 + dt/6*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
        y12 = y12 + dt/6*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
        y21 = y21 + dt/6*(k1[2] + 2*k2[2] + 2*k3[2] + k4[2])
        y22 = y22 + dt/6*(k1[3] + 2*k2[3] + 2*k3[3] + k4[3])
    return y11 + y22


fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.2, 3.7),
                               gridspec_kw={"width_ratios": [1.25, 1.0]})

# ---- Left: Ince-Strutt stability chart ------------------------------------
d = np.linspace(0.0, 4.5, 320)
e = np.linspace(0.0, 1.0, 220)
D, E = np.meshgrid(d, e)
tr = trace_monodromy(D, E)
unstable = np.abs(tr) > 2.0

axL.contourf(D, E, unstable.astype(float), levels=[0.5, 1.5],
             colors=[PALETTE[1]], alpha=0.55)
axL.contour(D, E, np.abs(tr), levels=[2.0], colors=[PALETTE[1]],
            linewidths=1.0)
for n in (1, 2):                              # tongue tips at delta = n^2
    axL.plot(n * n, 0, "o", color=INK, ms=4)
axL.text(1.0, 0.62, "unstable\ntongues", ha="center", va="center",
         fontsize=8.5, color=PALETTE[1])
axL.text(3.1, 0.28, "stable", ha="center", va="center",
         fontsize=9, color=MUTED)
axL.set_xlabel(r"$\delta$ (mean stiffness)")
axL.set_ylabel(r"$\varepsilon$ (forcing amplitude)")
axL.set_title("Ince–Strutt chart", fontsize=10)
axL.set_xlim(0, 4.5)
axL.set_ylim(0, 1.0)

# ---- Right: a stable and an unstable solution -----------------------------
def solve_mathieu(delta, eps, t_end=8 * np.pi, n=4000):
    t = np.linspace(0.0, t_end, n)
    dt = t[1] - t[0]
    x = np.empty(n); v = np.empty(n)
    x[0], v[0] = 1.0, 0.0
    for i in range(n - 1):
        q = delta + 2.0 * eps * np.cos(2.0 * t[i])
        a = -q * x[i]
        v[i+1] = v[i] + dt * a
        x[i+1] = x[i] + dt * v[i+1]
    return t, x


t_s, x_s = solve_mathieu(2.0, 0.2)            # stable band
t_u, x_u = solve_mathieu(1.0, 0.4)            # inside first tongue
axR.plot(t_u / np.pi, x_u, color=PALETTE[1], lw=1.4,
         label=r"unstable ($\delta{=}1,\varepsilon{=}0.4$)")
axR.plot(t_s / np.pi, x_s, color=PALETTE[0], lw=1.4,
         label=r"stable ($\delta{=}2,\varepsilon{=}0.2$)")
axR.axhline(0, color=MUTED, lw=0.6)
axR.set_xlabel(r"time $t/\pi$ (periods)")
axR.set_ylabel(r"$x(t)$")
axR.set_title("Solutions", fontsize=10)
axR.legend(loc="upper left", fontsize=7.5)
axR.set_ylim(-6, 6)

save(fig, "assets/figures/floquet-theory.svg")
