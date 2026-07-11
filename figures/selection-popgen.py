# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Selection at one locus. Left: iterating the selection recursion, directional
selection drives A monotonically to fixation (p -> 1) from any start, while
overdominance pulls every trajectory to the same stable interior polymorphism
p-hat = s2/(s1+s2) = 0.6. Right: at mutation-selection balance the equilibrium
frequency of a deleterious recessive (q-hat = sqrt(mu/s)) sits a hundredfold
above that of a dominant allele (q-hat = mu/s) for the same mu and s, because
recessives are shielded inside heterozygotes."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()


def step(p, wAA, wAa, waa):
    q = 1 - p
    wbar = p**2 * wAA + 2 * p * q * wAa + q**2 * waa
    return (p**2 * wAA + p * q * wAa) / wbar


def traj(p0, w, gens=60):
    p = p0
    out = [p]
    for _ in range(gens):
        p = step(p, *w)
        out.append(p)
    return np.array(out)


fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 3.6),
                               gridspec_kw={"width_ratios": [1.5, 1]})

# ---- trajectories ---------------------------------------------------------
g = np.arange(0, 61)
w_dir = (1.0, 0.9, 0.8)                 # directional -> fixation
w_over = (0.8, 1.0, 0.7)                # overdominance s1=0.2, s2=0.3 -> 0.6
for i, p0 in enumerate([0.05, 0.2, 0.5]):
    axL.plot(g, traj(p0, w_dir), color=PALETTE[1], lw=1.6,
             label="directional" if i == 0 else None)
for i, p0 in enumerate([0.05, 0.35, 0.95]):
    axL.plot(g, traj(p0, w_over), color=PALETTE[0], lw=1.6,
             label="overdominance" if i == 0 else None)
axL.axhline(0.6, ls="--", color=MUTED, lw=1.0)
axL.text(61, 0.6, r"$\hat p=0.6$", fontsize=8.5, color=INK, va="center")
axL.text(61, 1.0, "fixation", fontsize=8.5, color=PALETTE[1], va="center")
axL.set_xlabel("generation")
axL.set_ylabel("allele frequency $p$")
axL.set_title("Fixation vs stable polymorphism", fontsize=10)
axL.set_xlim(0, 60)
axL.set_ylim(0, 1.05)
axL.legend(fontsize=8.5, loc="center right")

# ---- mutation-selection balance -------------------------------------------
s, mu = 0.1, 1e-5
q_rec = np.sqrt(mu / s)                  # 0.01
q_dom = mu / s                            # 0.0001
axR.bar([0, 1], [q_rec, q_dom], color=[PALETTE[0], PALETTE[3]], width=0.6)
axR.set_yscale("log")
axR.set_xticks([0, 1])
axR.set_xticklabels(["recessive\n$\\sqrt{\\mu/s}$", "dominant\n$\\mu/s$"],
                    fontsize=8.5)
for x, qv in [(0, q_rec), (1, q_dom)]:
    axR.annotate(f"{qv:g}", (x, qv), textcoords="offset points",
                 xytext=(0, 5), ha="center", fontsize=8.5, color=INK)
axR.set_ylabel(r"equilibrium frequency $\hat q$ (log)")
axR.set_title("Mutation–selection balance", fontsize=10)
axR.set_ylim(5e-5, 3e-2)
axR.grid(axis="x", visible=False)

fig.tight_layout()
save(fig, "assets/figures/selection-popgen.svg")
