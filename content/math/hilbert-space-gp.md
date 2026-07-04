---
title: "Hilbert-Space Approximations for Gaussian Processes"
description: "The Hilbert-space (HSGP) approximation replaces a stationary Gaussian-process kernel with a finite basis of Laplacian eigenfunctions, turning O(n^3) exact inference into cost roughly linear in n."
---

# Hilbert-Space Approximations for Gaussian Processes

A [Gaussian process](gaussian-processes.md) is a beautifully flexible prior over functions, but exact inference means factorizing an $n \times n$ covariance matrix, which costs [$O(n^3)$ time and $O(n^2)$ memory](../programming/big-o-and-complexity.md) and stalls on more than a few thousand points.
The Hilbert-space approximation (HSGP) sidesteps this by writing the process as a short, fixed sum of deterministic basis functions with independent Gaussian weights, so the model becomes an ordinary linear regression whose cost grows roughly linearly in $n$.
The trick, due to [Solin and Särkkä (2020)](https://doi.org/10.1007/s11222-019-09886-w) and made practical for probabilistic programming by [Riutort-Mayol et al. (2023)](https://doi.org/10.1007/s11222-022-10167-2), is that a stationary kernel is diagonalized by the eigenfunctions of the Laplacian on a bounded domain.

![The first Laplacian eigenfunctions on $[-L, L]$ and sample paths drawn from the finite HSGP basis expansion.](../assets/figures/hilbert-space-gp.svg)

## Why exact GPs are expensive

Give a GP a mean of zero and a covariance (kernel) function $k(x, x')$, and the values $f(x_1), \dots, f(x_n)$ are jointly normal with covariance matrix $K_{ij} = k(x_i, x_j)$.
Conditioning on data or drawing samples requires the Cholesky factor of $K$ (or of $K + \sigma^2 I$), an $O(n^3)$ operation, and storing $K$ is $O(n^2)$.
Doubling the data multiplies the work eightfold, which is why plain GPs are a luxury reserved for small datasets unless some structure is exploited.
The HSGP replaces $K$ with a low-rank factorization $K \approx \Phi \, \mathrm{diag}(S) \, \Phi^\top$ built from $m \ll n$ fixed basis functions, and linear algebra on that costs $O(nm^2)$ — linear in $n$ for a fixed budget $m$.

## Kernels, eigenfunctions, and the Laplacian

The idea rests on two classical facts.
First, a stationary kernel $k(x, x') = k(x - x')$ is determined by its **spectral density** $S(\omega)$, the Fourier transform of $k$; this is Bochner's theorem, and it is the same statement as writing a covariance function as a mixture of cosines of every frequency.
Second, on a bounded interval the negative Laplacian $-\nabla^2$ has a discrete set of [eigenfunctions and eigenvalues](eigenvalues-and-eigenvectors.md) that form an orthonormal basis, and those eigenfunctions are exactly sines and cosines.
Solin and Särkkä tie the two together: because $-\nabla^2$ generates the same frequencies that the spectral density weights, a stationary kernel is *approximately diagonalized* by the Laplacian eigenbasis, with the spectral density evaluated at each eigenfrequency giving that basis function's variance.

On the symmetric domain $[-L, L]$ with Dirichlet (zero) boundary conditions, the eigenvalues and eigenfunctions are \[ \lambda_j = \left(\frac{j\pi}{2L}\right)^2, \qquad \phi_j(x) = \sqrt{\frac{1}{L}} \, \sin\!\left(\sqrt{\lambda_j}\,(x + L)\right), \qquad j = 1, 2, 3, \dots \] Each $\phi_j$ is a sine wave that completes $j$ half-oscillations across the interval, and $\sqrt{\lambda_j} = j\pi / (2L)$ is its angular frequency: larger $j$ means faster wiggles, exactly the high-frequency content that a short lengthscale demands.

## The Hilbert-space approximation

The approximation writes the process as a finite weighted sum of these eigenfunctions, \[ f(x) \;\approx\; \sum_{j=1}^{m} \sqrt{S\!\left(\sqrt{\lambda_j}\right)}\; \phi_j(x)\; \beta_j, \qquad \beta_j \sim \mathcal{N}(0, 1), \] where $S(\cdot)$ is the spectral density of the chosen kernel and the $\beta_j$ are independent standard-normal weights.
Because the $\phi_j$ are fixed and known, this is just a **linear model** in $m$ features: the design matrix $\Phi$ with entries $\Phi_{ij} = \phi_j(x_i)$ is precomputed once, the amplitudes $\sqrt{S(\sqrt{\lambda_j})}$ are simple functions of the kernel hyperparameters, and only the $\beta_j$ (plus the hyperparameters $\sigma$, $\ell$) are inferred.
Equivalently the covariance is approximated by \[ k(x, x') \;\approx\; \sum_{j=1}^{m} S\!\left(\sqrt{\lambda_j}\right)\, \phi_j(x)\, \phi_j(x'), \] a rank-$m$ factorization whose accuracy improves as $m$ grows and as the domain $[-L, L]$ comfortably contains the data.

### Spectral densities

The whole recipe needs only the spectral density $S(\omega)$ of the kernel, evaluated at the eigenfrequencies $\sqrt{\lambda_j}$.
For the **squared-exponential (RBF)** kernel $k(r) = \sigma^2 \exp(-r^2 / 2\ell^2)$ in one dimension, \[ S(\omega) = \sigma^2 \, \sqrt{2\pi}\, \ell \, \exp\!\left(-\tfrac{1}{2}\,\omega^2 \ell^2\right), \] a Gaussian in frequency that decays quickly, so a modest number of low-frequency basis functions suffices.
For the **Matérn** kernel with smoothness $\nu$, \[ S(\omega) = \sigma^2 \, \frac{2\sqrt{\pi}\,\Gamma\!\left(\nu + \tfrac{1}{2}\right)(2\nu)^{\nu}}{\Gamma(\nu)\,\ell^{2\nu}} \left(\frac{2\nu}{\ell^2} + \omega^2\right)^{-(\nu + 1/2)}, \] a power-law tail that decays more slowly, so rougher Matérn processes (small $\nu$) need more basis functions than the RBF to reach the same fidelity.
See [covariance functions](covariance-functions.md) for how $\sigma$, $\ell$, and $\nu$ shape these kernels in the first place.

## Two knobs: $m$ and the boundary factor $c$

The approximation has exactly two tuning parameters, and both trade accuracy against cost.

- **Number of basis functions $m$.** More terms resolve higher frequencies, so $m$ controls the shortest lengthscale the approximation can represent; the cost is $O(nm^2)$, so you want $m$ as small as fidelity allows.
- **Boundary factor $c$.** The domain half-width is set to $L = c \cdot S$, where $S$ is a scale for the data (e.g. half the range of $x$, after centering).
  The approximation degrades near the edges of $[-L, L]$, so the domain must be padded beyond the data with $c > 1$ (typically $c \approx 1.2$ to $2$); too small and the fit warps at the boundaries, too large and you waste basis functions on empty space.

These two interact: pushing $L$ outward with a larger $c$ stretches the eigenfunctions, lowering every eigenfrequency $\sqrt{\lambda_j} = j\pi / (2L)$, so a larger domain needs a larger $m$ to keep resolving the same short lengthscale.
The **accuracy/lengthscale tradeoff** is the crux: short lengthscales mean rapidly wiggling functions with high-frequency content, and capturing them requires many basis functions, while long, smooth lengthscales are represented well by just a handful.

## A worked example: how many basis functions?

Suppose the data are centered and scaled so their half-range is $S = 1$, and you pick a boundary factor $c = 1.5$, giving $L = c \cdot S = 1.5$.
The finest feature a basis of $m$ sines can represent has a half-wavelength of about $L / m$ across the half-domain, so to resolve a lengthscale $\ell$ we need roughly \[ \frac{L}{m} \lesssim \ell \qquad\Longrightarrow\qquad m \;\gtrsim\; \frac{2L}{\ell} \;=\; \frac{2c\,S}{\ell}, \] a Nyquist-style floor showing that the basis budget scales inversely with the lengthscale.
For $\ell = 0.25$ this gives $m \gtrsim 2(1.5)/0.25 = 12$ basis functions as a bare minimum; because the RBF spectral density still carries weight a little above the Nyquist frequency, a safety margin of roughly $m \approx 20$ keeps the approximation faithful.
Halve the lengthscale to $\ell = 0.125$ and the requirement doubles to $m \gtrsim 24$, so very wiggly functions quickly erode the speedup — HSGP shines when the process is smooth relative to its domain.
Riutort-Mayol et al. turn exactly this reasoning into practical diagnostics and recommendation tables for choosing $m$ and $c$ together from the inferred lengthscale.

## In code

### R

```r
library(brms)

# brms fits a Hilbert-space approximate GP through the gp() term:
#   k = number of basis functions (m), c = boundary factor.
# The HSGP eigenfunctions and spectral density are constructed internally,
# so the model stays a fast linear-in-basis regression fitted with Stan.
fit <- brm(
  y ~ gp(x, k = 20, c = 1.5),
  data = df, chains = 4, cores = 4
)

# The related s(...) smooth terms (brms/mgcv splines) are another low-rank
# basis idea, differing mainly in how the basis and its penalty are chosen.
conditional_effects(fit, effects = "x")
```

### Python

```python
import numpy as np

sigma, ell, L, m = 1.0, 0.6, 3.0, 30       # kernel + approximation settings
x = np.linspace(-L, L, 200)

j = np.arange(1, m + 1)
sqrt_lam = j * np.pi / (2 * L)             # sqrt of Laplacian eigenvalues
phi = np.sqrt(1.0 / L) * np.sin(sqrt_lam[:, None] * (x + L))   # (m, n) basis
S = sigma**2 * np.sqrt(2 * np.pi) * ell * np.exp(-0.5 * (sqrt_lam * ell)**2)

K_hsgp = (phi * S[:, None]).T @ phi        # rank-m approximate covariance
K_exact = sigma**2 * np.exp(-0.5 * (x[:, None] - x[None, :])**2 / ell**2)

print("basis functions m      =", m)
print("max abs covariance err =", round(np.abs(K_hsgp - K_exact).max(), 4))
```

<!-- python-output:auto -->
```text
basis functions m      = 30
max abs covariance err = 1.0
```
<!-- /python-output:auto -->

### Julia

```julia
# Illustrative: build the sine eigenbasis and RBF spectral density by hand,
# then draw a sample path f(x) = sum_j sqrt(S(sqrt(lam_j))) phi_j(x) beta_j.
L, ell, sigma, m = 3.0, 0.6, 1.0, 30
sqrt_lam(j) = j * pi / (2L)
phi(j, x)   = sqrt(1 / L) * sin(sqrt_lam(j) * (x + L))
S(w)        = sigma^2 * sqrt(2pi) * ell * exp(-0.5 * (w * ell)^2)

x    = range(-L, L; length = 200)
beta = randn(m)                             # beta_j ~ N(0, 1)
f    = [sum(sqrt(S(sqrt_lam(j))) * phi(j, xi) * beta[j] for j in 1:m) for xi in x]

# In practice the Stan/Turing model infers beta together with sigma and ell.
```

## Why it matters

Making GPs cheap turns them from a boutique method into a routine building block for [Bayesian inference](bayesian-inference.md) at scale.
A smooth spatial random field over thousands of locations, a temporal trend sampled at fine resolution, or a nonlinear covariate effect can all be given a GP prior and fitted with [MCMC](mcmc.md) in minutes rather than hours, because each likelihood evaluation touches an $m$-column design matrix instead of an $n \times n$ kernel.
This is precisely why HSGP underlies the `gp()` terms in [brms](https://paul-buerkner.github.io/brms/) and the reference implementations in [Stan](https://mc-stan.org/), and why penalized-spline `s(...)` smooths are the workhorse for wiggly effects in the same models.
In infectious-disease work the payoff is direct: smooth space–time surfaces for prevalence mapping, flexible time-varying reproduction numbers, and delay or reporting effects can all be modeled as approximate GPs that actually finish sampling on real surveillance datasets.

## Related

- [Gaussian Processes](gaussian-processes.md)
- [Covariance Functions](covariance-functions.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Bayesian Inference](bayesian-inference.md)
- [Markov Chain Monte Carlo](mcmc.md)
- [Quantitative Methods](../math.md)
