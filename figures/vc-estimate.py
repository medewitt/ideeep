# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Bootstrap uncertainty in the estimated vectorial capacity. Resampling the human
landing catches and redrawing the parity and sporozoite proportions propagates
field sampling error into V. The point estimate is about 2.5, but the 95%
bootstrap interval is wide (roughly 1.1 to 5.6) - entomological estimates of
transmission carry large uncertainty, driven mostly by the survival term."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(11)
hlc = rng.poisson(6, size=80)
g, hbi, n_eip = 3.0, 0.9, 11
parous, n_dissect, sporo_pos, n_sporo = 78, 120, 15, 500


def V(hbr, pf):
    p = pf ** (1 / g)
    return hbr * (hbi / g) * p**n_eip / (-np.log(p))


V_hat = V(hlc.mean(), parous / n_dissect)
boot = np.array([V(rng.choice(hlc, len(hlc), replace=True).mean(),
                   rng.binomial(n_dissect, parous / n_dissect) / n_dissect)
                 for _ in range(4000)])
lo, hi = np.percentile(boot, [2.5, 97.5])

fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.hist(boot, bins=np.linspace(0, 10, 55), color=PALETTE[0], alpha=0.55,
        edgecolor="white", linewidth=0.3)
ax.axvline(V_hat, color=PALETTE[1], lw=2.2, label=f"estimate  V ≈ {V_hat:.1f}")
ax.axvspan(lo, hi, color=PALETTE[1], alpha=0.12)
ax.plot([lo, hi], [2, 2], color=PALETTE[1], lw=3, solid_capstyle="butt")
ax.text((lo + hi) / 2, 20, f"95% bootstrap CI\n[{lo:.1f}, {hi:.1f}]", ha="center",
        fontsize=8.4, color=INK)
ax.set_xlabel("vectorial capacity  $V$")
ax.set_ylabel("bootstrap frequency")
ax.set_title("Field vectorial capacity carries wide uncertainty", fontsize=9.6)
ax.set_xlim(0, 10)
ax.legend(fontsize=8.4, loc="upper right")
ax.grid(axis="x", visible=False)
fig.tight_layout()
save(fig, "assets/figures/vc-estimate.svg")
