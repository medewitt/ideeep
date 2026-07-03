---
title: "Pharmacodynamics: Dose–Response"
---

# Pharmacodynamics: Dose–Response

Pharmacodynamics (PD) is what the drug does to the body — the quantitative relationship between drug concentration and the size of its effect.
Where [pharmacokinetics](pharmacokinetics.md) tells us the concentration over time, PD converts that concentration into an effect, and for antimicrobials the "effect" is the rate at which bacteria are killed.

![Sigmoid $E_{max}$ (Hill) dose–response curves for increasing Hill coefficients.](../assets/figures/pharmacodynamics.svg)

## The $E_{max}$ model

Almost every dose–response relationship saturates: doubling the concentration does not double the effect once receptors approach full occupancy.
The workhorse **$E_{max}$ model** captures this with a rectangular hyperbola:

\[
E = E_0 + \frac{E_{max}\, C}{EC_{50} + C}
\]

Here $E_0$ is the baseline effect with no drug, $E_{max}$ is the maximal drug-induced effect (efficacy), and $EC_{50}$ is the concentration producing half of $E_{max}$ (potency).
As $C \to \infty$ the effect approaches $E_0 + E_{max}$, and at $C = EC_{50}$ it sits exactly halfway.

## The sigmoid $E_{max}$ (Hill) model

Many systems respond more steeply than a simple hyperbola because of cooperativity or multi-step binding.
Adding a **Hill coefficient** $h$ produces the sigmoid $E_{max}$ model (writing the baseline as zero for clarity):

\[
E = \frac{E_{max}\, C^{h}}{EC_{50}^{h} + C^{h}}
\]

The exponent $h$ controls steepness: $h = 1$ recovers the plain hyperbola, $h > 1$ gives a switch-like S-curve, and $h < 1$ a shallow one.
Plotted against $\log C$ — the natural axis for dose–response, since concentrations span orders of magnitude — the curve is a symmetric sigmoid centered on $\log EC_{50}$, a shape you may recognize from [functions and graphs](functions-and-graphs.md) and from the [logistic curve](logistic-growth.md).

## Solving for a target effect

Because the Hill equation is invertible, we can find the concentration producing any fractional effect.
Setting $E/E_{max} = p$ and solving,

\[
C_p = EC_{50}\left(\frac{p}{1-p}\right)^{1/h}
\]

so the concentration for 90% of maximal effect is $EC_{90} = EC_{50}\,(9)^{1/h}$.
When $h=1$ this means $EC_{90}$ is nine times $EC_{50}$; a steep curve with large $h$ narrows that gap dramatically.

## Worked example

Suppose an antibiotic has $E_{max} = 4\ \mathrm{h^{-1}}$ (maximal kill rate), $EC_{50} = 2\ \mathrm{mg/L}$, and Hill coefficient $h = 2$.

At a concentration $C = 4\ \mathrm{mg/L}$ the effect is

\[
E = \frac{4 \times 4^{2}}{2^{2} + 4^{2}} = \frac{4 \times 16}{4 + 16} = \frac{64}{20} = 3.2\ \mathrm{h^{-1}}
\]

i.e. 80% of the maximal kill rate.
The concentration for 90% of maximum is

\[
EC_{90} = EC_{50}\,(9)^{1/h} = 2 \times 9^{1/2} = 2 \times 3 = 6\ \mathrm{mg/L}
\]

Because $h=2$, tripling the concentration from $EC_{50}$ takes the effect from 50% to 90% — steeper than the ninefold factor a hyperbola would require.

## In code

We plot the Hill curve and then recover its parameters by nonlinear least squares from noisy data — the estimation problem at the heart of [optimization](optimization.md).

### R

```r
Emax <- 4; EC50 <- 2; h <- 2
hill <- function(C, Emax, EC50, h) Emax * C^h / (EC50^h + C^h)

set.seed(1)
C <- c(0.25, 0.5, 1, 2, 4, 8, 16)
y <- hill(C, Emax, EC50, h) + rnorm(length(C), 0, 0.1)

fit <- nls(y ~ Emax * C^h / (EC50^h + C^h),
           start = list(Emax = 3, EC50 = 1, h = 1))
coef(fit)                       # ~ Emax 4, EC50 2, h 2
hill(4, Emax, EC50, h)          # 3.2 : effect at C = 4
```

### Python

```python
import numpy as np
from scipy.optimize import curve_fit

Emax, EC50, h = 4.0, 2.0, 2.0
hill = lambda C, Emax, EC50, h: Emax * C**h / (EC50**h + C**h)

rng = np.random.default_rng(1)
C = np.array([0.25, 0.5, 1, 2, 4, 8, 16])
y = hill(C, Emax, EC50, h) + rng.normal(0, 0.1, C.size)

p, _ = curve_fit(hill, C, y, p0=[3, 1, 1])
print(p)                        # ~ [4, 2, 2]
print(hill(4, *p))              # ~3.2 : effect at C = 4
```

<!-- python-output:auto -->
```text
[4.02057431 2.02736333 1.98503466]
3.1921646202469307
```
<!-- /python-output:auto -->

### Julia

```julia
using LsqFit

Emax, EC50, h = 4.0, 2.0, 2.0
hill(C, p) = @. p[1] * C^p[3] / (p[2]^p[3] + C^p[3])

C = [0.25, 0.5, 1, 2, 4, 8, 16]
y = hill(C, [Emax, EC50, h]) .+ 0.1 .* randn(length(C))

fit = curve_fit(hill, C, y, [3.0, 1.0, 1.0])
fit.param                       # ~ [4, 2, 2]
hill([4.0], [Emax, EC50, h])[1] # 3.2 : effect at C = 4
```

## Why it matters

The Hill curve is the bridge from a measured concentration to a predicted bacterial kill rate, and its two key numbers have direct clinical meaning: $E_{max}$ says how good a drug can be, $EC_{50}$ says how much you need.
Coupling this dose–response with the time-varying concentration from pharmacokinetics is precisely what defines the [PK/PD indices](antimicrobial-pkpd.md) used to design antibiotic regimens.

## Related

- [Pharmacokinetics: Compartment Models](pharmacokinetics.md)
- [Antimicrobial PK/PD](antimicrobial-pkpd.md)
- [Functions and Graphs](functions-and-graphs.md) — the sigmoid shape
- [Logistic Growth](logistic-growth.md) — the same S-curve algebra
- [Optimization](optimization.md) — least-squares curve fitting
- [Quantitative Methods](../math.md)
