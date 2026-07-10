---
title: "Final Size, the Herd Immunity Threshold, and Overshoot"
description: "Two consequences of R0: the final size relation that fixes the total attack rate of an epidemic, and the herd immunity threshold at which transmission turns over. Why an uncontrolled epidemic overshoots the threshold and infects more people than it needs to."
---

# Final Size, the Herd Immunity Threshold, and Overshoot

Two of the most useful results in epidemic theory follow from $R_0$ alone, without solving the dynamics in detail.
The **final size relation** fixes what fraction of the population is ultimately infected, and the **herd immunity threshold** fixes the level of immunity at which transmission stops growing.
The gap between them is the **overshoot**: an uncontrolled epidemic does not stop when it reaches herd immunity, it sails past and infects more people than were strictly needed to end it.

![Left: the final attack rate rises with R0 and always exceeds the herd immunity threshold 1 − 1/R0; the shaded gap between them is the overshoot. Right: an SIR time course at R0 = 2.5 where the susceptible fraction falls past the 1/R0 threshold down to its final value, the overshoot.](../assets/figures/final-size-and-herd-immunity.svg)

## The herd immunity threshold

In an [SIR model](sir.md), incidence grows while the effective reproduction number $R_t = R_0 S$ exceeds one, where $S$ is the susceptible fraction.
The epidemic peaks at the moment $R_0 S = 1$, that is, when the susceptible fraction has fallen to

\[ S^\* = \frac{1}{R_0}. \]

The complementary quantity, the fraction that must be immune for transmission to stop growing, is the **herd immunity threshold**,

\[ H = 1 - \frac{1}{R_0}. \]

For $R_0 = 2.5$ this is $0.6$: once 60% of the population is immune, each infection produces fewer than one successor on average and incidence turns over.
This is the number behind critical vaccination coverage — vaccinate a fraction $H$ (adjusted for vaccine efficacy) and you prevent an epidemic without anyone being infected.

## The final size relation

The threshold is where incidence peaks, not where the epidemic stops.
Infectious people are still circulating at the peak, so transmission continues and the susceptible pool keeps draining below $S^\*$.
For the closed SIR epidemic the total fraction ever infected, the **attack rate** $Z = 1 - S(\infty)$, satisfies the transcendental **final size equation**

\[ Z = 1 - e^{-R_0 Z}, \]

which has a positive solution whenever $R_0 > 1$.
It depends only on $R_0$, not on the specific rates, which is what makes it so useful: measure the growth rate, infer $R_0$, and you have the eventual attack rate before the epidemic is over.
For $R_0 = 2.5$ the solution is $Z \approx 0.89$, so about 89% of the population is infected in an uncontrolled epidemic.

:::spoiler Show where the final-size equation comes from

Work with fractions $s = S/N$ and $r = R/N$, and divide the susceptible equation by the recovered equation to eliminate time:

\[
\frac{ds}{dr} = \frac{-\beta s\,i}{\gamma\,i} = -\frac{\beta}{\gamma}\,s = -R_0\, s .
\]

This separable equation integrates to $s(t) = s(0)\,e^{-R_0[\,r(t) - r(0)\,]}$.
Take the epidemic from its start ($s(0) \approx 1$, $r(0) \approx 0$) to its end, where all infectious individuals have recovered ($i(\infty) = 0$, $r(\infty) = Z$):

\[
s(\infty) = e^{-R_0 Z} .
\]

Since $s(\infty) = 1 - Z$ (everyone is either still susceptible or has been infected), substituting gives the transcendental **final-size equation**

\[
Z = 1 - e^{-R_0 Z} .
\]

:::

## Overshoot

Now compare the two numbers.
Herd immunity is reached at $1 - S^\* = H = 0.6$, but the epidemic infects $Z \approx 0.89$.
The difference,

\[ \text{overshoot} = Z - H, \]

here about 29% of the population, is infected *after* the herd immunity threshold has already been crossed.
These infections are, in a sense, unnecessary: if transmission could be switched off the instant the threshold is reached, the epidemic would end with far fewer total cases.
Overshoot is why letting an epidemic burn to natural herd immunity is so costly, and why the timing of any relaxation of control matters — lift measures right at the threshold and the residual momentum still carries a large overshoot.
An implementation of the final size and overshoot calculations for applied use is available in the [`nccovid`](https://github.com/medewitt/nccovid) R package.

## A worked example

For $R_0 = 2.5$ we solve the final size equation for the attack rate, compute the herd immunity threshold, and take their difference as the overshoot.

## In code

### R

```r
R0 <- 2.5

# Solve Z = 1 - exp(-R0 Z) for the attack rate on (0, 1).
final_size <- uniroot(function(z) 1 - exp(-R0 * z) - z,
                      interval = c(1e-9, 1 - 1e-9))$root
herd <- 1 - 1 / R0
overshoot <- final_size - herd

round(c(final_size = final_size, herd_threshold = herd,
        overshoot = overshoot), 3)
```

### Python

```python
from scipy.optimize import brentq
import numpy as np

R0 = 2.5

# Solve Z = 1 - exp(-R0 Z) for the attack rate on (0, 1).
final_size = brentq(lambda z: 1 - np.exp(-R0 * z) - z, 1e-9, 1 - 1e-9)
herd = 1 - 1 / R0
overshoot = final_size - herd

print(f"final size (attack rate) = {final_size:.3f}")
print(f"herd immunity threshold  = {herd:.3f}")
print(f"overshoot                = {overshoot:.3f}")
```

<!-- python-output:auto -->
```text
final size (attack rate) = 0.893
herd immunity threshold  = 0.600
overshoot                = 0.293
```
<!-- /python-output:auto -->

### Julia

```julia
using Roots

R0 = 2.5

# Solve Z = 1 - exp(-R0 Z) for the attack rate on (0, 1).
final_size = find_zero(z -> 1 - exp(-R0 * z) - z, (1e-9, 1 - 1e-9))
herd = 1 - 1 / R0
overshoot = final_size - herd

(final_size = final_size, herd_threshold = herd, overshoot = overshoot)
```

## Why it matters

The final size relation and the herd immunity threshold turn a single number, $R_0$, into two of the quantities decision-makers ask for first: how many people will be infected, and what immunity is needed to stop it.
The overshoot between them is the quantitative case against uncontrolled epidemics — natural herd immunity arrives only after a large excess of infections that flattening the curve or vaccinating ahead of the threshold would avoid.
All three follow from the same threshold structure that the [next-generation matrix](next-generation-matrix.md) generalizes to structured populations.

## Related

- [Compartmental Models (SIR)](sir.md) — the model these results come from
- [SEIR and Compartmental Extensions](seir-models.md) — how latency and demography modify them
- [The Next-Generation Matrix and R₀](next-generation-matrix.md) — the threshold in structured populations
- [The Speed and Strength of Epidemic Control](../epidemiology/epidemic-control.md) — why the timing of control sets the overshoot
- [The Euler–Lotka Equation and the r–R₀ Relationship](../epidemiology/euler-lotka.md) — turning a growth rate into $R_0$
