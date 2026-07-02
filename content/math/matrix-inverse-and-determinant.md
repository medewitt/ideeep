---
title: "Inverse, Determinant, and Rank"
---

# Inverse, Determinant, and Rank

The determinant tells you whether a matrix can be "undone," the inverse does the undoing, and the rank counts how much independent information a matrix carries. Together they decide whether a regression has a unique solution — the normal equations $\hat\beta = (X^\top X)^{-1} X^\top y$ only work when $X^\top X$ is invertible.

## Determinant

For a $2 \times 2$ matrix the determinant has a simple formula:

\[
A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}, \qquad \det(A) = ad - bc.
\]

**Geometric meaning:** $|\det(A)|$ is the factor by which $A$ scales area (in 2-D) or volume (in 3-D). A determinant of $0$ means the transformation collapses space onto a lower-dimensional set — it destroys information and cannot be reversed.

## Inverse

The **inverse** $A^{-1}$ of a square matrix satisfies

\[
A A^{-1} = A^{-1} A = I.
\]

For a $2 \times 2$ matrix:

\[
A^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}.
\]

The inverse exists **if and only if** $\det(A) \neq 0$. Such a matrix is called *nonsingular* (or *invertible*); a matrix with $\det(A) = 0$ is *singular*.

## Rank and singularity

The **rank** of a matrix is the number of linearly independent rows (equivalently, columns). A square $n \times n$ matrix is **full rank** (rank $n$) exactly when it is invertible and $\det \neq 0$. If columns are linearly dependent — say one predictor is a copy or exact linear combination of others — the rank drops, the determinant is $0$, and no inverse exists.

## Worked example (by hand)

Let

\[
A = \begin{bmatrix} 4 & 7 \\ 2 & 6 \end{bmatrix}.
\]

Determinant:

\[
\det(A) = 4 \cdot 6 - 7 \cdot 2 = 24 - 14 = 10 \neq 0,
\]

so $A$ is invertible. The inverse:

\[
A^{-1} = \frac{1}{10} \begin{bmatrix} 6 & -7 \\ -2 & 4 \end{bmatrix}
= \begin{bmatrix} 0.6 & -0.7 \\ -0.2 & 0.4 \end{bmatrix}.
\]

Check:

\[
A A^{-1} = \begin{bmatrix} 4 & 7 \\ 2 & 6 \end{bmatrix}
\begin{bmatrix} 0.6 & -0.7 \\ -0.2 & 0.4 \end{bmatrix}
= \begin{bmatrix} 2.4 - 1.4 & -2.8 + 2.8 \\ 1.2 - 1.2 & -1.4 + 2.4 \end{bmatrix}
= \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}. \checkmark
\]

## The normal-equations connection

In linear regression with design matrix $X$ ($n \times p$) and response $y$, the least-squares estimates are

\[
\hat\beta = (X^\top X)^{-1} X^\top y.
\]

This requires $X^\top X$ (a $p \times p$ matrix) to be invertible, i.e. $X$ must have full column rank $p$. Perfect **multicollinearity** — a predictor that is an exact linear combination of others — makes $X^\top X$ singular and $\hat\beta$ undefined.

## Computing it

### R

```r
A <- matrix(c(4, 7, 2, 6), nrow = 2, byrow = TRUE)

det(A)          # 10
solve(A)        # inverse: [[0.6, -0.7], [-0.2, 0.4]]
qr(A)$rank      # 2 (full rank)

# Solve a linear system A x = b directly (preferred over solve(A) %*% b):
b <- c(1, 1)
solve(A, b)     # -> 0.1 0.1
```

### Python

```python
import numpy as np

A = np.array([[4.0, 7.0], [2.0, 6.0]])

np.linalg.det(A)          # 10.0 (up to floating point)
np.linalg.inv(A)          # [[0.6, -0.7], [-0.2, 0.4]]
np.linalg.matrix_rank(A)  # 2

# Prefer solving over explicit inverse for numerical stability:
np.linalg.solve(A, np.array([1.0, 1.0]))   # [0.1, 0.1]
```

### Julia

```julia
using LinearAlgebra

A = [4.0 7.0; 2.0 6.0]

det(A)      # 10.0
inv(A)      # [0.6 -0.7; -0.2 0.4]
rank(A)     # 2

# Backslash solves A x = b (preferred over inv):
A \ [1.0, 1.0]   # [0.1, 0.1]
```

## Why it matters for statistics

Invertibility is the dividing line between a regression that has a unique answer and one that does not. A near-singular $X^\top X$ (large but nonzero determinant issues, tiny [eigenvalues](eigenvalues-and-eigenvectors.md)) signals collinearity that inflates coefficient [variances](measures-of-variability.md). In practice, use `solve`/`\` rather than forming an explicit inverse — it is faster and numerically more stable.

## Related

- [Matrix and Vector Notation](matrix-notation.md)
- [Matrix Operations](matrix-operations.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Jacobians](jacobians.md)
- [Quantitative Methods](../math.md)
