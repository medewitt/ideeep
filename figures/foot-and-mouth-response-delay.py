# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Why the timing of a response matters: culling protects the moment you act,
but vaccination's protection is delayed by the time it takes immunity to
develop.

  (a) A timeline for the farms around a detected case. Both responses share a
      detection-and-reporting lead time; culling then removes the farms at
      once, while vaccination leaves them susceptible through an
      immunity-onset window before they are finally protected.
  (b) The consequence: with a constant infection hazard, cases keep accruing
      in the ring until protection takes hold, so the vaccination delay lets
      an extra slice of the ring be infected. All illustrative.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

LEAD = 4        # detection + reporting + decision (days), shared
IMMUNITY = 7    # extra decision-to-immunity delay for vaccination
END = 18

fig, (axa, axb) = plt.subplots(1, 2, figsize=(10.6, 3.9))

# --- (a) two-track timeline -----------------------------------------------
axa.set_xlim(0, END)
axa.set_ylim(0, 1)
axa.set_yticks([])
axa.set_xlabel("days since the farm became infectious")
axa.set_title("(a) When does protection start?")

RED, GREEN, GREY = PALETTE[1], PALETTE[2], "#c9d2da"


def bar(y, x0, w, color, label=None):
    axa.add_patch(plt.Rectangle((x0, y), w, 0.14, color=color, alpha=0.9))
    if label:
        axa.text(x0 + w / 2, y + 0.07, label, ha="center", va="center",
                 fontsize=8, color="white", weight="bold")


# Culling track (upper)
yc = 0.62
bar(yc, 0, LEAD, GREY)
bar(yc, LEAD, END - LEAD, GREEN, "protected (removed)")
axa.text(0, yc + 0.20, "Ring culling", fontsize=9.5, color=INK, weight="bold")

# Vaccination track (lower)
yv = 0.20
bar(yv, 0, LEAD, GREY)
bar(yv, LEAD, IMMUNITY, RED, "still susceptible")
bar(yv, LEAD + IMMUNITY, END - LEAD - IMMUNITY, GREEN, "immune")
axa.text(0, yv + 0.20, "Ring vaccination", fontsize=9.5, color=INK,
         weight="bold")

axa.axvline(LEAD, color=INK, lw=0.8, ls=":")
axa.text(LEAD, 0.02, "act", ha="center", fontsize=8, color=MUTED)
axa.annotate("", xy=(LEAD + IMMUNITY, yv - 0.03), xytext=(LEAD, yv - 0.03),
             arrowprops=dict(arrowstyle="<->", color=INK))
axa.text(LEAD + IMMUNITY / 2, yv - 0.10, "immunity delay",
         ha="center", fontsize=8, color=INK)
axa.text(LEAD, 0.99, "shared lead time", ha="center", va="top", fontsize=7.6,
         color=MUTED)

# --- (b) cases accrued in the ring while protection is pending ------------
t = np.linspace(0, END, 400)
hazard = 0.14
# fraction of the ring infected: hazard runs until protection starts
prot_cull = LEAD
prot_vacc = LEAD + IMMUNITY
inf_cull = 1 - np.exp(-hazard * np.minimum(t, prot_cull))
inf_vacc = 1 - np.exp(-hazard * np.minimum(t, prot_vacc))
axb.plot(t, 100 * inf_cull, color=PALETTE[0], lw=2.3, label="ring culling")
axb.plot(t, 100 * inf_vacc, color=PALETTE[1], lw=2.3, label="ring vaccination")
axb.axvline(prot_cull, color=PALETTE[0], lw=0.9, ls=":")
axb.axvline(prot_vacc, color=PALETTE[1], lw=0.9, ls=":")
axb.fill_between(t, 100 * inf_cull, 100 * inf_vacc, color=PALETTE[1],
                 alpha=0.15)
axb.set_xlim(0, END)
axb.set_xlabel("days since the farm became infectious")
axb.set_ylabel("% of the ring infected")
axb.set_title("(b) Cost of the delay")
axb.legend(fontsize=8, loc="lower right")
axb.annotate("extra infections\nduring the delay",
             xy=(prot_vacc, 100 * (1 - np.exp(-hazard * prot_vacc))),
             xytext=(6.2, 30), fontsize=8, color=MUTED,
             arrowprops=dict(arrowstyle="->", color=INK))

fig.suptitle("Culling protects the moment you act; vaccination protects only "
             "after immunity develops", fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "assets/figures/foot-and-mouth-response-delay.svg")
