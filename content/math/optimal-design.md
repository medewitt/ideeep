---
title: "Optimal Experimental Design"
---

# Optimal Experimental Design

When the design region is constrained or irregular — so classical factorials and central composite designs don't fit — **optimal design** picks run locations to make a model's parameter estimates as precise as possible.
It is model-based: you specify the model, then choose points that [optimize](optimization.md) a criterion on the information [matrix](matrix-operations.md).

## The information matrix

For a linear model $y = X\beta + \varepsilon$ with $\varepsilon \sim (0, \sigma^2 I)$, the least-squares estimator has [covariance](measures-of-variability.md)

\[
\operatorname{Var}(\hat\beta) = \sigma^2 (X^\top X)^{-1}.
\]

The matrix $X^\top X$ is the **information matrix**: larger information means smaller variance.
Optimal design chooses the rows of the model matrix $X$ (the runs) to make $X^\top X$ "big" in a chosen sense.
These criteria are named by letters — hence "alphabetic" optimality.

## Alphabetic optimality criteria

- **D-optimality** — maximize $\det(X^\top X)$.
  This minimizes the volume of the joint confidence ellipsoid for $\beta$, since that volume is proportional to $\det(X^\top X)^{-1/2}$.
  The most widely used criterion.
- **A-optimality** — minimize $\operatorname{tr}\big((X^\top X)^{-1}\big)$, the sum (average) of the parameter variances.
- **I-optimality** (a.k.a.
  IV) — minimize the *average* prediction variance over the design region.
- **G-optimality** — minimize the *maximum* prediction variance over the region.

The prediction variance at a point $x_0$ is $\sigma^2\, x_0^\top (X^\top X)^{-1} x_0$, which links the I/G criteria to $(X^\top X)^{-1}$.

## Exchange algorithms

For all but tiny problems, searching over subsets of a candidate set is combinatorial.
**Exchange algorithms** — the classic one is **Fedorov's** — start from an initial design and repeatedly swap a design point for a candidate point whenever the swap improves the criterion (e.g. increases $\det(X^\top X)$), stopping at a local optimum.
Modified Fedorov and coordinate-exchange variants scale this to many candidates.

## Worked example: endpoints are D-optimal for a line

Fit a straight line $y = \beta_0 + \beta_1 x$ on the region $x \in [-1, 1]$ with two runs at $\pm d$ (with $0 < d \le 1$).
The model matrix and information matrix are

\[
X = \begin{bmatrix} 1 & -d \\ 1 & \phantom{-}d \end{bmatrix},
\qquad
X^\top X = \begin{bmatrix} 2 & 0 \\ 0 & 2d^2 \end{bmatrix}.
\]

Then

\[
\det(X^\top X) = 2 \cdot 2d^2 = 4d^2,
\]

which increases in $d$ and is maximized at $d = 1$.
Compare two candidate designs:

- **Endpoints** $x = \{-1, +1\}$: $\det(X^\top X) = 4(1)^2 = 4$.
- **Interior points** $x = \{-0.5, +0.5\}$: $\det(X^\top X) = 4(0.5)^2 = 1$.

The endpoint design has four times the [determinant](matrix-inverse-and-determinant.md), so it estimates the slope far more precisely — spreading points as far apart as the region allows is D-optimal for a line.

## In code

### R

```r
library(AlgDesign)
set.seed(1)
# Candidate set on [-1, 1]; find best 2-point D-optimal design for a line
cand <- data.frame(x = seq(-1, 1, by = 0.1))
res <- optFederov(~ x, data = cand, nTrials = 2, criterion = "D")
res$design
#     x
#   -1
#    1        <- endpoints, as expected
```

### Python

```python
import numpy as np
from itertools import combinations

# Candidate points on [-1, 1]; greedily/exhaustively maximize det(X'X)
cand = np.linspace(-1, 1, 21)
best_det, best = -np.inf, None
for combo in combinations(range(len(cand)), 2):
    x = cand[list(combo)]
    X = np.column_stack([np.ones_like(x), x])   # model: 1, x
    d = np.linalg.det(X.T @ X)
    if d > best_det:
        best_det, best = d, x
print(best, best_det)
# [-1.  1.] 4.0   -> endpoints are D-optimal
```

<!-- python-output:auto -->
```text
[-1.  1.] 4.0
```
<!-- /python-output:auto -->

### Julia

```julia
using LinearAlgebra, Combinatorics

cand = collect(range(-1, 1, length = 21))
best_det, best = -Inf, Float64[]
for combo in combinations(1:length(cand), 2)
    x = cand[combo]
    X = hcat(ones(length(x)), x)        # model matrix: [1  x]
    d = det(X' * X)
    if d > best_det
        best_det, best = d, x
    end
end
println(best, "  det = ", best_det)
# [-1.0, 1.0]  det = 4.0   -> endpoints
```

## Why it matters for statistics

Real experiments rarely live on a tidy cube: budgets cap runs, some factor combinations are infeasible, and the region can be an odd polytope.
Optimal design gives a principled, criterion-driven way to place runs anywhere in such regions, tailored to the model you intend to fit.
It also unifies classical designs — for many standard settings the D-optimal design *is* the familiar factorial — and quantifies exactly what "precise estimation" means through $X^\top X$.

## Related

- [Matrix Inverse and Determinant](matrix-inverse-and-determinant.md)
- [Optimization](optimization.md)
- [Factorial Designs](factorial-designs.md)
- [Response Surface Methodology](response-surface.md)
- [Experimental Design](experimental-design.md)
- [Quantitative Methods](../math.md)
