# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Two mental models behind Git. Left: commits are snapshots on a line of
history; a feature branch is an independent line that diverges from main to let
you experiment safely, then merges back. Right: the everyday loop moves changes
across four places — the working directory, the staging area, the local repo,
and the remote (origin) on GitHub — via add, commit, push, and pull."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from _style import apply_style, save, INK, MUTED, PALETTE

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.0, 3.9))
BLUE, ORANGE, GREEN, PURPLE = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]

# ---- commit graph ---------------------------------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 6)
axL.axis("off")
axL.set_title("Commits, branches, and a merge", fontsize=10)

main_y, feat_y = 1.6, 4.0
main_x = [1, 2.6, 4.2, 7.4, 9.0]
feat_x = [5.0, 6.2]

# main line
axL.plot(main_x, [main_y] * len(main_x), color=BLUE, lw=2.0, zorder=1)
for x in main_x:
    axL.add_patch(Circle((x, main_y), 0.22, color=BLUE, zorder=2))
axL.text(main_x[0] - 0.1, main_y - 0.7, "main", fontsize=9, color=BLUE)

# feature branch diverges from 2nd main commit, merges into last-but-one
axL.plot([main_x[1]] + feat_x, [main_y] + [feat_y] * 2, color=ORANGE, lw=2.0)
axL.plot([feat_x[-1], main_x[3]], [feat_y, main_y], color=ORANGE, lw=2.0)
for x in feat_x:
    axL.add_patch(Circle((x, feat_y), 0.22, color=ORANGE, zorder=2))
axL.text(feat_x[0] - 0.1, feat_y + 0.45, "feature branch", fontsize=9, color=ORANGE)
axL.annotate("branch off", xy=(main_x[1], main_y), xytext=(2.7, 2.7),
             fontsize=7.8, color=MUTED)
axL.annotate("merge back", xy=(main_x[3], main_y), xytext=(6.7, 3.0),
             fontsize=7.8, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
axL.text(5, 0.35, "each commit = a labeled snapshot of your files",
         fontsize=8, color="0.35", ha="center", style="italic")

# ---- add / commit / push / pull loop --------------------------------------
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.axis("off")
axR.set_title("The everyday loop", fontsize=10)


def box(x, y, w, h, text, color):
    axR.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                  linewidth=1.6, edgecolor=color, facecolor=color + "14"))
    axR.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=8.6, color=INK)


box(0.4, 7.6, 4.0, 1.6, "working\ndirectory", BLUE)
box(0.4, 5.0, 4.0, 1.6, "staging area", GREEN)
box(0.4, 2.4, 4.0, 1.6, "local repo\n(.git)", PURPLE)
box(5.8, 2.4, 3.8, 1.6, "remote\norigin (GitHub)", ORANGE)


def arrow(x1, y1, x2, y2, label, dx=0.25):
    axR.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                  mutation_scale=15, color="0.4", lw=1.6))
    axR.text(x1 + dx, (y1 + y2) / 2, label, fontsize=8, color=INK, va="center")


arrow(2.4, 7.5, 2.4, 6.7, "git add")
arrow(2.4, 4.9, 2.4, 4.1, "git commit")
arrow(4.5, 3.2, 5.7, 3.2, "git push", dx=0.15)
# pull arrow back (remote -> working dir) along the right/top
axR.add_patch(FancyArrowPatch((7.7, 4.1), (4.4, 8.4), arrowstyle="-|>",
              mutation_scale=15, color=ORANGE, lw=1.5,
              connectionstyle="arc3,rad=0.32"))
axR.text(8.1, 6.6, "git pull", fontsize=8, color=ORANGE, rotation=0)

fig.tight_layout()
save(fig, "assets/figures/version-control-git.svg")
