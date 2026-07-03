# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""No assay wins on every axis: turnaround vs sensitivity, sized by cost/complexity."""
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

# (name, turnaround_hours, relative sensitivity 0-1, cost/complexity 1-5, category)
methods = [
    ("RAT",        0.3,  0.55, 1, "antigen"),
    ("LAMP",       1.0,  0.90, 2, "nucleic acid"),
    ("qPCR",       4.0,  0.98, 4, "nucleic acid"),
    ("ELISA",      5.0,  0.85, 3, "antibody/antigen"),
    ("Western",    24.0, 0.80, 3, "protein"),
    ("MALDI-TOF",  1.0,  0.92, 5, "protein"),
    ("Microscopy", 0.5,  0.60, 2, "visual"),
    ("Culture",    48.0, 0.85, 3, "growth"),
    ("EM",         6.0,  0.45, 5, "visual"),
]

cat_colors = {
    "nucleic acid": PALETTE[0],
    "antigen": PALETTE[1],
    "antibody/antigen": PALETTE[3],
    "protein": PALETTE[4],
    "visual": PALETTE[2],
    "growth": MUTED,
}

fig, ax = plt.subplots(figsize=(7.0, 4.2))
seen = set()
for name, hrs, sens, cost, cat in methods:
    color = cat_colors[cat]
    lab = cat if cat not in seen else None
    seen.add(cat)
    ax.scatter(hrs, sens, s=90 + cost * 90, color=color, alpha=0.75,
               edgecolor="white", linewidth=1.0, label=lab, zorder=3)
    ax.annotate(name, (hrs, sens), xytext=(0, 11 + cost), textcoords="offset points",
                ha="center", fontsize=8.5, color=INK)

ax.set_xscale("log")
ax.set_xticks([0.25, 1, 4, 12, 48])
ax.set_xticklabels(["15 min", "1 h", "4 h", "12 h", "2 d"])
ax.set_xlabel("time to result  (log scale)")
ax.set_ylabel("relative analytical sensitivity")
ax.set_ylim(0.35, 1.04)
ax.set_title("Diagnostic trade-offs  (bubble size ∝ cost & complexity)")
ax.legend(loc="lower left", fontsize=8, title="detects", title_fontsize=8)
save(fig, "assets/figures/diagnostics-tradeoffs.svg")
