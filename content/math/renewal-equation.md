---
title: "The Renewal Equation"
description: "How the renewal (Euler-Lotka) equation links new infections to past infections through the generation-interval distribution, and how it connects growth rate to R."
---

# The Renewal Equation

An epidemic remembers its own past.
Today's new infections are produced by people infected over the preceding days and weeks, each contributing according to how infectious they are now, and the renewal equation is the bookkeeping that turns that memory into the next day's cases.
It is the engine behind $R_t$ estimation, short-term forecasting, and the tight link between how fast an epidemic grows and how much transmission each case represents.

![Incidence simulated from the renewal equation, with the instantaneous growth rate below it crossing zero exactly when incidence peaks.](../assets/figures/renewal-equation.svg)

## New infections from old

Write $I(t)$ for the number of new infections on day $t$.
The renewal equation says that incidence today is a reproduction number times a weighted sum of past incidence:

\[
I(t) = R_t \sum_{s \ge 1} I(t - s)\, w(s).
\]

Here $w(s)$ is the **generation-interval distribution**, the probability that transmission from a case happens $s$ days after that case was itself infected, and $R_t$ is the **effective reproduction number**, the average number of people each current case goes on to infect.
The weighted sum $\sum_{s} I(t-s)\, w(s)$ is the current **force of infection**: everyone infected earlier, discounted by how likely they are to be transmitting right now.
$R_t$ is simply the multiplier that turns that force into new cases.

In continuous time the same statement is an integral over the age of infection $a$,

\[
I(t) = R_t \int_0^\infty I(t - a)\, g(a)\, \mathrm{d}a,
\]

with $g(a)$ the continuous generation-interval density.
The equation goes back to Lotka and Euler's work on population renewal, where births replace infections and the age-of-reproduction distribution replaces the generation interval.

## The generation interval is the memory kernel

The weights $w(s)$ decide how far back the epidemic reaches when producing new cases.
A short generation interval concentrates transmission soon after infection, so the epidemic turns over quickly; a long one spreads each case's transmission over many days.
The generation interval is rarely observed directly, because we almost never see the moment of infection, so in practice the **serial interval** (symptom onset to symptom onset) stands in for it.
The distinction and the bias it introduces are covered in [epidemiological intervals](../epidemiology/epidemiological-intervals.md).

## Estimating $R_t$

Rearranging the renewal equation isolates the reproduction number as a ratio:

\[
\hat{R}_t = \frac{I(t)}{\sum_{s \ge 1} I(t - s)\, w(s)}.
\]

Divide observed incidence by the transmission potential of everyone infected before, and what remains is the multiplier $R_t$.
Real incidence is noisy and reports are delayed, so estimators like EpiEstim model incidence as [Poisson](poisson-distribution.md) counts, place a prior on $R_t$, and smooth over a short sliding window.
The mechanics are developed on [the effective reproduction number](reproduction-number-rt.md) page.

## Growth rate and R

During exponential growth incidence behaves as $I(t) \propto e^{r t}$ for some growth rate $r$.
Substituting this into the renewal equation and canceling the common factor gives the **Euler-Lotka** relationship between $r$ and $R$:

\[
\frac{1}{R} = \int_0^\infty e^{-r a}\, g(a)\, \mathrm{d}a = M(-r),
\]

where $M$ is the moment-generating function of the generation-interval distribution (the discrete analogue replaces the integral by $\sum_s e^{-r s} w(s)$).
This is the Wallinga-Lipsitch relationship: measure the growth rate $r$ from the slope of the log-incidence curve, plug in the generation-interval distribution, and read off $R$.
For a fixed $r$ a longer generation interval implies a larger $R$, because the same growth has to be packed into slower cycles.
The linear approximation $R \approx 1 + r\, T_g$, with $T_g$ the mean generation time, follows from keeping only the first moment.

## A worked example

Take a gamma generation interval with mean 5 days and standard deviation about 2.2 days, discretized to daily weights $w(s)$, and drive the epidemic with a constant $R = 1.5$.
Iterating $I(t) = R \sum_s I(t-s)\, w(s)$ forward from a small seed reaches a clean exponential phase where $I(t)$ multiplies by a fixed factor each day.
Two checks then hold.
Dividing incidence by the weighted sum of past incidence returns $R = 1.5$ on every day, recovering the input.
Measuring the growth rate $r$ from the log-incidence slope and evaluating $1/\sum_s e^{-r s} w(s)$ returns the same $1.5$, confirming the Euler-Lotka bridge.

## In code

### R

```r
shape <- 5; scale <- 1                    # gamma generation interval, mean 5 d
s <- 1:20
w <- diff(pgamma(0:20, shape = shape, scale = scale)); w <- w / sum(w)

R <- 1.5; T <- 60
I <- numeric(T); I[1] <- 10
for (t in 2:T) {
  k <- 1:min(t - 1, length(w))
  I[t] <- R * sum(I[t - k] * w[k])
}

force <- function(t) { k <- 1:min(t - 1, length(w)); sum(I[t - k] * w[k]) }
c(R_hat_day20 = I[20] / force(20))        # recovers R = 1.5
```

### Python

```python
import numpy as np
from scipy.stats import gamma

# Discretize a gamma generation interval (mean 5 days, sd ~2.2 days).
shape, scale = 5.0, 1.0
s = np.arange(1, 21)
w = np.diff(gamma.cdf(np.arange(0, 21), a=shape, scale=scale))
w = w / w.sum()                                  # generation-interval weights

# Simulate the discrete renewal process with a constant R.
R = 1.5
T = 60
I = np.zeros(T); I[0] = 10.0
for t in range(1, T):
    k = np.arange(1, min(t, len(w)) + 1)
    I[t] = R * np.sum(I[t - k] * w[k - 1])

def force(t):
    k = np.arange(1, min(t, len(w)) + 1)
    return np.sum(I[t - k] * w[k - 1])

print(f"R input = {R}")
for t in (5, 10, 20):
    print(f"day {t:2d}: I_t = {I[t]:8.1f}  R_hat = {I[t] / force(t):.3f}")

# Growth rate r and the Euler-Lotka check: 1/R = sum_s e^{-r s} w_s.
r = np.log(I[40] / I[39])
mgf = np.sum(np.exp(-r * s) * w)
print(f"r = {r:.4f} /day; R from 1/mgf = {1 / mgf:.3f}")
```

<!-- python-output:auto -->
```text
R input = 1.5
day  5: I_t =      3.1  R_hat = 1.500
day 10: I_t =      4.2  R_hat = 1.500
day 20: I_t =      8.9  R_hat = 1.500
r = 0.0763 /day; R from 1/mgf = 1.500
```
<!-- /python-output:auto -->

The back-computed $R_t$ sits at $1.5$ on every day, and the growth rate recovered from the log-incidence slope reproduces the same $R$ through the moment-generating function.

### Julia

```julia
using Distributions
gi = Gamma(5.0, 1.0)                       # generation interval, mean 5 days
w = diff(cdf.(gi, 0:20)); w ./= sum(w)

R = 1.5; T = 60
I = zeros(T); I[1] = 10.0
for t in 2:T
    k = 1:min(t - 1, length(w))
    I[t] = R * sum(I[t .- k] .* w[k])
end

force(t) = (k = 1:min(t - 1, length(w)); sum(I[t .- k] .* w[k]))
I[20] / force(20)                          # recovers R = 1.5
```

## Why it matters

The renewal equation is the smallest model that still captures what makes an epidemic an epidemic: cases beget cases, delayed by the generation interval and scaled by $R_t$.
That economy is why it underlies so much real-time analysis, from $R_t$ dashboards to the [forecasts](../epidemiology/epidemic-forecasting.md) that project incidence a week or two ahead.
It also fixes a common confusion, showing exactly how a measured growth rate and a reproduction number are two views of the same dynamics, joined by the generation-interval distribution.

## Related

- [The Effective Reproduction Number and Forecasting](reproduction-number-rt.md)
- [Branching Processes](branching-processes.md)
- [The SIR Model](sir.md)
- [Epidemiological intervals](../epidemiology/epidemiological-intervals.md)
- [Epidemic Forecasting](../epidemiology/epidemic-forecasting.md)
- [Quantitative Methods](../math.md)
