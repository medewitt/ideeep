---
title: "Structured Population Models"
---

# Structured Population Models

A newborn, a juvenile, and a reproductive adult contribute very differently to a population's future, so treating everyone as identical throws away essential biology.
Structured models track these classes explicitly, and their long-run behavior is governed entirely by the eigenvalues and eigenvectors of a projection matrix — the same linear-algebra machinery behind next-generation matrices in disease ecology.

![Left: starting from an all-juvenile population, the stage proportions converge after transients decay to the stable stage distribution — about 63% juveniles, 29% subadults, and 8% adults — set by the dominant right eigenvector. Right: total population size then grows geometrically at the dominant eigenvalue $\lambda \approx 1.090$, so on a log scale it straightens into a line of slope $\ln\lambda$.](../assets/figures/structured-populations.svg "fig:structured")

## Projecting an age- or stage-structured population

When survival and fecundity depend on age or developmental stage, we split the population into classes and record their counts in a vector $\mathbf{n}_t$.
A **projection matrix** $L$ advances the population one time step, $$\mathbf{n}_{t+1}=L\,\mathbf{n}_t,$$ using the [matrix notation](matrix-notation.md) of a matrix acting on a vector.
For age classes this is a **Leslie matrix**; for stages (where individuals can remain in a class) it is a **Lefkovitch matrix**.

The structure of $L$ encodes the life cycle:

- the **top row** holds fecundities $F_i$ — offspring produced per individual of class $i$,
- the **sub-diagonal** holds survival probabilities $P_i$ — the fraction of class $i$ surviving and advancing to class $i+1$,
- a Lefkovitch matrix may add **diagonal** entries for individuals that survive but stay in the same stage.

Iterating $\mathbf{n}_{t+1}=L\mathbf{n}_t$ is a discrete-time projection, closely related to repeated [matrix multiplication](matrix-operations.md) since $\mathbf{n}_t=L^t\mathbf{n}_0$.

## Long-run growth and structure

After transients decay, the population settles into steady exponential growth at a fixed rate multiplied each step, and its composition stops changing ([@fig:structured]).
Both facts fall out of the [eigenvalues and eigenvectors](eigenvalues-and-eigenvectors.md) of $L$:

- The **dominant eigenvalue** $\lambda$ (largest in magnitude) is the asymptotic per-step growth rate — the discrete analogue of $e^r$.
  $\lambda>1$ means growth, $\lambda<1$ decline, $\lambda=1$ a stationary population.
- The **right eigenvector** for $\lambda$, solving $L\mathbf{w}=\lambda\mathbf{w}$, gives the **stable stage distribution** — the proportions in each class once structure equilibrates.
- The **left eigenvector**, solving $\mathbf{v}L=\lambda\mathbf{v}$, gives **reproductive value** — the relative expected lifetime contribution of each class to future generations.

The Perron–Frobenius theorem guarantees that a well-behaved (nonnegative, irreducible) projection matrix has a real, positive dominant eigenvalue with a nonnegative eigenvector, so these quantities are biologically meaningful.

## A worked example

Consider three stages — juveniles, subadults, adults — with the Leslie matrix $$L=\begin{pmatrix} 0 & 1 & 5 \\ 0.5 & 0 & 0 \\ 0 & 0.3 & 0 \end{pmatrix}.$$ Only adults and subadults reproduce (fecundities $1$ and $5$); half of juveniles survive to become subadults ($P_1=0.5$) and $30\%$ of subadults become adults ($P_2=0.3$).

The characteristic equation $\det(L-\lambda I)=0$ expands to $$\lambda^3-0.5\lambda-0.75=0.$$ Solving numerically gives the dominant eigenvalue $\lambda\approx 1.090$, so the population grows about $9\%$ per time step.
The corresponding right eigenvector (before normalizing) is $$\mathbf{w}\propto\left(1,\ \frac{0.5}{\lambda},\ \frac{0.3\cdot 0.5}{\lambda^2}\right)\approx(1,\ 0.459,\ 0.126).$$ Dividing by the sum $1.585$ gives the **stable stage distribution** $\approx(0.631,\ 0.289,\ 0.080)$: at steady state about $63\%$ juveniles, $29\%$ subadults, and $8\%$ adults.

## In code

We build $L$, extract the dominant eigenvalue, and normalize its eigenvector to get the stable stage distribution.

### R

```r
L <- matrix(c(0,   1,   5,
              0.5, 0,   0,
              0,   0.3, 0), nrow = 3, byrow = TRUE)

e <- eigen(L)
i <- which.max(Re(e$values))       # dominant eigenvalue index
lambda <- Re(e$values[i])
w <- Re(e$vectors[, i]); w <- w / sum(w)
lambda   # ~1.090  (per-step growth rate)
w        # ~c(0.631, 0.289, 0.080) stable stage distribution
```

### Python

```python
import numpy as np

L = np.array([[0.0, 1.0, 5.0],
              [0.5, 0.0, 0.0],
              [0.0, 0.3, 0.0]])

vals, vecs = np.linalg.eig(L)
i = np.argmax(vals.real)               # dominant eigenvalue
lam = vals[i].real
w = np.abs(vecs[:, i].real); w /= w.sum()
print(lam)   # ~1.090
print(w)     # ~[0.631, 0.289, 0.080]
```

<!-- python-output:auto -->
```text
1.0899905360790787
[0.63092527 0.28941777 0.07965696]
```
<!-- /python-output:auto -->

### Julia

```julia
using LinearAlgebra

L = [0.0 1.0 5.0;
     0.5 0.0 0.0;
     0.0 0.3 0.0]

vals, vecs = eigen(L)
i = argmax(real.(vals))                 # dominant eigenvalue
lambda = real(vals[i])
w = abs.(real.(vecs[:, i])); w ./= sum(w)
lambda   # ~1.090
w        # ~[0.631, 0.289, 0.080]
```

## Why it matters

Structured models turn detailed life-history data — stage-specific survival and fecundity — into a single number, the growth rate $\lambda$, plus the population composition and the relative worth of each stage, all read directly off an eigen-decomposition.
The same matrix-eigenvalue logic underlies the next-generation matrix that yields $R_0$ in epidemiology, so mastering Leslie and Lefkovitch matrices pays off across both population and disease ecology.

## Related

- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Matrix Operations](matrix-operations.md)
- [Matrix Notation](matrix-notation.md)
- [The Next-Generation Matrix](next-generation-matrix.md)
- [Reproductive Value and Demographic Sensitivity](reproductive-value.md) — how the left eigenvector weights each stage and how sensitivities read off the projection matrix
- [Quantitative Methods](../math.md)
