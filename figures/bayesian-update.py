# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Beta-Binomial update: prior Beta(2,2), 8/10 positives, posterior Beta(10,4)."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from _style import apply_style, save, PALETTE

apply_style()

p = np.linspace(0, 1, 500)
a0, b0 = 2, 2
successes, trials = 8, 10
a1, b1 = a0 + successes, b0 + (trials - successes)  # Beta(10, 4)

prior = stats.beta.pdf(p, a0, b0)
posterior = stats.beta.pdf(p, a1, b1)

# scaled likelihood for context
lik = stats.binom.pmf(successes, trials, p)
_trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))  # numpy 2.x renamed trapz
lik_scaled = lik / _trapz(lik, p)

post_mean = a1 / (a1 + b1)  # 10/14
print(f"prior Beta({a0},{b0}), posterior Beta({a1},{b1})")
print(f"posterior mean = {a1}/{a1 + b1} = {post_mean:.4f}")

fig, ax = plt.subplots()
ax.plot(p, prior, color=PALETTE[0], lw=2, label=f"prior Beta({a0},{b0})")
ax.plot(p, lik_scaled, color=PALETTE[4], lw=1.5, ls=":",
        label="scaled likelihood")
ax.plot(p, posterior, color=PALETTE[1], lw=2,
        label=f"posterior Beta({a1},{b1})")

ax.axvline(post_mean, color=PALETTE[1], lw=1, ls="--")
ax.annotate(f"posterior mean\n10/14 ≈ {post_mean:.2f}",
            xy=(post_mean, stats.beta.pdf(post_mean, a1, b1)),
            xytext=(0.15, 2.6),
            arrowprops=dict(arrowstyle="->", color="#26323f"))

ax.set_xlim(0, 1)
ax.set_xlabel("p (positive probability)")
ax.set_ylabel("density")
ax.set_title("Bayesian update (Beta-Binomial)")
ax.legend(loc="upper left")

save(fig, "assets/figures/bayesian-update.svg")
