# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy", "pillow"]
# ///
"""Car counting on real overhead imagery of the Eden Terrace hospital parking
deck, across three archived captures. A simple dark-blob detector (threshold +
connected components) marks the cars it finds; the count drops from a nearly
full deck to a nearly empty one -- the raw occupancy signal a surveillance
pipeline would turn into a time series. Imagery: Esri World Imagery (Wayback);
Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community. Used as
a static screen capture for non-commercial educational illustration.
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

captures = [("full", "Nearly full"), ("partial", "Partially full"),
            ("empty", "Nearly empty")]

fig, axes = plt.subplots(3, 1, figsize=(7.6, 5.4))

for ax, (key, label) in zip(axes, captures):
    img = np.asarray(Image.open(f"assets/photos/eden-terrace-deck-{key}.jpg")
                     .convert("RGB"), float) / 255.0
    gray = img.mean(2)
    dark = gray < 0.40                                   # cars are darker than asphalt
    lbl, n = ndimage.label(dark)
    sizes = ndimage.sum(np.ones_like(lbl), lbl, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if 6 <= s <= 140]
    cent = np.array(ndimage.center_of_mass(dark, lbl, keep)) if keep else np.empty((0, 2))
    ax.imshow(img)
    if len(cent):
        ax.scatter(cent[:, 1], cent[:, 0], s=14, facecolors="none",
                   edgecolors=PALETTE[1], linewidths=0.8)
    ax.set_title(f"{label} — {len(keep)} cars detected", fontsize=10, color=INK,
                 loc="left")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

fig.text(0.5, 0.005, "Imagery: Esri World Imagery (Wayback) — Esri, Maxar, "
         "Earthstar Geographics, and the GIS User Community",
         ha="center", fontsize=6.5, color=MUTED)
fig.suptitle("Eden Terrace deck occupancy across three archived captures",
             fontsize=11, color=INK, y=0.99)
fig.tight_layout(rect=[0, 0.02, 1, 0.96])
save(fig, "assets/figures/eden-terrace-occupancy.svg")
