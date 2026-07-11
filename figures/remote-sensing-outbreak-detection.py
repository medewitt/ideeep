# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Remote sensing -> counting -> outbreak signal. Left: a synthetic overhead
view of a hospital parking deck (mimicking the Eden Terrace deck layout); a
simple detector finds the dark car blobs and counts them. Right: the daily
occupancy count becomes a time series, and a surge above the control limit --
here standing in for a wave of hospital visits -- trips an alarm. The image is
synthetic and the pipeline deliberately crude: a licensing- and privacy-safe
illustration, not a validated surveillance system.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(7)

# --- build a synthetic overhead parking-deck raster ---
H, W = 96, 320
img = np.full((H, W), 0.78)                      # light asphalt
car_shades = [0.12, 0.18, 0.24, 0.30, 0.36]
rows_y = [26, 50, 74]                             # three rows of bays
occupied = 0
for ry in rows_y:
    for cx in range(16, W - 12, 12):              # a bay every 12 px
        if rng.random() < 0.82:                   # ~82% occupancy
            occupied += 1
            img[ry - 8:ry + 8, cx - 4:cx + 4] = rng.choice(car_shades)
img = np.clip(img + 0.02 * rng.standard_normal((H, W)), 0, 1)

# --- detect: label dark blobs, take those of car-like area ---
mask = img < 0.55
lbl, n = ndimage.label(mask)
sizes = ndimage.sum(np.ones_like(lbl), lbl, range(1, n + 1))
keep = [i + 1 for i, s in enumerate(sizes) if s > 30]
cent = np.array(ndimage.center_of_mass(mask, lbl, keep))

fig = plt.figure(figsize=(9.8, 4.0))
ax0 = fig.add_axes([0.02, 0.12, 0.60, 0.78])
ax0.imshow(img, cmap="gray", vmin=0, vmax=1)
ax0.scatter(cent[:, 1], cent[:, 0], s=26, facecolors="none",
            edgecolors=PALETTE[1], linewidths=1.4)
ax0.set_title(f"Overhead deck → detect & count: {len(keep)} cars", fontsize=10,
              color=INK)
ax0.set_xticks([]); ax0.set_yticks([])
for sp in ax0.spines.values():
    sp.set_visible(False)

# --- right: daily count time series with an outbreak-like surge ---
ax1 = fig.add_axes([0.70, 0.16, 0.28, 0.72])
days = np.arange(120)
base = 150 + 14 * np.sin(2 * np.pi * days / 7)     # weekly rhythm around 150
counts = base + rng.normal(0, 6, 120)
counts[104:] += np.linspace(0, 62, 16)             # a 2-week surge
mu, sd = counts[:100].mean(), counts[:100].std()
ucl = mu + 3 * sd
alarm = counts > ucl
ax1.plot(days, counts, color=INK, lw=1.2)
ax1.axhline(ucl, color=MUTED, lw=1.0, ls="--")
ax1.text(2, ucl + 2, "control limit", fontsize=7.5, color=MUTED)
ax1.scatter(days[alarm], counts[alarm], s=18, color=PALETTE[1], zorder=3,
            label="alarm")
ax1.set_title("Daily count → outbreak signal", fontsize=10, color=INK)
ax1.set_xlabel("day")
ax1.set_ylabel("cars parked")
ax1.legend(loc="upper left", fontsize=7.5)

save(fig, "assets/figures/remote-sensing-outbreak-detection.svg")
