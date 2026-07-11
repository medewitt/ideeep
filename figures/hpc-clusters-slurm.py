# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Running work on an HPC cluster. Left: the parts of a cluster — you SSH from
your laptop to a login node (staging only), write a job script and hand it to
the SLURM scheduler, which dispatches it to compute nodes; all of them share one
filesystem. Right: a job array launches one task per input and SLURM runs as
many in parallel as there is room for, so some tasks are RUNNING while others
wait PENDING behind a fair-share limit."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from _style import apply_style, save, INK, MUTED, PALETTE

apply_style()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.0, 3.9),
                               gridspec_kw={"width_ratios": [1.05, 1]})
BLUE, GREEN, ORANGE, PURPLE = PALETTE[0], PALETTE[2], PALETTE[1], PALETTE[3]

# ---- cluster architecture -------------------------------------------------
axL.set_xlim(0, 10)
axL.set_ylim(0, 10)
axL.axis("off")
axL.set_title("The parts of a cluster", fontsize=10)


def box(x, y, w, h, text, color, fs=8.3):
    axL.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                  linewidth=1.7, edgecolor=color, facecolor=color + "16"))
    axL.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
             color=INK)


box(0.4, 7.6, 3.0, 1.6, "your laptop", BLUE)
box(6.4, 7.6, 3.2, 1.6, "login node\n(staging only)", GREEN)
box(6.4, 4.7, 3.2, 1.4, "SLURM\nscheduler", ORANGE)
# compute nodes row
for i in range(3):
    box(0.4 + i * 1.15, 1.5, 1.0, 1.4, f"c{i+1}", PURPLE, fs=8)
axL.text(2.1, 3.15, "compute nodes", fontsize=8, color=PURPLE, ha="center")

# arrows
axL.add_patch(FancyArrowPatch((3.5, 8.4), (6.3, 8.4), arrowstyle="-|>",
              mutation_scale=14, color="0.4", lw=1.6))
axL.text(4.9, 8.7, "SSH", fontsize=8, ha="center", color=INK)
axL.add_patch(FancyArrowPatch((8.0, 7.5), (8.0, 6.2), arrowstyle="-|>",
              mutation_scale=13, color="0.4", lw=1.5))
axL.text(8.7, 6.85, "submit", fontsize=7.6, color=INK)
axL.add_patch(FancyArrowPatch((6.3, 5.4), (2.5, 2.95), arrowstyle="-|>",
              mutation_scale=13, color="0.4", lw=1.5))
axL.text(4.2, 4.6, "dispatch", fontsize=7.6, color=INK, rotation=-25)
# shared filesystem spanning
axL.add_patch(Rectangle((0.4, 0.3), 9.2, 0.7, facecolor="#d8dee4",
              edgecolor=MUTED))
axL.text(5.0, 0.65, "shared filesystem (home · scratch · project data)",
         ha="center", va="center", fontsize=7.8, color=INK)

# ---- job-array queue / Gantt ----------------------------------------------
axR.set_title("A job array across nodes", fontsize=10)
n_tasks = 10
slots = 4
# each task: (start, duration); RUNNING = start 0, PENDING waits for a slot
finish = [0.0] * slots
starts = []
for t in range(n_tasks):
    s = min(finish)
    k = finish.index(s)
    dur = 2.0 + (t % 3) * 0.6
    starts.append((s, dur, s == 0))
    finish[k] = s + dur
for t, (s, dur, running) in enumerate(starts):
    col = PALETTE[2] if running else PALETTE[3]
    axR.barh(t, dur, left=s, height=0.6, color=col + ("cc" if running else "88"))
    axR.text(s + 0.1, t, f"task {t}", va="center", fontsize=7, color="white")
axR.axvline(0, color=INK, lw=1.0)
axR.text(0.1, n_tasks - 0.2, "now", fontsize=7.5, color=INK)
axR.scatter([], [], color=PALETTE[2], marker="s", label="RUNNING")
axR.scatter([], [], color=PALETTE[3], marker="s", label="PENDING (queued)")
axR.legend(fontsize=7.8, loc="lower right")
axR.set_xlabel("time  (SLURM runs 4 at once, fair-share limit)")
axR.set_ylabel("task in the array (one per input)")
axR.set_yticks([])
axR.set_xlim(0, max(f for f in finish) + 0.5)

fig.tight_layout()
save(fig, "assets/figures/hpc-clusters-slurm.svg")
