---
title: "Matrix Operations"
---

# Matrix Operations

Matrix arithmetic is how statistical models are actually computed: fitting a regression, propagating a covariance, or stepping a dynamical system all reduce to a few matrix operations. The one rule that trips everyone up is that **matrix multiplication is not element-wise and is not commutative**.

## Addition, subtraction, and scalar multiplication

Addition and subtraction act **element-wise** and require identical dimensions:

\[
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
+
\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}
=
\begin{bmatrix} 6 & 8 \\ 10 & 12 \end{bmatrix}.
\]

Scalar multiplication scales every entry: $2A$ multiplies each $a_{ij}$ by $2$.

## Element-wise (Hadamard) vs matrix multiplication

The **Hadamard product** $A \circ B$ multiplies corresponding entries and needs identical dimensions:

\[
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
\circ
\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}
=
\begin{bmatrix} 5 & 12 \\ 21 & 32 \end{bmatrix}.
\]

**Matrix multiplication** $AB$ is different. It requires **conformability**: an $(m \times n)$ matrix times an $(n \times p)$ matrix yields an $(m \times p)$ matrix. The $(i,j)$ entry is the dot product of row $i$ of $A$ with column $j$ of $B$:

\[
(AB)_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}.
\]

## Transpose

The transpose $A^\top$ flips rows and columns: $(A^\top)_{ij} = a_{ji}$. Useful properties:

\[
(A^\top)^\top = A, \qquad (A + B)^\top = A^\top + B^\top, \qquad (AB)^\top = B^\top A^\top.
\]

Note the order reversal in the last identity.

## Worked example (by hand)

Let

\[
A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \ (2 \times 3),
\qquad
B = \begin{bmatrix} 7 & 8 \\ 9 & 10 \\ 11 & 12 \end{bmatrix} \ (3 \times 2).
\]

Since $A$ is $2 \times 3$ and $B$ is $3 \times 2$, $AB$ is $2 \times 2$. Compute each entry:

\[
\begin{aligned}
(AB)_{11} &= 1\cdot7 + 2\cdot9 + 3\cdot11 = 7 + 18 + 33 = 58, \\
(AB)_{12} &= 1\cdot8 + 2\cdot10 + 3\cdot12 = 8 + 20 + 36 = 64, \\
(AB)_{21} &= 4\cdot7 + 5\cdot9 + 6\cdot11 = 28 + 45 + 66 = 139, \\
(AB)_{22} &= 4\cdot8 + 5\cdot10 + 6\cdot12 = 32 + 50 + 72 = 154.
\end{aligned}
\]

So

\[
AB = \begin{bmatrix} 58 & 64 \\ 139 & 154 \end{bmatrix}.
\]

**Not commutative:** $BA$ here is $3 \times 3$, a completely different object. Even for square matrices, $AB \neq BA$ in general.

## Computing it

### R

```r
A <- matrix(c(1, 2, 3, 4, 5, 6), nrow = 2, byrow = TRUE)   # 2 x 3
B <- matrix(c(7, 8, 9, 10, 11, 12), nrow = 3, byrow = TRUE) # 3 x 2

A %*% B     # matrix multiplication -> [[58, 64], [139, 154]]
t(A)        # transpose -> 3 x 2

# Element-wise multiplication needs equal dimensions:
C <- matrix(1:4, 2, 2); D <- matrix(5:8, 2, 2)
C * D       # Hadamard product, NOT matrix mult
C %*% D     # matrix multiplication (different result)
```

### Python

```python
import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6]])         # 2 x 3
B = np.array([[7, 8], [9, 10], [11, 12]])    # 3 x 2

A @ B        # matrix multiplication -> [[58, 64], [139, 154]]
A.T          # transpose -> 3 x 2

C = np.array([[1, 2], [3, 4]]); D = np.array([[5, 6], [7, 8]])
C * D        # element-wise -> [[5, 12], [21, 32]]
C @ D        # matrix multiplication -> [[19, 22], [43, 50]]
```

### Julia

```julia
using LinearAlgebra

A = [1 2 3; 4 5 6]          # 2 x 3
B = [7 8; 9 10; 11 12]      # 3 x 2

A * B        # matrix multiplication -> [58 64; 139 154]
A'           # transpose (adjoint) -> 3 x 2

C = [1 2; 3 4]; D = [5 6; 7 8]
C .* D       # element-wise -> [5 12; 21 32]
C * D        # matrix multiplication -> [19 22; 43 50]
```

## Why it matters for statistics

The least-squares fit $\hat\beta = (X^\top X)^{-1} X^\top y$ is built entirely from transpose and matrix multiplication; the cross-product $X^\top X$ collapses an $n \times p$ dataset into a $p \times p$ summary. Confusing `*` (element-wise) with matrix multiplication is a classic source of silently wrong results, so keep the operators straight.

## Related

- [Matrix and Vector Notation](matrix-notation.md)
- [Inverse, Determinant, and Rank](matrix-inverse-and-determinant.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Jacobians](jacobians.md)
- [Quantitative Methods](../math.md)
