# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Rank-abundance curves for an even vs an uneven community."""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

np.random.seed(0)

S = 12  # shared species richness
rank = np.arange(1, S + 1)

# even community: abundances nearly equal
even = np.full(S, 100.0) + np.random.uniform(-4, 4, S)
even = np.sort(even)[::-1]
even_rel = even / even.sum()

# uneven community: one dominant, many rare (geometric decline)
uneven = 1000.0 * (0.5 ** (rank - 1))
uneven_rel = uneven / uneven.sum()


def shannon(p):
    p = p[p > 0]
    return -np.sum(p * np.log(p))


H_even = shannon(even_rel)
H_uneven = shannon(uneven_rel)

fig, ax = plt.subplots()
ax.semilogy(rank, even_rel, "o-", color=PALETTE[0], label="even")
ax.semilogy(rank, uneven_rel, "s-", color=PALETTE[1], label="uneven")

ax.annotate(f"even community has higher diversity\nH = {H_even:.2f} vs {H_uneven:.2f}",
            xy=(rank[-3], even_rel[-3]),
            xytext=(4.5, uneven_rel[0] * 0.9), color="#26323f",
            arrowprops=dict(arrowstyle="->", color="#26323f"))

ax.set_xticks(rank)
ax.set_xlabel("species rank")
ax.set_ylabel("relative abundance (log scale)")
ax.set_title(f"Rank-abundance (richness S = {S})")
ax.legend()

print(f"richness S = {S}")
print(f"Shannon H  even   = {H_even:.3f}")
print(f"Shannon H  uneven = {H_uneven:.3f}")

save(fig, "assets/figures/diversity-rank-abundance.svg")
