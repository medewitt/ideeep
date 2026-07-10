# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Within-host competitive release (Day, Huijben & Read 2015).

Left: a rare resistant clone is held below zero growth by an immune response
that the sensitive majority sustains (competitive suppression), then expands
once a drug pulse clears the sensitive population and immunity relaxes
(competitive release). Right: the resistant clone's absolute per-capita growth
rate versus drug concentration, with and without immunity; emergence needs
r_m > 0, a threshold set by the within-host ecological state, not by the MIC.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

lam_max, lam_r_max, MIC_s, MIC_r = 1.0, 0.9, 2.0, 16.0
a_imm, d_nat, alpha, delta = 0.9, 0.10, 1.0, 1.0


def lam_s(c):
    return lam_max * max(0.0, 1.0 - c / MIC_s)


def lam_r(c):
    return lam_r_max * max(0.0, 1.0 - c / MIC_r)


def rhs(t, y, cfun):
    S, R, I = y
    c = cfun(t)
    dS = (lam_s(c) - a_imm * I - d_nat) * S
    dR = (lam_r(c) - a_imm * I - d_nat) * R
    dI = alpha * (S + R) - delta * I           # immunity tracks total load
    return [dS, dR, dI]


t_eval = np.linspace(0, 120, 1600)
y0 = [1.0, 1e-6, 1.0]                          # rare resistant clone

sol_nd = solve_ivp(rhs, [0, 120], y0, args=(lambda t: 0.0,),
                   t_eval=t_eval, rtol=1e-9, atol=1e-12)


def pulse(t):
    return 6.0 if 30.0 <= t <= 60.0 else 0.0
sol_d = solve_ivp(rhs, [0, 120], y0, args=(pulse,),
                  t_eval=t_eval, rtol=1e-9, atol=1e-12)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.5))

# --- Left: suppression vs release ---------------------------------------
R_nd = np.clip(sol_nd.y[1], 1e-13, None)
R_d = np.clip(sol_d.y[1], 1e-13, None)
S_d = np.clip(sol_d.y[0], 1e-13, None)
axL.plot(sol_nd.t, np.log10(R_nd), color=MUTED, lw=2.0,
         label="resistant, no drug (suppressed)")
axL.plot(sol_d.t, np.log10(R_d), color=PALETTE[1], lw=2.2,
         label="resistant, drug pulse (released)")
axL.plot(sol_d.t, np.log10(S_d), color=PALETTE[0], lw=1.6, ls="--",
         label="sensitive, drug pulse")
axL.axvspan(30, 60, color="#d8dee4", alpha=0.5, zorder=0)
axL.annotate("drug pulse", xy=(45, 0.4), ha="center", fontsize=8, color=INK)
axL.set_xlabel("day post-infection")
axL.set_ylabel(r"$\log_{10}$ scaled density")
axL.set_title("competitive release")
axL.set_xlim(0, 120)
axL.set_ylim(-13, 1.5)
axL.legend(loc="lower left", fontsize=7)

# --- Right: absolute fitness vs drug concentration ----------------------
c_grid = np.linspace(0, 20, 300)
Wr_no = np.array([lam_r(c) - d_nat for c in c_grid])            # no immunity
Wr_imm = np.array([lam_r(c) - a_imm * 0.5 - d_nat for c in c_grid])
axR.plot(c_grid, Wr_no, color=PALETTE[1], lw=2.2, label="no immunity")
axR.plot(c_grid, Wr_imm, color=PALETTE[3], lw=2.0, ls="--", label="with immunity")
axR.axhline(0.0, color=INK, lw=0.9, ls=":")
for x, lab in [(MIC_s, r"MIC$_s$"), (MIC_r, r"MIC$_r$")]:
    axR.axvline(x, color=MUTED, lw=0.9, ls="--")
    axR.annotate(lab, xy=(x, -0.22), ha="center", fontsize=8, color=MUTED)
axR.annotate("emergence needs\n" + r"$r_m>0$", xy=(4.5, 0.0),
             xytext=(7.5, 0.28), fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
axR.set_xlabel(r"drug concentration $c$")
axR.set_ylabel(r"resistant absolute growth $r_m$")
axR.set_title("absolute fitness sets emergence")
axR.set_xlim(0, 20)
axR.set_ylim(-0.3, 0.9)
axR.legend(loc="upper right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/amr-within-host.svg")
