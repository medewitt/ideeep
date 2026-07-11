---
title: "Adaptive Dynamics and the Evolution of Virulence"
---

# Adaptive Dynamics and the Evolution of Virulence

Why doesn't natural selection make every pathogen either perfectly benign or maximally deadly?
The answer is a trade-off: the very transmission that spreads a pathogen is often tied to the harm it does its host, and selection settles on an intermediate, optimal virulence.

![Left: with a saturating trade-off β(α) = a√α, R₀(α) rises then falls and peaks at an intermediate optimum α* = γ + μ = 0.6, beating both a more benign (α = 0.2) and a more aggressive (α = 1.5) strain. Right: the pairwise-invasibility plot for the same model shades where a mutant strain can invade the resident; the singular strategy at α* is an ESS because its entire vertical line lies outside the invasion region.](../assets/figures/evolution-of-virulence.svg "fig:virulence")

## Adaptive dynamics and invasion fitness

**Adaptive dynamics** studies long-term evolution as a sequence of rare mutants trying to invade a resident population sitting at its ecological equilibrium.
The key quantity is **invasion fitness**: the per-capita growth rate of a rare mutant strain in the environment set by the resident.
If invasion fitness is positive the mutant spreads and may replace the resident; if negative it dies out.
Evolution proceeds as a succession of successful invasions that gradually change the trait — here, the pathogen's virulence.

For a pathogen introduced into a susceptible host population, invasion fitness is governed by the basic reproduction number: a mutant strain invades the resident's disease-free environment exactly when its own $R_0$ exceeds one, so **selection favours the strain with the largest $R_0$**.

## The transmission–virulence trade-off

Consider a standard [SIR](sir.md)-type infection with transmission rate $\beta$, recovery rate $\gamma$, disease-induced host mortality (virulence) $\alpha$, and background mortality $\mu$.
An infected host stays infectious for an average duration $1/(\gamma + \alpha + \mu)$, and transmits at rate $\beta$ throughout, so

\[
R_0(\alpha) = \frac{\beta(\alpha)}{\gamma + \alpha + \mu}.
\]

The crucial biological assumption is that transmission is not free: higher $\beta$ requires higher pathogen replication, which also raises host mortality $\alpha$.
We encode this as an increasing, decelerating **trade-off function** $\beta(\alpha)$.
Now virulence faces opposing pressures.
Raising $\alpha$ increases the numerator $\beta(\alpha)$, but it also shortens the infectious period $1/(\gamma+\alpha+\mu)$ in the denominator by killing the host sooner.
The pathogen "wants" high transmission but not at the price of a host that dies before infecting others, so the strain that maximises $R_0(\alpha)$ has some **intermediate optimal virulence** $\alpha^*$ — neither the avirulence of $\alpha \to 0$ nor unbounded harm.

## Singular strategies and invasibility

The value $\alpha^*$ that maximises $R_0$ is a **singular strategy** of the adaptive dynamics, found by setting $\mathrm{d}R_0/\mathrm{d}\alpha = 0$.
Finding it is an [optimization](optimization.md) problem, and because the winning strain is simply the one with the highest $R_0$, this optimum is both an ESS (uninvadable once established) and an attractor of the evolutionary dynamics.
Adaptive-dynamics analyses visualise this with a **pairwise-invasibility plot (PIP)** ([@fig:virulence]): for every resident trait on one axis and mutant trait on the other, the plot shades where a mutant can invade.
An evolutionarily stable $\alpha^*$ appears where no nearby mutant can invade the resident — the resident's row lies entirely outside the invasion region.

## Worked example: an optimal virulence

Take the common phenomenological trade-off $\beta(\alpha) = a\sqrt{\alpha}$, so that transmission rises with virulence but with diminishing returns.
Then

\[
R_0(\alpha) = \frac{a\sqrt{\alpha}}{\gamma + \alpha + \mu}.
\]

Write $d = \gamma + \mu$ and differentiate.
Using the quotient rule,

\[
\frac{\mathrm{d}R_0}{\mathrm{d}\alpha}
= a\,\frac{\tfrac{1}{2}\alpha^{-1/2}(\alpha + d) - \alpha^{1/2}}{(\alpha + d)^2}.
\]

The denominator is always positive, so the optimum occurs where the numerator vanishes: $\tfrac{1}{2}\alpha^{-1/2}(\alpha + d) = \alpha^{1/2}$, i.e. $\alpha + d = 2\alpha$, giving

\[
\alpha^* = d = \gamma + \mu.
\]

The optimal virulence equals the host's total background loss rate (recovery plus natural death): the pathogen should harm its host at roughly the rate the host would leave the infectious pool anyway.
With $\gamma = 0.5$, $\mu = 0.1$, and $a = 3$, we get $\alpha^* = 0.6$ and $R_0(\alpha^*) = 3\sqrt{0.6}/1.2 \approx 1.94$, higher than the $R_0$ of a more benign ($\alpha = 0.2$, $R_0 \approx 1.68$) or more aggressive ($\alpha = 1.5$, $R_0 \approx 1.75$) strain.

## Simulation

We compute $R_0(\alpha)$ across a range of virulence and locate the optimum numerically, confirming $\alpha^* = \gamma + \mu = 0.6$.

### R

```r
gamma <- 0.5; mu <- 0.1; a <- 3
R0 <- function(alpha) a * sqrt(alpha) / (gamma + alpha + mu)

opt <- optimize(R0, c(1e-6, 10), maximum = TRUE)
opt$maximum     # ~0.6  = gamma + mu
opt$objective   # ~1.936

curve(R0, 0, 3, xlab = "virulence alpha", ylab = "R0")
abline(v = gamma + mu, lty = 2)
```

### Python

```python
import numpy as np
from scipy.optimize import minimize_scalar

gamma, mu, a = 0.5, 0.1, 3.0
R0 = lambda al: a * np.sqrt(al) / (gamma + al + mu)

res = minimize_scalar(lambda al: -R0(al), bounds=(1e-6, 10), method="bounded")
print(res.x, R0(res.x))    # ~0.6 (= gamma + mu), ~1.936
```

<!-- python-output:auto -->
```text
0.6000014256626104 1.9364916731023418
```
<!-- /python-output:auto -->

### Julia

```julia
using Optim

γ, μ, a = 0.5, 0.1, 3.0
R0(α) = a * sqrt(α) / (γ + α + μ)

res = optimize(α -> -R0(α), 1e-6, 10.0)   # Brent's method on the interval
Optim.minimizer(res)     # ~0.6 = γ + μ
-Optim.minimum(res)      # ~1.936
```

## Why it matters

The trade-off theory of virulence explains why pathogens are neither harmless nor uniformly lethal, and it warns that interventions can shift the optimum: imperfect vaccines, treatments that extend the infectious period, or crowding that eases transmission can all select for higher virulence.
It rests on computing and maximising $R_0$ — the same threshold that, in structured host populations, is obtained as the dominant eigenvalue of the [next-generation matrix](next-generation-matrix.md) — and it links pathogen evolution to broader [evolutionary game theory](evolutionary-game-theory.md), since competing strains playing off transmission against host survival mirror the frequency-dependent contests and [competition for coexistence](competition-coexistence.md) seen throughout ecology.

## Related

- [Evolutionary Game Theory](evolutionary-game-theory.md)
- [Compartmental Models (SIR)](sir.md)
- [The Next-Generation Matrix and R₀](next-generation-matrix.md)
- [Optimization](optimization.md)
- [Competition and Coexistence](competition-coexistence.md)
- [Life-History Theory](life-history-theory.md) — the trade-off logic behind optimal virulence generalized to schedules of survival and reproduction
- [Multi-Scale (Nested) Models](../epidemiology/nested-models.md) — linking within-host replication to the between-host transmission–virulence trade-off
- [The Evolutionary Emergence of Pathogens](../epidemiology/evolutionary-emergence.md) — how a spillover strain adapts across the $R_0 = 1$ threshold to establish in a new host
- [Quantitative Methods](../math.md)
