---
title: "Eigenvalues and Eigenvectors"
---

# Eigenvalues and Eigenvectors

An eigenvector of a matrix is a direction that the matrix merely stretches or shrinks without rotating; the eigenvalue is the stretch factor.
These special directions govern the stability of disease models (via the Jacobian) and the axes of variation in PCA, making them one of the most useful tools in applied statistics.

## Definition

A nonzero vector $v$ is an **eigenvector** of a square matrix $A$ with **eigenvalue** $\lambda$ if

\[
A v = \lambda v.
\]

Applying $A$ to $v$ points along the same line — orientation is unchanged (or flipped if $\lambda < 0$), and the length scales by $\lambda$.

## Characteristic equation

Rearranging, $(A - \lambda I)v = 0$.
A nonzero $v$ exists only when $A - \lambda I$ is singular, giving the **characteristic equation**:

\[
\det(A - \lambda I) = 0.
\]

For a $2 \times 2$ matrix this is a quadratic in $\lambda$, so there are (up to) two eigenvalues; they may be real or complex conjugates.

## Worked example (by hand)

Let

\[
A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}.
\]

Form $A - \lambda I$ and take its [determinant](matrix-inverse-and-determinant.md):

\[
\det\!\begin{bmatrix} 2 - \lambda & 1 \\ 1 & 2 - \lambda \end{bmatrix}
= (2 - \lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = (\lambda - 1)(\lambda - 3) = 0.
\]

So $\lambda_1 = 3$ and $\lambda_2 = 1$.

**Eigenvector for $\lambda_1 = 3$:** solve $(A - 3I)v = 0$: \[ \begin{bmatrix} -1 & 1 \\ 1 & -1 \end{bmatrix} v = 0 \ \Rightarrow\ v_1 = v_2, \quad v^{(1)} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}. \]

**Eigenvector for $\lambda_2 = 1$:** solve $(A - I)v = 0$: \[ \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix} v = 0 \ \Rightarrow\ v_1 = -v_2, \quad v^{(2)} = \begin{bmatrix} 1 \\ -1 \end{bmatrix}. \]

Check: $A \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 3 \\ 3 \end{bmatrix} = 3\begin{bmatrix} 1 \\ 1 \end{bmatrix}$.
$\checkmark$

## Stability of dynamical systems

For a system of ODEs, linearize near an equilibrium using the [Jacobian](jacobians.md) matrix $J$ evaluated at that point.
The eigenvalues of $J$ determine **local stability**:

- If **every** eigenvalue has **negative real part**, the equilibrium is locally stable (perturbations decay).
- If **any** eigenvalue has **positive real part**, it is unstable (perturbations grow).
- Complex eigenvalues indicate oscillatory approach or departure.

In epidemiology, evaluating $J$ at the **disease-free equilibrium** and checking the eigenvalues is equivalent to the threshold condition on the basic reproduction number: the disease-free state is stable when $R_0 < 1$ and unstable (an outbreak grows) when $R_0 > 1$.
The dominant eigenvalue crossing zero corresponds to $R_0$ crossing $1$.

## PCA connection

In principal component analysis, the eigenvectors of the sample **[covariance](measures-of-variability.md) matrix** are the principal component directions, and each eigenvalue is the variance captured along that direction.
The largest eigenvalue points along the axis of greatest spread in the data — the covariance matrix is symmetric, so its eigenvalues are real and its eigenvectors orthogonal.

## Computing it

### R

```r
A <- matrix(c(2, 1, 1, 2), nrow = 2, byrow = TRUE)

e <- eigen(A)
e$values      # 3 1
e$vectors     # columns are eigenvectors (normalized to unit length)
```

### Python

```python
import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])

vals, vecs = np.linalg.eig(A)
vals    # array([3., 1.])
vecs    # columns are unit eigenvectors
# For symmetric matrices, np.linalg.eigh is more accurate.
```

### Julia

```julia
using LinearAlgebra

A = [2.0 1.0; 1.0 2.0]

eigvals(A)        # [1.0, 3.0]  (ascending order)
F = eigen(A)
F.values          # [1.0, 3.0]
F.vectors         # columns are unit eigenvectors
```

## Why it matters for statistics

Eigen-decomposition underpins PCA, factor analysis, and the diagnosis of multicollinearity (a near-zero eigenvalue of $X^\top X$ flags an ill-conditioned design).
In dynamical epidemiological models, eigenvalues of the Jacobian give a precise, computable stability criterion that mirrors the $R_0$ threshold — turning intuition about outbreaks into linear algebra.

## Related

- [Matrix and Vector Notation](matrix-notation.md)
- [Matrix Operations](matrix-operations.md)
- [Inverse, Determinant, and Rank](matrix-inverse-and-determinant.md)
- [Jacobians](jacobians.md)
- [Population Stratification and PCA Control](population-stratification.md)
- [Centrality and Node Importance](centrality.md)
- [Quantitative Methods](../math.md)
