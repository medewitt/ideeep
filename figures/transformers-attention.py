# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""The transformer's engine: attention. Left: a self-attention weight matrix
over a short sequence -- each row shows how much a token attends to every other,
here forming blocks because related tokens attend to one another. Right: the
scaled dot-product attention pipeline that produces those weights, from queries,
keys, and values to a weighted blend.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(0)

# --- left: attention heatmap with block structure (two "topics") ---
tokens = ["the", "patient", "has", "fever", "and", "cough", "since", "monday"]
n = len(tokens)
# hand-built embeddings: symptom words cluster, function words cluster
groups = np.array([0, 1, 0, 1, 0, 1, 0, 2])
emb = np.zeros((n, 3))
for i, g in enumerate(groups):
    emb[i, g] = 3.0                            # strong within-group similarity
emb += 0.25 * rng.standard_normal((n, 3))
scores = emb @ emb.T / np.sqrt(3)
attn = np.exp(scores - scores.max(1, keepdims=True))
attn /= attn.sum(1, keepdims=True)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.8, 4.0))
im = ax0.imshow(attn, cmap="magma_r", vmin=0)
ax0.set_xticks(range(n)); ax0.set_yticks(range(n))
ax0.set_xticklabels(tokens, rotation=45, ha="right", fontsize=8)
ax0.set_yticklabels(tokens, fontsize=8)
ax0.set_title("Self-attention weights", fontsize=10)
ax0.set_xlabel("attends to", fontsize=9)
ax0.set_ylabel("token", fontsize=9)
cb = fig.colorbar(im, ax=ax0, fraction=0.046, pad=0.03)
cb.ax.tick_params(labelsize=7)

# --- right: scaled dot-product attention schematic ---
ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis("off")


def box(x, y, w, h, text, color, fs=9):
    ax1.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                  linewidth=1.6, edgecolor=color, facecolor=color + "18"))
    ax1.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
             color=INK)


for i, (lab, col) in enumerate([("Q", PALETTE[0]), ("K", PALETTE[1]),
                                ("V", PALETTE[2])]):
    box(0.6 + i * 3.1, 8.2, 2.4, 1.3, lab, col)
box(1.4, 5.6, 5.6, 1.3, r"scores $= QK^\top/\sqrt{d}$", INK, fs=9.5)
box(1.4, 3.3, 5.6, 1.3, "softmax  (rows sum to 1)", PALETTE[3], fs=9.5)
box(1.0, 1.0, 6.4, 1.3, r"output $= \mathrm{softmax}(\cdot)\,V$", PALETTE[2],
    fs=9.5)
ax1.add_patch(FancyArrowPatch((1.8, 8.15), (3.5, 6.95), arrowstyle="-|>",
              mutation_scale=13, color="0.5", lw=1.4))
ax1.add_patch(FancyArrowPatch((4.9, 8.15), (4.5, 6.95), arrowstyle="-|>",
              mutation_scale=13, color="0.5", lw=1.4))
ax1.add_patch(FancyArrowPatch((4.2, 5.55), (4.2, 4.65), arrowstyle="-|>",
              mutation_scale=13, color="0.5", lw=1.4))
ax1.add_patch(FancyArrowPatch((4.2, 3.25), (4.2, 2.35), arrowstyle="-|>",
              mutation_scale=13, color="0.5", lw=1.4))
ax1.add_patch(FancyArrowPatch((8.0, 8.15), (7.2, 2.0), arrowstyle="-|>",
              mutation_scale=13, color=PALETTE[2], lw=1.4, ls=":"))
ax1.text(8.2, 5.0, "V", fontsize=8, color=PALETTE[2])
ax1.set_title("Scaled dot-product attention", fontsize=10)

fig.tight_layout()
save(fig, "assets/figures/transformers-attention.svg")
