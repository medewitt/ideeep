# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
#     "networkx",
# ]
# ///
"""Erdos-Renyi vs Barabasi-Albert degree distributions."""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from _style import apply_style, save, PALETTE
apply_style()

rng = np.random.default_rng(1)

N = 3000
mean_k = 4.0
p = mean_k / (N - 1)   # ER edge probability for <k> ~ 4
m_ba = 2               # BA edges per new node -> <k> ~ 4

G_er = nx.gnp_random_graph(N, p, seed=1)
G_ba = nx.barabasi_albert_graph(N, m_ba, seed=1)

deg_er = np.array([d for _, d in G_er.degree()])
deg_ba = np.array([d for _, d in G_ba.degree()])

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.5))

# LEFT: ER histogram, linear axes (roughly Poisson).
kmax = deg_er.max()
bins = np.arange(0, kmax + 2) - 0.5
axL.hist(deg_er, bins=bins, color=PALETTE[0], alpha=0.85,
         edgecolor="white", linewidth=0.4, label="ER data")

# Overlay the Poisson expectation.
lam = deg_er.mean()
ks = np.arange(0, kmax + 1)
from math import lgamma
poisson = np.exp(ks * np.log(lam) - lam - np.array([lgamma(k + 1) for k in ks]))
axL.plot(ks, poisson * N, color=PALETTE[1], linewidth=2.0,
         marker="o", markersize=3, label=f"Poisson ($\\lambda={lam:.1f}$)")

axL.set_xlabel("Degree $k$")
axL.set_ylabel("Number of nodes")
axL.set_title(f"Erdos-Renyi $G(N,p)$\n$\\langle k \\rangle \\approx {lam:.1f}$: "
              "homogeneous, no hubs")
axL.legend(fontsize="small")

# RIGHT: BA degree distribution, log-log (heavy tail).
counts = np.bincount(deg_ba)
ks_ba = np.nonzero(counts)[0]
prob = counts[ks_ba] / counts.sum()
axR.loglog(ks_ba, prob, linestyle="none", marker="o", markersize=4,
           color=PALETTE[2], label="BA data")

# Reference power-law slope ~ -3 for BA.
mask = ks_ba >= m_ba
ref_k = ks_ba[mask].astype(float)
ref = ref_k**(-3.0)
ref = ref * (prob[mask][0] / ref[0])
axR.loglog(ref_k, ref, color="0.4", linestyle="--", linewidth=1.5,
           label=r"$P(k)\propto k^{-3}$")

axR.set_xlabel("Degree $k$")
axR.set_ylabel("$P(k)$")
axR.set_title("Barabasi-Albert scale-free\nheavy tail: hubs act as "
              "superspreaders")
axR.legend(fontsize="small")

fig.suptitle("Network structure shapes epidemic potential: "
             "homogeneous vs scale-free degree distributions",
             fontsize="large")
fig.tight_layout(rect=(0, 0, 1, 0.94))

save(fig, "assets/figures/network-models.svg")
