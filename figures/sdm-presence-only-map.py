# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Presence-only data on a suitability landscape. The shading is the true
environmental suitability from a unimodal temperature-and-rainfall niche, peaking
in a central band. Presence records (filled points) concentrate where suitability
is high; a background sample (small grey points) is spread across the whole
landscape. The model learns the niche by contrasting the two."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(1)
temp = lambda x: 10 + 2.0 * x
rain = lambda y: 50 + 5.0 * y
t_opt, t_w, r_opt, r_w = 22.0, 4.0, 75.0, 12.0
suit = lambda x, y: np.exp(-((temp(x) - t_opt) ** 2) / (2 * t_w**2)
                           - ((rain(y) - r_opt) ** 2) / (2 * r_w**2))

cand = rng.uniform(0, 10, size=(20000, 2))
pres = cand[rng.uniform(size=len(cand)) < suit(cand[:, 0], cand[:, 1])][:300]
bg = rng.uniform(0, 10, size=(400, 2))          # show a thinned background for clarity

gx, gy = np.meshgrid(np.linspace(0, 10, 200), np.linspace(0, 10, 200))
S = suit(gx, gy)

fig, ax = plt.subplots(figsize=(5.8, 4.6))
im = ax.imshow(S, extent=[0, 10, 0, 10], origin="lower", cmap="YlGnBu",
               alpha=0.9, aspect="auto")
ax.scatter(bg[:, 0], bg[:, 1], s=6, color="#5b6b7a", alpha=0.5, label="background")
ax.scatter(pres[:, 0], pres[:, 1], s=16, color=PALETTE[1], edgecolor="white",
           linewidth=0.3, label="presence records")
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
cb.set_label("true suitability", fontsize=8.5)
# secondary axes labels for the environment
ax.set_xlabel("west → east   (temperature 10 → 30 °C)")
ax.set_ylabel("south → north   (rainfall 50 → 100 mm)")
ax.set_title("Presence-only records track suitability", fontsize=9.8)
ax.legend(fontsize=8.2, loc="lower right", framealpha=0.85)
fig.tight_layout()
save(fig, "assets/figures/sdm-presence-only-map.svg")
