# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Two 2x2 contact matrices with identical row sums: assortativity raises R0."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

rng = np.random.default_rng(0)  # nothing stochastic, but seed for reproducibility

# Epidemiological constants for the next-generation matrix K = q * D * C.
q, D = 0.04, 6.0  # per-contact transmission probability, mean infectious days

# Same total contacts per person (row sums 10 and 3), different distribution.
C_prop = np.array([[2.70, 7.30],
                   [0.81, 2.19]])   # proportionate mixing
C_assort = np.array([[8.0, 2.0],
                     [0.6, 2.4]])   # assortative: inflated diagonal


def R0(C):
    """Basic reproduction number = spectral radius of K = q*D*C."""
    return float(np.max(np.abs(np.linalg.eigvals(q * D * C))))


groups = ["High\ncontact", "Low\ncontact"]
panels = [("Proportionate mixing", C_prop), ("Assortative mixing", C_assort)]

vmax = max(C_prop.max(), C_assort.max())

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6), gridspec_kw={"wspace": 0.35})
im = None
for k, (ax, (name, C)) in enumerate(zip(axes, panels)):
    ax.grid(False)
    im = ax.imshow(C, cmap="Blues", vmin=0, vmax=vmax)
    for i in range(2):
        for j in range(2):
            val = C[i, j]
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    color="white" if val > 0.6 * vmax else INK, fontsize=11)
    ax.set_xticks([0, 1], groups, fontsize=8, color=MUTED)
    ax.set_xlabel("contacts with group $j$")
    # Label the y axis only on the left panel so the label does not collide
    # with the left panel's cells.
    if k == 0:
        ax.set_yticks([0, 1], groups, fontsize=8, color=MUTED)
        ax.set_ylabel("group $i$")
    else:
        ax.set_yticks([0, 1], ["", ""])
    ax.set_title(f"{name}\n$R_0 = {R0(C):.2f}$", fontsize=11)
    for spine in ax.spines.values():
        spine.set_visible(False)

cbar = fig.colorbar(im, ax=axes, fraction=0.045, pad=0.04)
cbar.set_label("contacts / person / day", color=INK)
cbar.outline.set_edgecolor(PALETTE[0])

fig.suptitle("Same total contacts, assortativity raises $R_0$",
             fontsize=12, color=INK)

save(fig, "assets/figures/social-drivers-of-transmission.svg")
