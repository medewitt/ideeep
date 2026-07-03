---
title: "Epidemiological Intervals and Delays"
---

# Epidemiological Intervals and Delays

Transmission is a sequence of events strung out in time: a person is infected, becomes infectious, perhaps develops symptoms, and infects others, who repeat the cycle.
The **intervals** between these events — incubation, latent, infectious, serial, and generation — are the clocks of an epidemic.
They set how fast cases accumulate, how much warning symptoms give before spread, and how we translate an epidemic growth rate into a reproduction number.

![A timeline of one infection showing the latent period before infectiousness, the incubation period before symptoms, and the pre-symptomatic transmission window where infectiousness precedes symptoms.](../assets/figures/epi-intervals-timeline.svg)

## The natural history of one infection

Set the clock to zero at the moment of **infection** (exposure).
Two independent processes then unfold, and it is essential to keep them separate.

The **disease clock** governs symptoms.
The **incubation period** is the time from infection to symptom onset.

The **transmission clock** governs infectiousness.
The **latent period** is the time from infection to the onset of infectiousness, and the **infectious period** is how long infectiousness then lasts.

The latent period and the incubation period are *not* the same thing, and their ordering matters enormously for control.

- When infectiousness begins *after* symptoms (latent period longer than incubation), sick people can be identified and isolated before they transmit.
  This was the situation with **SARS-CoV-1** in 2003, which is a large part of why it was containable.
- When infectiousness begins *before* symptoms (latent period shorter than incubation), there is a **pre-symptomatic transmission** window in which apparently healthy people spread the pathogen.
  This was a defining, and dangerous, feature of **SARS-CoV-2**.

**Asymptomatic** infections take this to its limit: infectious individuals who never develop symptoms at all, and so are invisible to any surveillance system that relies on people feeling ill.

## Serial interval and generation interval

To describe transmission *between* people we need intervals that span an infector–infectee pair.

The **generation interval** (or generation time) is the time between the **infection** of an infector and the **infection** of the person they infect.
It is the quantity that actually governs epidemic dynamics, but it is rarely observable directly — we almost never see the moment of infection.

The **serial interval** is the time between **symptom onset** in the infector and symptom onset in the infectee.
Onsets *are* usually observable, so the serial interval is what we typically measure and use as a proxy for the generation interval.

![An infector and infectee timeline: the generation interval runs infection-to-infection, the serial interval runs onset-to-onset, and the two differ because the two people have different incubation periods.](../assets/figures/serial-vs-generation-interval.svg)

The two intervals are linked through the incubation periods of the two people:

$$\text{serial interval} = \text{generation interval} + (I_{\text{infectee}} - I_{\text{infector}}),$$

where $I_{\text{infector}}$ and $I_{\text{infectee}}$ are the two incubation periods.
Two consequences follow.

- If incubation periods are independent and identically distributed across people, the serial and generation intervals have the **same mean**, so the serial interval is an unbiased estimator of the mean generation time.
- The serial interval has **larger variance** (it adds the variability of two incubation periods) and **can be negative**: if the infectee happens to have a much shorter incubation period than the infector, they can show symptoms *first*.
  Negative serial intervals were repeatedly observed for SARS-CoV-2 and are a direct signature of substantial pre-symptomatic transmission.

## Why the generation interval controls $R_t$

The generation interval distribution $g(a)$ is the bridge between the two things we can most easily measure about an epidemic — its **growth rate** $r$ and its **reproduction number** $R$.
The renewal (Euler–Lotka) equation ties them together:

$$\frac{1}{R} = \int_0^\infty e^{-r a}\, g(a)\, \mathrm{d}a.$$

For a given growth rate $r$, a **shorter** generation interval implies a reproduction number **closer to 1**, because each generation of transmission is turned over faster.
This is why estimating $g$ well matters: plug in the wrong generation interval and you get the wrong $R$, and the wrong sense of how hard the epidemic is to stop.
See [the effective reproduction number](../math/reproduction-number-rt.md) for how $R_t$ is estimated from incidence using $g$.

## A gallery of biological examples

Intervals vary enormously across pathogens, and that variation shapes both dynamics and control.

| Pathogen | Incubation (mean) | Serial interval (mean) | Note |
| --- | --- | --- | --- |
| Influenza A | ~2 days | ~2–3 days | short intervals → fast, hard-to-outrun epidemics |
| SARS-CoV-2 (ancestral) | ~5 days | ~5 days | serial interval sometimes < incubation → pre-symptomatic spread |
| SARS-CoV-1 | ~5 days | ~8–10 days | infectiousness peaks after symptoms → containable |
| Measles | ~10–14 days | ~12 days | very high $R_0$ (12–18) despite moderate intervals |
| Ebola virus | ~8–10 days | ~15 days | long intervals give contact tracing time to work |
| Smallpox | ~12 days | ~17 days | long, symptom-first transmission enabled eradication |

For **vector-borne** diseases there is an extra clock inside the vector.
The **extrinsic incubation period (EIP)** is the time from a mosquito taking an infectious blood meal to becoming able to transmit.
For *Plasmodium* (malaria) the EIP is roughly 10–14 days but is strongly **temperature-dependent** — warmer temperatures shorten it, which is one mechanism by which climate shifts transmission intensity (see [vector-borne models](../math/vector-borne.md)).

## Delays from onset to observation

Surveillance sees events even later than onset, through a chain of **reporting delays**: onset-to-testing, onset-to-hospitalization, onset-to-death, and onset-to-report.
These delays are why the most recent days of any epidemic curve are always incomplete, and correcting for them is the job of [nowcasting](delay-distributions-censoring.md).

## A worked example

Suppose the generation interval is Gamma-distributed with mean 5 days and standard deviation 2 days, and each person's incubation period is Gamma-distributed with mean 5 days and standard deviation 3 days, all independent.
The serial interval then has the same mean as the generation interval, 5 days, but a larger standard deviation of $\sqrt{2^2 + 3^2 + 3^2}=\sqrt{22}\approx 4.7$ days, and a non-trivial fraction of infector–infectee pairs will have **negative** serial intervals.

## In code

We simulate infector–infectee pairs to confirm that the serial interval shares the generation interval's mean, spreads wider, and goes negative.

### R

```r
set.seed(1)
n  <- 200000
gi <- rgamma(n, shape = 6.25, scale = 0.8)          # mean 5, sd 2
Ia <- rgamma(n, shape = 2.78, scale = 1.8)          # infector incubation: mean 5, sd 3
Ib <- rgamma(n, shape = 2.78, scale = 1.8)          # infectee incubation
si <- gi + (Ib - Ia)                                # serial interval

c(gen_mean = mean(gi), si_mean = mean(si),
  si_sd = sd(si), frac_negative = mean(si < 0))
```

### Python

We use [Polars](https://pola.rs) to hold and summarize the simulated pairs.

```python
import numpy as np
import polars as pl

rng = np.random.default_rng(1)
n = 200_000
gi = rng.gamma(shape=6.25, scale=0.8, size=n)       # generation interval: mean 5, sd 2
Ia = rng.gamma(shape=2.78, scale=1.8, size=n)       # infector incubation: mean 5, sd 3
Ib = rng.gamma(shape=2.78, scale=1.8, size=n)       # infectee incubation
si = gi + (Ib - Ia)                                 # serial interval

pairs = pl.DataFrame({"generation": gi, "serial": si})
summary = pairs.select(
    gen_mean=pl.col("generation").mean(),
    si_mean=pl.col("serial").mean(),
    si_sd=pl.col("serial").std(),
    frac_negative=(pl.col("serial") < 0).mean(),
)
print(summary)
```

<!-- python-output:auto -->
```text
shape: (1, 4)
┌──────────┬──────────┬──────────┬───────────────┐
│ gen_mean ┆ si_mean  ┆ si_sd    ┆ frac_negative │
│ ---      ┆ ---      ┆ ---      ┆ ---           │
│ f64      ┆ f64      ┆ f64      ┆ f64           │
╞══════════╪══════════╪══════════╪═══════════════╡
│ 4.989681 ┆ 4.989542 ┆ 4.689407 ┆ 0.130155      │
└──────────┴──────────┴──────────┴───────────────┘
```
<!-- /python-output:auto -->

The generation and serial means agree near 5 days, the serial standard deviation is about 4.7, and a noticeable fraction of serial intervals come out negative — exactly the pre-symptomatic-transmission signature.

### Julia

```julia
using Distributions, Statistics, Random
Random.seed!(1)

n  = 200_000
gi = rand(Gamma(6.25, 0.8), n)                      # mean 5, sd 2
Ia = rand(Gamma(2.78, 1.8), n)                      # mean 5, sd 3
Ib = rand(Gamma(2.78, 1.8), n)
si = gi .+ (Ib .- Ia)

(gen_mean = mean(gi), si_mean = mean(si),
 si_sd = std(si), frac_negative = mean(si .< 0))
```

## Why it matters

Intervals are where biology meets dynamics.
The gap between the latent and incubation periods decides whether symptom-based control can ever work; the generation interval decides how a measured growth rate maps to a reproduction number; and the serial interval is the observable stand-in we actually estimate, complete with its awkward tendency to go negative.
Getting these distributions right — and estimating them correctly from messy, real-time data — is the subject of the [next page](delay-distributions-censoring.md).

## Related

- [Fitting Delay Distributions: Truncation and Censoring](delay-distributions-censoring.md)
- [The Effective Reproduction Number and Forecasting](../math/reproduction-number-rt.md)
- [Compartmental Models (SIR)](../math/sir.md)
- [SEIR and Compartmental Extensions](../math/seir-models.md)
- [Vector-Borne Disease Models](../math/vector-borne.md)
- [Survival Analysis](../math/survival-analysis.md)
- [Epidemiology](../epidemiology.md)
