# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""How pulling data from an API works. Your code sends an HTTP request -- an
endpoint plus query parameters and (often) an API key -- to a remote database
like GenBank or GBIF, which returns structured data (JSON or XML) and a status
code. You then cache the raw response and parse it into a tidy table. The good
habits live in the margins: keep keys out of code, respect rate limits, and
cache so a rerun doesn't re-hit the server.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, INK

apply_style()

fig, ax = plt.subplots(figsize=(7.4, 4.2))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis("off")

BLUE, GREEN, ORANGE = "#2f6f9f", "#3f8f5b", "#c1531f"


def box(x, y, w, h, text, color, fs=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                 linewidth=1.8, edgecolor=color, facecolor=color + "14"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=INK)


box(0.4, 4.4, 4.0, 1.8, "Your code\n(R · Python · Julia)", BLUE)
box(9.4, 4.4, 4.2, 1.8, "API + database\n(GenBank · GBIF · Ensembl)", GREEN)

# request arrow (top, left -> right)
ax.add_patch(FancyArrowPatch((4.5, 5.7), (9.3, 5.7), arrowstyle="-|>",
             mutation_scale=18, color="0.4", lw=1.8))
ax.text(6.9, 6.15, "① request:  endpoint ? query  + API key",
        ha="center", fontsize=9, color=INK, fontweight="bold")

# response arrow (bottom, right -> left)
ax.add_patch(FancyArrowPatch((9.3, 4.9), (4.5, 4.9), arrowstyle="-|>",
             mutation_scale=18, color="0.4", lw=1.8))
ax.text(6.9, 4.35, "② response:  JSON / XML  + status code",
        ha="center", fontsize=9, color=INK)

# down to parse box
ax.add_patch(FancyArrowPatch((2.4, 4.3), (2.4, 2.9), arrowstyle="-|>",
             mutation_scale=16, color="0.4", lw=1.6))
box(0.4, 1.0, 4.0, 1.7, "③ cache raw →\nparse → tidy table", ORANGE)

# margin habits
ax.text(5.4, 2.65, "the good habits live in the margins:", ha="left",
        fontsize=9, color="0.35", style="italic")
for i, t in enumerate([
        "keep the API key out of code (env var)",
        "respect rate limits — back off on 429, batch",
        "cache responses; record query, date & version"]):
    ax.text(5.4, 2.05 - i * 0.55, "•  " + t, ha="left", fontsize=8.7,
            color="0.3")

fig.suptitle("Pulling data from an API, reproducibly", y=1.0, fontsize=12,
             color=INK)
save(fig, "assets/figures/api-request-flow.svg")
