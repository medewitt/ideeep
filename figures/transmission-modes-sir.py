# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""SIR epidemic curves under density- vs frequency-dependent transmission, at
two host population sizes. Colour encodes the contact rule (density vs
frequency); dashing encodes the population size (N=100 vs N=500)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.integrate import solve_ivp
from _style import apply_style, save, PALETTE, MUTED

apply_style()

# Same parameters as the page's worked example.
gamma = 0.1
bk_dd = 0.002     # density-dependent: mass-action term beta*kappa * S I
bk_fd = 0.3       # frequency-dependent: standard-incidence term beta*kappa * S I / N


def epidemic(mode, N):
    """Integrate the SIR model and return (t, I(t)) for one initial infection."""
    beta = bk_dd if mode == "dd" else bk_fd

    def rhs(t, y):
        S, I, _ = y
        force = beta * S * I if mode == "dd" else beta * S * I / N
        return [-force, force - gamma * I, gamma * I]

    sol = solve_ivp(rhs, (0, 150), [N - 1, 1, 0],
                    t_eval=np.linspace(0, 150, 400), rtol=1e-8, atol=1e-8)
    return sol.t, sol.y[1]


fig, ax = plt.subplots(figsize=(6.2, 4.0))

colors = {"dd": PALETTE[0], "fd": PALETTE[1]}   # colour = contact rule
styles = {100: "-", 500: "--"}                  # dashing = population size
for mode in ("dd", "fd"):
    for N in (100, 500):
        t, I = epidemic(mode, N)
        ax.plot(t, I, color=colors[mode], ls=styles[N], lw=1.6)

ax.set_xlabel("time (days)")
ax.set_ylabel("number infected $I(t)$")
ax.set_title("SIR epidemics at two population sizes")

# Two-part legend: colour keys the contact rule, dashing keys the size.
mode_handles = [
    Line2D([], [], color=PALETTE[0], lw=1.6, label="density-dependent  ($R_0=\\beta\\kappa N/\\gamma$)"),
    Line2D([], [], color=PALETTE[1], lw=1.6, label="frequency-dependent  ($R_0=\\beta\\kappa/\\gamma$)"),
]
size_handles = [
    Line2D([], [], color=MUTED, lw=1.6, ls="-", label="$N=100$"),
    Line2D([], [], color=MUTED, lw=1.6, ls="--", label="$N=500$"),
]
leg1 = ax.legend(handles=mode_handles, loc="upper right", fontsize=8, title="contact rule")
leg1._legend_box.align = "left"
ax.add_artist(leg1)
leg2 = ax.legend(handles=size_handles, loc="right", fontsize=8, title="population size")
leg2._legend_box.align = "left"

fig.tight_layout()
save(fig, "assets/figures/transmission-modes-sir.svg")
