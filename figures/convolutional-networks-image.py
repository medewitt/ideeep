# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""What a convolutional layer sees. Left: a synthetic skin lesion -- a dark,
irregular blob on skin. Middle: the response of an edge-detecting filter, which
lights up the lesion border (asymmetry and ragged edges are exactly the
dermatology "ABCD" cues). Right: a blob / colour-contrast filter that responds
to the dark core. A CNN stacks many such learned filters to build up from edges
to lesion-level features.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, sobel
from _style import apply_style, save, INK

apply_style()

rng = np.random.default_rng(4)

# --- synthetic "lesion": an irregular dark blob on lighter skin ---
N = 120
yy, xx = np.mgrid[0:N, 0:N]
cx, cy = 60, 58
r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
# ragged radius: base circle modulated by angular noise -> irregular border
theta = np.arctan2(yy - cy, xx - cx)
ragged = 28 + 7 * np.sin(3 * theta) + 4 * np.sin(7 * theta + 1.0)
lesion = 1.0 / (1.0 + np.exp((r - ragged) / 2.5))   # smooth dark blob
skin = 0.75 + 0.03 * rng.standard_normal((N, N))
img = skin - 0.55 * lesion
img = gaussian_filter(img, 1.0)

# --- filters: edge magnitude (Sobel) and a centre-surround blob (LoG) ---
edge = np.hypot(sobel(img, axis=0), sobel(img, axis=1))
log = gaussian_filter(img, 1.5) - gaussian_filter(img, 4.0)

fig, axes = plt.subplots(1, 3, figsize=(9.8, 3.6))
panels = [(img, "Input image (lesion)", "gray"),
          (edge, "Edge filter → border", "magma"),
          (-log, "Blob filter → dark core", "cividis")]
for ax, (data, title, cmap) in zip(axes, panels):
    ax.imshow(data, cmap=cmap)
    ax.set_title(title, fontsize=10, color=INK)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.tight_layout()
save(fig, "assets/figures/convolutional-networks-image.svg")
