---
title: "Distances on a Sphere: Haversine and Beyond"
description: "Why Euclidean distance on latitude/longitude is wrong, and how the haversine, spherical, and ellipsoidal formulas measure distance on the Earth's surface."
---

# Distances on a Sphere: Haversine and Beyond

Almost every spatial analysis begins by measuring how far apart two points are, and on the Earth's surface that innocent-looking step hides a trap.
Latitude and longitude are angles, not lengths, so treating them as if they were Cartesian coordinates and reaching for the Pythagorean theorem gives an answer that can be off by tens of percent.
This page builds up the right way to measure distance on a globe — the great-circle distance and the numerically stable haversine formula — then works through the cheaper approximations, the high-accuracy ellipsoidal geodesics, and when a flat projection is good enough.

![A great-circle path between New York and London curves across an equirectangular lat/long grid, unlike the straight coordinate segment; the relative error of the naive Euclidean-degrees and equirectangular approximations grows with separation.](../assets/figures/distance-measures.svg)

## Why latitude and longitude are not equal distances

A degree of latitude is very nearly a constant length: meridians are (almost) great circles, so one degree spans about $111\ \text{km}$ everywhere from the equator to the poles.
A degree of longitude is not.
Lines of longitude converge as they climb toward the poles, so the east–west ground distance covered by one degree of longitude shrinks with latitude as $$\Delta x \approx 111\ \text{km} \times \cos\varphi \times \Delta\lambda_{\text{deg}},$$ where $\varphi$ is the latitude and $\Delta\lambda_{\text{deg}}$ the longitude difference in degrees.
At the equator a degree of longitude is a full $111\ \text{km}$; at $\varphi = 60^\circ$ it is only $\cos 60^\circ = \tfrac12$ of that, about $55\ \text{km}$; at the pole it collapses to zero.
Any distance formula that adds $\Delta\varphi$ and $\Delta\lambda$ as if they were the same physical unit — the naive Euclidean-on-degrees calculation — therefore overcounts east–west separation everywhere except the equator, and the error grows with latitude.

## The great-circle distance

The shortest path between two points on a sphere runs along the **great circle** through them: the intersection of the sphere with a plane through its center.
The distance is the radius times the central angle $c$ subtended by the two points, $d = R\,c$, so the whole problem reduces to finding that angle.
Writing the two points as $(\varphi_1,\lambda_1)$ and $(\varphi_2,\lambda_2)$ with $\Delta\varphi = \varphi_2-\varphi_1$ and $\Delta\lambda = \lambda_2-\lambda_1$, and taking $R \approx 6371\ \text{km}$ for the mean Earth radius, gives an exact distance on the sphere.

### The haversine formula

The haversine formula routes the central angle through an intermediate quantity $a$, computing $$a = \sin^2\!\left(\frac{\Delta\varphi}{2}\right) + \cos\varphi_1 \cos\varphi_2 \, \sin^2\!\left(\frac{\Delta\lambda}{2}\right), \qquad c = 2\,\operatorname{atan2}\!\left(\sqrt{a},\ \sqrt{1-a}\right), \qquad d = R\,c,$$ so that $a$ is the **haversine** $\operatorname{hav}(\theta) = \sin^2(\theta/2)$ of the central angle and the final step inverts it.
The name recalls that old navigational function, but the formula is prized less for elegance than for **numerical stability**.

The older spherical law of cosines, $c = \arccos\!\big(\sin\varphi_1\sin\varphi_2 + \cos\varphi_1\cos\varphi_2\cos\Delta\lambda\big)$, is algebraically equivalent but fails for nearby points: when the two points are close, the argument of $\arccos$ is extremely near $1$, where $\arccos$ has an infinite slope, so the limited precision of floating-point arithmetic produces large relative errors or even a domain error from rounding past $1$.
The haversine sidesteps this by working with $\sin^2$ of half-angles, which stay well-conditioned for small separations, and by using $\operatorname{atan2}$ rather than $\arccos$ so the result is accurate across the full range.
Haversine is the sensible default for great-circle distance on a sphere.

## Cheaper approximations and their error regimes

When speed matters more than the last kilometer, two flat approximations are common.

The **spherical law of cosines** is the same great-circle distance as haversine, just computed the unstable way; on modern double precision its answers agree with haversine to well under a meter for points more than a few meters apart, so its only real drawback is the breakdown at tiny separations.
Use it only if you are sure your points are never nearly coincident.

The **equirectangular approximation** projects the two points onto a flat plane, correcting the longitude by the cosine of the mean latitude, then applies the Pythagorean theorem, $$d \approx R\sqrt{(\Delta\varphi)^2 + \big(\cos\varphi_m \, \Delta\lambda\big)^2}, \qquad \varphi_m = \tfrac12(\varphi_1+\varphi_2),$$ with $\Delta\varphi,\Delta\lambda$ in **radians**.
This is fast — no trigonometry beyond one cosine — and accurate to a fraction of a percent for separations up to a few hundred kilometers, because over a small patch the sphere is nearly flat and the cosine factor absorbs the longitude shrink.
Its error grows with separation as the curvature of the sphere starts to matter, reaching a percent or so at continental scales.

The **naive Euclidean-on-degrees** distance drops even the cosine correction and treats $\Delta\varphi$ and $\Delta\lambda$ as equal units; as the figure shows, its error is not a rounding detail but a systematic overestimate that scales with $1-\cos\varphi$ and can exceed $40\%$ at mid-latitudes for east–west separations.
It is essentially never the right choice for real distances.

## Ellipsoidal and geodesic distances

The Earth is not a sphere: it bulges at the equator, so it is better modeled as an oblate **ellipsoid**, and the standard reference is the **WGS84** ellipsoid used by GPS, with an equatorial radius of $6378.137\ \text{km}$ and a flattening of about $1/298.257$.
The shortest path on an ellipsoid is a **geodesic**, and computing its length is harder than on a sphere because there is no single radius.
[Vincenty's algorithm](https://en.wikipedia.org/wiki/Vincenty%27s_formulae) (1975) solves it by iteration and is accurate to a fraction of a millimeter, but it converges slowly and can fail to converge for nearly antipodal points.
[Karney's algorithm](https://link.springer.com/article/10.1007/s00190-012-0578-z) (2013), implemented in the **GeographicLib** library and now the default in most geospatial toolkits, is always accurate to a few nanometers and always converges.
The sphere-versus-ellipsoid difference is real but modest: haversine on a mean-radius sphere disagrees with a WGS84 geodesic by up to about $0.3\%$, so for continental distances the two differ by a few kilometers, which matters for surveying and aviation but rarely for exploratory spatial statistics.

## Euclidean-on-a-projection: when flat is fine

None of this means you must call a geodesic routine for every pairwise distance.
If you first project your coordinates into an appropriate **planar coordinate reference system** — a UTM zone for a study area, a national grid, or an equal-area or conformal projection chosen for the region — then ordinary Euclidean distance in those projected meters is both fast and accurate, because the projection has already done the work of turning angles into lengths.
This is the standard move for a single city, county, or study site: pick a projection that minimizes distortion over that extent, and treat the plane as a plane.
The approach degrades as the area grows, because every map projection trades off distortion in distance, area, angle, or shape and none preserves all of them, so at national or continental scale the projection error catches up with you and a great-circle or geodesic distance becomes worth the cost.

## A worked example

Take New York City at $(\varphi_1,\lambda_1) = (40.7128^\circ, -74.0060^\circ)$ and London at $(\varphi_2,\lambda_2) = (51.5074^\circ, -0.1278^\circ)$.
Here $\Delta\varphi = 10.795^\circ$ and $\Delta\lambda = 73.878^\circ$, a large east–west separation at mid-latitude — exactly the regime where the cosine effect bites.
Feeding these into the haversine formula with $R = 6371\ \text{km}$ gives $a = 0.1794$, $c = 0.8748\ \text{rad}$, and a great-circle distance of $$d = 6371 \times 0.8748 \approx 5570\ \text{km},$$ which matches the familiar flight distance.
The naive Euclidean-degrees estimate instead computes $\sqrt{10.795^2 + 73.878^2} = 74.68^\circ$ of "angle" and multiplies by $111.2\ \text{km}/^\circ$ to get about $8300\ \text{km}$ — roughly $49\%$ too large, because it credits each of London's $74^\circ$ of longitude with a full equatorial degree even though at these latitudes a longitude degree is barely $70\ \text{km}$.

## In code

### R

```r
library(geosphere)

ny <- c(-74.0060, 40.7128)   # geosphere uses (lon, lat)
lon <- c(-0.1278, 51.5074)

distHaversine(ny, lon) / 1000            # great-circle km, spherical
distVincentyEllipsoid(ny, lon) / 1000    # WGS84 geodesic km

# sf works in projected or geographic CRS and picks a geodesic automatically
library(sf)
pts <- st_sfc(st_point(ny), st_point(lon), crs = 4326)
st_distance(pts)[1, 2] / 1000            # metres -> km, ellipsoidal
```

### Python

```python
import numpy as np

R = 6371.0  # mean Earth radius, km
ny  = (40.7128, -74.0060)   # (lat, lon) New York
lon = (51.5074,  -0.1278)   # (lat, lon) London

def haversine(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlam = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlam / 2) ** 2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

d = haversine(*ny, *lon)
naive = (R * np.pi / 180) * np.hypot(lon[0] - ny[0], lon[1] - ny[1])
print(f"haversine great-circle: {d:8.1f} km")
print(f"naive Euclidean-degrees:{naive:8.1f} km")
print(f"naive overestimate:     {100 * (naive - d) / d:6.1f} %")
```

<!-- python-output:auto -->
```text
haversine great-circle:   5570.2 km
naive Euclidean-degrees:  8302.1 km
naive overestimate:       49.0 %
```
<!-- /python-output:auto -->

```text
haversine great-circle:   5570.2 km
naive Euclidean-degrees:  8302.1 km
naive overestimate:        49.0 %
```

### Julia

```julia
using Distances

ny  = (40.7128, -74.0060)   # (lat, lon) New York
lon = (51.5074,  -0.1278)   # (lat, lon) London

# Haversine(radius) is a Metric; feed (lon, lat) points, in degrees
d = Haversine(6371.0)((ny[2], ny[1]), (lon[2], lon[1]))   # -> ~5570 km

# For WGS84 ellipsoidal geodesics, reach for Geodesy.jl / Proj.jl
```

## Why it matters

The distance you choose is not a formatting detail; it is an input to the model.
Spatial statistics rests on the idea that nearby observations are more alike than distant ones, and that "alike-ness" is encoded in a [covariance function](covariance-functions.md) whose only spatial argument is the distance between locations.
Feed it a distorted distance and you feed the model a distorted picture of proximity: a longitude-inflated distance makes east–west neighbors look farther apart than they are, biasing the estimated range of correlation and, through it, the interpolated surface.
The same distances drive the weights in [kriging](kriging.md) and the pairwise interactions in spatial point-process models, so an error in the distance metric propagates straight into predictions, standard errors, and inference.
On small, projected study areas Euclidean distance is fine; the moment your data span a continent or straddle high latitudes, use a great-circle or geodesic distance and let the covariance function see the geometry the Earth actually has.

## Related

- [Covariance Functions](covariance-functions.md)
- [Kriging and Spatial Interpolation](kriging.md)
- [Reaction–Diffusion and Spatial Spread](reaction-diffusion.md)
- [Quantitative Methods](../math.md)
