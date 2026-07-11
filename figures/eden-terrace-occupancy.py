# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Car counting on a synthetic overhead deck modeled on the long, multi-row
layout of the Eden Terrace hospital parking deck, shown at three occupancy
levels. A simple dark-blob detector (threshold + connected components) marks the
cars it finds; the count falls from a nearly full deck to a nearly empty one --
the raw occupancy signal a surveillance pipeline would turn into a time series.
The imagery is synthetic (no real, license-restricted aerial photo is used) and
the detector deliberately crude: an illustration, not a validated system.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(7)

# a long, thin deck echoing the Eden Terrace layout: three rows of bays
H, W = 92, 380
rows_y = [24, 46, 68]
bays = [(ry, cx) for ry in rows_y for cx in range(16, W - 12, 12)]
propensity = rng.random(len(bays))                      # per-bay occupancy order
shade = rng.choice([0.12, 0.18, 0.24, 0.30], len(bays))  # a car's colour
levels = [("Nearly full", 0.95), ("Partially full", 0.55), ("Nearly empty", 0.15)]

fig, axes = plt.subplots(3, 1, figsize=(7.6, 5.2))

for ax, (label, frac) in zip(axes, levels):
    deck = np.full((H, W), 0.78)                        # light asphalt
    for (ry, cx), u, sh in zip(bays, propensity, shade):
        if u < frac:                                     # occupied bays are nested
            deck[ry - 5:ry + 5, cx - 3:cx + 3] = sh
    deck = np.clip(deck + 0.02 * rng.standard_normal((H, W)), 0, 1)

    dark = deck < 0.42                                   # cars are darker than asphalt
    lbl, n = ndimage.label(dark)
    sizes = ndimage.sum(np.ones_like(lbl), lbl, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if 6 <= s <= 140]
    cent = np.array(ndimage.center_of_mass(dark, lbl, keep)) if keep else np.empty((0, 2))

    ax.imshow(deck, cmap="gray", vmin=0, vmax=1)
    if len(cent):
        ax.scatter(cent[:, 1], cent[:, 0], s=13, facecolors="none",
                   edgecolors=PALETTE[1], linewidths=0.8)
    ax.set_title(f"{label} — {len(keep)} cars detected", fontsize=10, color=INK,
                 loc="left")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

fig.text(0.5, 0.01, "Synthetic imagery modeled on the Eden Terrace deck layout — "
         "no real aerial photograph is used", ha="center", fontsize=6.8,
         color=MUTED)
fig.suptitle("Deck occupancy across three snapshots (synthetic)", fontsize=11,
             color=INK, y=0.99)
fig.tight_layout(rect=[0, 0.03, 1, 0.96])
save(fig, "assets/figures/eden-terrace-occupancy.svg")
