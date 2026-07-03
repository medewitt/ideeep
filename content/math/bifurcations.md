---
title: "Bifurcations"
---

# Bifurcations

Ecosystems and epidemics rarely change smoothly forever: push a parameter past a threshold and the entire long-term behavior can flip — a population blinks into existence, a disease starts to invade, a stable state gives way to sustained cycles.
These qualitative switches are called bifurcations, and they are where the interesting biology lives.

## What is a bifurcation?

A **bifurcation** is a qualitative change in the long-term behavior of a dynamical system as a parameter crosses a critical value.
Below the threshold the system might have a single stable equilibrium; above it, that equilibrium may vanish, split, change stability, or be replaced by a cycle.
The parameter that we vary — a growth rate, a transmission rate, a harvesting effort — is the **bifurcation parameter**, and the value where the change occurs is the **bifurcation point**.

Because stability is set by the sign of the real parts of the Jacobian eigenvalues (see [equilibria and stability](equilibria-and-stability.md)), a bifurcation happens precisely when an eigenvalue's real part passes through zero as the parameter moves.

## Local bifurcations of equilibria

### Saddle-node (fold)

Two equilibria — one stable, one unstable — approach each other, collide, and annihilate.
On one side of the threshold there are two fixed points; on the other side there are none.
The normal form is $\dot x = r - x^2$: for $r > 0$ there are equilibria at $x = \pm\sqrt{r}$ (a stable and an unstable branch), which merge at $r = 0$ and disappear for $r < 0$.
Folds underlie many ecological **tipping points**, where a system suddenly collapses because the stable state it was sitting in ceased to exist.

### Transcritical

Two equilibria pass through each other and **exchange stability**; both continue to exist on either side, but which one is stable swaps.
The normal form is $$\dot x = rx - x^2 = x(r - x),$$ with equilibria $x^* = 0$ and $x^* = r$ for all $r$.
This is the generic bifurcation at an invasion threshold: the disease-free equilibrium of an [epidemic model](sir.md) exchanges stability with the endemic equilibrium exactly as $R_0$ crosses $1$, and the extinction state of a growing population loses stability as the growth rate turns positive.

### Pitchfork

A single equilibrium becomes unstable and gives birth to two new symmetric stable equilibria (supercritical case), as in $\dot x = rx - x^3$.
Pitchforks require a symmetry in the model and show up in symmetric competition and pattern-formation problems.

### Hopf

Instead of another equilibrium, a **limit cycle** is born.
A stable equilibrium loses stability when a complex-conjugate pair of eigenvalues crosses the imaginary axis ($\Re(\lambda)$ passes through zero while $\Im(\lambda) \ne 0$), and a small-amplitude oscillation appears around it.
Hopf bifurcations are the mathematical origin of sustained cycles in [predator-prey](predator-prey.md) systems and in seasonally or demographically forced epidemics.

## Bifurcation diagrams and tipping points

A **bifurcation diagram** plots the location of equilibria (and the amplitude of any cycles) against the bifurcation parameter, drawing stable branches solid and unstable branches dashed.
Reading such a diagram tells you, at a glance, how many attractors exist for each parameter value and where they are created or destroyed.

In ecology these diagrams formalize **critical transitions** or **regime shifts**: lakes flipping from clear to turbid, fisheries collapsing, vegetation giving way to desert.
When a fold creates a region of bistability, the system can show **hysteresis** — the parameter value that triggers collapse is not the same as the one needed to recover, so the damage is hard to undo.

## A worked example: the transcritical bifurcation

Take the single-population model $$\dot x = rx - x^2 = x(r - x),$$ where $x \ge 0$ is population size and $r$ is the net per-capita growth rate.
The equilibria are $x^* = 0$ (extinction) and $x^* = r$ (a nonzero state).

Linearize with $f(x) = rx - x^2$, so $f'(x) = r - 2x$.

At $x^* = 0$: $f'(0) = r$.
This is stable when $r < 0$ and unstable when $r > 0$.

At $x^* = r$: $f'(r) = r - 2r = -r$.
This is stable when $r > 0$ and unstable (or biologically irrelevant, being negative) when $r < 0$.

So as $r$ increases through $0$, extinction ($x^*=0$) hands off its stability to the positive equilibrium $x^*=r$: the two branches cross at the origin and swap stability.
For $r < 0$ the only sensible attractor is extinction; for $r > 0$ the population settles at $x^* = r$.
This is exactly the [density-dependent](logistic-growth.md) story of a growth rate turning positive, and the same structure controls the disease-free-to-endemic switch handled rigorously by the [next-generation matrix](next-generation-matrix.md).

## Simulation

We sweep the parameter, solve for the stable equilibrium at each value, and plot the resulting bifurcation diagram.

### R

```r
r <- seq(-1, 2, length.out = 300)
stable <- ifelse(r > 0, r, 0)        # stable branch: x* = max(r, 0)
unstable <- ifelse(r > 0, 0, r)      # unstable branch

plot(r, stable, type = "l", lwd = 2, ylab = "equilibrium x*",
     xlab = "r", ylim = c(-1, 2))
lines(r, unstable, lty = 2)          # dashed = unstable
abline(v = 0, col = "grey")          # bifurcation point at r = 0
```

### Python

```python
import numpy as np
from scipy.optimize import brentq

def equilibria(r):
    return sorted({0.0, r})          # x(r - x) = 0

r = np.linspace(-1, 2, 300)
# stable branch is x* = r for r>0, else x* = 0
stable = np.where(r > 0, r, 0.0)
print(stable[r > 1][0])              # ~1.0: at r just above 1, x* ~ r

# confirm stability via f'(x*) = r - 2x*
for rv in (-0.5, 0.5):
    xs = rv if rv > 0 else 0.0
    print(rv, rv - 2*xs)             # negative -> stable
```

<!-- python-output:auto -->
```text
1.0066889632107023
-0.5 -0.5
0.5 -0.5
```
<!-- /python-output:auto -->

### Julia

```julia
rs = range(-1, 2; length = 300)
stable = [r > 0 ? r : 0.0 for r in rs]     # stable equilibrium branch
unstable = [r > 0 ? 0.0 : r for r in rs]   # unstable branch

# stability check: f'(x*) = r - 2x*
fprime(r, x) = r - 2x
println(fprime(0.5, 0.5))   # -0.5 < 0: x* = r is stable for r > 0
println(fprime(-0.5, 0.0))  # -0.5 < 0: extinction is stable for r < 0
```

## Why it matters

Bifurcations tell us where the switches are: the growth rate at which a population escapes extinction, the transmission level ($R_0 = 1$) at which a pathogen can invade, the harvesting or nutrient loading at which an ecosystem tips into collapse.
Understanding whether a threshold is a gentle transcritical exchange or an abrupt fold with hysteresis is the difference between a warning we can heed and a regime shift we cannot easily reverse.
The same thresholds appear in [discrete-time models](discrete-population-models.md), where increasing growth drives period-doubling cascades into chaos.

## Related

- [Equilibria and Linear Stability](equilibria-and-stability.md)
- [Discrete-Time Models and the Logistic Map](discrete-population-models.md)
- [The Next-Generation Matrix and R₀](next-generation-matrix.md)
- [Compartmental Models (SIR)](sir.md)
- [Exponential and Logistic Growth](logistic-growth.md)
- [Quantitative Methods](../math.md)
