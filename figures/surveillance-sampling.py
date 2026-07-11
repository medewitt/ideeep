# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Whom and where you sample: the same true risk surface, seen through three
sampling designs.

  (a) The true risk over a landscape -- two hotspots on a low background.
  (b) Opportunistic sampling follows access (a road corridor), not risk, so
      it over-samples the easy-to-reach low-risk strip and misses a hotspot.
  (c) Risk-based sampling aims effort where risk is predicted to be high, so
      both hotspots are covered.
  (d) Adaptive sampling starts coarse, then concentrates a second round where
      the first round found the strongest signal. All illustrative.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(105281)

# --- true risk surface: two Gaussian hotspots on a low background ----------
g = np.linspace(0, 1, 200)
gx, gy = np.meshgrid(g, g)


def bump(cx, cy, s, a):
    return a * np.exp(-((gx - cx) ** 2 + (gy - cy) ** 2) / (2 * s ** 2))


risk = bump(0.72, 0.76, 0.09, 1.0) + bump(0.34, 0.30, 0.10, 0.8) + 0.05
risk /= risk.max()


def risk_at(x, y):
    r = (np.exp(-((x - 0.72) ** 2 + (y - 0.76) ** 2) / (2 * 0.09 ** 2))
         + 0.8 * np.exp(-((x - 0.34) ** 2 + (y - 0.30) ** 2) / (2 * 0.10 ** 2))
         + 0.05)
    return r


def draw_surface(ax):
    ax.imshow(risk, extent=(0, 1, 0, 1), origin="lower", cmap="OrRd",
              alpha=0.9, vmin=0, vmax=1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)


def risk_based(nkeep, spread_rng):
    """Rejection-sample points with acceptance proportional to risk."""
    pts = []
    while len(pts) < nkeep:
        x, y = spread_rng.random(2)
        if spread_rng.random() < risk_at(x, y):
            pts.append((x, y))
    return np.array(pts)


fig, axes = plt.subplots(2, 2, figsize=(8.8, 8.4))
(axa, axb), (axc, axd) = axes

# --- (a) true risk ---------------------------------------------------------
draw_surface(axa)
axa.set_title("(a) True risk")
axa.text(0.72, 0.88, "hotspot", ha="center", fontsize=8, color=INK)
axa.text(0.34, 0.16, "hotspot", ha="center", fontsize=8, color=INK)

# --- (b) opportunistic: cluster along an access corridor -------------------
draw_surface(axb)
n = 55
ox = np.clip(rng.normal(0.18, 0.11, n), 0, 1)      # near the road at x~0.18
oy = rng.uniform(0, 1, n)
axb.scatter(ox, oy, s=18, c=INK, edgecolors="white", linewidths=0.4)
axb.axvline(0.18, color=INK, lw=1.0, ls=":")
axb.text(0.20, 0.95, "road", ha="left", va="top", fontsize=7.6, color=INK)
axb.annotate("hotspot\nmissed", xy=(0.72, 0.76), xytext=(0.52, 0.5),
             fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="->", color=INK))
axb.set_title("(b) Opportunistic (follows access)")

# --- (c) risk-based --------------------------------------------------------
draw_surface(axc)
pts = risk_based(55, rng)
axc.scatter(pts[:, 0], pts[:, 1], s=18, c=INK, edgecolors="white",
            linewidths=0.4)
axc.set_title("(c) Risk-based (follows risk)")

# --- (d) adaptive ----------------------------------------------------------
draw_surface(axd)
round1 = risk_based(16, rng)
best = round1[np.argmax([risk_at(x, y) for x, y in round1])]
round2 = np.column_stack([np.clip(rng.normal(best[0], 0.07, 34), 0, 1),
                          np.clip(rng.normal(best[1], 0.07, 34), 0, 1)])
axd.scatter(round1[:, 0], round1[:, 1], s=26, facecolors="none",
            edgecolors=INK, linewidths=1.1, label="round 1")
axd.scatter(round2[:, 0], round2[:, 1], s=16, c=INK, edgecolors="white",
            linewidths=0.4, label="round 2")
axd.legend(fontsize=7.6, loc="lower left")
axd.set_title("(d) Adaptive (re-targets on signal)")

fig.suptitle("Shading is true risk; dots are where you actually sampled",
             fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.96))
save(fig, "assets/figures/surveillance-sampling.svg")
