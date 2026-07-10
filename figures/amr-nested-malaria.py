# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""A joint within-host / between-host malaria model of resistance across scales.

Following the cross-scale logic of Mideo, Alizon & Day, a within-host model of
sensitive and resistant Plasmodium competing for red blood cells produces
gametocytes; gametocyte density sets the host's transmissibility, which feeds a
between-host two-strain SIS model.

Panel A: within-host asexual densities and the shared red-cell resource under a
drug pulse -- sensitive parasites crash, red cells rebound, resistant parasites
are competitively released. Panel B: the gametocytes each strain sheds, and how
gametocyte density maps to transmissibility. Panel C: the resulting between-host
resistant fraction of infections, rising faster as more of the population is
treated.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()

# --- Within-host model ---------------------------------------------------
# Shared resource R (red cells, scaled to equilibrium 1), asexual parasites
# Ps/Pr, gametocytes Gs/Gr. Resistant pays a growth cost.
muR, Lam = 0.025, 0.025           # red-cell turnover; supply (R* = 1)
psi = 2.0                         # infection / consumption coefficient
b_s = 1.5                         # sensitive asexual replication yield
cost = 0.15                       # fitness cost of resistance
b_r = b_s * (1 - cost)
dp = 1.0                          # asexual death rate
gconv = 0.10                      # gametocyte conversion rate
mug = 0.25                        # gametocyte death rate
kmax = 6.0                        # drug kill rate on sensitive asexuals


def drug(t, treat):
    return kmax if (treat and 20.0 <= t <= 32.0) else 0.0


def within_host(t, y, treat):
    R, Ps, Pr, Gs, Gr = y
    k = drug(t, treat)
    inf_s = psi * R * Ps
    inf_r = psi * R * Pr
    dR = Lam - muR * R - inf_s - inf_r
    dPs = b_s * inf_s - dp * Ps - gconv * Ps - k * Ps
    dPr = b_r * inf_r - dp * Pr - gconv * Pr
    dGs = gconv * Ps - mug * Gs
    dGr = gconv * Pr - mug * Gr
    return [dR, dPs, dPr, dGs, dGr]


t_eval = np.linspace(0, 60, 1200)
# Mixed infection (rare resistant sub-population) for the within-host panels.
y0 = [1.0, 1e-3, 1e-5, 0.0, 0.0]
sol_u = solve_ivp(within_host, [0, 60], y0, args=(False,),
                  t_eval=t_eval, rtol=1e-9, atol=1e-12)
sol_t = solve_ivp(within_host, [0, 60], y0, args=(True,),
                  t_eval=t_eval, rtol=1e-9, atol=1e-12)
# Single-strain-dominant infections set each strain's transmissibility: a host
# infected with resistant carries it at its own (cost-reduced) equilibrium.
s_dom = solve_ivp(within_host, [0, 60], [1.0, 1e-3, 0.0, 0.0, 0.0],
                  args=(False,), t_eval=t_eval, rtol=1e-9, atol=1e-12)
r_dom = solve_ivp(within_host, [0, 60], [1.0, 0.0, 1e-3, 0.0, 0.0],
                  args=(False,), t_eval=t_eval, rtol=1e-9, atol=1e-12)


# Gametocyte area under the curve -> transmissibility weight per strain.
def auc(t, g):
    return np.trapezoid(np.clip(g, 0, None), t)


Gs_dom, Gr_dom = auc(s_dom.t, s_dom.y[3]), auc(r_dom.t, r_dom.y[4])
Gs_t, Gr_t = auc(sol_t.t, sol_t.y[3]), auc(sol_t.t, sol_t.y[4])

fig = plt.figure(figsize=(8.2, 6.2))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.42, wspace=0.30)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])
axC = fig.add_subplot(gs[1, :])

# --- Panel A: within-host asexual + resource (treated host) -------------
axA.plot(sol_t.t, sol_t.y[1], color=PALETTE[0], lw=2.0, label="sensitive asexual")
axA.plot(sol_t.t, sol_t.y[2], color=PALETTE[1], lw=2.0, label="resistant asexual")
axA.plot(sol_t.t, sol_t.y[0], color=PALETTE[2], lw=1.6, ls="--", label="red cells")
axA.axvspan(20, 32, color="#d8dee4", alpha=0.5, zorder=0)
axA.annotate("drug", xy=(26, axA.get_ylim()[1] * 0.9), ha="center",
             fontsize=8, color=INK)
axA.set_xlabel("day post-infection")
axA.set_ylabel("scaled density")
axA.set_title("A. within host: competitive release")
axA.set_xlim(0, 60)
axA.legend(loc="upper right", fontsize=7)

# --- Panel B: gametocytes and the transmission map ----------------------
axB.plot(sol_t.t, sol_t.y[3], color=PALETTE[0], lw=2.0, label="sensitive gametocytes")
axB.plot(sol_t.t, sol_t.y[4], color=PALETTE[1], lw=2.0, label="resistant gametocytes")
axB.plot(sol_u.t, sol_u.y[4], color=PALETTE[1], lw=1.4, ls=":",
         label="resistant, untreated")
axB.set_xlabel("day post-infection")
axB.set_ylabel("gametocyte density")
axB.set_title("B. gametocytes drive transmission")
axB.set_xlim(0, 60)
axB.legend(loc="upper right", fontsize=7)
# Inset: saturating transmission map beta(G).
axins = axB.inset_axes([0.16, 0.52, 0.34, 0.40])
G = np.linspace(0, 6, 100)
axins.plot(G, 0.4 * G / (G + 1.0), color=INK, lw=1.6)
axins.set_title(r"$\beta(G)$", fontsize=7)
axins.tick_params(labelsize=6)
axins.set_xticks([0, 3, 6])
axins.set_yticks([0, 0.2])

# --- Panel C: between-host two-strain SIS -------------------------------
# Transmissibility of each strain built from within-host gametocyte output.
# A host infected with a strain sheds that strain's gametocytes at its own
# equilibrium; the resistant cost makes beta_r < beta_s. kappa scales the
# gametocyte AUC to a per-day transmission rate. The mixed treated infection
# gives rho, the chance a treated sensitive infection seeds a transmissible
# resistant one through competitive release.
kappa = 0.31
gamma_h = 0.10                        # host recovery / clearance
beta_s = kappa * Gs_dom              # sensitive-infected host
beta_r = kappa * Gr_dom              # resistant-infected host (cost-reduced)
rho = Gr_t / (Gs_t + Gr_t)          # per-treatment release probability


def between_host(t, y, tau):
    S, Is, Ir = y
    new_s = beta_s * S * Is
    new_r = beta_r * S * Ir
    dIs = new_s - gamma_h * Is - tau * Is
    dIr = new_r - gamma_h * Ir + rho * tau * Is
    dS = gamma_h * (Is + Ir) + (1 - rho) * tau * Is - new_s - new_r
    return [dS, dIs, dIr]


t_pop = np.linspace(0, 3000, 900)
for tau, col, lab in zip([0.02, 0.05, 0.10], PALETTE,
                         ["20% treated", "50% treated", "80% treated"]):
    sol = solve_ivp(between_host, [0, 3000], [0.98, 0.01, 1e-4],
                    args=(tau,), t_eval=t_pop, rtol=1e-9, atol=1e-12)
    S, Is, Ir = sol.y
    axC.plot(sol.t, Ir / (Is + Ir), color=col, lw=2.2,
             label=f"{lab} " + r"($\tau=%.2f$)" % tau)

axC.set_xlabel("time (days)")
axC.set_ylabel("resistant fraction of infections")
axC.set_title("C. between host: resistance emerges across the population")
axC.set_xlim(0, 3000)
axC.set_ylim(-0.02, 1.05)
axC.legend(loc="center right", fontsize=8)

save(fig, "assets/figures/amr-nested-malaria.svg")
