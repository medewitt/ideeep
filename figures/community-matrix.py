# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Community matrices and stability. Left: May's random-matrix experiment — the
fraction of randomly assembled communities that are stable collapses sharply as
the complexity parameter sigma*sqrt(SC) crosses 1, so adding species,
connectance, or interaction strength destabilizes. Right: the worked 2x2
predator-prey matrix has eigenvalues -0.35 +/- 0.614i; both lie in the
left half-plane (negative real part), so the equilibrium is a stable focus and
perturbations spiral back in."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6))

# ---- May's stability transition -------------------------------------------
S, C = 30, 0.3
sigmas = np.linspace(0.05, 0.55, 16)


def frac_stable(sigma, reps=80):
    ok = 0
    for _ in range(reps):
        A = rng.normal(0, sigma, (S, S)) * (rng.random((S, S)) < C)
        np.fill_diagonal(A, -1.0)
        if np.max(np.linalg.eigvals(A).real) < 0:
            ok += 1
    return ok / reps


x = sigmas * np.sqrt(S * C)
frac = np.array([frac_stable(s) for s in sigmas])
axL.plot(x, frac, color=PALETTE[0], lw=2.0, marker="o", ms=4)
axL.axvline(1.0, ls="--", color=PALETTE[1], lw=1.3)
axL.text(1.03, 0.55, r"threshold $\sigma\sqrt{SC}=1$", fontsize=8.5,
         color=PALETTE[1])
axL.annotate("complexity\ndestabilizes", xy=(1.3, 0.1), xytext=(1.25, 0.45),
             fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
axL.set_xlabel(r"complexity  $\sigma\sqrt{SC}$")
axL.set_ylabel("fraction of stable communities")
axL.set_title("May's complexity–stability transition", fontsize=10)
axL.set_ylim(-0.03, 1.05)

# ---- eigenvalues in the complex plane -------------------------------------
tr, det = -0.7, 0.5
disc = tr**2 - 4 * det
im = np.sqrt(-disc) / 2
re = tr / 2
axR.axvspan(-1.2, 0, color=PALETTE[2] + "18", zorder=0)
axR.axvline(0, color=INK, lw=1.0)
axR.axhline(0, color=MUTED, lw=0.6)
axR.scatter([re, re], [im, -im], s=70, color=PALETTE[1], zorder=5)
axR.annotate(fr"$\lambda={re:.2f}\pm{im:.3f}\,i$", xy=(re, im),
             xytext=(-1.15, 0.75), fontsize=9, color=INK)
axR.text(-0.95, -0.75, "Re < 0:\nstable focus\n(damped spiral)", fontsize=8,
         color=PALETTE[2])
axR.text(0.55, 0.75, "Re > 0:\nunstable", fontsize=8, color=MUTED, ha="center")
axR.set_xlabel("real part")
axR.set_ylabel("imaginary part")
axR.set_title("Eigenvalues of the worked matrix", fontsize=10)
axR.set_xlim(-1.2, 1.2)
axR.set_ylim(-1.0, 1.0)
axR.grid(False)

fig.tight_layout()
save(fig, "assets/figures/community-matrix.svg")
