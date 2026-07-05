# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Functional responses and the paradox of enrichment.

Left: the three Holling functional-response curves. Middle: the
Rosenzweig-MacArthur phase plane, showing that enriching the prey (raising K)
slides the equilibrium left of the hump of the prey nullcline. Right: prey
time series at a low (stable) and a high (cycling) carrying capacity.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()

r, a, h, c, m = 1.0, 1.0, 0.5, 0.5, 0.3
Nstar = m / (a * (c - m * h))          # predator nullcline, independent of K


def rhs(t, y, K):
    N, P = y
    f = a * N / (1 + a * h * N)
    return [r * N * (1 - N / K) - f * P, c * f * P - m * P]


fig, (axA, axB, axC) = plt.subplots(1, 3, figsize=(13.5, 4.2))

# ---- A: the three Holling functional responses ----
N = np.linspace(0, 10, 300)
axA.plot(N, a * N, color=PALETTE[0], lw=2, label="type I  $aN$")
axA.plot(N, a * N / (1 + a * h * N), color=PALETTE[1], lw=2,
         label=r"type II  $\dfrac{aN}{1+ahN}$")
axA.plot(N, a * N**2 / (1 + a * h * N**2), color=PALETTE[2], lw=2,
         label=r"type III  $\dfrac{aN^2}{1+ahN^2}$")
axA.axhline(1 / h, color=MUTED, ls=":", lw=1.0)
axA.text(6.2, 1 / h + 0.06, r"saturation $1/h$", color=MUTED, fontsize=8.5)
axA.set_ylim(0, 3)
axA.set_xlabel("prey density $N$")
axA.set_ylabel("prey eaten per predator  $f(N)$")
axA.set_title("Holling functional responses")
axA.legend(loc="upper left", fontsize=9)

# ---- B: Rosenzweig-MacArthur phase plane ----
Ngrid = np.linspace(0.001, 6, 400)
for K, ls, col, tag in [(2.5, "--", PALETTE[2], "$K=2.5$ (stable)"),
                        (6.0, "-", PALETTE[1], "$K=6$ (enriched)")]:
    prey_null = (r / a) * (1 - Ngrid / K) * (1 + a * h * Ngrid)
    axB.plot(Ngrid, np.clip(prey_null, 0, None), ls, color=col, lw=2,
             label=f"prey nullcline {tag}")
    Pstar = (r / a) * (1 - Nstar / K) * (1 + a * h * Nstar)
    axB.plot(Nstar, Pstar, "o", color=col, ms=7, zorder=6)

axB.axvline(Nstar, color=PALETTE[0], lw=2, label="predator nullcline")
# spiral-out trajectory to the limit cycle at K = 6
sol = solve_ivp(rhs, (0, 400), [Nstar + 0.05, 1.0], args=(6.0,),
                t_eval=np.linspace(200, 400, 4000), rtol=1e-9, atol=1e-9)
axB.plot(sol.y[0], sol.y[1], color=MUTED, lw=0.9, alpha=0.8,
         label="limit cycle ($K=6$)")
axB.set_xlim(0, 6)
axB.set_ylim(0, 2.2)
axB.set_xlabel("prey density $N$")
axB.set_ylabel("predator density $P$")
axB.set_title("Enrichment moves $N^*$ left of the hump")
axB.legend(loc="upper right", fontsize=7.5)

# ---- C: prey time series, stable vs cycling ----
for K, col, tag in [(2.5, PALETTE[2], "$K=2.5$: damps to equilibrium"),
                    (6.0, PALETTE[1], "$K=6$: sustained cycle")]:
    s = solve_ivp(rhs, (0, 120), [Nstar + 0.05, 1.0], args=(K,),
                  t_eval=np.linspace(0, 120, 2000), rtol=1e-9, atol=1e-9)
    axC.plot(s.t, s.y[0], color=col, lw=1.8, label=tag)
axC.set_xlabel("time")
axC.set_ylabel("prey density $N$")
axC.set_title("Paradox of enrichment")
axC.legend(loc="upper right", fontsize=9)

fig.suptitle("Saturating predation and the paradox of enrichment",
             fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "assets/figures/functional-responses.svg")
