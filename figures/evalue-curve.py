# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""How the E-value grows with the observed effect. Stronger associations need
stronger unmeasured confounding to explain them away, so the E-value rises with the
observed risk ratio. A risk ratio of 1.8 has an E-value of 3.0: only a confounder
associated with both exposure and outcome by a risk ratio of at least 3 could
account for it. Weak effects (RR near 1) are fragile; strong ones are robust."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
evalue = lambda rr: rr + np.sqrt(rr * (rr - 1))

rr = np.linspace(1.0, 4.0, 400)
fig, ax = plt.subplots(figsize=(6.2, 4.0))
ax.plot(rr, evalue(rr), color=PALETTE[0], lw=2.4)
ax.plot([1, 4], [1, 1], color=MUTED, lw=0.8, ls=":")

for r in (1.3, 1.8, 2.5):
    ax.plot([r, r], [1, evalue(r)], color=MUTED, lw=0.8, ls=":")
    ax.plot([1, r], [evalue(r), evalue(r)], color=MUTED, lw=0.8, ls=":")
    ax.scatter([r], [evalue(r)], s=55, color=PALETTE[1], zorder=5)
    ax.annotate(f"RR {r} → E {evalue(r):.2f}", xy=(r, evalue(r)),
                xytext=(r + 0.05, evalue(r) + 0.15), fontsize=8.3, color=INK)

ax.set_xlabel("observed risk ratio")
ax.set_ylabel("E-value")
ax.set_title("The E-value rises with the observed effect", fontsize=9.8)
ax.set_xlim(1, 4)
ax.set_ylim(1, 8)
fig.tight_layout()
save(fig, "assets/figures/evalue-curve.svg")
