# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Probability of target attainment (PTA) versus MIC by Monte Carlo.

A one-compartment IV drug is dosed intermittently to steady state. Clearance
varies lognormally between patients, so each patient has a different
concentration-time profile and a different fraction of the interval above the
MIC. PTA is the fraction of simulated patients whose fT>MIC clears a target.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()

rng = np.random.default_rng(1834)

V = 15.0        # volume of distribution (L)
tau = 8.0       # dosing interval (h)
target = 0.50   # required fraction of the interval above MIC
cl_med = 6.0    # median clearance (L/h)
cl_cv = 0.40    # coefficient of variation of clearance
n = 5000        # simulated patients

sigma = np.sqrt(np.log(1 + cl_cv**2))
cl = cl_med * np.exp(rng.normal(0.0, sigma, n))    # lognormal clearance
k = cl / V                                          # elimination rate (per h)


def ft_above_mic(dose, mic):
    cmax_ss = (dose / V) / (1 - np.exp(-k * tau))   # steady-state peak
    above = cmax_ss > mic
    t_cross = np.where(above, np.log(cmax_ss / np.maximum(mic, 1e-9)) / k, 0.0)
    return np.minimum(t_cross, tau) / tau


mics = np.geomspace(0.25, 32, 60)
fig, ax = plt.subplots()
for dose, color in [(1000.0, PALETTE[0]), (2000.0, PALETTE[1])]:
    pta = [np.mean(ft_above_mic(dose, m) >= target) for m in mics]
    ax.plot(mics, pta, color=color, lw=2.2, label=f"{dose/1000:.0f} g q8h")

ax.axhline(0.90, color=INK, ls="--", lw=1.0)
ax.text(0.27, 0.915, "90% PTA target", fontsize=9, color=INK)

ax.set_xscale("log", base=2)
ax.set_xlabel("MIC (mg/L)")
ax.set_ylabel(r"PTA:  $P(fT_{>MIC} \geq 50\%)$")
ax.set_ylim(-0.03, 1.03)
ax.set_title("Target attainment falls as the MIC rises")
ax.legend(loc="lower left", fontsize=9)

save(fig, "assets/figures/pkpd-target-attainment.svg")
