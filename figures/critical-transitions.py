# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Critical slowing down and early-warning signals.

Panel (a) shows the potential well of a fold normal form flattening as the
control parameter nears the tipping point. Panel (b) simulates a scalar SDE
drifting toward the fold, with the rolling variance rising. Panel (c) drives a
stochastic SIS across R0 = 1, with the rolling lag-1 autocorrelation rising.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)


def rolling(x, win, fn):
    out = np.full(x.size, np.nan)
    for k in range(win, x.size):
        out[k] = fn(x[k - win:k])
    return out


def ar1(seg):
    s = seg - seg.mean()
    denom = np.sum(s * s)
    return np.sum(s[1:] * s[:-1]) / denom if denom > 0 else np.nan


fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.7))

# Panel (a): potential wells U(x) = -mu x + x^3/3 for the fold dx/dt = mu - x^2.
ax = axes[0]
xg = np.linspace(-0.2, 1.6, 400)
for mu, col in zip([1.0, 0.45, 0.12], [PALETTE[0], PALETTE[3], PALETTE[1]]):
    xstar = np.sqrt(mu)
    U = -mu * xg + xg**3 / 3.0
    U = U - (-mu * xstar + xstar**3 / 3.0)
    ax.plot(xg, U, color=col, lw=2, label=fr"$\mu={mu:.2f}$")
    ax.plot(xstar, 0.0, "o", color=col, ms=6)
ax.set_ylim(-0.05, 0.6)
ax.set_xlabel("state $x$")
ax.set_ylabel("potential $U(x)$")
ax.set_title("(a) the well flattens near the fold", fontsize=10)
ax.legend(fontsize=8.5)

# Panel (b): scalar SDE toward the fold, rolling variance rising.
n = 4000
dt, sigma = 0.05, 0.09
mu_t = np.linspace(1.1, 0.03, n)
x = np.empty(n)
x[0] = np.sqrt(mu_t[0])
for k in range(1, n):
    drift = mu_t[k - 1] - x[k - 1] ** 2
    x[k] = x[k - 1] + drift * dt + sigma * np.sqrt(dt) * rng.standard_normal()
t = np.arange(n) * dt
var = rolling(x, 300, np.var)
ax = axes[1]
ax.plot(t, x, color=PALETTE[0], lw=0.7, alpha=0.8)
ax.set_xlabel("time")
ax.set_ylabel("state $x$", color=PALETTE[0])
ax.set_title("(b) drift to the fold: variance rises", fontsize=10)
ax2 = ax.twinx()
ax2.plot(t, var, color=PALETTE[1], lw=2)
ax2.set_ylabel("rolling variance", color=PALETTE[1])
ax2.grid(False)
ax2.spines["top"].set_visible(False)

# Panel (c): slowly forced stochastic SIS crossing R0 = 1.
m = 5000
dt2, gamma, Npop, s2 = 0.1, 0.12, 1000.0, 0.6
R0_t = np.linspace(0.55, 1.6, m)
beta_t = R0_t * gamma
I = np.empty(m)
I[0] = 5.0
for k in range(1, m):
    prev = I[k - 1]
    drift = beta_t[k - 1] * (Npop - prev) / Npop * prev - gamma * prev
    prev = prev + drift * dt2 + s2 * np.sqrt(dt2) * rng.standard_normal()
    I[k] = max(prev, 0.5)
t2 = np.arange(m) * dt2
rho = rolling(I, 400, ar1)
cross = t2[np.argmin(np.abs(R0_t - 1.0))]
ax = axes[2]
ax.plot(t2, I, color=PALETTE[2], lw=0.7, alpha=0.8)
ax.axvline(cross, color=MUTED, ls="--", lw=1.2)
ax.text(cross, ax.get_ylim()[1] * 0.9, r" $R_0=1$", color=MUTED, fontsize=8.5)
ax.set_xlabel("time")
ax.set_ylabel("infected $I$", color=PALETTE[2])
ax.set_title("(c) SIS toward emergence: autocorrelation rises", fontsize=10)
ax3 = ax.twinx()
ax3.plot(t2, rho, color=PALETTE[1], lw=2)
ax3.set_ylabel("lag-1 autocorrelation", color=PALETTE[1])
ax3.grid(False)
ax3.spines["top"].set_visible(False)

fig.tight_layout()
save(fig, "assets/figures/critical-transitions.svg")
