# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Mean abundance of an immigration-fed sink versus the temporal autocorrelation
of its growth rate, from the exact two-state ("good year / bad year") Markov
model. Inflation rises with autocorrelation and with environmental variance, and
diverges at a persistence threshold where the coupled-sink system becomes
self-sustaining (Gonzalez & Holt 2002; Roy, Holt & Barfield 2005)."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

lam_bar = 0.8
I = 10.0
baseline = I / (1 - lam_bar)   # 50


def mean_and_specrad(lamH, lamL, p, I=I):
    """Stationary mean of N_{t+1}=lambda_{s_t} N_t + I under a symmetric
    two-state Markov environment with stay-probability p (lag-1 autocorr 2p-1)."""
    A = np.array([[1 - p * lamH, -(1 - p) * lamL],
                  [-(1 - p) * lamH, 1 - p * lamL]])
    u = np.linalg.solve(A, np.array([I / 2, I / 2]))
    G = np.array([[p * lamH, (1 - p) * lamL],
                  [(1 - p) * lamH, p * lamL]])
    return u.sum(), max(abs(np.linalg.eigvals(G)))


def threshold_rho(lamH, lamL):
    ps = np.linspace(0.5, 0.999, 20000)
    sr = np.array([mean_and_specrad(lamH, lamL, p)[1] for p in ps])
    return 2 * ps[np.argmin(np.abs(sr - 1))] - 1


spreads = [(0.40, "large amplitude  ($\\lambda$: 0.4 – 1.2)", PALETTE[1]),
           (0.25, "small amplitude  ($\\lambda$: 0.55 – 1.05)", PALETTE[0])]

fig, ax = plt.subplots(figsize=(8.4, 5.2))

for d, label, color in spreads:
    lamH, lamL = lam_bar + d, lam_bar - d
    rho_star = threshold_rho(lamH, lamL)
    rho = np.linspace(0.0, rho_star - 1e-3, 300)
    means = []
    for r in rho:
        p = (r + 1) / 2
        m, sr = mean_and_specrad(lamH, lamL, p)
        means.append(m if sr < 1 else np.nan)
    means = np.array(means)
    ax.plot(rho, means, color=color, lw=2.2, label=label)
    ax.axvline(rho_star, color=color, ls=":", lw=1.2, alpha=0.8)
    ax.text(rho_star, baseline * 6.5, f"  threshold\n  $\\rho^*$ = {rho_star:.2f}",
            color=color, fontsize=8.5, va="top")

ax.axhline(baseline, color=INK, ls="--", lw=1.2)
ax.text(0.01, baseline * 1.15, "deterministic baseline  $I/(1-\\bar\\lambda)$ = 50",
        color=INK, fontsize=9)

# annotate the worked-example point
ax.plot(0.5, 150, "o", color=PALETTE[1], ms=8, zorder=5)
ax.annotate("$\\rho=0.5\\Rightarrow$ mean 150  (3×)",
            xy=(0.5, 150), xytext=(0.18, 340),
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.0),
            color=INK, fontsize=9)

ax.set_xlabel("temporal autocorrelation of the growth rate  $\\rho$")
ax.set_ylabel("long-run mean abundance  $\\mathbb{E}[N]$")
ax.set_ylim(0, baseline * 8)
ax.set_xlim(0, 0.66)
ax.set_title("Autocorrelation inflates mean abundance — up to a persistence threshold",
             fontweight="bold")
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout()
save(fig, "assets/figures/inflation-autocorrelation.svg")
