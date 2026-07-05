---
title: "Climate Forcing in Transmission Models"
description: "Making the transmission rate time-varying to fold seasonality and climate into epidemic models, and the resonances this produces."
---

# Climate Forcing in Transmission Models

Most compartmental models freeze the transmission rate $\beta$ at a single number, but the real world has seasons: measles surges when schools reopen, influenza peaks in winter, and mosquito-borne infections track the rains.
Climate forcing lets $\beta$ breathe with the calendar, and that one change turns a model that settles to a flat endemic level into one that can beat out annual, biennial, or irregular multi-year cycles.
Despite the name, periodic forcing is not reserved for climate-driven diseases: the same time-varying-transmission machinery captures any recurring change in contact or transmission over time.
A time-dependent $\beta(t)$ can encode changing contact rates from any source — school-term forcing of childhood infections such as measles, holiday travel and seasonal aggregation, weekly rhythms of work and social mixing, or other behavioral and social periodicity — not just temperature.

![A seasonally forced SIR model showing recurrent annual epidemics, with stronger seasonal forcing producing larger swings than weak forcing.](../assets/figures/climate-forcing-in-transmission-models.svg)

## Seasonal forcing of the transmission rate

The simplest way to inject seasonality is to write the transmission rate as a periodic function of time.
A sinusoidal form is the standard first choice,

\[
\beta(t) = \beta_0\left(1 + \varepsilon \cos\!\left(\frac{2\pi t}{365}\right)\right),
\]

where $\beta_0$ is the annual-mean transmission rate, $\varepsilon \in [0,1)$ is the forcing amplitude, and the period is one year for $t$ in days.
When $\varepsilon = 0$ we recover the ordinary constant-$\beta$ model; as $\varepsilon$ grows the transmission rate swings a fraction $\varepsilon$ above and below its mean each year.
A term-time forcing that switches $\beta$ between school and holiday values is a common alternative, but the sinusoid captures the physics with one interpretable knob.

## Where the forcing comes from

The sinusoid is a summary of real biology, not a fudge factor.
For directly transmitted childhood infections the dominant driver is the school calendar, which packs susceptible children together for two-thirds of the year and disperses them in summer.
For respiratory viruses, low humidity and cold temperatures stabilise airborne particles and dry out mucosal defences, raising the per-contact transmission probability.
For vector-borne diseases the forcing is thermal: temperature controls the mosquito biting rate, development, and survival, and rainfall sets breeding-habitat availability, so the effective $\beta$ inherits the seasonality of the climate itself.
This mechanistic layer connects to the [climate and disease transmission](../epidemiology/climate-and-disease-transmission.md) page, where the thermal-response curves of vector traits are unpacked — exactly what a covariate-driven $\beta(t)$ should encode.
Disease ecologists have long argued that these environmental forces belong at the centre of transmission theory, not the margin ([Arthur et al., 2017, Philosophical Transactions of the Royal Society B](https://doi.org/10.1098/rstb.2016.0454)).

## Time-averaged and seasonal reproduction numbers

With a time-varying $\beta$ there is no single reproduction number.
A useful first summary is the time-averaged value, obtained by replacing $\beta(t)$ with its mean $\bar\beta = \beta_0$,

\[
\bar R_0 = \frac{\beta_0}{\gamma + \mu},
\]

which governs whether the pathogen can persist on average.
But the *seasonal* reproduction number $R_0(t) = \beta(t)/(\gamma+\mu)$ can rise above one for part of the year and fall below it for the rest, and it is the phasing of this window against the supply of susceptibles that sets when the epidemic actually takes off.
Forcing does not usually change whether disease persists, but it strongly shapes epidemic *timing*: the outbreak ignites when $\beta(t)$ is climbing and susceptibles are abundant, so the peak leads or lags the peak in $\beta(t)$ depending on how depleted the susceptible pool is.

## Resonance and multi-year cycles

An unforced endemic model does not sit still if perturbed: it rings at a natural inter-epidemic period \[ T \approx 2\pi \sqrt{\frac{1}{\mu(R_0 - 1)}\cdot\frac{1}{\gamma+\mu}}, \] the period of the damped oscillations back to the endemic equilibrium.
Seasonal forcing drives this intrinsic oscillator at a one-year period, and the interplay is a resonance.
When the natural period $T$ is close to one year the system locks to an **annual** cycle; when $T$ is near two years the forcing entrains a **biennial** cycle in which large and small years alternate; and for other detunings the model can visit longer periodic or even chaotic multi-year patterns.
This resonance is why measles famously ran on a two-year clock in many prevaccine cities: the intrinsic period sat near two years, and modest term-time forcing snapped it into a biennial attractor.
Keeling and Rohani (*Modeling Infectious Diseases in Humans and Animals*) work through this forced-SIR bifurcation structure in detail.

## Coupling climate covariates into parameters

Beyond a bare sinusoid, one can make parameters explicit functions of measured climate drivers.
Writing $\beta(t) = \beta_0\, g\!\big(T_{\text{air}}(t),\, H(t),\, P(t)\big)$ lets temperature $T_{\text{air}}$, humidity $H$, and rainfall $P$ enter through a fitted or mechanistic response $g$, often a thermal-performance curve borrowed from vector physiology.
This is the natural bridge between statistical climate–disease regressions and dynamical models: the covariate supplies the shape of the forcing, and the transmission model supplies the nonlinear amplification that turns a smooth climate signal into a sharp epidemic.
It also exposes a practical caution: projecting such a model forward under climate change means extrapolating $g$ beyond the range where it was fitted, into a non-stationary regime where the historical relationship may not hold.
The environmental leg of this reasoning is also the one most often under-served in applied training, a gap noted for One Health curricula by [Adeyemi et al., 2024, One Health Outlook](https://doi.org/10.1186/s42522-024-00097-6).

## The forced model

We take a seasonally forced SIRS model, where waning immunity at rate $\omega$ recycles recovered individuals and sustains recurrence:

\[
\begin{aligned}
\frac{dS}{dt} &= -\beta(t)\, S I + \omega R, \\
\frac{dI}{dt} &= \beta(t)\, S I - \gamma I, \\
\frac{dR}{dt} &= \gamma I - \omega R,
\end{aligned}
\]

with $S + I + R = 1$ and $\beta(t)$ the sinusoid above.
Setting $\varepsilon = 0$ gives the flat endemic SIRS model; turning $\varepsilon$ up engages the forcing.

## A worked example

Take $\beta_0 = 0.5\ \text{day}^{-1}$, $\gamma = 0.2\ \text{day}^{-1}$ (a $5$-day infectious period, so $\bar R_0 = \beta_0/\gamma = 2.5$), and waning rate $\omega = 0.01\ \text{day}^{-1}$ (about $100$-day immunity).
We integrate for $60$ years to shed transients and read off the final year, comparing weak forcing $\varepsilon = 0.05$ against strong forcing $\varepsilon = 0.25$ with every other parameter held fixed.
The weak-forcing run barely ripples — prevalence rises and falls by only about $16\%$ across the year — while the strong-forcing run swings by a factor of three and its incidence peak shifts nearly two months earlier, as the steeper $\beta(t)$ ignites the outbreak sooner.

## In code

### R

```r
# illustrative: forced SIRS, weak vs strong seasonality
library(deSolve)
beta0 <- 0.5; gamma <- 0.2; omega <- 0.01; R0 <- beta0/gamma
beta_t <- function(t, eps) beta0 * (1 + eps * cos(2*pi*t/365))
sirs <- function(t, y, p) with(as.list(c(y, p)), {
  b <- beta_t(t, eps)
  list(c(-b*S*I + omega*R, b*S*I - gamma*I, gamma*I - omega*R))
})
y0 <- c(S = 1/R0, I = 1e-3, R = 1 - 1/R0 - 1e-3)
out <- ode(y0, seq(0, 60*365, 1), sirs, c(eps = 0.25))
tail(out, 365)   # inspect the seasonal swing in the final year
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

# Seasonally forced SIRS (waning immunity), rates in days^-1
beta0 = 0.50           # baseline transmission rate
gamma = 0.20           # recovery rate, 5-day infectious period
omega = 0.01           # waning rate, ~100-day immunity
R0    = beta0 / gamma  # = 2.5

years  = 60
t_end  = years * 365.0
t_eval = np.arange(0, t_end + 1, 1.0)

def beta(t, eps):                      # sinusoidal forcing of transmission
    return beta0 * (1.0 + eps * np.cos(2 * np.pi * t / 365.0))

def sirs(t, y, eps):
    S, I, R = y
    b = beta(t, eps)
    return [-b*S*I + omega*R,
             b*S*I - gamma*I,
             gamma*I - omega*R]

def cycle(eps):                        # integrate, then read the final year
    y0 = [1.0/R0, 1e-3, 1.0 - 1.0/R0 - 1e-3]
    sol = solve_ivp(sirs, [0, t_end], y0, args=(eps,),
                    t_eval=t_eval, rtol=1e-9, atol=1e-12)
    t, S, I = sol.t, sol.y[0], sol.y[1]
    inc  = beta(t, eps) * S * I         # incidence = force of infection x S
    last = t >= (years - 1) * 365       # final year, transients gone
    doy  = t[last][np.argmax(inc[last])] % 365
    return doy, I[last].max(), I[last].min()

for eps in (0.05, 0.25):
    doy, imax, imin = cycle(eps)
    print(f"eps={eps}: peak incidence on day-of-year {doy:.0f}")
    print(f"eps={eps}: prevalence peak {imax:.4f}, trough {imin:.4f}, swing x{imax/imin:.2f}")
```

<!-- python-output:auto -->
```text
eps=0.05: peak incidence on day-of-year 300
eps=0.05: prevalence peak 0.0305, trough 0.0264, swing x1.16
eps=0.25: peak incidence on day-of-year 253
eps=0.25: prevalence peak 0.0444, trough 0.0145, swing x3.06
```
<!-- /python-output:auto -->

### Julia

```julia
# illustrative: forced SIRS, weak vs strong seasonality
using DifferentialEquations
beta0, gamma, omega = 0.5, 0.2, 0.01; R0 = beta0/gamma
beta_t(t, eps) = beta0 * (1 + eps * cos(2pi*t/365))
function sirs!(du, u, eps, t)
    S, I, R = u; b = beta_t(t, eps)
    du[1] = -b*S*I + omega*R
    du[2] =  b*S*I - gamma*I
    du[3] =  gamma*I - omega*R
end
u0 = [1/R0, 1e-3, 1 - 1/R0 - 1e-3]
sol = solve(ODEProblem(sirs!, u0, (0.0, 60*365.0), 0.25), saveat = 1.0)
sol.u[end]   # state after 60 years of strong forcing
```

The printed run confirms the story: the weak-forcing peak lands near day-of-year $300$ with a gentle swing of about $\times 1.16$, while the strong-forcing peak moves to day-of-year $253$ and swings by roughly $\times 3.06$ — stronger climate forcing yields both a sharper seasonal amplitude and a shifted epidemic calendar, with no other parameter touched.

## Why it matters

Seasonality is not a nuisance to be averaged away; it is a structural feature that decides when hospitals fill, when vector control should be timed, and whether an infection cycles annually or in harder-to-forecast multi-year bursts.
By making $\beta(t)$ track temperature, humidity, and rainfall, the same compartmental skeleton becomes a tool for early warning and for reasoning about how a warming, wetter, or more erratic climate might reschedule disease.
The catch is that this power rests on relationships fitted to past climate, so projections under climate change demand explicit care about extrapolation and non-stationarity rather than blind trust in a curve fit to yesterday's weather.

## Related

- [The SIR model](sir.md)
- [SEIR models](seir-models.md)
- [Vector-borne disease](vector-borne.md)
- [Climate and disease transmission](../epidemiology/climate-and-disease-transmission.md)
- [Quantitative Methods](../math.md)
