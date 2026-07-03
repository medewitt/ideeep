---
title: "Equilibria and Linear Stability"
---

# Equilibria and Linear Stability

Whether a population settles at a carrying capacity, an epidemic burns out, or a predator and its prey cycle forever is decided by a handful of special states and their stability.
Equilibria are the resting points of a dynamical system, and linear stability analysis tells us which ones the system will actually be found near.

![A phase portrait: trajectories spiral in to a stable equilibrium.](../assets/figures/phase-portrait.svg)

## Equilibria

An **equilibrium** (or fixed point, or steady state) of an ordinary differential equation system $\frac{d\mathbf{x}}{dt} = \mathbf{f}(\mathbf{x})$ is a state where every rate of change vanishes, $$\frac{d\mathbf{x}}{dt} = \mathbf{0}.$$ Once the system reaches such a point it stays there forever, because nothing is changing.
Finding equilibria means solving the algebraic equations $\mathbf{f}(\mathbf{x}^*) = \mathbf{0}$ for the state $\mathbf{x}^*$.

### Nullclines

In the plane, with variables $x$ and $y$, it helps to draw the **nullclines**: the curves where each derivative is individually zero.
The $x$-nullcline is the set where $\dot x = 0$ and the $y$-nullcline is the set where $\dot y = 0$.
Equilibria sit exactly where an $x$-nullcline crosses a $y$-nullcline, since only there are both derivatives zero at once.
Nullclines also carve the phase plane into regions where the flow moves up-or-down and left-or-right, so they organize the whole phase portrait.

## Linear stability

An equilibrium is **stable** if small perturbations decay and the system returns to it, and **unstable** if perturbations grow.
To decide, we linearize: near $\mathbf{x}^*$ a small displacement $\mathbf{u} = \mathbf{x} - \mathbf{x}^*$ obeys, to first order, $$\frac{d\mathbf{u}}{dt} \approx J(\mathbf{x}^*)\,\mathbf{u},$$ where $J$ is the [Jacobian matrix](jacobians.md) of first-order [partial derivatives](partial-derivatives.md) evaluated at the equilibrium.

The linear system grows or decays like $e^{\lambda t}$ along its [eigenvectors](eigenvalues-and-eigenvectors.md), so stability is governed entirely by the eigenvalues $\lambda$ of $J$.
An equilibrium is **locally asymptotically stable if and only if every eigenvalue of the Jacobian has negative real part**, $\Re(\lambda) < 0$.
If any eigenvalue has $\Re(\lambda) > 0$, the equilibrium is unstable.

### One dimension

For a single equation $\dot x = f(x)$, the Jacobian is just the scalar $f'(x^*)$.
The equilibrium is stable when $$f'(x^*) < 0$$ and unstable when $f'(x^*) > 0$.
Geometrically, if the graph of $f$ crosses zero with a downward slope, the flow pushes $x$ back toward $x^*$ from both sides.

### Two dimensions: trace and determinant

For a $2\times 2$ Jacobian we rarely need the eigenvalues explicitly.
Write the trace $\tau = J_{11} + J_{22}$ and the determinant $\Delta = \det J$; the eigenvalues solve $$\lambda^2 - \tau\lambda + \Delta = 0, \qquad \lambda = \frac{\tau \pm \sqrt{\tau^2 - 4\Delta}}{2}.$$ The sign pattern of $(\tau, \Delta)$ classifies the equilibrium:

- $\Delta < 0$ — **saddle** (one positive, one negative eigenvalue), always unstable.
- $\Delta > 0$ and $\tau < 0$ — **stable** node (if $\tau^2 \ge 4\Delta$) or **stable spiral** (if $\tau^2 < 4\Delta$).
- $\Delta > 0$ and $\tau > 0$ — **unstable** node or spiral.
- $\tau = 0$, $\Delta > 0$ — **center**: purely imaginary eigenvalues, neutral cycles (borderline; nonlinear terms decide the true behavior).

A stable node or spiral requires both $\tau < 0$ and $\Delta > 0$ — the standard two-dimensional stability test.

## A worked example

Consider the system $$\dot x = x(3 - x - 2y), \qquad \dot y = y(2 - x - y).$$ This is a [competition](competition-coexistence.md)-style model.

### Equilibria

Setting $\dot x = 0$ requires $x = 0$ or $x + 2y = 3$; setting $\dot y = 0$ requires $y = 0$ or $x + y = 2$.
Combining the branches gives four equilibria: $(0,0)$, $(3,0)$, $(0,2)$, and the interior point where $x + 2y = 3$ and $x + y = 2$, which solves to $(1,1)$.

### Jacobian

Differentiating, $$J(x,y) = \begin{bmatrix} 3 - 2x - 2y & -2x \\ -y & 2 - x - 2y \end{bmatrix}.$$

### Classify each

At $(0,0)$: $J = \begin{bmatrix} 3 & 0 \\ 0 & 2\end{bmatrix}$, eigenvalues $3, 2 > 0$ — **unstable node**.

At $(3,0)$: $J = \begin{bmatrix} -3 & -6 \\ 0 & -1\end{bmatrix}$, eigenvalues $-3, -1$ — $\tau = -4 < 0$, $\Delta = 3 > 0$: **stable node**.

At $(0,2)$: $J = \begin{bmatrix} -1 & 0 \\ -2 & -2\end{bmatrix}$, eigenvalues $-1, -2$ — **stable node**.

At $(1,1)$: $J = \begin{bmatrix} -1 & -2 \\ -1 & -1\end{bmatrix}$, $\tau = -2$, $\Delta = (-1)(-1) - (-2)(-1) = 1 - 2 = -1 < 0$: **saddle** (unstable).

So the interior coexistence point is a saddle, and the two single-species states are both stable — the classic bistable outcome of strong competition, where the winner depends on initial conditions.

## Simulation

We draw the nullclines, mark the equilibria, and overlay a phase portrait (a direction field with a few trajectories).

### R

```r
library(deSolve)

f <- function(t, s, p) {
  x <- s[1]; y <- s[2]
  list(c(x * (3 - x - 2*y), y * (2 - x - y)))
}

# vector field on a grid
g <- expand.grid(x = seq(0, 3.2, 0.3), y = seq(0, 2.4, 0.3))
d <- with(g, cbind(x*(3 - x - 2*y), y*(2 - x - y)))
plot(g$x, g$y, type = "n", xlab = "x", ylab = "y")
arrows(g$x, g$y, g$x + 0.08*d[,1], g$y + 0.08*d[,2], length = 0.03)

abline(a = 1.5, b = -0.5, col = "blue")   # x-nullcline x + 2y = 3
abline(a = 2,   b = -1,   col = "red")    # y-nullcline x + y = 2
points(rbind(c(0,0), c(3,0), c(0,2), c(1,1)), pch = 19)

# trajectory near the saddle drifts to a stable node
ode(c(1.1, 0.9), seq(0, 20, 0.1), f, NULL)[201, ]  # -> near (3, 0)
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

def f(t, s):
    x, y = s
    return [x*(3 - x - 2*y), y*(2 - x - y)]

# Jacobian eigenvalues at the interior equilibrium (1, 1)
J = np.array([[-1., -2.], [-1., -1.]])
print(np.linalg.eigvals(J))          # ~[ 0.414, -2.414] -> saddle

sol = solve_ivp(f, (0, 20), [1.1, 0.9], rtol=1e-8, dense_output=True)
print(sol.y[:, -1])                  # ~[3, 0]: settles at the stable node
```

<!-- python-output:auto -->
```text
[ 0.41421356 -2.41421356]
[3.00000032e+00 3.98062839e-07]
```
<!-- /python-output:auto -->

### Julia

```julia
using LinearAlgebra

J(x, y) = [3 - 2x - 2y   -2x;
           -y            2 - x - 2y]

for (x, y) in ((0,0), (3,0), (0,2), (1,1))
    println((x, y), " -> ", eigvals(J(x, y)))
end
# (1, 1) gives one positive, one negative eigenvalue: a saddle
```

## Why it matters

Nearly every question about long-run ecological and epidemic dynamics reduces to "which equilibria exist, and which are stable."
The disease-free equilibrium of an [epidemic model](sir.md) is stable exactly when $R_0 < 1$, and it loses stability as $R_0$ crosses $1$; a [predator-prey](predator-prey.md) coexistence point can be a stable spiral (damped oscillations) or a neutral center (persistent cycles).
Because stability can flip as a parameter moves, this analysis is also the entry point to [bifurcations](bifurcations.md), where equilibria are created, destroyed, or exchange stability.

## Related

- [Jacobians](jacobians.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Partial Derivatives](partial-derivatives.md)
- [Bifurcations](bifurcations.md)
- [Predator-Prey Dynamics](predator-prey.md)
- [Compartmental Models (SIR)](sir.md)
- [Quantitative Methods](../math.md)
