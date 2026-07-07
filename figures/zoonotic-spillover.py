# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
"""Zoonotic spillover: the barrier cascade and subcritical stuttering chains."""
import numpy as np
from scipy.special import gammaln
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
np.random.seed(1834)


def chain_size_pmf(j, R, k):
    """Blumberg & Lloyd-Smith (2013) negative-binomial chain-size pmf."""
    logp = (gammaln(k * j + j - 1) - gammaln(k * j) - gammaln(j + 1)
            + (j - 1) * np.log(R / k) - (k * j + j - 1) * np.log(1 + R / k))
    return np.exp(logp)


fig, (axa, axb, axc) = plt.subplots(1, 3, figsize=(11.4, 3.7))

# --- Panel (a): the spillover cascade as a narrowing funnel ----------------
stages = ["reservoir\nprevalence", "release /\nshedding",
          "environmental\nsurvival", "human\nexposure",
          "dose &\nestablishment"]
probs = [1.0, 0.6, 0.35, 0.18, 0.06]                 # cumulative pass-through
widths = np.array(probs)
n = len(stages)
ys = np.linspace(n, 1, n)
for i in range(n):
    w0, w1 = widths[i], widths[i + 1] if i + 1 < n else widths[i] * 0.5
    y_top, y_bot = ys[i] + 0.42, ys[i] - 0.42
    poly = Polygon([(-w0 / 2, y_top), (w0 / 2, y_top),
                    (w1 / 2, y_bot), (-w1 / 2, y_bot)],
                   closed=True, facecolor=PALETTE[0],
                   alpha=0.30 + 0.12 * i, edgecolor=INK, lw=0.8)
    axa.add_patch(poly)
    axa.text(0, ys[i], stages[i], ha="center", va="center",
             fontsize=8, color=INK)
    axa.text(w0 / 2 + 0.06, y_top - 0.05, f"$p_{i+1}$", fontsize=8.5,
             color=MUTED, ha="left", va="top")
axa.text(0, 0.15, r"spillover rate $=\prod_i p_i$", ha="center",
         fontsize=9, color=INK)
axa.set_xlim(-0.75, 0.95)
axa.set_ylim(-0.2, n + 0.9)
axa.axis("off")
axa.set_title("(a) the barrier cascade")

# --- Panel (b): chain-size distribution for two dispersion values ----------
R = 0.6
j = np.arange(1, 41)
for k, col in [(0.1, PALETTE[1]), (1.0, PALETTE[0])]:
    axb.plot(j, chain_size_pmf(j, R, k), "o-", ms=3.5, lw=1.5,
             color=col, label=f"$k={k}$")
axb.set_yscale("log")
axb.set_ylim(1e-4, 1)
axb.set_title(f"(b) chain-size distribution ($R_0={R}$)")
axb.set_xlabel("final chain size $j$")
axb.set_ylabel("probability")
axb.legend(fontsize=8.5)

# --- Panel (c): P(chain exceeds N) vs R0 for several k ---------------------
N = 10
Rs = np.linspace(0.05, 0.98, 120)
for k, col in [(0.1, PALETTE[1]), (0.5, PALETTE[2]), (2.0, PALETTE[0])]:
    tail = []
    for R in Rs:
        jj = np.arange(1, N + 1)
        tail.append(1.0 - chain_size_pmf(jj, R, k).sum())
    axc.plot(Rs, tail, lw=2, color=col, label=f"$k={k}$")
axc.set_title(f"(c) $P(\\mathrm{{chain}} > {N})$")
axc.set_xlabel("reservoir-to-human $R_0$")
axc.set_ylabel(f"probability chain exceeds {N}")
axc.legend(fontsize=8.5, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/zoonotic-spillover.svg")
