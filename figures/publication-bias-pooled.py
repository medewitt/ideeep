# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""What publication bias does to the pooled estimate. The naive pooled effect,
built only from the published studies, sits above the truth because the missing
studies were the small null ones. Trim-and-fill adjusts it partway back toward the
true value (0.20) by adding the imputed studies - a rough correction that typically
under-corrects, but moves in the right direction."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK

apply_style()
rng = np.random.default_rng(3)
m = 64
se = rng.uniform(0.04, 0.6, m)
y = rng.normal(0.20, se)
pub = (se < 0.12) | (y / se > 1.28)
ys, ses = y[pub], se[pub]
v = ses**2


def fe(yy, vv):
    w = 1 / vv
    mu = (w * yy).sum() / w.sum()
    return mu, np.sqrt(1 / w.sum())


naive, se_n = fe(ys, v)
th = naive
for _ in range(30):
    T = ys - th; r = stats.rankdata(np.abs(T)); Sr = np.sum(r[T > 0])
    k = len(ys); L0 = max(0, int(round((4 * Sr - k * (k + 1)) / (2 * k - 1))))
    order = np.argsort(ys)
    thn = fe(ys[order[:k - L0]] if L0 else ys, v[order[:k - L0]] if L0 else v)[0]
    if abs(thn - th) < 1e-7:
        break
    th = thn
ex = np.argsort(ys)[k - L0:] if L0 else []
adj, se_a = fe(np.r_[ys, 2 * th - ys[ex]], np.r_[v, ses[ex]**2])

rows = [("true effect", 0.20, 0.0, INK),
        ("naive pooled\n(published only)", naive, se_n, PALETTE[1]),
        ("trim-and-fill\nadjusted", adj, se_a, PALETTE[2])]
fig, ax = plt.subplots(figsize=(6.2, 3.0))
ax.axvline(0.20, color=INK, lw=1.0, ls=":")
for i, (lab, est, s, col) in enumerate(rows):
    yy = len(rows) - 1 - i
    if s > 0:
        ax.plot([est - 1.96 * s, est + 1.96 * s], [yy, yy], color=col, lw=2.4)
    ax.plot([est], [yy], "o", color=col, ms=10)
    ax.annotate(f"{est:.3f}", (est, yy + 0.18), fontsize=8.6, color=INK, ha="center")
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=8.6)
ax.set_xlabel("pooled log risk ratio")
ax.set_title("Publication bias inflates the pooled effect", fontsize=9.6)
ax.set_xlim(0.15, 0.32)
ax.set_ylim(-0.5, 2.5)
ax.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "assets/figures/publication-bias-pooled.svg")
