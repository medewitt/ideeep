# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Publishing a personal website. Left: the build-and-deploy pipeline — write
Markdown / R Markdown source, build it to static HTML, push the repo to GitHub,
and a host (GitHub Pages or Netlify) serves it at a live URL, rebuilding
automatically on each push. Right: a custom domain points at that host through
DNS — the registrar's CNAME (for www) and A/ALIAS (for the apex) records
resolve your domain to the host, which returns the site."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _style import apply_style, save, INK, MUTED, PALETTE

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 3.8))

# ---- deploy pipeline ------------------------------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 10)
axL.axis("off")
axL.set_title("Build & deploy", fontsize=9.8)
steps = [("source\n.qmd · .Rmd", 8.4, PALETTE[0]),
         ("quarto render →\nstatic HTML (_site/)", 6.3, PALETTE[2]),
         ("git push to\nGitHub repo", 4.2, PALETTE[3]),
         ("host serves it:\nPages / Netlify → live URL", 1.9, PALETTE[1])]
for text, y, col in steps:
    axL.add_patch(FancyBboxPatch((1.2, y - 0.72), 7.6, 1.44,
                  boxstyle="round,pad=0.06", linewidth=1.6, edgecolor=col,
                  facecolor=col + "16"))
    axL.text(5.0, y, text, ha="center", va="center", fontsize=8.3, color=INK)
for y in (7.55, 5.45, 3.35):
    axL.add_patch(FancyArrowPatch((5.0, y), (5.0, y - 0.6), arrowstyle="-|>",
                  mutation_scale=13, color="0.4", lw=1.5))
axL.text(5.0, 0.4, "auto-rebuilds on each push", ha="center", fontsize=7.6,
         color=MUTED, style="italic")

# ---- DNS pointing ---------------------------------------------------------
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.axis("off")
axR.set_title("Point a custom domain (DNS)", fontsize=9.8)
nodes = [("visitor's\nbrowser", 8.6, PALETTE[0]),
         ("registrar DNS\nCNAME www · A/ALIAS apex", 5.6, PALETTE[3]),
         ("host\n(Pages / Netlify)", 2.6, PALETTE[1])]
for text, y, col in nodes:
    axR.add_patch(FancyBboxPatch((1.4, y - 0.72), 7.2, 1.44,
                  boxstyle="round,pad=0.06", linewidth=1.6, edgecolor=col,
                  facecolor=col + "16"))
    axR.text(5.0, y, text, ha="center", va="center", fontsize=8.3, color=INK)
axR.add_patch(FancyArrowPatch((5.0, 7.85), (5.0, 6.35), arrowstyle="-|>",
              mutation_scale=13, color="0.4", lw=1.5))
axR.text(5.4, 7.1, "look up yoursite.com", fontsize=7.4, color=INK)
axR.add_patch(FancyArrowPatch((5.0, 4.85), (5.0, 3.35), arrowstyle="-|>",
              mutation_scale=13, color="0.4", lw=1.5))
axR.text(5.4, 4.1, "resolves to the host", fontsize=7.4, color=INK)
axR.add_patch(FancyArrowPatch((1.4, 2.6), (0.7, 8.6), arrowstyle="-|>",
              mutation_scale=13, color=PALETTE[1], lw=1.4,
              connectionstyle="arc3,rad=0.35"))
axR.text(0.15, 5.6, "returns the site", fontsize=7.4, color=PALETTE[1],
         rotation=90, va="center", ha="center")

fig.tight_layout()
save(fig, "assets/figures/personal-website.svg")
