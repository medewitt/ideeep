---
title: "Factorial Designs"
---

# Factorial Designs

Factorial designs let you study several factors at once by testing every combination of their levels.
This is far more efficient than changing one factor at a time, and — crucially — it is the only way to detect **interactions**, where the effect of one factor depends on the level of another.

![Left: an interaction plot of the worked $2^2$ corner means — the response versus $A$ at low $B$ and at high $B$ are two non-parallel lines, and the gap between their slopes is the $AB$ interaction of $5$: the boost from $A$ is larger when $B$ is high. Right: the factorial design visits all four corners of the $(A,B)$ square, so the $(+,+)$ combination that reveals the interaction is measured, whereas a one-factor-at-a-time path never leaves the low level of the other factor and misses it.](../assets/figures/factorial-designs.svg "fig:factorial")

## Crossing factors: the $2^k$ design

Suppose we have $k$ factors, each set to a **low** ($-1$) and **high** ($+1$) level.
Crossing all levels gives $2^k$ treatment combinations (runs).
With $k=2$ factors $A$ and $B$ we get $2^2 = 4$ runs; with $k=3$ we get $8$, and so on.

Coding levels as $\pm 1$ makes the algebra clean and the columns orthogonal.

| Run | $A$ | $B$ | $AB$ |
|-----|-----|-----|------|
| 1   | $-1$ | $-1$ | $+1$ |
| 2   | $+1$ | $-1$ | $-1$ |
| 3   | $-1$ | $+1$ | $-1$ |
| 4   | $+1$ | $+1$ | $+1$ |

The interaction column $AB$ is the elementwise product of the $A$ and $B$ columns.

## Main effects and interactions

A **main effect** of a factor is the change in the average response as the factor goes from low to high.
An **interaction** measures how much the effect of one factor changes across the levels of another.

Why one-factor-at-a-time (OFAT) fails: if you vary $A$ while holding $B$ fixed, then vary $B$ while holding $A$ fixed, you never observe the $A$–$B$ combination that reveals synergy or antagonism ([@fig:factorial]).
Factorial designs cross the factors, so interactions become estimable.

### Effect = difference of averages

Using the $\pm 1$ coding, the effect of a factor is the average response at its high level minus the average at its low level:

\[
\text{Effect}(A) = \bar{y}_{A+} - \bar{y}_{A-}.
\]

Equivalently, each effect is a **contrast** — a weighted sum $\sum_i c_i \bar{y}_i$ with the sign column as weights, divided by the number of $+$ (or $-$) entries.

## Estimating effects via a linear model

Fit the regression

\[
y = \beta_0 + \beta_A x_A + \beta_B x_B + \beta_{AB}\, x_A x_B + \varepsilon,
\]

where $x_A, x_B \in \{-1, +1\}$.
Because the design columns are orthogonal, the least-squares coefficients are independent, and each **regression coefficient equals half the corresponding effect**:

\[
\beta_A = \tfrac{1}{2}\,\text{Effect}(A).
\]

## Worked $2^2$ example

Take the four corner means (average response at each combination):

\[
\begin{aligned}
y_{(-,-)} &= 20, & y_{(+,-)} &= 30, \\
y_{(-,+)} &= 25, & y_{(+,+)} &= 45.
\end{aligned}
\]

**Main effect of $A$** — average at $A+$ minus average at $A-$:

\[
\text{Effect}(A) = \frac{30 + 45}{2} - \frac{20 + 25}{2} = 37.5 - 22.5 = 15.
\]

**Main effect of $B$**:

\[
\text{Effect}(B) = \frac{25 + 45}{2} - \frac{20 + 30}{2} = 35 - 25 = 10.
\]

**Interaction $AB$** — use the $AB$ sign column $(+,-,-,+)$:

\[
\text{Effect}(AB) = \frac{y_{(-,-)} + y_{(+,+)}}{2} - \frac{y_{(+,-)} + y_{(-,+)}}{2}
= \frac{20 + 45}{2} - \frac{30 + 25}{2} = 32.5 - 27.5 = 5.
\]

So going high on $A$ adds about $15$ units, high on $B$ adds about $10$, and there is a modest positive interaction of $5$: the boost from $A$ is larger when $B$ is also high.
The fitted coefficients would be $\beta_A = 7.5$, $\beta_B = 5$, $\beta_{AB} = 2.5$.

## In code

### R

```r
set.seed(1)
# Full 2^2 factorial with 3 replicates per corner
d <- expand.grid(A = c(-1, 1), B = c(-1, 1))
d <- d[rep(1:4, each = 3), ]
# True model: intercept 28.75, A eff 15 (beta 7.5), B eff 10 (5), AB eff 5 (2.5)
d$y <- 28.75 + 7.5 * d$A + 5 * d$B + 2.5 * d$A * d$B + rnorm(nrow(d), 0, 2)

fit <- lm(y ~ A * B, data = d)
coef(fit)
# (Intercept)  A     B     A:B
#   ~28.7      ~7.4  ~5.0  ~2.6   (each = half the effect)
```

### Python

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from pyDOE3 import fullfact

np.random.seed(1)
# fullfact([2,2]) gives 0/1 levels; recode to -1/+1
levels = fullfact([2, 2]) * 2 - 1          # rows of (A, B) in {-1,+1}
d = pd.DataFrame(np.repeat(levels, 3, axis=0), columns=["A", "B"])
d["y"] = (28.75 + 7.5 * d.A + 5 * d.B + 2.5 * d.A * d.B
          + np.random.normal(0, 2, len(d)))

fit = smf.ols("y ~ A * B", data=d).fit()
print(fit.params)
# Intercept ~28.7, A ~7.4, B ~5.0, A:B ~2.6
```

### Julia

```julia
using DataFrames, GLM, Random
Random.seed!(1)

# Build the full 2^2 grid, 3 reps each
grid = [(a, b) for a in (-1, 1) for b in (-1, 1)]
d = DataFrame(A = Int[], B = Int[])
for (a, b) in grid, _ in 1:3
    push!(d, (a, b))
end
d.y = 28.75 .+ 7.5 .* d.A .+ 5 .* d.B .+ 2.5 .* d.A .* d.B .+ 2 .* randn(nrow(d))

fit = lm(@formula(y ~ A * B), d)
coef(fit)
# ≈ [28.7, 7.4, 5.0, 2.6]  (intercept, A, B, A&B)
```

## Why it matters for statistics

Factorial designs are the workhorse of planned experimentation.
They squeeze maximum information out of each run, estimate main effects and interactions with the same data, and keep effect estimates orthogonal (hence uncorrelated).
In fields from agronomy to clinical trials to industrial process [optimization](optimization.md), they answer "which factors matter, and do they act together?" efficiently — a question OFAT experiments simply cannot address.

## Related

- [Experimental Design](experimental-design.md)
- [Fractional Factorial Designs](fractional-factorial-designs.md)
- [Optimal Experimental Design](optimal-design.md)
- [Response Surface Methodology](response-surface.md)
- [Matrix Operations](matrix-operations.md)
- [Quantitative Methods](../math.md)
