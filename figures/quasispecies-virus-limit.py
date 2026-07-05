# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""Where RNA viruses sit relative to the error-threshold ceiling.

The error threshold caps genome length at L_max = ln(sigma) / mu, a
downward-sloping ceiling in the (mutation rate, genome length) plane. Real
RNA viruses cluster just beneath it -- their genomic mutation rate L*mu is of
order one -- while coronaviruses evolved proofreading to push mu down and L
up, escaping the crowd.

Mutation rates and genome lengths are approximate order-of-magnitude values
from viral mutation-rate reviews (e.g. Sanjuan et al. 2010; Drake & Holland
1999); they are illustrative, not precise.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED
apply_style()

# name, per-site mutation rate mu (subs/site/replication), genome length L (nt)
viruses = [
    ("Qβ phage",   3.5e-4,  4215),
    ("Poliovirus",      1.5e-4,  7440),
    ("Hepatitis C",     9.0e-5,  9600),
    ("Measles",         5.0e-5, 15900),
    ("Influenza A",     4.5e-5, 13500),
    ("HIV-1",           3.0e-5,  9700),
    ("SARS-CoV-2",      1.0e-6, 29900),
]

fig, ax = plt.subplots(figsize=(6.6, 4.4))

mu = np.logspace(-6.4, -2.7, 200)

# Error-threshold ceilings L_max = ln(sigma)/mu for two fitness superiorities.
for sigma, style, lab in ((np.e, "-", r"$\sigma=e$  ($\ln\sigma=1$)"),
                          (20.0, "--", r"$\sigma=20$  ($\ln\sigma\approx3$)")):
    ax.plot(mu, np.log(sigma) / mu, style, color=INK, linewidth=1.4,
            label=r"$L_{\max}=\ln\sigma/\mu$: " + lab)

# Shade the error-catastrophe region above the higher ceiling.
ax.fill_between(mu, np.log(20.0) / mu, 1e6, color=PALETTE[1], alpha=0.10,
                linewidth=0)
ax.text(3.5e-4, 4.6e4, "error catastrophe", color=PALETTE[1],
        fontsize=10, ha="center", style="italic")

# Plot the viruses; highlight the proofreading coronavirus.
offsets = {
    "Qβ phage": (6, 6), "Poliovirus": (7, -3), "Hepatitis C": (8, 2),
    "Measles": (8, 4), "Influenza A": (-8, -14), "HIV-1": (8, -4),
    "SARS-CoV-2": (-10, 8),
}
for name, m, L in viruses:
    proof = name == "SARS-CoV-2"
    color = PALETTE[2] if proof else PALETTE[0]
    ax.scatter([m], [L], s=55, color=color, zorder=5,
               edgecolor="white", linewidth=0.8)
    dx, dy = offsets[name]
    ax.annotate(name, (m, L), textcoords="offset points", xytext=(dx, dy),
                fontsize=9.5, color=color if proof else INK,
                ha="left" if dx >= 0 else "right",
                fontweight="bold" if proof else "normal")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(5e-7, 2e-3)
ax.set_ylim(2.5e3, 6e4)
ax.set_xlabel(r"Per-site mutation rate  $\mu$  (substitutions / site / replication)")
ax.set_ylabel("Genome length  $L$  (nucleotides)")
ax.set_title("The error threshold caps genome length: "
             r"$L_{\max}=\ln\sigma/\mu$")
ax.legend(loc="lower left", fontsize="small")

ax.text(6.8e-7, 5.6e3,
        r"RNA viruses hug the ceiling ($L\mu\sim1$);"
        "\ncoronaviruses proofread to lower $\\mu$"
        "\nand lengthen $L$.",
        fontsize=9, color=MUTED, va="bottom")

save(fig, "assets/figures/quasispecies-virus-limit.svg")
