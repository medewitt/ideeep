---
title: "Areal Models: CAR, ICAR, and BYM"
description: "Modeling spatial correlation for region-aggregated data through a neighborhood graph: the CAR model, its intrinsic (ICAR) limit, the BYM decomposition, and the BYM2 reparameterization."
---

# Areal Models: CAR, ICAR, and BYM

Much epidemiological data arrives already aggregated to areal units — counts of cases per county, deaths per district, prevalence per health zone — rather than as points with coordinates.
For such data there is no continuous distance to work with, so spatial correlation is encoded instead through a **neighborhood graph**: which regions share a border.
The conditional autoregressive (CAR) family and its relatives build a spatial prior from that graph, letting each region borrow strength from its neighbors so that noisy small-area estimates are smoothed toward a coherent surface.

![Two copies of a small region graph: raw noisy region values on the left, and the same regions after CAR smoothing on the right, where neighboring regions are pulled toward one another.](../assets/figures/areal-models-car.svg)

## The neighborhood graph

Label the regions $1,\dots,n$ and record adjacency in a symmetric $n\times n$ matrix $W$ with $w_{ij}=1$ when regions $i$ and $j$ share a border and $w_{ij}=0$ otherwise (and $w_{ii}=0$).
This is exactly an [adjacency matrix](networks.md), and the areal model lives on the graph it defines.
The row sums $d_i=\sum_j w_{ij}$ are the numbers of neighbors, and collecting them on a diagonal gives the degree matrix $D=\operatorname{diag}(d_1,\dots,d_n)$.
The modeling premise is simple: **neighbors are similar**.
A spatial effect $x_i$ attached to each region should vary smoothly across the map, so adjacent regions ought to have similar values, while regions far apart in the graph are only indirectly linked.

## The conditional autoregressive (CAR) model

Rather than write down a joint distribution directly, the CAR model specifies each region's **full conditional** — the distribution of $x_i$ given every other region.
The standard proper CAR sets \[ x_i \mid x_{-i} \;\sim\; \mathrm{Normal}\!\left(\frac{\alpha \sum_j w_{ij}\,x_j}{\sum_j w_{ij}},\ \frac{\tau^2}{\sum_j w_{ij}}\right), \] so each region is pulled toward a weighted average of its neighbors, scaled by a spatial dependence parameter $\alpha\in[0,1)$, with a conditional variance that shrinks as a region gains more neighbors.
When $\alpha=0$ the regions are independent; as $\alpha\to 1$ the pull toward the neighbor mean becomes total.

By Brook's lemma these conditionals are compatible with a single multivariate [normal](normal-distribution.md) joint distribution, and its precision (inverse-covariance) matrix is \[ Q \;=\; \tau^{-2}\,(D - \alpha W). \] The precision is what makes CAR practical: $Q$ is **sparse**, with a nonzero off-diagonal entry only where two regions are neighbors, so even for thousands of regions the model stays cheap to store and factorize.
For $\alpha<1$ the matrix $D-\alpha W$ is positive definite, so $Q$ is a valid precision and the joint distribution is proper.

## The intrinsic CAR (ICAR)

Taking the limit $\alpha\to 1$ gives the **intrinsic** CAR, whose precision $Q=\tau^{-2}(D-W)$ is exactly the graph Laplacian scaled by $\tau^{-2}$.
The Laplacian has the constant vector in its null space — every row of $D-W$ sums to zero — so $Q$ is singular and the distribution is **improper**: it specifies the differences between regions but leaves the overall level undetermined.
Concretely, the ICAR density is proportional to \[ \exp\!\left(-\frac{1}{2\tau^2}\sum_{i\sim j}(x_i - x_j)^2\right), \] a penalty on squared differences across every edge $i\sim j$ of the graph, which is precisely a statement that neighbors should be similar and says nothing about where the whole surface sits.
Because the mean level floats, an ICAR term must be fitted under a **sum-to-zero constraint** $\sum_i x_i = 0$, letting a separate intercept carry the overall level.
Despite being improper as a prior, the ICAR yields a proper posterior once data anchor the level, and its smoothness penalty makes it the workhorse spatial prior for disease mapping.

## The BYM model

A spatial prior alone is too rigid: real region effects mix smooth spatial structure with unstructured, region-specific noise.
The Besag–York–Mollié (BYM) model captures both by giving each region a sum of two random effects, \[ \eta_i \;=\; u_i + v_i, \] where $u$ is an ICAR **spatial** term that borrows strength from neighbors and $v_i \sim \mathrm{Normal}(0,\sigma_v^2)$ is an independent **heterogeneity** term absorbing local overdispersion.
Fitted inside a [hierarchical model](hierarchical-models.md) — typically a Poisson [GLM](generalized-linear-models.md) for counts — BYM lets the data decide, region by region, how much of an effect is smooth spatial signal and how much is idiosyncratic noise.

### The identifiability problem and BYM2

BYM has a nagging flaw: only the sum $u_i+v_i$ is identified by the data, so the two variance parameters $\tau^2$ (spatial) and $\sigma_v^2$ (iid) trade off against each other and are hard to prior sensibly.
Worse, the ICAR precision is not scaled to a standard reference, so the same value of $\tau^2$ implies wildly different amounts of smoothing on different graphs, making priors non-transferable.
The **BYM2** parameterization of [Riebler et al. (2016)](https://doi.org/10.1177/0962280216660421) fixes both problems by writing the combined effect with a single marginal precision $\tau$ and a mixing proportion $\phi\in[0,1]$, \[ \eta \;=\; \frac{1}{\sqrt{\tau}}\left(\sqrt{\phi}\,u_\star + \sqrt{1-\phi}\,v\right), \] where $u_\star$ is a **scaled** ICAR term whose generalized variance is standardized to $1$ so that $\tau$ has the same meaning on every graph.
Now $\tau$ controls the total marginal variance while $\phi$ is an interpretable dial: $\phi=0$ is pure iid heterogeneity, $\phi=1$ is pure spatial smoothing, and values between mix them.
This clean separation lets you place principled, transferable priors — penalized-complexity priors on both $\tau$ and $\phi$ — which is why BYM2 is the recommended default in [INLA](inla.md).

## A worked example

Take four regions arranged in a chain, $1 - 2 - 3 - 4$, so regions $1$ and $4$ have one neighbor each and regions $2$ and $3$ have two.
The adjacency and degree matrices are \[ W = \begin{pmatrix} 0&1&0&0\\ 1&0&1&0\\ 0&1&0&1\\ 0&0&1&0 \end{pmatrix}, \qquad D = \begin{pmatrix} 1&0&0&0\\ 0&2&0&0\\ 0&0&2&0\\ 0&0&0&1 \end{pmatrix}. \] The proper CAR precision is then \[ Q = \tau^{-2}(D-\alpha W) = \tau^{-2}\begin{pmatrix} 1 & -\alpha & 0 & 0\\ -\alpha & 2 & -\alpha & 0\\ 0 & -\alpha & 2 & -\alpha\\ 0 & 0 & -\alpha & 1 \end{pmatrix}, \] which is tridiagonal — nonzero only on the diagonal and where regions are adjacent — exactly the sparsity that makes CAR scale.
Sending $\alpha\to1$ gives the ICAR precision $\tau^{-2}(D-W)$, whose rows each sum to zero; it is singular, confirming that the intrinsic model pins down only the differences $x_i-x_j$ and needs the constraint $\sum_i x_i=0$ to be fitted.

## In code

### R

Fit a BYM2 disease-mapping model with INLA, the most common route in practice; `CARBayes` and `nimble` offer MCMC alternatives with the same $W$.

```r
library(INLA)
# g: an adjacency graph built from a neighbour list (e.g. spdep::poly2nb -> INLA graph)
# df: one row per region with observed count y, expected count E, and region id
formula <- y ~ f(region, model = "bym2", graph = g,
                 scale.model = TRUE,             # scaled ICAR -> comparable priors
                 hyper = list(
                   prec = list(prior = "pc.prec", param = c(1, 0.01)),
                   phi  = list(prior = "pc",      param = c(0.5, 0.5))))

fit <- inla(formula, family = "poisson", E = E, data = df,
            control.predictor = list(compute = TRUE))
summary(fit)                    # posterior for precision tau and mixing phi
exp(fit$summary.fitted.values$mean)   # smoothed relative risks per region
```

### Python

Build $W$ and $D$ for the four-region chain, form the CAR precision $Q=D-\alpha W$, check the ICAR eigenvalues, and take one conditional-expectation smoothing step.

```python
import numpy as np
np.random.seed(0)

# 4-region chain 1-2-3-4
W = np.array([[0, 1, 0, 0],
              [1, 0, 1, 0],
              [0, 1, 0, 1],
              [0, 0, 1, 0]], float)
D = np.diag(W.sum(1))
alpha = 0.95
Q = D - alpha * W                       # CAR precision, tau^2 = 1

print("degrees:", W.sum(1).astype(int))
print("ICAR eigenvalues:", np.round(np.linalg.eigvalsh(D - W), 3))  # a 0 -> improper

# One CAR smoothing step: posterior mean of x given noisy y,
# with observation precision kappa and prior precision Q / tau^2.
y = np.array([2.0, 0.0, 0.0, -2.0])     # noisy region values
kappa, tau2 = 1.0, 0.3
xhat = np.linalg.solve(kappa * np.eye(4) + Q / tau2, kappa * y)
print("smoothed:", np.round(xhat, 3))   # pulled toward neighbours
```

<!-- python-output:auto -->
```text
degrees: [1 2 2 1]
ICAR eigenvalues: [0.    0.586 2.    3.414]
smoothed: [ 0.587  0.172 -0.172 -0.587]
```
<!-- /python-output:auto -->

### Julia

```julia
using LinearAlgebra, SparseArrays
# Adjacency of the 4-region chain and its degree matrix.
W = sparse([1, 2, 2, 3, 3, 4], [2, 1, 3, 2, 4, 3], 1.0, 4, 4)
D = spdiagm(0 => vec(sum(W, dims = 2)))

α, τ² = 0.95, 0.3
Q = (D - α * W) ./ τ²                    # sparse CAR precision
L = D - W                               # ICAR limit: the graph Laplacian
println(round.(eigvals(Matrix(L)), digits = 3))   # a zero -> singular, improper
```

## Why it matters

Areal models are the backbone of **disease mapping**: given observed and expected counts per region, a BYM or BYM2 model turns jumpy standardized incidence or mortality ratios into smoothed relative-risk surfaces that reveal genuine spatial pattern instead of small-sample noise.
The same machinery drives **small-area estimation** across public health and official statistics, wherever an estimate is needed for every district but each district has too few observations to stand alone.
Because the CAR prior is defined by a sparse precision, it slots naturally into fast [Bayesian](bayesian-inference.md) fitting via [INLA](inla.md) and into large hierarchical Poisson models.
When the underlying process is genuinely continuous and observed at points rather than regions, the analogous tool is [kriging](kriging.md) with a distance-based covariance instead of a graph-based precision.

## Related

- [Hierarchical (Multilevel) Models](hierarchical-models.md)
- [Bayesian Inference](bayesian-inference.md)
- [The Normal Distribution](normal-distribution.md)
- [Networks and Graphs](networks.md)
- [Integrated Nested Laplace Approximation (INLA)](inla.md)
- [Kriging and Gaussian-Process Regression](kriging.md)
- [Quantitative Methods](../math.md)
