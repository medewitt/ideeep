---
title: "Turing Patterns"
---

# Turing Patterns

Diffusion usually smooths things out, blurring any bump back into uniformity.
Alan Turing's 1952 insight was that in a system of two interacting chemicals, diffusion can do the opposite — it can break a bland uniform state into spots and stripes, the same patterns we see on animal coats and across arid vegetation.

![A Turing pattern emerging from a near-uniform state through diffusion-driven instability (Gray–Scott model).](../assets/figures/turing-patterns.svg)

## The paradox of diffusion-driven instability

Consider two species (or morphogens) with densities $u$ and $v$ obeying the reaction–diffusion system $$\partial_t u = D_u\,\nabla^2 u + f(u,v), \qquad \partial_t v = D_v\,\nabla^2 v + g(u,v).$$ This is the two-component version of a [reaction–diffusion](reaction-diffusion.md) model, with reaction terms $f$ and $g$ and separate diffusion coefficients $D_u$ and $D_v$.
Suppose there is a spatially uniform [steady state](equilibria-and-stability.md) $(u^*,v^*)$ where $f=g=0$, and suppose it is stable when the species are well mixed (no diffusion).
Turing's surprise is that turning diffusion on can make this same state unstable, so tiny fluctuations grow into a stationary pattern.
Because the instability is created rather than cured by diffusion, it is called **diffusion-driven** (or Turing) instability.

The mechanism requires an **activator–inhibitor** structure: $u$ is a short-range activator that promotes both itself and the inhibitor $v$, while $v$ suppresses $u$.
Crucially, the inhibitor must diffuse faster than the activator, $D_v \gg D_u$.
A local bump of activator amplifies itself but also spawns inhibitor that spreads out ahead of it, quenching activation in the surroundings — "local activation, long-range inhibition" — which fixes a characteristic spacing between peaks.

## The instability conditions

Linearize the reaction terms about the steady state using the reaction [Jacobian](jacobians.md) $$J = \begin{pmatrix} f_u & f_v \\ g_u & g_v \end{pmatrix},$$ where the entries are the partial derivatives evaluated at $(u^*,v^*)$.
Stability of the well-mixed system (no diffusion) requires the trace negative and determinant positive, the standard conditions from the [eigenvalues](eigenvalues-and-eigenvectors.md) of a $2\times 2$ matrix: $$\text{(1)}\quad f_u + g_v < 0, \qquad \text{(2)}\quad f_u g_v - f_v g_u > 0.$$ Now allow a spatial perturbation proportional to $\cos(kx)$ with **wavenumber** $k$.
Each mode adds $-k^2 D_u$ and $-k^2 D_v$ to the diagonal of $J$, and instability of some mode requires two further conditions: $$\text{(3)}\quad D_v f_u + D_u g_v > 0, \qquad \text{(4)}\quad (D_v f_u + D_u g_v)^2 > 4 D_u D_v (f_u g_v - f_v g_u).$$ Condition (3) is the one that forces unequal diffusion: since (1) makes $f_u+g_v<0$, having $D_v f_u + D_u g_v>0$ demands $D_v$ and $D_u$ be sufficiently different (with the activator's self-term $f_u>0$, this means $D_v > D_u$).
Condition (4) guarantees there is actually a band of unstable wavenumbers rather than a single marginal point.

### The selected wavelength

When (1)–(4) hold, growth rate is positive over a finite band of $k$, and the fastest-growing mode $$k_c^2 = \sqrt{\frac{f_u g_v - f_v g_u}{D_u D_v}}$$ sets the dominant spacing of the pattern, wavelength $2\pi/k_c$.
Because $k_c$ depends on the diffusion coefficients but not on the size of the domain, Turing patterns have an intrinsic length scale — spots and stripes of a characteristic size, independent of how large the animal or the landscape is.

## A worked example: the generic activator–inhibitor sign pattern

For an activator–inhibitor system the Jacobian signs are typically $$J = \begin{pmatrix} + & - \\ + & - \end{pmatrix},$$ i.e. $f_u>0$ (activator self-enhances), $f_v<0$ (inhibitor suppresses activator), $g_u>0$ (activator produces inhibitor), $g_v<0$ (inhibitor self-limits).
Take $f_u=1,\ f_v=-1,\ g_u=2,\ g_v=-1.5$.
Then trace $f_u+g_v = 1-1.5 = -0.5 < 0$ satisfies (1), and determinant $f_u g_v - f_v g_u = (1)(-1.5)-(-1)(2)=0.5>0$ satisfies (2): the well-mixed state is stable.
For condition (3), $D_v f_u + D_u g_v = D_v(1) + D_u(-1.5) > 0$ needs $D_v > 1.5\,D_u$; take $D_u=1,\ D_v=20$, giving $20-1.5=18.5>0$.
Condition (4): $(18.5)^2 = 342 > 4(1)(20)(0.5)=40$, comfortably satisfied.
All four inequalities hold, so this system undergoes a Turing [bifurcation](bifurcations.md), and the fastest mode sits near $k_c^2=\sqrt{0.5/(1\cdot 20)}\approx 0.158$.

## Simulation

We integrate the Gray–Scott system, a well-known activator–inhibitor model, on a 2D grid by explicit finite differences.
Two chemicals $U$ and $V$ react as $U + 2V \to 3V$, with $V$ decaying, feed rate $F$ and kill rate $\kappa$; $V$ is the slower-diffusing activator.
Starting from the uniform state plus a small seeded square, spots and stripes emerge.

### R

```r
set.seed(1)
n <- 100; Du <- 0.16; Dv <- 0.08; F <- 0.035; k <- 0.065; dt <- 1
U <- matrix(1, n, n); V <- matrix(0, n, n)
c0 <- 45:55
V[c0, c0] <- 0.25; U[c0, c0] <- 0.5
V <- V + matrix(runif(n*n, 0, 0.01), n, n)

lap <- function(A) {            # 5-point stencil, periodic wrap
  (A[c(n,1:(n-1)),] + A[c(2:n,1),] + A[,c(n,1:(n-1))] + A[,c(2:n,1)] - 4*A)
}
for (s in 1:5000) {
  uvv <- U * V * V
  U <- U + dt * (Du*lap(U) - uvv + F*(1 - U))
  V <- V + dt * (Dv*lap(V) + uvv - (F + k)*V)
}
range(V)                        # V has organized into spots (heterogeneous)
```

### Python

```python
import numpy as np
rng = np.random.default_rng(1)
n, Du, Dv, F, k, dt = 100, 0.16, 0.08, 0.035, 0.065, 1.0
U = np.ones((n, n)); V = np.zeros((n, n))
V[45:56, 45:56] = 0.25; U[45:56, 45:56] = 0.5
V += rng.uniform(0, 0.01, (n, n))

def lap(A):                     # 5-point stencil, periodic wrap
    return (np.roll(A, 1, 0) + np.roll(A, -1, 0) +
            np.roll(A, 1, 1) + np.roll(A, -1, 1) - 4 * A)

for _ in range(5000):
    uvv = U * V * V
    U += dt * (Du * lap(U) - uvv + F * (1 - U))
    V += dt * (Dv * lap(V) + uvv - (F + k) * V)

print(V.min(), V.max())         # spread-out range: pattern of spots formed
```

### Julia

```julia
using Random
Random.seed!(1)
n, Du, Dv, F, k, dt = 100, 0.16, 0.08, 0.035, 0.065, 1.0
U = ones(n, n); V = zeros(n, n)
V[45:55, 45:55] .= 0.25; U[45:55, 45:55] .= 0.5
V .+= 0.01 .* rand(n, n)

lap(A) = circshift(A,(1,0)) .+ circshift(A,(-1,0)) .+
         circshift(A,(0,1)) .+ circshift(A,(0,-1)) .- 4 .* A

for _ in 1:5000
    uvv = U .* V .* V
    U .+= dt .* (Du .* lap(U) .- uvv .+ F .* (1 .- U))
    V .+= dt .* (Dv .* lap(V) .+ uvv .- (F + k) .* V)
end
extrema(V)                      # heterogeneous: spots/stripes have formed
```

## Why it matters

Turing patterns explain how a featureless field of cells can organize itself into structure without a pre-drawn blueprint — the central puzzle of morphogenesis.
The theory accounts for the spots on a leopard, the stripes on a zebrafish, the regular spacing of hair follicles and digits, and the striking banded and spotted vegetation of semi-arid ecosystems, where plants act as local activators competing for water that diffuses like a long-range inhibitor.
More broadly, it shows that instability and pattern can be an emergent property of coupled dynamics, a lesson that recurs whenever local reinforcement meets long-range suppression.

## Related

- [Reaction–Diffusion and Spatial Spread](reaction-diffusion.md)
- [Equilibria and Stability](equilibria-and-stability.md)
- [Jacobians](jacobians.md)
- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Bifurcations](bifurcations.md)
- [Quantitative Methods](../math.md)
