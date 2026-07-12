# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""A two-state hidden Markov model for STI reinfection: a latent low/high-risk
regime is decoded from a longitudinal series of test results."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

A = np.array([[0.95, 0.05], [0.15, 0.85]])       # low/high-risk transitions
p_inf = np.array([0.03, 0.55])                    # test-positive prob per period
pi = np.array([0.85, 0.15])
Npat, T = 80, 60
rng = np.random.default_rng(2)


def simulate():
    z = np.zeros(T, int)
    z[0] = rng.random() > pi[0]
    for t in range(1, T):
        z[t] = rng.random() > A[z[t - 1], 0]
    return z, (rng.random(T) < p_inf[z]).astype(int)


Z, X = zip(*[simulate() for _ in range(Npat)])
Z, X = np.array(Z), np.array(X)


def emit(p, xt):
    return np.where(xt == 1, p, 1 - p)


def fwd_bwd(x, A, p, pi):
    al = np.zeros((T, 2))
    be = np.zeros((T, 2))
    c = np.zeros(T)
    al[0] = pi * emit(p, x[0])
    c[0] = al[0].sum()
    al[0] /= c[0]
    for t in range(1, T):
        al[t] = (al[t - 1] @ A) * emit(p, x[t])
        c[t] = al[t].sum()
        al[t] /= c[t]
    be[-1] = 1
    for t in range(T - 2, -1, -1):
        be[t] = A @ (emit(p, x[t + 1]) * be[t + 1]) / c[t + 1]
    g = al * be
    g /= g.sum(1, keepdims=True)
    return g, al, be


def viterbi(x, A, p, pi):
    lA = np.log(A)
    d = np.log(pi) + np.log(emit(p, x[0]))
    bp = np.zeros((T, 2), int)
    for t in range(1, T):
        mm = d[:, None] + lA
        bp[t] = mm.argmax(0)
        d = mm.max(0) + np.log(emit(p, x[t]))
    path = np.zeros(T, int)
    path[-1] = d.argmax()
    for t in range(T - 2, -1, -1):
        path[t] = bp[t + 1, path[t + 1]]
    return path


# ---- pooled Baum-Welch over the cohort ----
Ah = np.array([[0.9, 0.1], [0.3, 0.7]])
ph = np.array([0.05, 0.40])
pih = np.array([0.8, 0.2])
for _ in range(60):
    xit = np.zeros((2, 2))
    g0 = np.zeros(2)
    ne = np.zeros(2)
    de = np.zeros(2)
    for x in X:
        g, al, be = fwd_bwd(x, Ah, ph, pih)
        for t in range(T - 1):
            m = (al[t][:, None] * Ah) * (emit(ph, x[t + 1]) * be[t + 1])[None, :]
            xit += m / m.sum()
        g0 += g[0]
        ne += (g * x[:, None]).sum(0)
        de += g.sum(0)
    Ah = xit / xit.sum(1, keepdims=True)
    ph = ne / de
    pih = g0 / Npat

# ---- pick a patient with a clear high-risk episode for display ----
best = max(range(Npat), key=lambda i: (Z[i, 15:45] == 1).sum())
z, x = Z[best], X[best]
gamma, _, _ = fwd_bwd(x, Ah, ph, pih)
vit = viterbi(x, Ah, ph, pih)
t = np.arange(T)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 4.4), sharex=True)


def shade_high(ax, z):
    inhi = False
    for k in range(T):
        if z[k] == 1 and not inhi:
            start = k
            inhi = True
        if inhi and (k == T - 1 or z[k] == 0):
            ax.axvspan(start - 0.5, (k if z[k] == 0 else k + 1) - 0.5,
                       color=PALETTE[1], alpha=0.13, lw=0)
            inhi = False


# ---- Top: observed data over the (unknown) true regime.
shade_high(ax1, z)
pos = t[x == 1]
neg = t[x == 0]
ax1.scatter(neg, np.zeros_like(neg), s=10, color=MUTED, marker="|", label="negative test")
ax1.scatter(pos, np.ones_like(pos), s=45, color=PALETTE[0], marker="o",
            zorder=5, label="positive test")
ax1.set_yticks([0, 1])
ax1.set_yticklabels(["neg", "pos"])
ax1.set_ylim(-0.5, 1.5)
ax1.set_title("test results (shading = true high-risk regime)", fontsize=10)
ax1.legend(loc="center left", fontsize=7, ncol=2)

# ---- Bottom: decoded latent risk state.
shade_high(ax2, z)
ax2.fill_between(t, gamma[:, 1], color=PALETTE[0], alpha=0.25)
ax2.plot(t, gamma[:, 1], color=PALETTE[0], lw=2, label="P(high-risk | data)")
ax2.step(t, vit, where="mid", color=INK, lw=1.6, label="Viterbi path")
ax2.set_ylim(-0.05, 1.05)
ax2.set_xlabel("month")
ax2.set_ylabel("high-risk prob.")
ax2.set_title("HMM-decoded latent regime", fontsize=10)
ax2.legend(loc="center left", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/hidden-markov-model.svg")
