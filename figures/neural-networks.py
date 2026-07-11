# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scikit-learn"]
# ///
"""Two ideas that make a neural network: nonlinear activations, and the
nonlinear decision boundaries they buy. Left: three common activation
functions. Right: a small multilayer perceptron carves a curved boundary
between two classes that a straight logistic-regression line cannot separate.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from _style import apply_style, save, PALETTE, INK

apply_style()

rng = np.random.default_rng(0)

# --- left: activation functions ---
z = np.linspace(-6, 6, 300)
sigmoid = 1.0 / (1.0 + np.exp(-z))
tanh = np.tanh(z)
relu = np.maximum(0.0, z)

# --- right: two interleaving "moons" of cases vs non-cases ---
n = 200
t = rng.uniform(0, np.pi, n)
x0 = np.c_[np.cos(t), np.sin(t)] + 0.12 * rng.standard_normal((n, 2))
x1 = np.c_[1 - np.cos(t), 0.5 - np.sin(t)] + 0.12 * rng.standard_normal((n, 2))
X = np.vstack([x0, x1])
y = np.r_[np.zeros(n), np.ones(n)]

mlp = MLPClassifier(hidden_layer_sizes=(16, 16), activation="relu",
                    max_iter=2000, random_state=0).fit(X, y)
logit = LogisticRegression().fit(X, y)

gx, gy = np.meshgrid(np.linspace(-1.6, 2.6, 300), np.linspace(-1.3, 1.8, 300))
grid = np.c_[gx.ravel(), gy.ravel()]
zz_mlp = mlp.predict_proba(grid)[:, 1].reshape(gx.shape)
zz_lin = logit.predict_proba(grid)[:, 1].reshape(gx.shape)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.4, 3.9))

ax0.plot(z, sigmoid, color=PALETTE[0], lw=2, label="sigmoid")
ax0.plot(z, tanh, color=PALETTE[1], lw=2, label="tanh")
ax0.plot(z, relu, color=PALETTE[2], lw=2, label="ReLU")
ax0.axhline(0, color=INK, lw=0.7)
ax0.set_ylim(-1.4, 3.2)
ax0.set_title("Activation functions")
ax0.set_xlabel("input  z")
ax0.set_ylabel(r"$\phi(z)$")
ax0.legend(loc="upper left")

ax1.contourf(gx, gy, zz_mlp, levels=[0, 0.5, 1], colors=[PALETTE[0], PALETTE[1]],
             alpha=0.15)
ax1.contour(gx, gy, zz_mlp, levels=[0.5], colors=[INK], linewidths=1.8)
ax1.contour(gx, gy, zz_lin, levels=[0.5], colors=[PALETTE[3]], linewidths=1.6,
            linestyles="--")
ax1.scatter(x0[:, 0], x0[:, 1], s=10, color=PALETTE[0], label="non-case")
ax1.scatter(x1[:, 0], x1[:, 1], s=10, color=PALETTE[1], label="case")
ax1.plot([], [], color=INK, lw=1.8, label="MLP boundary")
ax1.plot([], [], color=PALETTE[3], lw=1.6, ls="--", label="logistic line")
ax1.set_title("A curved boundary the line can't draw")
ax1.set_xlabel(r"feature $x_1$")
ax1.set_ylabel(r"feature $x_2$")
ax1.legend(loc="lower right", fontsize=8)

fig.tight_layout()
save(fig, "assets/figures/neural-networks.svg")
