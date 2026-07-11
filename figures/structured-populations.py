# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Long-run behaviour of a stage-structured (Leslie) model. Left: starting from
an arbitrary all-juvenile vector, the stage proportions converge to the stable
stage distribution (63% juveniles, 29% subadults, 8% adults) once transients
decay. Right: total population size grows exponentially at the dominant
eigenvalue lambda ~ 1.090, so on a log scale it straightens into a line of slope
ln(lambda)."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

L = np.array([[0.0, 1.0, 5.0],
              [0.5, 0.0, 0.0],
              [0.0, 0.3, 0.0]])

vals, vecs = np.linalg.eig(L)
i = np.argmax(vals.real)
lam = vals[i].real                                  # ~1.090
w = np.abs(vecs[:, i].real)
w = w / w.sum()                                     # stable stage distribution

steps = 30
n = np.zeros((steps + 1, 3))
n[0] = np.array([100.0, 0.0, 0.0])                  # start: all juveniles
for t in range(steps):
    n[t + 1] = L @ n[t]

prop = n / n.sum(axis=1, keepdims=True)
total = n.sum(axis=1)
tt = np.arange(steps + 1)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- stage proportions converging ----------------------------------------
names = ["juveniles", "subadults", "adults"]
cols = [PALETTE[0], PALETTE[2], PALETTE[1]]
axL.stackplot(tt, prop.T, labels=names, colors=[c + "cc" for c in cols])
for k in range(3):
    axL.axhline(np.sum(w[:k + 1]) if k < 2 else 1.0, color="white", lw=0)
for k, wk in enumerate(np.cumsum(w)):
    axL.text(steps + 0.3, wk - w[k] / 2, f"{w[k]*100:.0f}%", fontsize=8,
             color=INK, va="center")
axL.set_xlabel("time step")
axL.set_ylabel("share of population")
axL.set_title("Convergence to the stable stage distribution", fontsize=10)
axL.set_xlim(0, steps)
axL.set_ylim(0, 1)
axL.legend(loc="lower center", ncol=3, fontsize=8)
axL.grid(False)

# ---- total population on a log scale --------------------------------------
axR.semilogy(tt, total, color=PALETTE[0], lw=2.0, marker="o", ms=3,
             label="total population")
# reference line of slope ln(lambda) anchored after transients
anchor = 8
ref = total[anchor] * lam ** (tt - anchor)
axR.semilogy(tt[anchor:], ref[anchor:], ls="--", color=MUTED, lw=1.3,
             label=fr"slope $\ln\lambda$, $\lambda={lam:.3f}$")
axR.set_xlabel("time step")
axR.set_ylabel("population size (log scale)")
axR.set_title("Asymptotic growth at rate $\\lambda$", fontsize=10)
axR.legend(fontsize=8.5, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/structured-populations.svg")
