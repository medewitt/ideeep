# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""A funnel plot showing publication bias. Each study is plotted by its effect
against its standard error (precise studies at the top). Without bias the points
scatter symmetrically inside the funnel; here the bottom-left is empty - small
studies with null or negative results went unpublished - so the cloud is
asymmetric. Trim-and-fill imputes the missing studies (open points), and the
pooled estimate shifts back toward the null."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()
rng = np.random.default_rng(3)
m = 64
se = rng.uniform(0.04, 0.6, m)
y = rng.normal(0.20, se)
pub = (se < 0.12) | (y / se > 1.28)
ys, ses = y[pub], se[pub]
v = ses**2
fe = lambda yy, vv: (yy / vv).sum() / (1 / vv).sum()
naive = fe(ys, v)

# trim-and-fill (L0) to locate imputed studies
th = naive
for _ in range(30):
    T = ys - th; r = stats.rankdata(np.abs(T)); Sr = np.sum(r[T > 0])
    k = len(ys); L0 = max(0, int(round((4 * Sr - k * (k + 1)) / (2 * k - 1))))
    order = np.argsort(ys)
    thn = fe(ys[order[:k - L0]] if L0 else ys, v[order[:k - L0]] if L0 else v)
    if abs(thn - th) < 1e-7:
        break
    th = thn
ex = np.argsort(ys)[k - L0:] if L0 else []
imp_y = 2 * th - ys[ex]
imp_se = ses[ex]
adj = fe(np.r_[ys, imp_y], np.r_[v, imp_se**2])

fig, ax = plt.subplots(figsize=(5.8, 4.6))
smax = ses.max() * 1.05
ss = np.linspace(0, smax, 50)
ax.plot(th + 1.96 * ss, ss, color=MUTED, lw=1.0, ls="--")
ax.plot(th - 1.96 * ss, ss, color=MUTED, lw=1.0, ls="--")
ax.axvline(th, color=INK, lw=1.0, ls=":")
ax.scatter(ys, ses, s=34, color=PALETTE[0], edgecolor="white", linewidth=0.4,
           zorder=3, label=f"published ({len(ys)})")
ax.scatter(imp_y, imp_se, s=40, facecolor="none", edgecolor=PALETTE[1],
           linewidth=1.4, zorder=3, label=f"imputed ({L0})")
ax.axvline(0, color=INK, lw=0.8)
ax.annotate("missing:\nsmall null studies", xy=(-0.15, 0.45), xytext=(-0.9, 0.33),
            fontsize=8.2, color=INK, arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
ax.set_ylim(smax, -0.02)                                # precise at top
ax.set_xlim(-1.0, 1.3)
ax.set_xlabel("study effect (log risk ratio)")
ax.set_ylabel("standard error")
ax.set_title("Funnel plot: asymmetry from missing small studies", fontsize=9.4)
ax.legend(fontsize=8.2, loc="lower right")
fig.tight_layout()
save(fig, "assets/figures/publication-bias-funnel.svg")
