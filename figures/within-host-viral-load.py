# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Within-host viral dynamics from the target-cell-limited (TCL) model.

Three panels:
(a) the T-I-V compartment diagram (target cells, infected cells, free virus);
(b) the viral-load trajectory on a log scale, showing exponential rise,
    peak set by target-cell depletion, and clearance;
(c) an antiviral that reduces virus production p by efficacy epsilon,
    started early versus late, shifting the peak and the area under the
    viral-load curve.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# Target-cell-limited parameters (scaled within-host units).
BETA, DELTA, P, C = 5e-7, 3.0, 40.0, 6.0
T0, V0 = 1e7, 1e-2
R0 = BETA * T0 * P / (DELTA * C)


def simulate(eps=0.0, t_treat=0.0, tmax=12.0):
    """Integrate the TCL model; a drug cuts production p by eps after t_treat."""
    def rhs(t, y):
        T, I, V = y
        p_eff = P * (1 - eps) if t >= t_treat else P
        return [-BETA * T * V, BETA * T * V - DELTA * I, p_eff * I - C * V]
    sol = solve_ivp(rhs, [0, tmax], [T0, 0.0, V0], method="LSODA",
                    rtol=1e-9, atol=1e-9, dense_output=True)
    t = np.linspace(0, tmax, 3000)
    return t, sol.sol(t)[2]


fig, (axd, axb, axc) = plt.subplots(1, 3, figsize=(11.6, 3.7))

# ---- Panel (a): compartment diagram.
axd.set_xlim(0, 10)
axd.set_ylim(0, 10)
axd.axis("off")
axd.set_title("(a) target-cell-limited model")
boxes = {"T": (1.4, 6.0, "$T$\ntarget"), "I": (5.0, 6.0, "$I$\ninfected"),
         "V": (5.0, 1.7, "$V$\nvirus")}
for key, (x, y, lab) in boxes.items():
    axd.add_patch(FancyBboxPatch((x, y), 2.2, 1.9,
                  boxstyle="round,pad=0.1", linewidth=1.4,
                  edgecolor=INK, facecolor="none"))
    axd.text(x + 1.1, y + 0.95, lab, ha="center", va="center", fontsize=10)


def arrow(a, b, color, rad=0.0):
    axd.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13,
                  color=color, lw=1.4,
                  connectionstyle=f"arc3,rad={rad}"))


arrow((3.6, 6.95), (5.0, 6.95), PALETTE[0])          # T -> I (infection)
axd.text(4.3, 7.5, r"$\beta T V$", ha="center", fontsize=9, color=PALETTE[0])
arrow((6.1, 6.0), (6.1, 3.6), PALETTE[2])            # I -> V (production)
axd.text(6.9, 4.8, r"$pI$", ha="center", fontsize=9, color=PALETTE[2])
arrow((5.0, 2.65), (2.6, 6.0), PALETTE[1], rad=0.25)  # V -> infection of T
axd.text(2.7, 4.0, "new\ninfection", ha="center", fontsize=8, color=PALETTE[1])
arrow((7.2, 6.5), (8.7, 6.5), MUTED)                 # I death
axd.text(7.95, 7.05, r"$\delta I$", ha="center", fontsize=9, color=MUTED)
arrow((7.2, 2.2), (8.7, 2.2), MUTED)                 # V clearance
axd.text(7.95, 2.75, r"$cV$", ha="center", fontsize=9, color=MUTED)

# ---- Panel (b): viral-load trajectory (log scale).
t, V = simulate()
ipk = int(np.argmax(V))
axb.semilogy(t, V, color=PALETTE[0], lw=2)
axb.plot(t[ipk], V[ipk], "o", color=PALETTE[1], ms=7)
axb.annotate(f"peak\n$t={t[ipk]:.1f}$ d", xy=(t[ipk], V[ipk]),
             xytext=(t[ipk] + 2.4, V[ipk] * 0.9), fontsize=8,
             arrowprops=dict(arrowstyle="->", color=INK))
axb.axhline(1e2, color=MUTED, ls="--", lw=0.9)
axb.text(0.2, 1.5e2, "PCR / detection threshold", fontsize=7.5, color=MUTED)
axb.text(1.2, 3e5, "exponential\nrise", fontsize=8, color=PALETTE[2])
axb.text(7.0, 3e4, "clearance", fontsize=8, color=PALETTE[3])
axb.set_xlabel("time since infection (days)")
axb.set_ylabel("viral load $V$ (log scale)")
axb.set_title("(b) viral-load trajectory")
axb.set_ylim(1e-1, 1e8)

# ---- Panel (c): antiviral efficacy and timing.
eps = 0.6
scen = [(0.0, 0.0, PALETTE[0], "no drug"),
        (eps, 0.5, PALETTE[2], f"$\\varepsilon={eps}$, day 0.5"),
        (eps, 3.0, PALETTE[1], f"$\\varepsilon={eps}$, day 3")]
for e, tt, col, lab in scen:
    t, V = simulate(e, tt)
    auc = np.trapezoid(V, t)
    axc.semilogy(t, V, color=col, lw=2, label=f"{lab} (AUC {auc:.1e})")
axc.set_xlabel("time since infection (days)")
axc.set_ylabel("viral load $V$ (log scale)")
axc.set_title("(c) antiviral efficacy and timing")
axc.set_ylim(1e-1, 1e8)
axc.legend(loc="lower center", fontsize=7.5)

fig.tight_layout()
save(fig, "assets/figures/within-host-viral-load.svg")
