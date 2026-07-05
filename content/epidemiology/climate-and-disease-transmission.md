---
title: "Climate and Disease Transmission"
description: "How temperature, water, and ecological change drive infectious-disease transmission, the environmental leg of One Health that quantitative programs tend to under-develop."
---

# Climate and Disease Transmission

Pathogens do not circulate in a vacuum; they ride on mosquitoes that breed in warm standing water, on rodents that follow shifting rainfall, and on human contact with disturbed ecosystems.
Climate and environment set the stage on which transmission plays out, tuning vector abundance, pathogen replication, and the chance of spillover.
This page treats that environmental leg quantitatively, because it is the part of [One Health surveillance](one-health-surveillance.md) and planetary health that data-focused programs most often leave thin.

![A unimodal thermal performance curve where relative transmission peaks at an intermediate temperature and falls toward both cold and hot extremes.](../assets/figures/climate-and-disease-transmission.svg)

## Temperature shapes vector and pathogen traits

Most vectors are ectotherms, so nearly every rate that matters for transmission depends on temperature.
Biting and feeding rate, larval development, adult mortality, and the **extrinsic incubation period** (the days a pathogen needs to develop inside the vector before it can be transmitted) all respond to warming.
Warmth speeds development and biting up to a point, but past that point mortality climbs and the vector dies before it can transmit.
Because these traits push in opposite directions as temperature rises, their product, transmission intensity, is **unimodal**: it climbs, peaks at an intermediate thermal optimum, and falls off at both cold and hot extremes.

We can write relative vectorial capacity, or relative $R_0$, as a product of temperature-dependent traits.
Following the Ross–Macdonald form, transmission scales roughly as

\[
R_0(T) \;\propto\; \frac{a(T)^2 \, b(T) \, e^{-\mu(T)/\text{EIR}(T)}}{\mu(T)},
\]

where $a(T)$ is the biting rate, $b(T)$ vector competence, $\mu(T)$ the adult mortality rate, and $\text{EIR}(T)$ the extrinsic incubation rate.
Each trait is itself a hump-shaped function of temperature, so their combination is sharply peaked.

## A unimodal thermal response

A convenient empirical form for a single thermal trait is the **Briere function**,

\[
f(T) = c \, T \, (T - T_0) \, \sqrt{T_m - T}, \qquad T_0 \le T \le T_m,
\]

and $f(T) = 0$ outside $[T_0, T_m]$.
Here $T_0$ is the lower thermal limit, $T_m$ the upper thermal limit, and $c$ a scaling constant.
The curve rises from zero at $T_0$, peaks at an optimum skewed toward the warm end, and drops back to zero at $T_m$.
This is why the same disease can be limited by cold at high latitudes and by heat in the hottest seasons, with a transmission belt in between.

## Precipitation, water, and climate variability

Temperature is only one axis; water is the other.
Rainfall creates the standing pools where *Aedes* and *Anopheles* mosquitoes lay eggs, so transmission often tracks the rainy season with a lag of a few weeks.
Yet the relationship is not monotone: heavy rain can flush out breeding sites, and drought can concentrate people and vectors around the few remaining water sources.
Climate variability adds a lower-frequency rhythm, and the **El Niño–Southern Oscillation (ENSO)** is the clearest example, with El Niño years reshaping temperature and rainfall enough to trigger malaria, dengue, and cholera anomalies across whole regions.
Arthur and colleagues emphasize that these environmental forces act alongside social ones, so climate signals must be read against human context rather than in isolation ([Arthur et al., 2017, Philosophical Transactions of the Royal Society B](https://consensus.app/papers/details/82e0c9e61a145a1a933419630f12d3c3/?utm_source=claude_desktop)).

## Range shifts, land use, and spillover

As the climate warms, thermal envelopes move, and so do the diseases tied to them.
Vectors and their pathogens expand into newly suitable altitudes and latitudes, exposing populations with no prior immunity and health systems with no prior experience.
At the same time, **land-use change**, deforestation, agricultural expansion, and urban encroachment on wildlife habitat, brings people into novel contact with reservoir species.
Biodiversity loss can concentrate transmission in the competent hosts that persist in degraded landscapes, raising **spillover** risk at the human–wildlife interface, the theme of [reservoir ecology](../math/reservoir-ecology.md).
The planetary-health framing makes this explicit: ecosystem change is not a backdrop to human health but a direct driver of it, and warming is expanding the caseload that clinicians must handle ([Öncü et al., 2025, Infection](https://consensus.app/papers/details/ab1887a54b445d15acf0562528d7f850/?utm_source=claude_desktop)).

## WASH, environmental pathways, and surveillance

Not all environmental transmission runs through a vector.
Water, sanitation, and hygiene (**WASH**) govern the fecal–oral pathogens, so a cholera or rotavirus outbreak is often an environmental-infrastructure failure as much as a biological event.
Pathogens also persist in soil, surface water, and air, and monitoring those compartments is how the environment becomes a data stream rather than only a risk factor.
**Environmental surveillance**, wastewater sampling for viral shedding and systematic vector trapping and identification, turns the environment into an early-warning sensor, feeding the integrated signal described in [one-health surveillance](one-health-surveillance.md).

## A worked example

Consider a mosquito-borne pathogen whose relative transmission follows a Briere thermal curve with lower limit $T_0 = 15\,^\circ\text{C}$, upper limit $T_m = 34\,^\circ\text{C}$, and scaling $c = 2 \times 10^{-4}$.
We evaluate $f(T)$ across a temperature grid, normalize by its peak, and read off the thermal optimum and the relative transmission at a few representative temperatures.
The optimum sits at about $29\,^\circ\text{C}$, transmission is only a fifth of its peak at a cool $18\,^\circ\text{C}$, near-maximal at $30\,^\circ\text{C}$, and collapses to zero at $35\,^\circ\text{C}$ once temperature exceeds the vector's upper thermal limit.
The lesson is that transmission peaks in the middle and fails at both extremes, so warming can either raise or lower risk depending on which side of the optimum a place starts.

## In code

The Python block evaluates the Briere thermal-performance curve, finds the optimum, and prints relative transmission at representative temperatures.
The R and Julia snippets are illustrative sketches of the same calculation.

### R

```r
c <- 2e-4; T0 <- 15; Tm <- 34
briere <- function(T) ifelse(T > T0 & T < Tm,
                             c * T * (T - T0) * sqrt(Tm - T), 0)
grid <- seq(10, 36, by = 0.01)
vals <- briere(grid)
opt  <- grid[which.max(vals)]
peak <- max(vals)
cat("thermal optimum (C):", round(opt, 2), "\n")
for (T in c(18, 25, 30, 35))
  cat(T, "C ->", round(briere(T) / peak, 3), "\n")
```

### Python

```python
import numpy as np

c, T0, Tm = 2.0e-4, 15.0, 34.0

def briere(T):
    T = np.asarray(T, dtype=float)
    val = c * T * (T - T0) * np.sqrt(np.clip(Tm - T, 0, None))
    return np.where((T > T0) & (T < Tm), val, 0.0)

grid = np.linspace(10, 36, 2601)
vals = briere(grid)
opt = grid[np.argmax(vals)]
peak = vals.max()

print("thermal optimum (C):", round(float(opt), 2))
for T in (18, 25, 30, 35):
    rel = float(briere(T)) / peak
    print(f"{T} C -> relative transmission {rel:.3f}")
```

<!-- python-output:auto -->
```text
thermal optimum (C): 29.22
18 C -> relative transmission 0.238
25 C -> relative transmission 0.826
30 C -> relative transmission 0.991
35 C -> relative transmission 0.000
```
<!-- /python-output:auto -->

### Julia

```julia
c, T0, Tm = 2e-4, 15.0, 34.0
briere(T) = (T0 < T < Tm) ? c * T * (T - T0) * sqrt(Tm - T) : 0.0

grid = 10:0.01:36
vals = briere.(grid)
opt  = grid[argmax(vals)]
peak = maximum(vals)
println("thermal optimum (C): ", round(opt, digits = 2))
for T in (18, 25, 30, 35)
    println(T, " C -> ", round(briere(T) / peak, digits = 3))
end
```

## Why it matters

Treating the environment as a first-class driver, not a footnote, changes what a transmission model can explain and predict.
The unimodal thermal response alone tells us that warming does not raise risk everywhere; it shifts risk poleward and upward while eventually suppressing transmission where it becomes too hot.
This is the leg of One Health that postgraduate and quantitative training most neglects, with environment and conservation under-represented relative to human and animal health ([Adeyemi et al., 2024, One Health Outlook](https://consensus.app/papers/details/738b691d2ad75509a84b673bc00bbb74/?utm_source=claude_desktop)).
Building environmental drivers, temperature, water, land use, and surveillance streams, into our models is how planetary health becomes something we can measure and act on rather than merely invoke.

## Related

- [Vector-borne disease](../math/vector-borne.md)
- [Climate forcing in transmission models](../math/climate-forcing-in-transmission-models.md)
- [Reservoir ecology](../math/reservoir-ecology.md)
- [One Health surveillance](one-health-surveillance.md)
- [Epidemiology](../epidemiology.md)
