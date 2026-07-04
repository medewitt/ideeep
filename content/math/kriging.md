---
title: "Kriging and Geostatistics"
description: "Kriging is spatial interpolation as the best linear unbiased predictor, equivalent to Gaussian-process regression, built from the variogram."
---

# Kriging and Geostatistics

Suppose you have measured a soil contaminant, a rainfall total, or a disease prevalence at a scattered handful of locations and you want a map — a prediction at every point in between, with honest uncertainty.
Kriging solves exactly this problem: it is the **best linear unbiased predictor** of a spatially correlated field, weighting nearby observations more heavily than distant ones according to how quickly the field decorrelates with distance.
It is named for the mining engineer Danie Krige and formalized by Georges Matheron, and it turns out to be the same estimator as [Gaussian-process regression](gaussian-processes.md) dressed in geostatistical language.

![A fitted exponential variogram with its nugget, sill, and range marked, and an ordinary-kriging surface interpolated from scattered sample points.](../assets/figures/kriging.svg)

## The geostatistical model

Geostatistics treats the observed field as one realization of a random process $Z(s)$ indexed by spatial location $s$.
The workhorse decomposition splits it into a deterministic mean and a zero-mean, spatially correlated residual, \[ Z(s) = \mu(s) + \delta(s), \qquad \mathbb{E}[\delta(s)] = 0. \] The mean $\mu(s)$ captures large-scale trend (often just a constant $\mu$, or a [regression](linear-regression.md) on covariates like elevation), while the residual $\delta(s)$ carries the smooth, short-range structure that makes nearby values resemble one another.
The essential assumption is **second-order stationarity**: the covariance between two locations depends only on the vector $h$ separating them, not on where they sit, so $\operatorname{Cov}[\delta(s), \delta(s+h)] = C(h)$.
Under isotropy this depends only on the distance $\lVert h \rVert$, and the whole modeling problem reduces to estimating one function of separation.

## The variogram

The central object of geostatistics is the **(semi)variogram**, which measures how different two values become as they move apart, \[ \gamma(h) = \tfrac{1}{2}\operatorname{Var}\!\left[\,Z(s+h) - Z(s)\,\right]. \] The factor of one half is why it is called the *semi*variogram; it makes $\gamma$ line up cleanly with the covariance.
Near $h = 0$ the two values are almost identical so $\gamma$ is small, and as separation grows $\gamma$ rises toward a plateau where the values are effectively independent.

### Nugget, sill, and range

A fitted variogram is summarized by three parameters, each with a physical reading.
The **nugget** is the intercept $\gamma(0^+) > 0$, the variance that does not vanish even at tiny separations; it lumps together measurement error and micro-scale variation finer than the sampling spacing.
The **sill** is the plateau value the variogram approaches at large $h$, equal to the total variance $\sigma^2$ of the field.
The **range** is the separation at which the variogram (essentially) reaches the sill — the distance beyond which observations carry no useful information about one another; the difference sill $-$ nugget is the *partial sill*, the portion of variance that is spatially structured.

A common parametric choice is the **exponential** model $\gamma(h) = c_0 + c_1\left(1 - e^{-3h/a}\right)$, with nugget $c_0$, partial sill $c_1$, and practical range $a$ (chosen so $\gamma$ reaches $95\%$ of its sill at $h = a$).
Other standard families are the spherical (which hits the sill exactly at $h = a$) and the [Matérn](covariance-functions.md), whose smoothness parameter controls how differentiable the field is.

### Empirical versus fitted

The **empirical variogram** is computed directly from data by binning all pairs of points by separation distance and averaging their squared differences, \[ \hat{\gamma}(h) = \frac{1}{2\,N(h)} \sum_{(i,j)} \bigl(Z(s_i) - Z(s_j)\bigr)^2, \] where the sum runs over the $N(h)$ pairs separated by roughly $h$.
These binned points are noisy, so a smooth parametric model (exponential, spherical, Matérn) is **fitted** to them by least squares or maximum likelihood, and it is the fitted $\gamma$ — guaranteed to yield a valid covariance — that goes into the kriging equations.

### Relationship to the covariance

For a stationary field the variogram and covariance are two views of the same structure.
Expanding the variance of the difference and using $\operatorname{Var}[Z(s)] = C(0) = \sigma^2$ gives the fundamental identity \[ \gamma(h) = \sigma^2 - C(h). \] The variogram is the covariance flipped upside down: where $C$ starts high at $\sigma^2$ and decays to zero, $\gamma$ starts at zero (or the nugget) and rises to the sill $\sigma^2$.
This is why kriging can be written interchangeably in terms of $\gamma$ or $C$, and it is the bridge to the covariance-function view used in Gaussian processes.

## The kriging equations

Kriging predicts the value at an unsampled location $s_0$ as a weighted average of the observations, $\hat{Z}(s_0) = \sum_{i=1}^{n} w_i\, Z(s_i)$, and chooses the weights $w_i$ to minimize the mean-squared prediction error subject to being unbiased.

### Ordinary kriging

When the mean $\mu$ is constant but unknown, unbiasedness forces the weights to sum to one, $\sum_i w_i = 1$.
Enforcing that constraint while minimizing the error variance introduces a **Lagrange multiplier** $\lambda$, and the weights solve the linear system \[ \sum_{j=1}^{n} w_j\, C(s_i, s_j) + \lambda = C(s_i, s_0), \qquad \sum_{j=1}^{n} w_j = 1. \] In block-matrix form this augments the $n\times n$ covariance matrix with a row and column of ones, \[ \begin{bmatrix} \mathbf{C} & \mathbf{1} \\ \mathbf{1}^{\top} & 0 \end{bmatrix} \begin{bmatrix} \mathbf{w} \\ \lambda \end{bmatrix} = \begin{bmatrix} \mathbf{c}_0 \\ 1 \end{bmatrix}, \] where $\mathbf{C}_{ij} = C(s_i, s_j)$ and $(\mathbf{c}_0)_i = C(s_i, s_0)$.
The multiplier $\lambda$ is the price paid for estimating the mean from the data.

### Simple kriging

If the mean $\mu$ is known, no unbiasedness constraint is needed and the weights need not sum to one.
The predictor works on residuals from the known mean, \[ \hat{Z}(s_0) = \mu + \sum_{i=1}^{n} w_i\,\bigl(Z(s_i) - \mu\bigr), \qquad \mathbf{C}\,\mathbf{w} = \mathbf{c}_0. \] Simple kriging pulls the prediction toward $\mu$ where data are sparse, whereas ordinary kriging, having spent a degree of freedom to estimate the mean locally, does not.

### The kriging variance

Kriging returns not just a prediction but its error variance, which for ordinary kriging is \[ \sigma_{\text{OK}}^2(s_0) = \sigma^2 - \sum_{i=1}^{n} w_i\, C(s_i, s_0) - \lambda. \] Crucially this depends only on the *geometry* of the sample locations relative to $s_0$ — not on the observed values — so it can be mapped in advance to show where predictions are trustworthy and where more sampling is needed.
The variance is small near observations and inflates in the gaps between them, tending to the sill $\sigma^2$ far from any data.

## Equivalence to Gaussian-process regression

Kriging is Gaussian-process regression under another name.
If $Z$ is a [Gaussian process](gaussian-processes.md) with mean $\mu$ and [covariance function](covariance-functions.md) $C$, then the GP posterior mean at $s_0$ is \[ \hat{Z}(s_0) = \mu + \mathbf{c}_0^{\top}\mathbf{C}^{-1}(\mathbf{z} - \mu), \] which is exactly the simple-kriging predictor, and the GP posterior variance is exactly the kriging variance.
Ordinary kriging corresponds to a GP with an (improper) flat prior on the unknown constant mean, integrated out.
The dictionary is direct: the variogram sill is the GP marginal variance, the nugget is the GP observation-noise variance, and the range is the GP length-scale.
This equivalence is why the same machinery appears as "kriging" in the earth sciences and "GP regression" in machine learning, and why model-based geostatistics fits these models by likelihood or in a fully Bayesian framework such as [INLA](inla.md).

## A worked example

Take simple kriging at a target $s_0$ from two samples, with the field standardized so $\sigma^2 = 1$ and the mean known to be $\mu = 10$.
Suppose the fitted covariance gives correlations $C(s_0,s_1) = 0.8$ and $C(s_0,s_2) = 0.5$ to the target, and $C(s_1,s_2) = 0.3$ between the two samples.
The weights solve $\mathbf{C}\,\mathbf{w} = \mathbf{c}_0$, i.e. \[ \begin{bmatrix} 1 & 0.3 \\ 0.3 & 1 \end{bmatrix} \begin{bmatrix} w_1 \\ w_2 \end{bmatrix} = \begin{bmatrix} 0.8 \\ 0.5 \end{bmatrix}, \] whose solution is $w_1 = 0.65/0.91 \approx 0.714$ and $w_2 = 0.26/0.91 \approx 0.286$.
The nearer, more strongly correlated sample earns the larger weight, as it should.
With observed values $z_1 = 12$ and $z_2 = 9$, the prediction is $\hat{Z}(s_0) = 10 + 0.714(12-10) + 0.286(9-10) \approx 11.14$.
The kriging variance is $\sigma_{\text{SK}}^2 = 1 - (0.714\times 0.8 + 0.286\times 0.5) \approx 0.286$, so the field's variance of $1$ has been cut by roughly $71\%$ thanks to the two neighbors.
As a sanity check on reading a variogram: an exponential $\gamma$ that levels off at $\gamma = 1.0$ with an intercept of $0.2$ has sill $1.0$, nugget $0.2$, and partial sill $0.8$, and its range is wherever the curve first flattens against that plateau.

## In code

### R

```r
library(gstat)
library(sp)

# scattered samples with coordinates (x, y) and observed value z
d <- data.frame(x = c(0, 2, 0, 4), y = c(0, 0, 3, 4), z = c(3, 3.5, 2, 5))
coordinates(d) <- ~ x + y

# empirical variogram, then fit an exponential model (nugget, partial sill, range)
ev  <- variogram(z ~ 1, d)
mod <- fit.variogram(ev, vgm(psill = 0.8, model = "Exp", range = 4, nugget = 0.1))

# ordinary kriging onto a target location; out$var1.pred and out$var1.var
grid <- data.frame(x = 1.5, y = 1.5); coordinates(grid) <- ~ x + y
out  <- krige(z ~ 1, d, grid, model = mod)
```

### Python

```python
import numpy as np

# Exponential variogram gamma(h) = c0 + c1*(1 - exp(-3h/a)); C(h) = sill - gamma(h).
nugget, sill, a = 0.1, 1.0, 4.0
c1 = sill - nugget

def cov(h):                                   # nugget lives on the diagonal only
    h = np.asarray(h, float)
    return np.where(h == 0.0, sill, c1 * np.exp(-3.0 * h / a))

s  = np.array([[0., 0.], [2., 0.], [0., 3.], [4., 4.]])   # sampled locations
z  = np.array([3.0, 3.5, 2.0, 5.0])                       # observed values
s0 = np.array([1.5, 1.5])                                 # predict here
n  = len(z)

D  = np.hypot(s[:, None, 0] - s[None, :, 0], s[:, None, 1] - s[None, :, 1])
c0 = cov(np.hypot(s[:, 0] - s0[0], s[:, 1] - s0[1]))

A = np.ones((n + 1, n + 1)); A[:n, :n] = cov(D); A[n, n] = 0.0   # Lagrange row/col
sol = np.linalg.solve(A, np.append(c0, 1.0))
w, lam = sol[:n], sol[n]

pred = w @ z
var  = sill - w @ c0 - lam                    # ordinary-kriging variance
print("weights       :", np.round(w, 3))
print("sum of weights:", round(w.sum(), 3))
print("prediction    :", round(pred, 3))
print("kriging var   :", round(var, 3))
```

<!-- python-output:auto -->
```text
weights       : [0.22  0.342 0.267 0.171]
sum of weights: 1.0
prediction    : 3.246
kriging var   : 0.938
```
<!-- /python-output:auto -->

### Julia

```julia
using GeoStats

# scattered samples: coordinates and the observed variable z
d = georef((z = [3.0, 3.5, 2.0, 5.0],),
           [(0.0, 0.0), (2.0, 0.0), (0.0, 3.0), (4.0, 4.0)])

# exponential variogram with nugget, sill, and range, then ordinary kriging
g   = ExponentialVariogram(sill = 1.0, range = 4.0, nugget = 0.1)
sol = d |> InterpolateNeighbors(PointSet([(1.5, 1.5)]), Kriging(g))
```

## Why it matters

Kriging is the default tool wherever a continuous field is measured at points but wanted everywhere.
It builds rainfall and pollutant surfaces from monitoring stations, soil-property and ore-grade maps from cores, and — through **model-based geostatistics** — smoothed disease-prevalence surfaces from georeferenced survey clusters, the backbone of projects that map malaria, helminth, or other prevalence across a country.
Because the [kriging variance](measures-of-variability.md) is a map of prediction uncertainty that depends only on where you sampled, it also drives *where to sample next*, guiding survey design toward the gaps.
And because kriging is [Gaussian-process regression](gaussian-processes.md), the same fitted covariance can be embedded in a Bayesian hierarchical model — via [INLA](inla.md) or MCMC — that propagates spatial uncertainty into downstream estimates rather than treating the interpolated map as if it were observed truth.

## Related

- [Gaussian Processes](gaussian-processes.md)
- [Covariance Functions](covariance-functions.md)
- [Linear Regression](linear-regression.md)
- [Measures of Variability](measures-of-variability.md)
- [INLA](inla.md)
- [Spatial Point Processes](spatial-point-processes.md)
- [Distance Measures](distance-measures.md)
- [Quantitative Methods](../math.md)
```
