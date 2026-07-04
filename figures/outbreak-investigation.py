# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Two epidemic curves: a tight point-source outbreak versus a
propagated outbreak that spreads through successive generations."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.8), sharey=True)

# Point-source: a single brief exposure produces one tight wave whose
# spread reflects the incubation-period distribution.
days_ps = np.arange(0, 21)
counts_ps = np.array([0, 0, 1, 3, 8, 14, 11, 6, 3, 1, 1,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
ax1.bar(days_ps, counts_ps, color=PALETTE[0], width=0.85)
ax1.set_title("Point-source")
ax1.set_xlabel("day of onset")
ax1.set_ylabel("cases")
ax1.annotate("one exposure\n-> one incubation-period-wide peak",
             xy=(5, 14), xytext=(9, 12), fontsize=8, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=INK))

# Propagated: person-to-person spread gives successive peaks roughly one
# serial interval apart, each larger than the last while susceptibles last.
days_pp = np.arange(0, 42)
peaks = [(5, 3.0, 1.4), (14, 6.5, 2.0), (24, 10.5, 2.6), (34, 7.0, 3.0)]
counts_pp = np.zeros_like(days_pp, dtype=float)
for mu, amp, sd in peaks:
    counts_pp += amp * np.exp(-0.5 * ((days_pp - mu) / sd) ** 2)
counts_pp = np.round(counts_pp).astype(int)
ax2.bar(days_pp, counts_pp, color=PALETTE[1], width=0.85)
ax2.set_title("Propagated")
ax2.set_xlabel("day of onset")
for mu, _, _ in peaks:
    ax2.axvline(mu, color=MUTED, lw=0.7, ls=":")
ax2.annotate("successive generations\n~one serial interval apart",
             xy=(24, 10.5), xytext=(4, 9), fontsize=8, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=INK))

fig.suptitle("Epidemic-curve shapes distinguish outbreak types", fontsize=11)
fig.tight_layout()
save(fig, "assets/figures/outbreak-investigation.svg")
