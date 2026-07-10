# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Vaccine efficacy vs effectiveness, and the test-negative design."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(1834)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.8, 3.6))

# --- LEFT: attack rate, unvaccinated vs vaccinated ---
# Trial efficacy: RR = AR_vacc / AR_unvacc; VE = 1 - RR.
ar_unvacc = 90.0   # cases per 1000
ar_vacc = 18.0     # cases per 1000
rr = ar_vacc / ar_unvacc
ve = 1.0 - rr

x = np.array([0, 1])
axL.bar(x[0], ar_unvacc, width=0.55, color=PALETTE[1],
        label="unvaccinated")
axL.bar(x[1], ar_vacc, width=0.55, color=PALETTE[0],
        label="vaccinated")

# Faded overlay: real-world effectiveness < trial efficacy.
ar_vacc_field = 30.0
axL.bar(x[1], ar_vacc_field, width=0.55, color=PALETTE[0],
        alpha=0.28, hatch="///", edgecolor=PALETTE[0], lw=0.0)
axL.annotate("effectiveness < efficacy\n(waning, variants, coverage)",
             xy=(1, ar_vacc_field), xytext=(1.30, 82),
             fontsize="x-small", color=MUTED, ha="right",
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))

# Arrow between bar tops showing the relative reduction.
axL.annotate("", xy=(1, ar_vacc), xytext=(0, ar_unvacc),
             arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
axL.text(0.28, 64, f"VE = 1 - RR = {ve:.0%}",
         ha="center", fontsize="small", color=INK)

axL.set_xticks(x)
axL.set_xticklabels(["unvaccinated", "vaccinated"])
axL.set_ylabel("attack rate (per 1000)")
axL.set_ylim(0, 105)
axL.set_title("Efficacy vs effectiveness")
axL.legend(loc="upper right", fontsize="x-small")

# --- RIGHT: test-negative design 2x2 (axis-free, drawn by hand) ---
axR.axis("off")
axR.set_xlim(0, 10)
axR.set_ylim(0, 10)
axR.set_title("Test-negative design")

# Counts: a = test-positive vaccinated, b = test-positive unvaccinated,
# c = test-negative vaccinated, d = test-negative unvaccinated.
a, b = 40, 160     # cases (test-positive)
c, d = 260, 240    # controls (test-negative)
odds_ratio = (a / b) / (c / d)
ve_tnd = 1.0 - odds_ratio

# Grid geometry.
x0, x1, x2 = 3.4, 6.0, 8.6   # column centers offset; use box edges below
left, right = 2.4, 9.2
top, bot = 8.4, 3.2
midx = (left + right) / 2
midy = (top + bot) / 2

for xv in (left, midx, right):
    axR.plot([xv, xv], [bot, top], color=INK, lw=1.0)
for yv in (bot, midy, top):
    axR.plot([left, right], [yv, yv], color=INK, lw=1.0)

# Column headers (test-positive = cases, test-negative = controls).
axR.text((left + midx) / 2, top + 0.55, "test-positive\n(cases)",
         ha="center", va="bottom", fontsize="x-small", color=MUTED)
axR.text((midx + right) / 2, top + 0.55, "test-negative\n(controls)",
         ha="center", va="bottom", fontsize="x-small", color=MUTED)

# Row labels.
axR.text(left - 0.3, (midy + top) / 2, "vaccinated",
         ha="right", va="center", fontsize="x-small", color=MUTED)
axR.text(left - 0.3, (bot + midy) / 2, "unvaccinated",
         ha="right", va="center", fontsize="x-small", color=MUTED)

# Cell counts.
axR.text((left + midx) / 2, (midy + top) / 2, f"a = {a}",
         ha="center", va="center", fontsize="medium", color=INK)
axR.text((midx + right) / 2, (midy + top) / 2, f"c = {c}",
         ha="center", va="center", fontsize="medium", color=INK)
axR.text((left + midx) / 2, (bot + midy) / 2, f"b = {b}",
         ha="center", va="center", fontsize="medium", color=INK)
axR.text((midx + right) / 2, (bot + midy) / 2, f"d = {d}",
         ha="center", va="center", fontsize="medium", color=INK)

# Formula beneath the grid.
axR.text(midx, bot - 0.9,
         "VE = 1 - OR,  OR = (a/b) / (c/d)",
         ha="center", va="center", fontsize="small", color=INK)
axR.text(midx, bot - 1.8,
         f"OR = {odds_ratio:.2f},  VE = {ve_tnd:.0%}",
         ha="center", va="center", fontsize="x-small", color=PALETTE[0])

fig.tight_layout()

print(f"trial: RR = {rr:.3f}, VE = {ve:.3f}")
print(f"TND:   OR = {odds_ratio:.3f}, VE = {ve_tnd:.3f}")

save(fig, "assets/figures/vaccine-effectiveness.svg")
