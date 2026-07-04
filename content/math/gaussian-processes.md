---
title: "Gaussian Processes"
description: "A Gaussian process is a distribution over functions, giving a nonparametric interpolator that reports calibrated uncertainty alongside every prediction."
---

# Gaussian Processes

Ordinary regression fits a function with a fixed number of parameters; a Gaussian process (GP) instead puts a probability distribution directly over functions themselves.
Ask it for the value at any input and it returns not a single number but a whole Gaussian: a best guess plus a variance that widens where data are sparse and pinches shut near observations.
That makes a GP a flexible interpolator that always carries its own error bars, which is why it underpins simulator emulation, spatial [kriging](kriging.md), and probabilistic time-series models.

![Left: four sample functions drawn from a GP prior with an RBF kernel. Right: the GP posterior mean and 95% band after conditioning on five noisy observations, interpolating the data while widening away from it.](../assets/figures/gaussian-processes.svg)

## The definition

A Gaussian process is a collection of random variables, any finite subset of which is jointly [multivariate normal](normal-distribution.md).
We write \[ f(x) \sim \mathcal{GP}\!\bigl(m(x),\, k(x,x')\bigr), \] where the **mean function** $m(x) = \mathbb{E}[f(x)]$ sets the average value at each input and the **covariance function** (or **kernel**) \[ k(x,x') = \mathbb{E}\!\bigl[(f(x)-m(x))(f(x')-m(x'))\bigr] \] says how strongly the function values at two inputs $x$ and $x'$ co-vary.
Together $m$ and $k$ specify the process completely: every property of the infinite-dimensional distribution over functions is encoded in these two functions of the inputs.

The definition becomes concrete the moment you pick a finite set of inputs.
For inputs $X = \{x_1,\dots,x_n\}$ the vector of function values $\mathbf{f} = \bigl(f(x_1),\dots,f(x_n)\bigr)^\top$ has an ordinary [multivariate normal distribution](normal-distribution.md) \[ \mathbf{f} \sim \mathcal N(\mathbf{m},\, K), \] where $\mathbf{m}$ is the vector of means $m(x_i)$ and $K$ is the $n\times n$ **covariance matrix** (or Gram matrix) with entries $K_{ij} = k(x_i, x_j)$; see [matrix notation](matrix-notation.md) for the conventions.
A GP is thus a multivariate normal "of infinite length", and any question you ask of it collapses to linear algebra on the relevant finite block.
It is common, and harmless after centering, to take the mean function $m(x)=0$, so that all the structure lives in the kernel.

## Sampling from the prior

To *draw a function* from the prior, choose a dense grid of inputs $x_1,\dots,x_N$, build the covariance matrix $K$, and sample the vector $\mathbf{f}\sim\mathcal N(\mathbf 0, K)$.
The standard recipe factors $K = LL^\top$ by a Cholesky decomposition and sets $\mathbf{f} = L\mathbf{z}$ for a vector $\mathbf{z}$ of independent standard normals, which reproduces the target covariance because $\operatorname{Cov}(L\mathbf z) = L L^\top = K$.
Connecting the sampled values across the grid traces one sample function, and repeating with fresh $\mathbf z$ gives the family of prior draws on the left of the figure.
The kernel controls what these draws look like: with a smooth kernel neighbouring values are highly correlated, so the samples are smooth wiggly curves rather than jagged noise.

## GP regression: conditioning on data

The point of a GP is prediction, and prediction is just conditioning a joint Gaussian on the part you have observed.
Suppose we observe noisy data $y_i = f(x_i) + \varepsilon_i$ with independent Gaussian noise $\varepsilon_i \sim \mathcal N(0,\sigma_n^2)$, collected in the vector $\mathbf y$ at training inputs $X$, and we want the function at a set of test inputs $X_\star$.
Because the training outputs and the test values are jointly Gaussian, they stack into \[ \begin{bmatrix} \mathbf y \\ \mathbf f_\star \end{bmatrix} \sim \mathcal N\!\left( \mathbf 0,\; \begin{bmatrix} K + \sigma_n^2 I & K_\star \\ K_\star^\top & K_{\star\star} \end{bmatrix} \right), \] where $K = k(X,X)$ is training-to-training, $K_\star = k(X,X_\star)$ is training-to-test, and $K_{\star\star} = k(X_\star,X_\star)$ is test-to-test.

Applying the standard Gaussian conditioning formulas gives the **posterior** (or predictive) distribution $\mathbf f_\star \mid \mathbf y \sim \mathcal N(\bar{\mathbf f}_\star,\, \Sigma_\star)$ with \[ \bar{\mathbf f}_\star = K_\star^\top \bigl(K + \sigma_n^2 I\bigr)^{-1}\mathbf y, \] \[ \Sigma_\star = K_{\star\star} - K_\star^\top \bigl(K + \sigma_n^2 I\bigr)^{-1} K_\star. \] These two lines are the whole of GP regression.
The posterior mean is a weighted combination of the observed outputs — write $\boldsymbol\alpha = (K+\sigma_n^2 I)^{-1}\mathbf y$ and the prediction at a test point is $\sum_i \alpha_i\, k(x_i, x_\star)$, a smooth blend that leans on nearby observations — so the [matrix inverse](matrix-inverse-and-determinant.md) does the interpolating.
The posterior covariance *starts* from the prior covariance $K_{\star\star}$ and *subtracts* what the data explain, so uncertainty shrinks near observations and returns to the prior far from them.
Setting the observation noise $\sigma_n^2$ to zero forces the posterior mean through every data point exactly; a positive $\sigma_n^2$ lets the mean pass smoothly near noisy points instead of chasing each one.
This is Bayesian [inference](bayesian-inference.md) with the GP as a prior over functions, and it generalizes [linear regression](linear-regression.md): a GP with a linear kernel reproduces Bayesian linear regression exactly, while richer kernels buy nonlinearity for free.

## The kernel and its hyperparameters

The kernel is where modelling choices live, because it dictates how function values borrow strength from one another.
A ubiquitous default is the **radial basis function** (RBF, or squared-exponential) kernel \[ k(x,x') = \sigma_f^2 \exp\!\left(-\frac{(x-x')^2}{2\ell^2}\right), \] governed by two **hyperparameters**.
The **lengthscale** $\ell$ sets the distance over which the function stays correlated: small $\ell$ yields wiggly functions that turn over quickly, large $\ell$ yields gently varying ones.
The **signal variance** $\sigma_f^2$ sets the marginal amplitude, the typical vertical spread of the function around its mean.
Alongside the kernel sits the **noise variance** $\sigma_n^2$, which separates genuine signal from observation error.

Different kernels encode different beliefs — smoothness, periodicity, roughness — and they can be added or multiplied to combine structure.
This page keeps the kernel light on purpose; for the Matérn family, periodic and rational-quadratic kernels, and the rules for composing them, see the dedicated [covariance functions](covariance-functions.md) page.

## Marginal likelihood and fitting hyperparameters

The hyperparameters $\theta = (\ell, \sigma_f^2, \sigma_n^2)$ are not guessed but *learned* from data by maximizing the **marginal likelihood** — the probability of the observed outputs with the latent function integrated out.
Because everything is Gaussian, this integral is available in closed form: \[ \log p(\mathbf y \mid X, \theta) = -\tfrac12\,\mathbf y^\top K_y^{-1}\mathbf y \;-\; \tfrac12 \log\lvert K_y\rvert \;-\; \tfrac{n}{2}\log 2\pi, \] where $K_y = K + \sigma_n^2 I$ is the noisy covariance matrix and $\lvert K_y\rvert$ is its [determinant](matrix-inverse-and-determinant.md).
The three terms trade off against each other and give hyperparameter fitting its self-regularizing character: the $-\tfrac12\mathbf y^\top K_y^{-1}\mathbf y$ term rewards a model that fits the data, the $-\tfrac12\log\lvert K_y\rvert$ term penalizes overly flexible (complex) models, and the constant just normalizes.
Maximizing this objective over $\theta$ — typically by gradient ascent, since the gradients are also closed-form — automatically balances fit against complexity, so a GP tends to choose a sensible lengthscale rather than overfitting.

## Computational cost

The price of this flexibility is that every prediction and every likelihood evaluation needs $(K + \sigma_n^2 I)^{-1}$, or more stably its Cholesky factor, for an $n\times n$ matrix built from $n$ training points.
That factorization costs $\mathcal O(n^3)$ time and $\mathcal O(n^2)$ memory, which is comfortable for thousands of points but prohibitive for millions.
Scaling GPs to large $n$ is an active field; a common route is a basis-function approximation such as the [Hilbert-space GP](hilbert-space-gp.md), which reduces the cost to roughly linear in $n$.

## A worked example

Take two training points $x_1 = 0$ and $x_2 = 1$ with noisy observations $y_1 = 1$ and $y_2 = 2$, an RBF kernel with $\ell = 1$ and $\sigma_f^2 = 1$, and noise variance $\sigma_n^2 = 0.1$.
We want the posterior at the test point $x_\star = 0.5$.
The kernel entries use $k(x,x') = \exp\!\bigl(-\tfrac12(x-x')^2\bigr)$, so $k(0,1) = e^{-0.5} = 0.6065$ and $k(0.5,0) = k(0.5,1) = e^{-0.125} = 0.8825$.
The noisy training covariance is \[ K_y = \begin{bmatrix} 1 & 0.6065 \\ 0.6065 & 1 \end{bmatrix} + 0.1\,I = \begin{bmatrix} 1.1 & 0.6065 \\ 0.6065 & 1.1 \end{bmatrix}, \] with determinant $1.1^2 - 0.6065^2 = 0.8421$.
Solving $K_y\boldsymbol\alpha = \mathbf y$ gives the weights $\boldsymbol\alpha = (-0.1343,\ 1.8922)^\top$.
The cross-covariance to the test point is $K_\star = (0.8825,\ 0.8825)^\top$, so the posterior mean is \[ \bar f_\star = K_\star^\top\boldsymbol\alpha = 0.8825\,(-0.1343 + 1.8922) = 1.55. \] The posterior variance is $\Sigma_\star = 1 - K_\star^\top K_y^{-1} K_\star = 1 - 0.913 = 0.087$, a standard deviation of about $0.30$.
So the GP predicts $f(0.5) \approx 1.55 \pm 0.30$: sensibly between the two observations, with moderate uncertainty because $x_\star$ sits in the gap where neither point pins it down tightly.

## In code

### R

```r
# The GauPro and DiceKriging packages fit GPs directly; here GauPro on 1D data.
library(GauPro)
set.seed(1)
x <- matrix(c(0, 1), ncol = 1)
y <- c(1, 2)

gp <- GauPro(x, y, kernel = "matern52", nug = 0.1)  # nugget = noise variance
pred <- gp$predict(matrix(0.5, ncol = 1), se.fit = TRUE)
pred$mean            # posterior mean at x* = 0.5
pred$se              # posterior standard deviation
```

### Python

```python
import numpy as np
from scipy.linalg import cho_factor, cho_solve

rng = np.random.default_rng(0)

def rbf(a, b, ell=1.0, sf2=1.0):                 # RBF / squared-exponential kernel
    d2 = (a[:, None] - b[None, :]) ** 2
    return sf2 * np.exp(-0.5 * d2 / ell ** 2)

X = np.array([0.0, 1.0])                         # training inputs
y = np.array([1.0, 2.0])                         # noisy observations
sn2 = 0.1                                         # noise variance
Xs = np.array([-0.5, 0.5, 1.5])                  # test inputs

L = cho_factor(rbf(X, X) + sn2 * np.eye(len(X)))  # Cholesky of K + sn2 I
alpha = cho_solve(L, y)                            # weights (K + sn2 I)^-1 y
Ks = rbf(Xs, X)
mean = Ks @ alpha
cov = rbf(Xs, Xs) - Ks @ cho_solve(L, Ks.T)       # posterior covariance
sd = np.sqrt(np.diag(cov))
for xi, mi, si in zip(Xs, mean, sd):
    print(f"x*={xi:+.1f}  mean={mi:.3f}  sd={si:.3f}")
print("posterior draw:", np.round(rng.multivariate_normal(mean, cov), 3))
```

<!-- python-output:auto -->
```text
x*=-0.5  mean=0.496  sd=0.508
x*=+0.5  mean=1.551  sd=0.295
x*=+1.5  mean=1.626  sd=0.508
posterior draw: [0.511 1.744 1.551]
```
<!-- /python-output:auto -->

### Julia

```julia
# GaussianProcesses.jl provides kernels, exact inference, and hyperparameter fits.
using GaussianProcesses, Random
Random.seed!(1)
x = [0.0, 1.0]                       # training inputs
y = [1.0, 2.0]                       # observations

kern = SE(0.0, 0.0)                  # RBF kernel: log lengthscale, log signal sd
gp = GP(x, y, MeanZero(), kern, log(sqrt(0.1)))   # last arg: log noise sd
mu, sig2 = predict_y(gp, [0.5])      # posterior mean and variance at x* = 0.5

optimize!(gp)                        # maximize the marginal likelihood
```

## Why it matters

A Gaussian process is the natural tool whenever you need predictions *and* honest uncertainty from limited, expensive data.
In computer experiments it serves as an **emulator** (or surrogate): fit a GP to a handful of runs of a slow mechanistic simulator — an agent-based epidemic model, a climate model — and the cheap posterior mean stands in for the simulator, while the variance flags where another expensive run would most reduce ignorance, the engine behind Bayesian optimization and calibration.
In spatial statistics the same mathematics is **[kriging](kriging.md)**: interpolate a disease rate, a pollutant, or a soil property across a landscape from scattered measurements, with the posterior variance mapping where the interpolation is trustworthy.
In time series, GPs model smooth trends and periodic seasonality with kernels that add and multiply, giving forecasts with growing error bars into the future.
Across all three the appeal is the same — a flexible, nonparametric fit that never forgets to tell you how much it does not know.

## Related

- [The Normal Distribution](normal-distribution.md)
- [Matrix Notation](matrix-notation.md)
- [Matrix Inverse and Determinant](matrix-inverse-and-determinant.md)
- [Bayesian Inference](bayesian-inference.md)
- [Linear Regression](linear-regression.md)
- [Covariance Functions](covariance-functions.md)
- [Kriging](kriging.md)
- [Hilbert-Space Gaussian Processes](hilbert-space-gp.md)
- [Quantitative Methods](../math.md)
