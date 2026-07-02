---
title: "The Legendre Transform"
---

# The Legendre Transform

The Legendre transform re-expresses a convex function in terms of its slopes
instead of its inputs. It is the mathematical engine behind exponential
families, cumulant generating functions, and large-deviations rate functions —
places where "the dual variable is a slope."

## Definition

The Legendre–Fenchel transform (convex conjugate) of a function $f$ is
\[
f^*(p) = \sup_{x}\, \big(px - f(x)\big).
\]
For each slope $p$, we tilt $f$ by the line $px$ and record the largest vertical
gap between that line and the curve.

### Geometric intuition

Fix a slope $p$. The line $y = px - c$ supports $f$ from below when $c$ is as
large as possible while still $px - c \le f(x)$ for all $x$, i.e.
$c = \sup_x(px - f(x)) = f^*(p)$. So $f^*(p)$ is **minus the intercept** of the
supporting line of slope $p$. The transform stores a convex curve as the family
of its tangent lines, indexed by slope.

### Key facts

- **$f^*$ is always convex**, being a supremum of the affine functions
  $p \mapsto px - f(x)$, one for each $x$.
- **Stationarity.** If $f$ is differentiable, the sup is attained where
  $\frac{d}{dx}(px - f(x)) = 0$, i.e. at the $x$ with
  \[
  p = f'(x), \qquad\text{and then}\qquad f^*(p) = p x - f(x).
  \]
  The conjugate variable $p$ is the slope of $f$.
- **Involution.** For a (closed) convex $f$, applying the transform twice
  returns the original: $f^{**} = f$. For non-convex $f$, $f^{**}$ is its convex
  hull (the largest convex function below it).
- **Fenchel–Young inequality.** Directly from the definition,
  $f(x) + f^*(p) \ge px$ for all $x, p$, with equality iff $p = f'(x)$. This is
  the general form of Young's inequality.

## Worked examples

**Quadratic.** Let $f(x) = \tfrac12 x^2$. Then $f'(x) = x$, so $p = x$ and
\[
f^*(p) = p\cdot p - \tfrac12 p^2 = \tfrac12 p^2 .
\]
The Gaussian's energy is self-dual. More generally, for $f(x)=\tfrac12 a x^2$
with $a>0$, stationarity gives $x = p/a$ and $f^*(p) = \tfrac{p^2}{2a}$ — larger
curvature $a$ gives a flatter conjugate.

**Exponential.** Let $f(x) = e^x$. Then $p = f'(x) = e^x$, so $x = \ln p$ (valid
for $p>0$) and
\[
f^*(p) = p\ln p - e^{\ln p} = p\ln p - p, \qquad p > 0,
\]
with $f^*(p) = +\infty$ for $p<0$ and $f^*(0)=0$. This $p\ln p - p$ is the
entropy-like function appearing in Poisson large deviations.

**Power law (Young's inequality).** For $f(x) = \tfrac{1}{r}|x|^{r}$ with $r>1$,
the conjugate is $f^*(p) = \tfrac{1}{s}|p|^{s}$ where $\tfrac1r + \tfrac1s = 1$.
Fenchel–Young then reads $xp \le \tfrac{|x|^r}{r} + \tfrac{|p|^s}{s}$, the
classical Young's inequality underlying Hölder's inequality.

## Role in statistics

- **Exponential families & CGFs.** The cumulant generating function
  $K(t) = \log \mathbb{E}[e^{tX}]$ is convex, and its Legendre transform
  $K^*(x) = \sup_t (tx - K(t))$ is the **large-deviations rate function**
  (Cramér's theorem): $\Pr(\bar X_n \approx x) \approx e^{-nK^*(x)}$.
- **Duality with Jensen.** Because $K$ is convex, $K(t) \ge K(0) + K'(0)t = \mu t$,
  which is exactly [Jensen's inequality](jensens-inequality.md) applied to the
  convex $e^{tx}$. The Fenchel–Young gap $K(t)+K^*(x)-tx \ge 0$ is the same
  convexity fact seen through the conjugate.

## In code

### Python (symbolic conjugate)

```python
import sympy as sp
x, p = sp.symbols("x p", real=True)

def conjugate(f_expr):
    fp = sp.diff(f_expr, x)          # f'(x)
    x_star = sp.solve(sp.Eq(fp, p), x)[0]   # solve p = f'(x) for x
    return sp.simplify((p * x - f_expr).subs(x, x_star))

print(conjugate(x**2 / 2))           # p**2/2
print(conjugate(sp.exp(x)))          # p*log(p) - p
```

### R (numeric conjugate via optimize)

```r
f <- function(x) exp(x)
fstar <- function(p) {
  # maximize p*x - f(x); optimize minimizes, so negate
  opt <- optimize(function(x) f(x) - p * x, interval = c(-20, 20))
  -opt$objective
}
p <- 2
c(numeric = fstar(p), exact = p * log(p) - p)   # both ~ -0.6137
# 2*log(2) - 2 = -0.6137, matching the numeric sup
```

### Julia (numeric conjugate via Optim)

```julia
using Optim
f(x) = exp(x)
function fstar(p)
    res = optimize(x -> f(x) - p * x, -20.0, 20.0)   # minimizes f(x)-p*x
    -Optim.minimum(res)                               # negate to get the sup
end
p = 2.0
println((fstar(p), p * log(p) - p))   # (~-0.6137, -0.6137)
```

## Why it matters for statistics

The Legendre transform is the bridge between a convex objective and its dual
description by slopes. In statistics it converts a cumulant generating function
into a rate function (large deviations, concentration inequalities), links the
natural and mean parameters of exponential families, and provides the convex
duality behind many estimation and optimization problems, including
regularized [maximum likelihood](maximum-likelihood.md). Recognizing a
$\sup_x(px - f(x))$ pattern tells you a convex-conjugate structure is at play.

## Related

- [Jensen's Inequality and Nonlinear Averaging](jensens-inequality.md)
- [Optimization](optimization.md)
- [Derivatives](derivatives.md)
- [Maximum Likelihood](maximum-likelihood.md)
- [Quantitative Methods](../math.md)
