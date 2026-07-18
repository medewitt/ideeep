# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""The summary ROC plot from a bivariate diagnostic-accuracy meta-analysis. Each
study is a point in ROC space (sensitivity against 1 - specificity), area
proportional to sample size, scattering along an ROC-shaped arc because of the
threshold effect. The bivariate model gives the summary operating point, a tight
95% confidence region for the mean, and a much wider 95% prediction region for
where a new study would fall."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
# regenerate the study data (matches the page's seed)
rng = np.random.default_rng(15)
k = 16
cov = np.array([[0.7**2, -0.5 * 0.7 * 0.6], [-0.5 * 0.7 * 0.6, 0.6**2]])
theta = rng.multivariate_normal([1.7, 2.0], cov, k)
sens, spec = 1 / (1 + np.exp(-theta[:, 0])), 1 / (1 + np.exp(-theta[:, 1]))
n_dis, n_hlth = rng.integers(20, 120, k), rng.integers(30, 200, k)
TP, FP = rng.binomial(n_dis, sens), rng.binomial(n_hlth, 1 - spec)
obs_se, obs_x = TP / n_dis, FP / n_hlth                    # sensitivity, 1-specificity

# fitted bivariate summary (posterior means from the page's model)
mu = np.array([1.584, 2.092])
tau = np.array([0.692, 0.646]); corr = -0.164
se_mu = np.array([0.212, 0.186])
expit = lambda z: 1 / (1 + np.exp(-z))


def ellipse(mean, C, ax, color, ls, label):
    t = np.linspace(0, 2 * np.pi, 200)
    Lc = np.linalg.cholesky(C) * np.sqrt(stats.chi2.ppf(0.95, 2))
    pts = mean[:, None] + Lc @ np.vstack([np.cos(t), np.sin(t)])
    y = expit(pts[0]); x = 1 - expit(pts[1])              # -> ROC space
    ax.plot(x, y, color=color, lw=1.8, ls=ls, label=label)


Sigma = np.array([[tau[0]**2, corr * tau[0] * tau[1]],
                  [corr * tau[0] * tau[1], tau[1]**2]])
Cconf = np.diag(se_mu**2)

fig, ax = plt.subplots(figsize=(5.6, 4.8))
ax.scatter(obs_x, obs_se, s=15 + 0.6 * (n_dis + n_hlth), color=PALETTE[0],
           alpha=0.55, edgecolor=INK, linewidth=0.4, zorder=3, label="studies")
ax.scatter([1 - expit(mu[1])], [expit(mu[0])], s=110, color=PALETTE[1], marker="D",
           edgecolor="white", zorder=5, label="summary point")
ellipse(mu, Cconf, ax, PALETTE[1], "-", "95% confidence region")
ellipse(mu, Sigma + Cconf, ax, PALETTE[3], "--", "95% prediction region")
ax.plot([0, 1], [1, 0], color=MUTED, lw=0.7, ls=":")
ax.set_xlabel("1 − specificity  (false positive rate)")
ax.set_ylabel("sensitivity  (true positive rate)")
ax.set_title(f"Bivariate SROC: {expit(mu[0])*100:.0f}% sens, {expit(mu[1])*100:.0f}% spec",
             fontsize=9.6)
ax.set_xlim(0, 0.6)
ax.set_ylim(0.4, 1.0)
ax.legend(fontsize=7.8, loc="lower right")
fig.tight_layout()
save(fig, "assets/figures/dta-sroc.svg")
