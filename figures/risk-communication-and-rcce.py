# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Plain-language rewrite scores far higher on Flesch Reading Ease than the jargon original."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

jargon = ("Implementation of nonpharmaceutical interventions necessitates "
          "epidemiological characterization of transmission heterogeneity "
          "prior to operationalization of mitigation strategies.")
plain = ("Some people catch this illness more easily than others. "
         "We must find out who is most at risk first. "
         "Then we can choose the best ways to keep them safe.")


def syllables(word):
    w = "".join(c for c in word.lower() if c.isalpha())
    if not w:
        return 0
    vowels = "aeiouy"
    groups, prev = 0, False
    for c in w:
        is_v = c in vowels
        if is_v and not prev:
            groups += 1
        prev = is_v
    if w.endswith("e") and groups > 1:
        groups -= 1
    return max(1, groups)


def flesch(text):
    sentences = max(1, sum(text.count(p) for p in ".!?"))
    words = text.split()
    n_syll = sum(syllables(w) for w in words)
    return 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (n_syll / len(words))


labels = ["jargon", "plain language"]
scores = np.array([flesch(jargon), flesch(plain)])
colors = [PALETTE[1], PALETTE[0]]

fig, ax = plt.subplots(figsize=(7.0, 3.6))

# readability interpretation reference bands / ticks
bands = [(30, "difficult"), (60, "plain English"), (80, "easy")]
for x, name in bands:
    ax.axvline(x, color=MUTED, linewidth=0.8, linestyle=(0, (4, 3)), zorder=1)
    ax.text(x, 1.62, f"{x}\n{name}", ha="center", va="bottom",
            fontsize=8, color=MUTED)

y = np.arange(len(labels))
ax.barh(y, scores, color=colors, height=0.55, zorder=3, edgecolor="white")

for yi, s in zip(y, scores):
    off = 4 if s >= 0 else -4
    ha = "left" if s >= 0 else "right"
    ax.annotate(f"{s:.1f}", (s, yi), xytext=(off, 0),
                textcoords="offset points", ha=ha, va="center",
                fontsize=10, color=INK, fontweight="bold")

ax.axvline(0, color=INK, linewidth=0.9, zorder=2)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_ylim(-0.6, 1.55)
ax.set_xlabel("Flesch Reading Ease (higher = easier)")
ax.set_title("Plain language lifts a message into readable range")
ax.grid(axis="y", visible=False)

save(fig, "assets/figures/risk-communication-and-rcce.svg")
