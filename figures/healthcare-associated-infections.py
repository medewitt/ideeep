# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Forest plot of Standardized Infection Ratios across hospital units."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

# --- Ten units: SIR = observed / predicted, with 95% CI ---
units = [f"Unit {c}" for c in "ABCDEFGHIJ"]
sir = np.array([1.62, 1.44, 1.28, 1.15, 1.05, 0.98,
                0.90, 0.78, 0.66, 0.52])
# Half-widths of the 95% CI (wider where counts are smaller).
half = np.array([0.34, 0.22, 0.31, 0.24, 0.30, 0.21,
                 0.28, 0.16, 0.20, 0.19])
lo = sir - half
hi = sir + half

# Sort by SIR (ascending -> worst at top of the plotted axis).
order = np.argsort(sir)
units = [units[i] for i in order]
sir, lo, hi = sir[order], lo[order], hi[order]

# Color by where the CI sits relative to the baseline of 1.0.
colors = []
for l, h in zip(lo, hi):
    if l > 1.0:
        colors.append(PALETTE[1])   # worse than expected
    elif h < 1.0:
        colors.append(PALETTE[2])   # better than expected
    else:
        colors.append(PALETTE[0])   # spans 1.0

y = np.arange(len(units))

fig, ax = plt.subplots(figsize=(6.4, 4.0))

ax.axvline(1.0, ls="--", color=MUTED, lw=1.2)
ax.text(1.0, len(units) - 0.35, "national baseline",
        ha="center", va="bottom", fontsize="x-small", color=MUTED)

for yi, (s, l, h, col) in enumerate(zip(sir, lo, hi, colors)):
    ax.plot([l, h], [yi, yi], color=col, lw=1.8, zorder=2)
    ax.plot([s], [yi], marker="o", ms=7, color=col,
            markeredgecolor="white", markeredgewidth=0.6, zorder=3)

ax.set_yticks(y)
ax.set_yticklabels(units)
ax.set_ylim(-0.7, len(units) - 0.2)
ax.set_xlim(0, max(hi) + 0.25)
ax.set_xlabel("Standardized Infection Ratio (observed / predicted)")
ax.set_title("Standardized Infection Ratio by unit")

ax.annotate("> 1: more infections than predicted",
            xy=(0.98, 0.97), xycoords="axes fraction",
            ha="right", va="top", fontsize="x-small", color=PALETTE[1])

fig.tight_layout()

for u, s, l, h in zip(units, sir, lo, hi):
    print(f"{u}: SIR = {s:.2f} (95% CI {l:.2f}-{h:.2f})")

save(fig, "assets/figures/healthcare-associated-infections.svg")
