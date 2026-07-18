# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Why correlation is not agreement. Two assays measuring the same antibody
concentration are plotted against each other; they are almost perfectly
correlated (r = 0.99), so a correlation coefficient would call them
interchangeable. But the cloud sits above the line of equality (the new assay
reads systematically high) and fans out at large values, so the two methods do
not actually agree. Correlation measures association, not agreement."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(7)
n = 50
true = rng.uniform(20, 300, n)
B = true + rng.normal(0, 6, n)                 # reference assay
A = true + 8 + 0.05 * (true - 160) + rng.normal(0, 8, n)   # new assay
r = np.corrcoef(A, B)[0, 1]

fig, ax = plt.subplots(figsize=(5.6, 4.4))
lim = [0, 340]
ax.plot(lim, lim, color=INK, lw=1.3, ls="--", label="line of equality (A = B)")
ax.scatter(B, A, s=34, color=PALETTE[0], alpha=0.85, edgecolor="white",
           linewidth=0.4, zorder=3)
ax.set_xlim(lim)
ax.set_ylim(lim)
ax.set_aspect("equal")
ax.set_xlabel("reference assay B (BAU/mL)")
ax.set_ylabel("new assay A (BAU/mL)")
ax.set_title(f"Near-perfect correlation (r = {r:.2f})…\n…but the methods do not agree",
             fontsize=9.6)
ax.annotate("points sit above equality\n(new assay reads high)", xy=(230, 258),
            xytext=(70, 300), fontsize=8.3, color=INK,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
ax.legend(fontsize=8.3, loc="lower right")
fig.tight_layout()
save(fig, "assets/figures/bland-altman.svg")
