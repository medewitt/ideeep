# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "networkx"]
# ///
"""Generate homepage card background motifs -> assets/cards/*.svg.

These are on-brand, abstract scientific backgrounds (in the site figure palette)
used behind a dark scrim on the homepage section cards. They are stand-ins for
photography (e.g. NIH BIOART); swap the files in assets/cards/ to use real
images without touching markup. Regenerate with: uv run figures/_card_motifs.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

OUT = "assets/cards"
os.makedirs(OUT, exist_ok=True)
W, H = 6.0, 4.0  # 3:2

LIGHT = "#ffffff"
ACCENTS = ["#8fc2e8", "#8fd6ab", "#c7a7e0", "#f0b48a", "#ffd27a"]


def new_ax(bg):
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor(bg)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(bg)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.margins(0)
    return fig, ax


def save(fig, name):
    fig.savefig(f"{OUT}/{name}.svg", facecolor=fig.get_facecolor())
    plt.close(fig)


def sir(bg):
    fig, ax = new_ax(bg)
    t = np.linspace(0, 80, 400)
    beta, gamma, N = 0.5, 0.1, 1000
    S, I, R = [990.0], [10.0], [0.0]
    dt = t[1] - t[0]
    for _ in t[1:]:
        s, i, r = S[-1], I[-1], R[-1]
        ds = -beta * s * i / N
        di = beta * s * i / N - gamma * i
        S.append(s + ds * dt); I.append(i + di * dt); R.append(r + gamma * i * dt)
    for arr, a in zip((S, I, R), (0.9, 0.75, 0.6)):
        ax.fill_between(t, arr, color=LIGHT, alpha=0.06)
        ax.plot(t, arr, color=LIGHT, lw=2.4, alpha=a)
    ax.plot(t, I, color=ACCENTS[3], lw=2.8)
    ax.set_xlim(0, 80); ax.set_ylim(0, 1050)
    save(fig, "programs")


def network(bg, name, accent, seed, k):
    fig, ax = new_ax(bg)
    rng = np.random.default_rng(seed)
    G = nx.random_geometric_graph(k, 0.34, seed=seed)
    pos = nx.spring_layout(G, seed=seed)
    for u, v in G.edges():
        x = [pos[u][0], pos[v][0]]; y = [pos[u][1], pos[v][1]]
        ax.plot(x, y, color=LIGHT, lw=1.0, alpha=0.22, zorder=1)
    xs = [pos[n][0] for n in G.nodes()]; ys = [pos[n][1] for n in G.nodes()]
    deg = np.array([d for _, d in G.degree()])
    ax.scatter(xs, ys, s=60 + deg * 55, color=accent, edgecolor=LIGHT,
               linewidth=1.0, alpha=0.9, zorder=2)
    ax.set_xlim(-0.15, 1.15); ax.set_ylim(-0.15, 1.15)
    save(fig, name)


def distributions(bg):
    fig, ax = new_ax(bg)
    x = np.linspace(-4, 8, 400)
    for mu, sd, a in [(0, 1, 0.9), (2.2, 1.4, 0.7), (4.2, 0.9, 0.8)]:
        y = np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
        ax.fill_between(x, y, color=LIGHT, alpha=0.07)
        ax.plot(x, y, color=LIGHT, lw=2.4, alpha=a)
    ax.plot(x, np.exp(-0.5 * ((x - 2.2) / 1.4) ** 2) / (1.4 * np.sqrt(2 * np.pi)),
            color=ACCENTS[0], lw=2.8)
    ax.set_xlim(-4, 8); ax.set_ylim(0, 0.46)
    save(fig, "math")


def matrix(bg):
    fig, ax = new_ax(bg)
    rng = np.random.default_rng(7)
    m = rng.random((6, 9)) ** 1.6
    ax.imshow(m, cmap="cividis", alpha=0.9, aspect="auto",
              extent=[0, 9, 0, 6], interpolation="nearest")
    for gx in range(10):
        ax.plot([gx, gx], [0, 6], color=bg, lw=3)
    for gy in range(7):
        ax.plot([0, 9], [gy, gy], color=bg, lw=3)
    ax.set_xlim(0, 9); ax.set_ylim(0, 6)
    save(fig, "programming")


def epicurve(bg):
    fig, ax = new_ax(bg)
    rng = np.random.default_rng(3)
    days = np.arange(28)
    shape = np.exp(-0.5 * ((days - 12) / 4.5) ** 2)
    counts = shape * 40 + rng.random(28) * 4
    ax.bar(days, counts, color=LIGHT, alpha=0.85, width=0.82)
    ax.bar(days[9:15], counts[9:15], color=ACCENTS[3], alpha=0.95, width=0.82)
    ax.set_xlim(-1, 28); ax.set_ylim(0, counts.max() * 1.15)
    save(fig, "epidemiology")


sir("#1f4a6b")
network("#245a44", "research", ACCENTS[1], 11, 16)
network("#4a3d63", "people", ACCENTS[2], 5, 13)
distributions("#2a4258")
matrix("#3b2c47")
epicurve("#7c3b28")
print("wrote", len(os.listdir(OUT)), "card motifs to", OUT)
