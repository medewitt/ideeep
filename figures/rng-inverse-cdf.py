# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""How a computer draws from any distribution: inverse-CDF sampling. Start
with uniform random numbers on [0, 1] -- the one thing the generator gives you
directly -- and pass them through the inverse cumulative distribution
function. For an Exponential(rate) that map is x = -ln(U)/rate, and uniform
draws come out exponentially distributed.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

rng = np.random.default_rng(0)
rate = 1.5
u = rng.random(50_000)
x = -np.log(u) / rate               # inverse-CDF of the exponential

fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.8, 3.6))

# left: the raw uniform draws
axL.hist(u, bins=40, density=True, color=PALETTE[0], alpha=0.85)
axL.axhline(1.0, color="0.3", ls="--", lw=1.3)
axL.set_title("uniform draws  U ∼ Uniform(0,1)", fontsize=10)
axL.set_xlabel("u")
axL.set_ylabel("density")
axL.set_ylim(0, 1.6)

# right: after the transform, with the true pdf overlaid
axR.hist(x, bins=60, density=True, color=PALETTE[2], alpha=0.85,
         label="transformed draws")
grid = np.linspace(0, x.max(), 300)
axR.plot(grid, rate * np.exp(-rate * grid), color="#b0332f", lw=2.2,
         label="true pdf  λe^(−λx)")
axR.set_title("x = −ln(U)/λ  ∼  Exponential(λ)", fontsize=10)
axR.set_xlabel("x")
axR.set_xlim(0, 5)
axR.legend(fontsize="small")

fig.suptitle("Inverse-CDF sampling: uniform in, any distribution out", y=1.02)
fig.tight_layout()
save(fig, "assets/figures/rng-inverse-cdf.svg")
