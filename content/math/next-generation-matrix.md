---
title: "The Next-Generation Matrix and R₀"
---

# The Next-Generation Matrix and R₀

The basic reproduction number $R_0$ decides whether a pathogen invades, but for anything more structured than a textbook SIR model — multiple host types, stages, or transmission routes — the naive "$\beta$ over $\gamma$" recipe breaks down.
The next-generation matrix gives a rigorous, general way to compute $R_0$ as the dominant eigenvalue of a matrix built from the infection dynamics.

## The idea

$R_0$ is the expected number of secondary cases produced by one typical infected individual in a fully susceptible population.
In a structured model there are several kinds of infected individuals — say infants and adults, or exposed and infectious classes — and one infected of type $j$ produces a mixture of new infections across all types.
We therefore need a **matrix** that bookkeeps "new infections in group $i$ caused by an infected in group $j$," and $R_0$ becomes a summary of that matrix rather than a single ratio.

## Construction

Work with the infected compartments only (for SIR-type models these are the $E$, $I$, and similar classes; $S$ and $R$ are excluded).
Linearize their dynamics about the **disease-free equilibrium** (DFE), and split the linearized system into two parts:

- $\mathcal{F}$ — the rate of appearance of **new infections**, and
- $\mathcal{V}$ — the rate of all **other transitions** out of and between infected compartments (recovery, death, progression, waning).

Let $F$ and $V$ be the Jacobian matrices of $\mathcal{F}$ and $\mathcal{V}$ with respect to the infected variables, both evaluated at the DFE.
The **next-generation matrix** is $$K = F V^{-1},$$ and the basic reproduction number is its **spectral radius** (largest-magnitude eigenvalue), $$R_0 = \rho(K) = \rho\!\left(F V^{-1}\right).$$ Here $V^{-1}$ requires the [matrix inverse and determinant](matrix-inverse-and-determinant.md), and $\rho$ is found from an [eigenvalue](eigenvalues-and-eigenvectors.md) decomposition.

### Interpretation

The pieces have a clean meaning.
$V^{-1}$ is the matrix of expected times spent in each infected state: entry $(V^{-1})_{jk}$ is the expected time an individual who starts in state $k$ spends in state $j$ before leaving the infected classes.
Multiplying by $F$, which converts time-in-state into new infections, gives $$K_{ij} = \text{expected number of new infections in group } i \text{ produced by one infected introduced into group } j.$$ Because the total reproduction over generations is governed by repeated multiplication by $K$, the long-run per-generation growth factor is the dominant eigenvalue $\rho(K)$, and the epidemic can invade the DFE if and only if $R_0 > 1$.
This is the [stability](equilibria-and-stability.md) threshold of the disease-free equilibrium, restated as a spectral radius.

## Worked example 1: simple SIR

For the [SIR model](sir.md) the only infected compartment is $I$, with $$\frac{dI}{dt} = \beta \frac{S}{N} I - \gamma I.$$ New infections appear at rate $\mathcal{F} = \beta \frac{S}{N} I$ and transitions (recovery) remove them at rate $\mathcal{V} = \gamma I$.
At the disease-free equilibrium $S = N$, so the $1\times 1$ Jacobians are $$F = \beta, \qquad V = \gamma.$$ Then $K = F V^{-1} = \beta/\gamma$ and, since a $1\times 1$ matrix is its own eigenvalue, $$R_0 = \rho(K) = \frac{\beta}{\gamma},$$ recovering the familiar result.

## Worked example 2: a two-type model

Suppose infection spreads in two host groups (say children and adults) that mix, and an infected in group $j$ transmits to group $i$ at rate $\beta_{ij}$, while every infected recovers at rate $\gamma$.
Then $$F = \begin{bmatrix} \beta_{11} & \beta_{12} \\ \beta_{21} & \beta_{22} \end{bmatrix}, \qquad V = \begin{bmatrix} \gamma & 0 \\ 0 & \gamma \end{bmatrix} = \gamma I_2,$$ so $V^{-1} = \frac{1}{\gamma} I_2$ and $$K = F V^{-1} = \frac{1}{\gamma}\begin{bmatrix} \beta_{11} & \beta_{12} \\ \beta_{21} & \beta_{22} \end{bmatrix}.$$ $R_0$ is the spectral radius of this matrix.
Take $\beta_{11} = 2,\ \beta_{12} = 1,\ \beta_{21} = 1,\ \beta_{22} = 1$ (per unit time) and $\gamma = 1$.
The eigenvalues of $K$ solve $\lambda^2 - (\operatorname{tr}K)\lambda + \det K = 0$, i.e. $\lambda^2 - 3\lambda + 1 = 0$, giving $$\lambda = \frac{3 \pm \sqrt{5}}{2} \approx 2.618,\ 0.382.$$ So $R_0 = \rho(K) \approx 2.62$, larger than any single group's own $\beta_{ii}/\gamma$ because cross-group transmission amplifies spread.

## In code

We build $F$ and $V$, form $K = FV^{-1}$, and take the spectral radius from an eigen-decomposition.

### R

```r
gamma <- 1
F <- matrix(c(2, 1,
              1, 1), nrow = 2, byrow = TRUE)
V <- gamma * diag(2)

K <- F %*% solve(V)
R0 <- max(abs(eigen(K)$values))
R0                       # ~2.618 = (3 + sqrt(5)) / 2
```

### Python

```python
import numpy as np

gamma = 1.0
F = np.array([[2., 1.],
              [1., 1.]])
V = gamma * np.eye(2)

K = F @ np.linalg.inv(V)
R0 = max(abs(np.linalg.eigvals(K)))
print(R0)               # ~2.618, the spectral radius of F V^{-1}
```

### Julia

```julia
using LinearAlgebra

γ = 1.0
F = [2.0 1.0;
     1.0 1.0]
V = γ * I(2)

K = F * inv(Matrix(V))
R0 = maximum(abs.(eigvals(K)))
println(R0)             # ~2.618 = (3 + √5)/2
```

## Why it matters

The next-generation matrix is the standard tool for computing $R_0$ in any structured epidemic model — age groups, spatial patches, vector-borne cycles, or staged infections like SEIR.
It turns the vague notion of "average secondary cases" into a precise spectral quantity whose value above or below $1$ decides invasion, and its dominant eigenvector tells you which mix of host types the epidemic will settle into.
Because $R_0 = \rho(FV^{-1})$ crosses $1$ exactly when the disease-free equilibrium loses stability, it is also the parameter that drives the transcritical [bifurcation](bifurcations.md) between elimination and endemicity.

## Related

- [Compartmental Models (SIR)](sir.md)
- [Jacobians](jacobians.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Inverse, Determinant, and Rank](matrix-inverse-and-determinant.md)
- [Equilibria and Linear Stability](equilibria-and-stability.md)
- [Networks in Ecology and Epidemiology](ecological-networks.md)
- [Branching Processes](branching-processes.md)
- [Quantitative Methods](../math.md)
