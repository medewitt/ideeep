# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "networkx",
#     "matplotlib",
# ]
# ///
"""Signed causal-loop diagram for a vector-borne outbreak."""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from _style import apply_style, save, PALETTE, INK, MUTED
apply_style()

# Signed edges: +1 links move together, -1 links move oppositely.
edges = [
    ("rainfall",    "vector\nabundance", +1),  # rain fills breeding sites
    ("vector\nabundance", "cases",       +1),  # more vectors, more cases
    ("cases",       "control\neffort",   +1),  # outbreaks trigger control
    ("control\neffort", "vector\nabundance", -1),  # control suppresses vectors [balancing]
    ("cases",       "complacency",        +1),  # a grinding caseload breeds fatigue (delay)
    ("complacency", "control\neffort",   -1),  # complacency erodes control [reinforcing path]
]

G = nx.DiGraph()
for u, v, s in edges:
    G.add_edge(u, v, sign=s)

# Hand-placed, deterministic layout.
pos = {
    "rainfall":          (-1.6,  1.1),
    "vector\nabundance": (-0.6,  0.2),
    "cases":             ( 0.7,  0.6),
    "control\neffort":   ( 0.3, -0.9),
    "complacency":       ( 1.7, -0.4),
}

POS = PALETTE[2]   # solid green for + edges
NEG = PALETTE[1]   # dashed orange for - edges

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.set_axis_off()

nx.draw_networkx_nodes(
    G, pos, ax=ax, node_size=2600, node_color="#eef2f5",
    edgecolors=INK, linewidths=1.2,
)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_color=INK)

# Draw signed edges and their +/- labels.
for u, v, s in edges:
    color = POS if s > 0 else NEG
    style = "solid" if s > 0 else "dashed"
    delay = (u == "cases" and v == "complacency")  # mark the delayed link
    nx.draw_networkx_edges(
        G, pos, edgelist=[(u, v)], ax=ax, edge_color=color,
        style=style, width=2.0, arrowsize=18, node_size=2600,
        connectionstyle="arc3,rad=0.12",
    )
    x = 0.5 * (pos[u][0] + pos[v][0])
    y = 0.5 * (pos[u][1] + pos[v][1]) + 0.12
    label = "+" if s > 0 else "−"
    if delay:
        label += " (delay)"
    ax.text(x, y, label, color=color, fontsize=12, fontweight="bold",
            ha="center", va="center")

# Legend explaining the sign convention.
handles = [
    plt.Line2D([0], [0], color=POS, lw=2.0, linestyle="solid",
               label="+  move together (reinforcing)"),
    plt.Line2D([0], [0], color=NEG, lw=2.0, linestyle="dashed",
               label="−  move oppositely (balancing)"),
]
ax.legend(handles=handles, loc="lower left", fontsize="small",
          frameon=False, labelcolor=INK)

ax.set_title("Systems mapping: a signed causal-loop diagram",
             color=INK, fontsize="large")
fig.tight_layout()

save(fig, "assets/figures/systems-thinking-and-systems-mapping.svg")
