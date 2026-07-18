# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Why 1 minus Kaplan-Meier overestimates in competing risks. The cumulative
incidence functions for two competing events (death from infection, and discharge/
other) rise over time and together account for everyone who has left the at-risk
state. The naive 1 - Kaplan-Meier curve for infection death (dashed), which treats
the competing event as ordinary censoring, sits well above the correct cumulative
incidence - it counts hazard that the competing event never let materialize."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(6)
n = 700
Z = rng.binomial(1, 0.5, n)
l1 = 0.15 * np.exp(0.7 * Z)
T1 = rng.exponential(1 / l1, n)
T2 = rng.exponential(1 / 0.35, n)
Ts = np.minimum(T1, T2)
cause = np.where(T1 <= T2, 1, 2)
tau = 3.0
obs = np.minimum(Ts, tau)
cause = np.where(Ts <= tau, cause, 0)

times = np.unique(obs[cause > 0])
S = 1.0; cif1 = cif2 = 0.0; km1 = 1.0
tt, c1, c2, nk = [0], [0], [0], [0]
for t in times:
    Y = np.sum(obs >= t)
    d1 = np.sum((obs == t) & (cause == 1)); d2 = np.sum((obs == t) & (cause == 2))
    cif1 += S * d1 / Y; cif2 += S * d2 / Y; km1 *= (1 - d1 / Y); S *= (1 - (d1 + d2) / Y)
    tt.append(t); c1.append(cif1); c2.append(cif2); nk.append(1 - km1)

fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.step(tt, c1, where="post", color=PALETTE[0], lw=2.4,
        label=f"CIF: death from infection ({c1[-1]:.2f})")
ax.step(tt, c2, where="post", color=PALETTE[2], lw=2.0,
        label=f"CIF: discharge / other ({c2[-1]:.2f})")
ax.step(tt, nk, where="post", color=PALETTE[1], lw=2.0, ls="--",
        label=f"naive 1 − KM for infection ({nk[-1]:.2f})")
ax.fill_between(tt, c1, nk, step="post", color=PALETTE[1], alpha=0.12)
ax.annotate("overestimate", xy=(2.3, (c1[-1] + nk[-1]) / 2), xytext=(1.4, 0.52),
            fontsize=8.6, color=INK, arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
ax.set_xlabel("time")
ax.set_ylabel("cumulative probability")
ax.set_title("Cumulative incidence vs the 1 − Kaplan–Meier trap", fontsize=9.6)
ax.set_xlim(0, tau)
ax.set_ylim(0, 0.75)
ax.legend(fontsize=8.2, loc="upper left")
fig.tight_layout()
save(fig, "assets/figures/competing-risks-cif.svg")
