---
title: "One Health Surveillance"
description: "Surveillance that integrates human, animal, and environmental streams so that a signal at the spillover interface can warn before human cases appear."
---

# One Health Surveillance

Most emerging infections in people begin somewhere else, in livestock, wildlife, or the environment, and reach humans only after circulating unseen.
One Health surveillance watches those other compartments alongside human cases, so that a rise in animal or environmental signals can warn before the human curve turns up.
It extends ordinary [surveillance](surveillance-systems.md) to the interface where spillover actually happens.

![Three surveillance streams, human cases, animal sentinels, and environmental sampling, feed one integrated early-warning signal; an environmental stream rises before the human case curve, and the gap is the lead time.](../assets/figures/one-health-surveillance.svg)

## Three streams, one signal

One Health surveillance draws on data that ordinary human-case reporting ignores.

- **Human** streams: clinical cases, syndromic reports, laboratory confirmations, the usual backbone of public-health surveillance.
- **Animal** streams: disease in domestic animals (dairy herds, poultry flocks) and in wildlife (bats, wild birds, rodents), plus **sentinel animals** deliberately monitored as early detectors, such as chickens watched for West Nile virus.
- **Environmental** streams: pathogen or its genetic material sampled from where it accumulates, most prominently **wastewater**, but also surface water, soil, and air.

The point is not three separate systems but one integrated signal.
Read together, the streams cover the transmission cycle rather than only its human endpoint, and they can confirm each other: an environmental detection plus an animal cluster is far stronger evidence than either alone.

## Why a cross-stream signal leads

An animal or environmental stream can rise before human cases for a simple reason: it sits earlier in the causal chain.

Wastewater aggregates shedding from everyone in a sewershed, including pre-symptomatic and [asymptomatic](epidemiological-intervals.md) infections, so it does not wait for people to feel ill, seek care, get tested, and be reported.
That removes the onset-to-report [delays](nowcasting.md) that hold back clinical surveillance.
A sentinel or wildlife signal leads when the pathogen amplifies in an animal population before spilling over, as with avian influenza in wild birds and poultry ahead of human exposure.

The practical value is **lead time**: the number of days by which the leading stream anticipates the human curve.
Even a week of warning changes what control can do, moving it from reactive to anticipatory.

## Data linkage and governance

The obstacle is rarely the biology; it is the institutions.
Human health, agriculture, and environmental agencies keep separate data systems, mandates, and legal authorities, and animal or wildlife data may be commercially or politically sensitive.
Linking streams means agreeing on shared case definitions, spatial and temporal resolution, and data-sharing rules across sectors that do not normally report to one another.
One Health surveillance is as much a governance problem as a technical one, which is why sustained programs pair the data pipelines with formal cross-sector agreements.

## A worked example

Suppose an environmental (wastewater) stream and a human case curve both trace the same outbreak, but the wastewater signal peaks ten days earlier because it captures shedding before care-seeking and reporting.
We recover that lead time from the two noisy series by sliding one against the other and taking the lag at which their [cross-correlation](../math/covariance-functions.md) peaks.
The estimated lead, about ten days, is exactly the warning a One Health system buys over human-case reporting alone.

## In code

We simulate a leading environmental signal and a lagged human case curve, then estimate the lead time as the shift that maximizes the correlation between the two streams.

### R

```r
set.seed(1834)
t <- 0:119
lead <- 10                                   # true environmental lead
wave <- function(peak) exp(-0.5 * ((t - peak) / 14)^2)

env   <- wave(45)        + rnorm(length(t), 0, 0.02)
human <- wave(45 + lead) + rnorm(length(t), 0, 0.02)

lags <- 0:30
corr <- sapply(lags, function(L) {
  h <- human[(L + 1):length(t)]
  cor(env[1:length(h)], h)
})
cat("estimated lead time (days):", lags[which.max(corr)], "\n")
```

### Python

```python
import numpy as np

rng = np.random.default_rng(1834)
t = np.arange(0, 120)
lead = 10                                    # true environmental lead

def wave(peak):
    return np.exp(-0.5 * ((t - peak) / 14.0) ** 2)

env = wave(45) + rng.normal(0, 0.02, t.size)
human = wave(45 + lead) + rng.normal(0, 0.02, t.size)

# Slide the human curve earlier by L days; find the best-aligning lag.
lags = np.arange(0, 31)
ec = env - env.mean()
corr = np.array([
    np.corrcoef(ec[:t.size - L], human[L:] - human[L:].mean())[0, 1]
    for L in lags
])
best = int(lags[np.argmax(corr)])
print("estimated lead time (days):", best)
print("peak correlation:", round(float(corr.max()), 3))
```

<!-- python-output:auto -->
```text
estimated lead time (days): 10
peak correlation: 0.996
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics
Random.seed!(1834)

t = 0:119
lead = 10
wave(peak) = exp.(-0.5 .* ((t .- peak) ./ 14).^2)

env   = wave(45)        .+ 0.02 .* randn(length(t))
human = wave(45 + lead) .+ 0.02 .* randn(length(t))

lags = 0:30
corr = [cor(env[1:length(t)-L], human[L+1:end]) for L in lags]
println("estimated lead time (days): ", lags[argmax(corr)])
```

## Why it matters

Spillover happens at the interface between people, animals, and the environment, and a surveillance system that only counts human cases sees it last.
Integrating animal and environmental streams turns that interface into a warning system, buying lead time that reactive case reporting cannot.
The gains are real but bounded by governance: the harder work is linking data across agencies that were never built to share it.

## Related

- [Surveillance Systems](surveillance-systems.md)
- [Outbreak Investigation](outbreak-investigation.md)
- [Nowcasting and Reporting Delays](nowcasting.md)
- [Epidemiological Intervals and Delays](epidemiological-intervals.md)
- [Reservoir Ecology](../math/reservoir-ecology.md)
- [Diagnostics & Surveillance](../diagnostics.md)
- [Epidemiology](../epidemiology.md)
