# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""A measure with a continuous part plus atoms: the cumulative force of
infection built from a background hazard and discrete superspreading events,
and the survival curve it drives."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

lam0 = 0.03                                   # continuous background hazard / day
atoms = [(3.0, 0.5), (8.0, 0.8), (11.0, 0.3)]  # (time, jump) superspreading events

t = np.linspace(0, 14, 1400)
cont = lam0 * t
jumps = np.zeros_like(t)
for tau, a in atoms:
    jumps += a * (t >= tau)
Lam = cont + jumps            # cumulative hazard Lambda((0, t])
S = np.exp(-Lam)              # survival against colonization

fig, axL = plt.subplots(figsize=(7.0, 3.6))
axR = axL.twinx()

# Left axis: cumulative hazard (a step + ramp).
axL.plot(t, Lam, color=PALETTE[0], lw=2.0, label=r"cumulative hazard $\Lambda$")
axL.set_xlabel("time since admission (days)")
axL.set_ylabel(r"$\Lambda((0,t])$", color=PALETTE[0])
axL.tick_params(axis="y", labelcolor=PALETTE[0])
axL.set_ylim(0, Lam.max() * 1.15)

# Right axis: survival.
axR.plot(t, S, color=PALETTE[1], lw=2.0, label="survival $S=e^{-\\Lambda}$")
axR.set_ylabel("uncolonized fraction $S(t)$", color=PALETTE[1])
axR.tick_params(axis="y", labelcolor=PALETTE[1])
axR.set_ylim(0, 1.02)
axR.grid(False)

# Mark the atoms.
for i, (tau, a) in enumerate(atoms):
    axL.axvline(tau, color=MUTED, ls=":", lw=1.0)
    lbl = "superspreading events" if i == 0 else None
    axL.plot([], [])  # keep color cycle stable
axL.annotate("superspreading\nevents (atoms)", xy=(8.0, lam0 * 8 + 0.5),
             xytext=(8.6, 0.55), fontsize=8.5, color=INK,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
axL.set_title("A measure with a continuous part and atoms")

save(fig, "assets/figures/lebesgue-mixed-measure.svg")
