---
title: "Covariance Functions and the Matérn Family"
description: "How the covariance function (kernel) of a Gaussian process encodes spatial smoothness, and why the Matérn family — especially ν = 3/2 and 5/2 — is the pragmatic default."
---

# Covariance Functions and the Matérn Family

A Gaussian process is only as concrete as its covariance function: the kernel $k(x,x')$ is what turns the abstract idea of "a distribution over functions" into something you can compute with.
It answers a single question — how strongly do the values at two locations $x$ and $x'$ covary? — and its answer, as a function of the separation between points, silently fixes how wiggly or how smooth the resulting functions are.
Choosing a kernel is therefore choosing your assumptions about the world, and the Matérn family gives you a single dial, the smoothness parameter $\nu$, to set them deliberately.

![Matérn correlation as a function of distance for smoothness $\nu = 1/2, 3/2, 5/2$ and the $\nu \to \infty$ (squared-exponential) limit, all at lengthscale $\rho = 1$.](../assets/figures/covariance-functions.svg)

## What makes a covariance function valid

A covariance function assigns to every pair of inputs $x, x'$ the covariance $k(x,x') = \operatorname{Cov}\big(f(x), f(x')\big)$ between the (random) function values there.
For this to be a legitimate covariance, $k$ must be **positive semi-definite**: for any finite set of points $x_1,\dots,x_n$ the Gram matrix $K$ with entries $K_{ij}=k(x_i,x_j)$ must satisfy $$\mathbf{a}^\top K\, \mathbf{a} = \sum_{i,j} a_i a_j\, k(x_i, x_j) \ge 0 \quad \text{for all } \mathbf{a}\in\mathbb{R}^n.$$ This is exactly the condition that the variance of any linear combination $\sum_i a_i f(x_i)$ is non-negative, which any real covariance must obey.
Not every symmetric function of two points qualifies, and this constraint is what rules out many "reasonable-looking" kernels; the families below are valid by construction.

## Stationarity and isotropy

A kernel is **stationary** if it depends only on the separation $x - x'$ rather than on the absolute locations, so the statistical behavior of the process looks the same everywhere.
It is **isotropic** if it depends only on the distance $r = \lVert x - x' \rVert$, so direction does not matter either — the process has no preferred orientation.
Both the squared-exponential and the Matérn kernels are stationary and isotropic, which lets us write them as a one-variable **correlation function** $k(r)$ that decays from its peak at $r=0$ toward zero as points move apart.
This is the natural setting for [spatial](kriging.md) and temporal models, where "nearby points are similar" is the whole modeling premise.

## The squared-exponential (RBF) kernel

The most common starting point is the **squared-exponential** kernel, also called the radial-basis-function (RBF) or Gaussian kernel, $$k(r) = \sigma^2 \exp\!\left(-\frac{r^2}{2\rho^2}\right),$$ where $\rho$ is the **lengthscale** (the distance over which the function changes appreciably) and $\sigma^2$ is the marginal variance.
Its correlation falls off very fast — like $r^2$ in the exponent — so distant points decorrelate quickly while nearby points are almost perfectly correlated.
The catch is that this kernel produces functions that are **infinitely differentiable**: sample paths are unrealistically smooth, analytic curves with no roughness at any scale.
For many physical and biological processes that is too strong an assumption, and it is precisely the assumption the Matérn family relaxes.

## The Matérn family

The Matérn kernel introduces a **smoothness parameter** $\nu > 0$ that controls exactly how rough the sample paths are, alongside the lengthscale $\rho$.
Its general isotropic form uses the modified Bessel function of the second kind $K_\nu$ and the gamma function $\Gamma$: $$k(r) = \sigma^2\, \frac{2^{1-\nu}}{\Gamma(\nu)} \left(\frac{\sqrt{2\nu}\,r}{\rho}\right)^{\!\nu} K_\nu\!\left(\frac{\sqrt{2\nu}\,r}{\rho}\right).$$ As written it looks forbidding, but for the half-integer values $\nu = p + 1/2$ the Bessel function collapses to an exponential times a polynomial, giving the clean closed forms that are used in practice.
Writing the correlation (with $\sigma^2 = 1$) for the common choices:

$$
\begin{aligned}
\nu = \tfrac12: &\quad k(r) = \exp\!\left(-\frac{r}{\rho}\right), \\[2pt]
\nu = \tfrac32: &\quad k(r) = \left(1 + \frac{\sqrt{3}\,r}{\rho}\right)\exp\!\left(-\frac{\sqrt{3}\,r}{\rho}\right), \\[2pt]
\nu = \tfrac52: &\quad k(r) = \left(1 + \frac{\sqrt{5}\,r}{\rho} + \frac{5r^2}{3\rho^2}\right)\exp\!\left(-\frac{\sqrt{5}\,r}{\rho}\right), \\[2pt]
\nu \to \infty: &\quad k(r) = \exp\!\left(-\frac{r^2}{2\rho^2}\right).
\end{aligned}
$$

The bottom line is the payoff: as $\nu \to \infty$ the Matérn kernel converges to the squared-exponential, so the RBF is simply the infinitely-smooth end of the same family.

### How ν controls differentiability

The smoothness parameter has a precise meaning: a Matérn process is **$\lceil \nu \rceil - 1$ times mean-square differentiable**.
So $\nu = 1/2$ gives continuous-but-nowhere-differentiable paths (very rough), $\nu = 3/2$ gives once-differentiable paths, $\nu = 5/2$ gives twice-differentiable paths, and only in the $\nu\to\infty$ limit do the paths become infinitely differentiable.
Small $\nu$ therefore means jagged realizations that can change direction abruptly, while large $\nu$ means gently rolling curves; the parameter interpolates continuously between these regimes.
This is the sense in which the kernel *is* the smoothness assumption — you are choosing the differentiability of the functions you believe generated the data.

### The exponential and Ornstein–Uhlenbeck link

The $\nu = 1/2$ case, $k(r) = \sigma^2 \exp(-r/\rho)$, is the **exponential kernel**, and it is worth singling out.
In one dimension the resulting stationary Gaussian process is exactly the **Ornstein–Uhlenbeck process**, the mean-reverting continuous-time analogue of a first-order autoregressive process.
Its paths are continuous but nowhere differentiable — the mathematical fingerprint of a process driven by white noise — which is why the exponential kernel is the right default when you expect genuinely rough, memoryless-in-slope behavior.

## Marginal variance, combinations, and noise

The prefactor $\sigma^2 = k(0)$ is the **marginal variance**: it sets the overall vertical scale of the function, i.e. how far $f(x)$ typically strays from its mean, and it factors out of the correlation entirely.
Kernels are also closed under **addition and multiplication**: if $k_1$ and $k_2$ are valid covariance functions then so are $k_1 + k_2$ (superimposing two behaviors, e.g. a slow trend plus fast wiggles) and $k_1 k_2$ (an AND-like interaction), which lets you compose structured kernels from simple parts.
Finally, real measurements carry noise, modeled by adding a **nugget** term $\sigma_n^2\,\delta_{xx'}$ to the diagonal: $$k_{\text{obs}}(x,x') = k(x,x') + \sigma_n^2\,\delta_{xx'},$$ where $\delta_{xx'}$ is $1$ only when $x = x'$.
The nugget represents observation error (or micro-scale [variability](measures-of-variability.md)), keeps the Gram matrix well-conditioned for inversion, and — because it is a valid kernel added to another — preserves positive semi-definiteness.

## A worked example

Consider a spatial model with a Matérn $\nu = 3/2$ kernel and lengthscale $\rho = 10\ \text{km}$, and ask how correlated two sites $r = 15\ \text{km}$ apart are.
The scaled distance is $\sqrt{3}\,r/\rho = \sqrt{3}\times 15/10 = 1.5\sqrt{3} \approx 2.598$, so $$k(r) = \left(1 + 2.598\right)\exp(-2.598) = 3.598 \times 0.07442 \approx 0.268.$$ So the two sites share a correlation of about $0.27$: still meaningfully linked, but well down from the perfect correlation at $r=0$.
For comparison, an RBF kernel with the same $\rho$ would give $\exp(-15^2/(2\cdot 10^2)) = \exp(-1.125) \approx 0.325$, and an exponential ($\nu=1/2$) kernel would give $\exp(-15/10) \approx 0.223$ — the smoother the kernel, the more slowly correlation bleeds away at these separations.

## In code

We implement the Matérn correlation directly from the general Bessel-function formula and check it against the closed forms.

### R

```r
matern <- function(r, nu, rho = 1) {
  s <- sqrt(2 * nu) * r / rho
  k <- (2^(1 - nu) / gamma(nu)) * s^nu * besselK(s, nu)
  k[r == 0] <- 1                       # fill the r = 0 limit
  k
}

matern(15, nu = 1.5, rho = 10)         # ~0.268, the worked example
matern(1, nu = c(0.5, 1.5, 2.5), rho = 1)
```

### Python

```python
import numpy as np
from scipy.special import kv, gamma

def matern(r, nu, rho=1.0):
    """Matern correlation at separation r (array-safe, with the r=0 limit)."""
    r = np.asarray(r, dtype=float)
    out = np.ones_like(r)              # k(0) = 1
    nz = r > 0
    s = np.sqrt(2 * nu) * r[nz] / rho
    out[nz] = 2 ** (1 - nu) / gamma(nu) * s ** nu * kv(nu, s)
    return out

# Worked example: Matern 3/2 at r = 15 km, rho = 10 km
print("Matern 3/2, r=15, rho=10:", round(float(matern(15, 1.5, 10)), 4))

# General Bessel formula agrees with the closed forms at r = 1, rho = 1
r = 1.0
closed = {
    0.5: np.exp(-r),
    1.5: (1 + np.sqrt(3) * r) * np.exp(-np.sqrt(3) * r),
    2.5: (1 + np.sqrt(5) * r + 5 * r ** 2 / 3) * np.exp(-np.sqrt(5) * r),
}
for nu, ck in closed.items():
    print(f"nu={nu}: general={float(matern(r, nu)):.6f}  closed={ck:.6f}")
```

<!-- python-output:auto -->
```text
Matern 3/2, r=15, rho=10: 0.2678
nu=0.5: general=0.367879  closed=0.367879
nu=1.5: general=0.483358  closed=0.483358
nu=2.5: general=0.523994  closed=0.523994
```
<!-- /python-output:auto -->

### Julia

```julia
using SpecialFunctions   # besselk, gamma

function matern(r, nu; rho = 1.0)
    r == 0 && return 1.0             # k(0) = 1
    s = sqrt(2nu) * r / rho
    2.0^(1 - nu) / gamma(nu) * s^nu * besselk(nu, s)
end

matern(15, 1.5; rho = 10)            # ~0.268, the worked example
[matern(1.0, nu) for nu in (0.5, 1.5, 2.5)]
```

## Why it matters

In [kriging](kriging.md) and other spatial models, the covariance function is where your belief about how smoothly a field varies over space actually lives, so picking it well is not a technicality — it changes both the predictions and their uncertainty.
The squared-exponential kernel is often too smooth to be credible for real spatial or environmental fields, which is why practitioners reach for the Matérn family and, overwhelmingly, for $\nu = 3/2$ or $\nu = 5/2$: these give once- or twice-differentiable fields that look like real data while remaining cheap to evaluate through their closed forms.
The same kernel choice underlies [Gaussian process](gaussian-processes.md) regression and its scalable [Hilbert-space](hilbert-space-gp.md) approximations, where the Matérn spectral density has an especially clean form.
Because the marginal $f(x)$ at any single location is [normally distributed](normal-distribution.md) with variance $\sigma^2$, the kernel simultaneously sets the pointwise uncertainty and the correlation structure that ties neighboring predictions together.

## Related

- [The Normal Distribution](normal-distribution.md)
- [Measures of Variability](measures-of-variability.md)
- [Gaussian Processes](gaussian-processes.md)
- [Kriging](kriging.md)
- [Hilbert-Space Gaussian Processes](hilbert-space-gp.md)
- [Quantitative Methods](../math.md)
