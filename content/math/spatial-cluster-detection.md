---
title: "Spatial Cluster Detection"
description: "Testing whether disease is spatially clustered rather than random: global autocorrelation with Moran's I and Geary's C, local indicators (LISA), and Kulldorff's spatial scan statistic, all judged against a null of constant risk by permutation."
---

# Spatial Cluster Detection

A map of case counts almost always looks lumpy, but lumpiness alone proves nothing.
The question cluster detection answers is whether the pattern is more aggregated than you would expect if risk were constant and cases fell independently across the map.
The tools split into three jobs: measuring overall clustering with a single global statistic, pointing to *where* the clusters sit with local indicators, and testing a specific candidate cluster with a scan statistic.

![Left: a lattice of areal units with a planted high-risk cluster and the rook adjacency of one unit sketched in. Right: the Moran scatterplot of each unit's standardized risk against the average of its neighbors, whose slope is Moran's I.](../assets/figures/spatial-cluster-detection.svg)

## The null: complete spatial randomness

Every test needs a reference pattern that means "no clustering."
For point locations that reference is [complete spatial randomness](spatial-point-processes.md), a homogeneous Poisson process where events fall independently and uniformly.
For areal counts aggregated to regions the analogous null is **constant risk**: each unit's count is what you would get by allocating cases to units in proportion to their population at risk, with no extra spatial structure.
Under that null the observed values are exchangeable across units up to their expected counts, which is exactly what a permutation test exploits: reshuffle the values across the map many times and see where the observed statistic lands in the reshuffled distribution.

## Global autocorrelation: Moran's I

**Moran's I** measures whether nearby units carry similar values.
Attach a spatial weight $w_{ij}$ to each pair of units, large when $i$ and $j$ are neighbors and zero otherwise, exactly the [adjacency matrix](areal-models-car.md) of the region graph.
With values $x_i$, mean $\bar{x}$, and total weight $W = \sum_{i}\sum_{j} w_{ij}$, the statistic is \[ I = \frac{n}{W}\,\frac{\sum_{i}\sum_{j} w_{ij}\,(x_i - \bar{x})(x_j - \bar{x})}{\sum_{i}(x_i - \bar{x})^2}, \] a spatial correlation coefficient whose numerator is a weighted covariance between each unit and its neighbors and whose denominator is the ordinary variance.
Under the constant-risk null its expectation is slightly negative, $\mathbb{E}[I] = -1/(n-1)$, not zero, because each unit is excluded from its own neighborhood.
Values well above that expectation signal positive autocorrelation, similar values sitting together, which is the areal signature of clustering; values below it signal a checkerboard where neighbors are dissimilar.

The **Moran scatterplot** makes this visual.
Plot each unit's standardized value $z_i$ against its **spatial lag** $(Wz)_i$, the average of its neighbors' standardized values under row-standardized weights.
The slope of the fitted line through that cloud is Moran's I, so a steep positive slope is a picture of clustering.

### Geary's C

**Geary's C** is a close relative that works with squared differences between neighbors rather than cross-products, \[ C = \frac{(n-1)}{2W}\,\frac{\sum_{i}\sum_{j} w_{ij}\,(x_i - x_j)^2}{\sum_{i}(x_i - \bar{x})^2}, \] and it sits near $1$ under the null, drops below $1$ for positive autocorrelation, and rises above $1$ for negative autocorrelation, running opposite to Moran's I in sign.
Geary's C weights differences between close neighbors more heavily, while Moran's I responds to the broad pattern, and in practice the two usually agree, with Moran's I reported more often.

## Local indicators: LISA

A single global number can hide as much as it reveals.
A map can be strongly clustered in one corner and random everywhere else, yet report only a middling global value.
**Local indicators of spatial association (LISA)** decompose the global statistic into a contribution from each unit.
The **local Moran's I** for unit $i$ is \[ I_i = \frac{(x_i - \bar{x})}{\tfrac{1}{n}\sum_{k}(x_k - \bar{x})^2}\,\sum_{j} w_{ij}\,(x_j - \bar{x}), \] and the local statistics sum, up to a constant, back to the global statistic.
A large positive $I_i$ marks a unit whose own value and its neighbors' values are both far from the mean in the same direction, a high-high hot spot or a low-low cold spot; a large negative $I_i$ marks a spatial outlier surrounded by unlike neighbors.
Each $I_i$ is tested against its own permutation null, so LISA both locates candidate clusters and labels their type.

## The spatial scan statistic

Moran's I asks whether clustering exists; **Kulldorff's spatial scan statistic** asks where the single most likely cluster is and whether it is significant.
Slide a scanning window, usually a circle centered on each unit and grown through a range of radii, across the map.
For each candidate window $Z$, compare a model where risk inside differs from risk outside against a model of constant risk everywhere, using a likelihood ratio.
For Poisson counts with $c$ cases and $\mu$ expected cases inside the window, out of $C$ and $\mu_{\text{tot}}$ overall, the ratio is \[ \mathrm{LR}(Z) \propto \left(\frac{c}{\mu}\right)^{c}\left(\frac{C-c}{\mu_{\text{tot}}-\mu}\right)^{C-c} \quad\text{whenever}\quad \frac{c}{\mu} > \frac{C-c}{\mu_{\text{tot}}-\mu}, \] that is, only for windows with elevated internal risk.
The window with the largest ratio is the **most likely cluster**.
Its significance cannot be read from a chi-square table, because scanning many overlapping windows and keeping the maximum is a severe multiple-testing problem; instead the whole scan is repeated on many datasets simulated under constant risk, and the observed maximum is compared to the distribution of maxima from those simulations.
That Monte Carlo p-value already accounts for all the windows examined.

## A worked example

Take a $6\times 6$ lattice of areal units with **rook** adjacency, so each interior unit has four neighbors sharing an edge.
Plant a $2\times 2$ high-risk block in one corner by adding a constant to those four units, on top of a flat noisy background.
Compute Moran's I on the resulting surface, then build its null distribution by permuting the values across the $36$ units thousands of times and recomputing I each time.
Because the corner block makes several pairs of neighbors simultaneously high, the observed I lands far to the right of the permutation null, and the permutation p-value is small: the map is more clustered than constant risk would produce.
The expected I under the null is $-1/(n-1) = -1/35 \approx -0.029$, which the permutation mean recovers.

## In code

### R

```r
library(spdep)   # areal autocorrelation and LISA
library(sf)

# nb: a neighbours list (e.g. from poly2nb on region polygons)
# risk: a numeric vector of per-region values (rates, SMRs, residuals)
lw <- nb2listw(nb, style = "W")            # row-standardised weights

moran.test(risk, lw)                        # global Moran's I + p-value
geary.test(risk, lw)                        # Geary's C
moran.plot(risk, lw)                        # the Moran scatterplot

lisa <- localmoran(risk, lw)                # per-region local Moran's I
head(lisa)                                  # Ii, expectation, variance, p

# Kulldorff spatial scan statistic (Poisson model) via SpatialEpi
library(SpatialEpi)
scan <- kulldorff(geo = centroids, cases = y, population = pop,
                  expected.cases = E, pop.upper.bound = 0.5,
                  n.simulations = 999, alpha.level = 0.05)
scan$most.likely.cluster
```

### Python

Build a rook-adjacency weight matrix on a small lattice, compute Moran's I for a surface with a corner cluster, and test it against a permutation null.

```python
import numpy as np

rng = np.random.default_rng(1834)

# A 6x6 lattice of areal units with rook (shared-edge) adjacency.
side = 6
coords = [(r, c) for r in range(side) for c in range(side)]
n = len(coords)
W = np.zeros((n, n))
for i, a in enumerate(coords):
    for j, b in enumerate(coords):
        if i != j and abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1:
            W[i, j] = 1.0

# Risk surface: flat noisy background plus a 2x2 high-risk corner cluster.
risk = rng.normal(0.0, 0.4, size=n)
for i, (r, c) in enumerate(coords):
    if r < 2 and c < 2:
        risk[i] += 2.5


def morans_i(x):
    z = x - x.mean()
    return (n / W.sum()) * (z @ W @ z) / (z @ z)


i_obs = morans_i(risk)

# Permutation null: reshuffle values across units (constant-risk null).
perm = np.array([morans_i(rng.permutation(risk)) for _ in range(999)])
p_value = (1 + (perm >= i_obs).sum()) / (1 + len(perm))

print(f"Moran's I    = {i_obs:.3f}")
print(f"null mean    = {perm.mean():.3f}  (expected -1/(n-1) = {-1/(n-1):.3f})")
print(f"perm p-value = {p_value:.4f}")
```

<!-- python-output:auto -->
```text
Moran's I    = 0.481
null mean    = -0.028  (expected -1/(n-1) = -0.029)
perm p-value = 0.0010
```
<!-- /python-output:auto -->

### Julia

```julia
using Statistics, Random
Random.seed!(1834)

# 6x6 lattice with rook adjacency.
side = 6
coords = [(r, c) for r in 0:side-1 for c in 0:side-1]
n = length(coords)
W = zeros(n, n)
for i in 1:n, j in 1:n
    a, b = coords[i], coords[j]
    if i != j && abs(a[1] - b[1]) + abs(a[2] - b[2]) == 1
        W[i, j] = 1.0
    end
end

risk = 0.4 .* randn(n)
for (i, (r, c)) in enumerate(coords)
    (r < 2 && c < 2) && (risk[i] += 2.5)
end

morans_i(x) = (n / sum(W)) * ((x .- mean(x))' * W * (x .- mean(x))) /
              sum((x .- mean(x)).^2)

i_obs = morans_i(risk)
perm = [morans_i(shuffle(risk)) for _ in 1:999]
p = (1 + count(>=(i_obs), perm)) / (1 + length(perm))
println("Moran's I = ", round(i_obs, digits = 3), "  p = ", round(p, digits = 4))
```

## Why it matters

Cluster detection is the front line of disease surveillance.
Health departments run scan statistics on incoming case data to flag emerging outbreaks, and global and local autocorrelation statistics turn a noisy incidence map into a defensible claim that risk is genuinely aggregated somewhere specific rather than scattered by chance.
The permutation and Monte Carlo machinery matters because spatial data violate the independence that classical tests assume, and scanning many windows inflates false positives unless the search itself is built into the null.
Once a cluster is confirmed, the natural next step is to model the whole risk surface with an [areal model](areal-models-car.md) or a [point-process](spatial-point-processes.md) intensity, and to ask whether the cluster persists, moves, or grows over time with a [spatiotemporal model](spatiotemporal-models.md).

## Related

- [Areal Models: CAR, ICAR, and BYM](areal-models-car.md)
- [Spatial Point Processes](spatial-point-processes.md)
- [Distances on a Sphere: Haversine and Beyond](distance-measures.md)
- [Spatiotemporal Models](spatiotemporal-models.md)
- [Quantitative Methods](../math.md)
