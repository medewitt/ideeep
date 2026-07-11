---
title: "The Community Matrix and Stability"
---

# The Community Matrix and Stability

Whether a whole ecological community holds together or unravels depends on the web of pairwise interactions among its species.
The community matrix packages those interactions into a single object whose eigenvalues tell us, at a glance, whether an equilibrium is stable — and it sits at the heart of the famous debate over whether complexity begets stability.

![Left: May's random-matrix experiment — the fraction of randomly assembled communities that are stable collapses sharply as the complexity $\sigma\sqrt{SC}$ crosses $1$, so more species, connectance, or interaction strength destabilizes. Right: the worked $2\times2$ predator–prey matrix has eigenvalues $-0.35\pm0.614\,i$; both lie in the left half-plane (negative real part), so the equilibrium is a stable focus and perturbations spiral back in.](../assets/figures/community-matrix.svg "fig:community")

## Definition

Consider a community of $S$ species with densities $N_1, \dots, N_S$ governed by $\frac{dN_i}{dt} = f_i(N_1, \dots, N_S)$.
Suppose the system has a feasible equilibrium $\mathbf{N}^*$ where every $\frac{dN_i}{dt}=0$.
The **community matrix** $A$ collects the effect of a small change in each species' density on each species' growth rate, evaluated at that equilibrium:

\[
a_{ij} = \left.\frac{\partial\, (dN_i/dt)}{\partial N_j}\right|_{\mathbf{N}^*}.
\]

In other words, $A$ is the [Jacobian](jacobians.md) of the interaction dynamics evaluated at equilibrium.
The sign of $a_{ij}$ encodes the interaction type: predator–prey gives opposite signs ($a_{ij}<0$, $a_{ji}>0$), competition gives both negative, mutualism both positive, and the diagonal $a_{ii}$ is usually negative (self-regulation).

## The stability criterion

Near the equilibrium, small perturbations $\mathbf{x} = \mathbf{N} - \mathbf{N}^*$ evolve approximately as $\frac{d\mathbf{x}}{dt} = A\mathbf{x}$.
The equilibrium is **locally stable** — perturbations decay — if and only if every [eigenvalue](eigenvalues-and-eigenvectors.md) of $A$ has negative real part.

For a $2\times 2$ community matrix the condition simplifies to the **Routh–Hurwitz** conditions:

\[
\operatorname{tr}(A) = a_{11} + a_{22} < 0 \quad\text{and}\quad \det(A) = a_{11}a_{22} - a_{12}a_{21} > 0.
\]

A negative trace means self-regulation dominates on average; a positive determinant rules out a saddle point.
Together they guarantee both eigenvalues have negative real part.

## May's complexity–stability result

Ecologists once assumed that more complex communities — more species, more connections — are inherently more stable.
Robert May tested this with random matrices.
Build a large $S\times S$ community matrix with diagonal $-1$ (each species self-limiting) and off-diagonal entries that are nonzero with probability $C$ (the **connectance**), drawn from a distribution with mean zero and standard deviation $\sigma$ (the interaction strength).

May showed that as $S$ grows, such a system is almost surely stable when

\[
\sigma\sqrt{SC} < 1
\]

and almost surely unstable once $\sigma\sqrt{SC} > 1$.
The striking implication is that **complexity tends to destabilize**: increasing the number of species $S$, the connectance $C$, or the interaction strength $\sigma$ pushes a randomly assembled community toward instability ([@fig:community]).
Real communities persist despite this, which tells us their interaction structure is far from random — a puzzle that still drives research.

## Worked example

Take a predator–prey pair with self-limitation, community matrix

\[
A = \begin{bmatrix} -0.5 & -1 \\ 0.4 & -0.2 \end{bmatrix}.
\]

Trace and determinant:

\[
\operatorname{tr}(A) = -0.5 + (-0.2) = -0.7 < 0,
\]
\[
\det(A) = (-0.5)(-0.2) - (-1)(0.4) = 0.10 + 0.40 = 0.50 > 0.
\]

Both Routh–Hurwitz conditions hold, so the equilibrium is **stable**.
The eigenvalues solve $\lambda^2 - \operatorname{tr}(A)\lambda + \det(A) = 0$, i.e. $\lambda^2 + 0.7\lambda + 0.5 = 0$:

\[
\lambda = \frac{-0.7 \pm \sqrt{0.49 - 2.0}}{2} = -0.35 \pm 0.614\,i.
\]

The real part is $-0.35 < 0$ and the imaginary part is nonzero, so perturbations spiral inward: a **stable focus** (damped oscillations back to equilibrium).

## In code

We reproduce May's random-matrix experiment: the fraction of stable random communities as $\sigma\sqrt{SC}$ crosses 1.

### R

```r
set.seed(1)
frac_stable <- function(S, C, sigma, reps = 200) {
  ok <- 0
  for (k in 1:reps) {
    A <- matrix(rnorm(S * S, 0, sigma), S, S)
    A <- A * (matrix(runif(S * S), S, S) < C)  # connectance
    diag(A) <- -1                              # self-regulation
    if (max(Re(eigen(A, only.values = TRUE)$values)) < 0) ok <- ok + 1
  }
  ok / reps
}

S <- 50; C <- 0.3
for (sigma in c(0.15, 0.25, 0.35))            # sigma*sqrt(S*C) ~ 0.58, 0.97, 1.36
  cat(sigma, frac_stable(S, C, sigma), "\n")
# ~1.0 well below 1, ~0.5 near the threshold, ~0.0 above it
```

### Python

```python
import numpy as np
rng = np.random.default_rng(1)

def frac_stable(S, C, sigma, reps=200):
    ok = 0
    for _ in range(reps):
        A = rng.normal(0, sigma, (S, S)) * (rng.random((S, S)) < C)
        np.fill_diagonal(A, -1.0)
        if np.max(np.linalg.eigvals(A).real) < 0:
            ok += 1
    return ok / reps

S, C = 50, 0.3
for sigma in (0.15, 0.25, 0.35):     # sigma*sqrt(S*C) ~ 0.58, 0.97, 1.36
    print(sigma, frac_stable(S, C, sigma))
# ~1.0, ~0.5, ~0.0 : stability collapses past the threshold
```

<!-- python-output:auto -->
```text
0.15 1.0
0.25 0.83
0.35 0.0
```
<!-- /python-output:auto -->

### Julia

```julia
using LinearAlgebra, Random
Random.seed!(1)

function frac_stable(S, C, sigma; reps = 200)
    ok = 0
    for _ in 1:reps
        A = randn(S, S) .* sigma .* (rand(S, S) .< C)
        A[diagind(A)] .= -1.0
        maximum(real, eigvals(A)) < 0 && (ok += 1)
    end
    ok / reps
end

S, C = 50, 0.3
for sigma in (0.15, 0.25, 0.35)      # sigma*sqrt(S*C) ~ 0.58, 0.97, 1.36
    println(sigma, "  ", frac_stable(S, C, sigma))
end
# ~1.0, ~0.5, ~0.0 across the threshold
```

## Why it matters

The community matrix turns a tangle of species interactions into a tractable stability question, letting ecologists reason about food webs, mutualist networks, and disease-carrying host communities.
May's result reframed the diversity–stability debate and continues to guide questions about why real ecosystems are stable, how they respond to species loss, and where tipping points may lie.

## Related

- [Jacobians](jacobians.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Equilibria and Stability](equilibria-and-stability.md)
- [Lotka–Volterra Predator–Prey Dynamics](predator-prey.md)
- [Competition and Coexistence](competition-coexistence.md)
- [Networks in Ecology and Epidemiology](ecological-networks.md)
- [Quantitative Methods](../math.md)
