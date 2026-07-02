---
title: "Matrix and Vector Notation"
---

# Matrix and Vector Notation

Matrices and vectors are the language for organizing data and the parameters of statistical models. A regression dataset, a [covariance](measures-of-variability.md) structure, or a disease-model state are all naturally written as arrays of numbers, and a shared notation keeps the bookkeeping honest.

## Scalars, vectors, and matrices

A **scalar** is a single number, written in lowercase italics: $a = 3$.

A **vector** is an ordered list of numbers. By convention a vector is a *column vector* (a single column):

\[
x = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}.
\]

Its [transpose](matrix-operations.md) is a *row vector* $x^\top = \begin{bmatrix} x_1 & x_2 & x_3 \end{bmatrix}$.

A **matrix** is a rectangular array of numbers with $m$ rows and $n$ columns; we say it has **dimension** $m \times n$:

\[
A = \begin{bmatrix} a_{11} & a_{12} & a_{13} \\ a_{21} & a_{22} & a_{23} \end{bmatrix}
\quad (2 \times 3).
\]

## Indexing

The entry in row $i$ and column $j$ is $a_{ij}$ (row first, then column). For the matrix above, $a_{23}$ is the number in the second row, third column. A vector entry $x_i$ uses a single index.

## Special matrices

- **Identity** $I_n$: square, $1$s on the diagonal and $0$s elsewhere. It is the multiplicative identity: $AI = IA = A$.
\[
I_3 = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}.
\]
- **Zero matrix** $0$: every entry is $0$.
- **Diagonal** matrix: nonzero entries only on the diagonal, $a_{ij} = 0$ for $i \neq j$.
- **Symmetric** matrix: square with $A = A^\top$, i.e. $a_{ij} = a_{ji}$. Covariance matrices are symmetric.

## Conformability

Operations only make sense when dimensions match. Addition requires two matrices of *identical* dimension. Matrix multiplication $AB$ requires the number of columns of $A$ to equal the number of rows of $B$: an $(m \times n)$ times an $(n \times p)$ gives an $(m \times p)$ result. Checking conformability first is the quickest way to catch mistakes.

## Statistical motivation: the data matrix

The canonical object in statistics is the **data matrix** $X$ with $n$ observations (rows) and $p$ variables (columns):

\[
X = \begin{bmatrix}
x_{11} & x_{12} & \cdots & x_{1p} \\
x_{21} & x_{22} & \cdots & x_{2p} \\
\vdots & \vdots & \ddots & \vdots \\
x_{n1} & x_{n2} & \cdots & x_{np}
\end{bmatrix}
\quad (n \times p).
\]

Row $i$ is one subject; column $j$ is one measured variable. Nearly every model — linear regression, PCA, generalized linear models — begins by writing the data this way.

## Computing it

### R

```r
# Column vector and matrix (R fills column-by-column by default)
x <- c(1, 2, 3)
A <- matrix(c(1, 2, 3, 4, 5, 6), nrow = 2, byrow = TRUE)
A          # 2 x 3 matrix, rows: (1 2 3) and (4 5 6)
dim(A)     # 2 3
A[2, 3]    # 6  (row 2, col 3)
diag(3)    # 3x3 identity matrix
```

### Python

```python
import numpy as np

x = np.array([1, 2, 3])                 # 1-D array
A = np.array([[1, 2, 3], [4, 5, 6]])    # 2 x 3
A.shape      # (2, 3)
A[1, 2]      # 6  (0-based: row index 1, col index 2)
np.eye(3)    # 3x3 identity
```

### Julia

```julia
using LinearAlgebra

x = [1, 2, 3]                    # column vector
A = [1 2 3; 4 5 6]              # 2 x 3
size(A)      # (2, 3)
A[2, 3]      # 6  (1-based indexing)
I(3)         # 3x3 identity (UniformScaling as a matrix)
```

## Why it matters for statistics

Clear notation is the foundation for everything downstream: the design matrix in regression, the covariance matrix, and the [Jacobian](jacobians.md) of a disease model are all matrices. Knowing dimensions and conformability lets you predict whether an expression like $X^\top X$ is even defined (it is: $(p \times n)(n \times p) = p \times p$) before you compute anything.

## Related

- [Matrix Operations](matrix-operations.md)
- [Inverse, Determinant, and Rank](matrix-inverse-and-determinant.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Jacobians](jacobians.md)
- [Quantitative Methods](../math.md)
