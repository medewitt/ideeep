# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""ICU colonization as a birth-death queue: the two-bed transition chain, and
how endemic colonized prevalence rises with the transmission rate and shifts
under infection-prevention practices."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()


def stationary_prevalence(N, beta, mu, gamma, f):
    """Stationary colonized prevalence of a full N-bed ward (birth-death CTMC)."""
    b = np.zeros(N + 1)
    d = np.zeros(N + 1)
    for X in range(N + 1):
        S = N - X
        transmission = beta * X * S / (N - 1) if N > 1 else 0.0
        b[X] = transmission + mu * f * S
        d[X] = (mu * (1 - f) + gamma) * X
    pi = np.ones(N + 1)
    for X in range(1, N + 1):
        pi[X] = pi[X - 1] * b[X - 1] / d[X]
    pi /= pi.sum()
    return (np.arange(N + 1) * pi).sum() / N


fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.2, 3.7),
                               gridspec_kw={"width_ratios": [1.05, 1.0]})

# ---- Left: two-bed birth-death chain, states X = 0, 1, 2 colonized ----
axL.set_xlim(-0.5, 5.0)
axL.set_ylim(-1.2, 1.4)
axL.axis("off")
axL.set_title("Two-bed ward: number colonized")
centers = [0.4, 2.2, 4.0]
labels = ["0", "1", "2"]
cols = ["#e8eef3", PALETTE[0], PALETTE[1]]
for cx, lab, c in zip(centers, labels, cols):
    axL.add_patch(Circle((cx, 0), 0.42, facecolor=c, edgecolor=INK, lw=1.4, zorder=3))
    axL.text(cx, 0, lab, ha="center", va="center", fontsize=13,
             color="white" if c != "#e8eef3" else INK, zorder=4)


def arc(x0, x1, up, text):
    y = 0.0
    rad = 0.35 if up else -0.35
    a = FancyArrowPatch((x0, 0.0 + (0.28 if up else -0.28)),
                        (x1, 0.0 + (0.28 if up else -0.28)),
                        connectionstyle=f"arc3,rad={rad}",
                        arrowstyle="-|>", mutation_scale=13,
                        color=INK, lw=1.3, zorder=2)
    axL.add_patch(a)
    ym = 0.86 if up else -0.86
    axL.text((x0 + x1) / 2, ym, text, ha="center", va="center",
             fontsize=9, color=MUTED)


# births (colonization) along the top, deaths (loss) along the bottom
arc(centers[0], centers[1], True, r"$2\mu f$")
arc(centers[1], centers[2], True, r"$\beta + \mu f$")
arc(centers[2], centers[1], False, r"$2(\mu(1{-}f){+}\gamma)$")
arc(centers[1], centers[0], False, r"$\mu(1{-}f)+\gamma$")
axL.text(2.2, 1.25, "colonization  →", ha="center", fontsize=8.5, color=INK)
axL.text(2.2, -1.25, "←  discharge / clearance", ha="center", fontsize=8.5, color=INK)

# ---- Right: endemic prevalence vs transmission rate, by IP practice ----
mu, f = 0.2, 0.05
betas = np.linspace(0.0, 0.9, 120)
scenarios = [
    ("12-bed baseline ($\\gamma$=0.05)", 12, 0.05, f, PALETTE[0], "-"),
    ("12-bed + decolonization ($\\gamma$=0.30)", 12, 0.30, f, PALETTE[2], "-"),
    ("12-bed + admission screening ($f$=0.01)", 12, 0.05, 0.01, PALETTE[3], "-"),
    ("2-bed baseline", 2, 0.05, f, PALETTE[1], "--"),
]
for lab, N, gamma, fi, col, ls in scenarios:
    prev = [stationary_prevalence(N, b, mu, gamma, fi) for b in betas]
    axR.plot(betas, np.array(prev) * 100, color=col, lw=1.9, ls=ls, label=lab)

# threshold R_A = 1 at beta = mu + gamma (baseline gamma)
axR.axvline(mu + 0.05, color=MUTED, lw=1.0, ls=":")
axR.text(mu + 0.05 + 0.01, 46, r"$R_A=1$", fontsize=8.5, color=MUTED)
axR.set_xlabel(r"transmission rate $\beta$ (per day)")
axR.set_ylabel("colonized prevalence (%)")
axR.set_title("Endemic prevalence vs. transmission")
axR.set_ylim(0, 55)
axR.legend(fontsize=7.3, loc="upper left")

fig.tight_layout()
save(fig, "assets/figures/icu-colonization-queue.svg")
