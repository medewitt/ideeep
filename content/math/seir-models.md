---
title: "SEIR and Compartmental Extensions"
---

# SEIR and Compartmental Extensions

Many pathogens do not make a host infectious the instant they are infected — there is a latent period during which the virus or bacterium replicates unseen.
The SEIR model captures this by inserting an *Exposed* compartment between susceptible and infectious, and a whole family of extensions builds on the same idea.

## From SIR to SEIR

The [SIR model](sir.md) assumes a newly infected individual is immediately infectious.
For measles, COVID-19, and many other diseases this is wrong: there is an incubation delay before the host can transmit.
The SEIR model adds an *Exposed* (E) class of individuals who are infected but not yet infectious.

The compartments are $S \to E \to I \to R$, and the closed-population dynamics are

\[
\begin{aligned}
\frac{dS}{dt} &= -\beta \frac{S I}{N} \\
\frac{dE}{dt} &= \beta \frac{S I}{N} - \sigma E \\
\frac{dI}{dt} &= \sigma E - \gamma I \\
\frac{dR}{dt} &= \gamma I
\end{aligned}
\]

where $\beta$ is the transmission rate, $\gamma$ is the recovery rate, and $\sigma$ is the rate at which exposed individuals become infectious.
The mean latent period is $1/\sigma$, just as the mean infectious period is $1/\gamma$.
The total population $N = S + E + I + R$ is constant, since every term that leaves one compartment enters another.

## R₀ for the closed SEIR

A subtle and important point: the latent stage does **not** change the basic reproduction number.
For the closed SEIR model,

\[
R_0 = \frac{\beta}{\gamma}
\]

exactly as in the SIR model.
The reason is that $R_0$ counts secondary infections per infectious individual over a whole infectious career, and every exposed individual eventually becomes infectious (with probability one, since there is no death).
Adding the E class delays the epidemic — it lengthens the generation interval and slows the initial growth rate — but it does not alter how many people each case ultimately infects.
This distinction between the *speed* and the *size* of an epidemic is one of the most useful lessons of the SEIR model.

## Adding vital dynamics

Over longer time horizons we cannot ignore births and deaths.
Suppose individuals are born susceptible at rate $\mu N$ and every compartment experiences a per-capita death rate $\mu$ (so the population size stays constant on average):

\[
\begin{aligned}
\frac{dS}{dt} &= \mu N -\beta \frac{S I}{N} - \mu S \\
\frac{dE}{dt} &= \beta \frac{S I}{N} - (\sigma + \mu) E \\
\frac{dI}{dt} &= \sigma E - (\gamma + \mu) I \\
\frac{dR}{dt} &= \gamma I - \mu R
\end{aligned}
\]

Now the latent stage *does* affect $R_0$, because an exposed individual can die before ever becoming infectious.
The [next-generation matrix](next-generation-matrix.md) yields

\[
R_0 = \frac{\beta}{\gamma+\mu}\cdot\frac{\sigma}{\sigma+\mu}
\]

The first factor is the SIR-with-deaths reproduction number; the second, $\sigma/(\sigma+\mu)$, is the probability of surviving the latent period.
When mortality is slow relative to the latent period ($\mu \ll \sigma$) this factor is close to $1$ and we recover $R_0 \approx \beta/(\gamma+\mu)$.

## Endemic equilibrium

With vital dynamics the disease need not die out — it can settle into a steady endemic state.
Setting the derivatives to zero gives two [equilibria](equilibria-and-stability.md): the disease-free equilibrium $(S,E,I,R)=(N,0,0,0)$ and an endemic equilibrium with $I^*>0$.
The disease-free state is stable when $R_0<1$ and loses stability at $R_0=1$, where the endemic branch appears — a transcritical bifurcation.
At the endemic equilibrium the susceptible fraction is pinned at $S^*/N = 1/R_0$: the pathogen depletes susceptibles until each case just replaces itself.

## Other compartmental extensions

The same building blocks generate a large model family.

- **SIS** — no lasting immunity; recovered individuals return directly to susceptible ($I \to S$).
This suits many bacterial and sexually transmitted infections.
- **SIRS** — immunity wanes at rate $\omega$, so $R \to S$; the flux $\omega R$ recycles recovered individuals and can sustain recurrent epidemics.
- **Vector-borne** — coupling a host model to a mosquito population, as in the [Ross–Macdonald model](vector-borne.md) for malaria and dengue.
- **Stochastic** — replacing the ODEs with a random jump process to capture chance extinction in small populations, treated in [stochastic epidemics](stochastic-epidemics.md).

## Vaccination and herd immunity

Vaccination moves individuals from $S$ directly to $R$, shrinking the susceptible pool that fuels transmission.
If a fraction $p$ of the population is immune, the *effective* reproduction number is $R_0(1-p)$.
Transmission cannot be sustained once $R_0(1-p) < 1$, i.e. once

\[
p > 1 - \frac{1}{R_0}
\]

This is the **herd-immunity threshold**: for measles with $R_0 \approx 15$ it demands about $93\%$ coverage, while for a pathogen with $R_0 = 2$ only $50\%$ immunity suffices.
It is the same $1/R_0$ that sets the endemic susceptible fraction — vaccination simply pre-empts the depletion the epidemic would otherwise cause.

## Worked example

Consider a respiratory pathogen with mean latent period $3$ days, mean infectious period $5$ days, and transmission rate $\beta = 0.5\ \text{day}^{-1}$.
Then $\sigma = 1/3 \approx 0.333\ \text{day}^{-1}$ and $\gamma = 1/5 = 0.2\ \text{day}^{-1}$.

For the closed SEIR model, \[ R_0 = \frac{\beta}{\gamma} = \frac{0.5}{0.2} = 2.5. \] The latent period does not enter — each case infects $2.5$ others on average regardless of how long it waits to become infectious.

Now add a slow demographic turnover with $\mu = 1/(70\times 365) \approx 3.9\times 10^{-5}\ \text{day}^{-1}$.
The survival-through-latency factor is $\sigma/(\sigma+\mu) \approx 0.9999$, so \[ R_0 = \frac{0.5}{0.2 + 3.9\times 10^{-5}}\cdot 0.9999 \approx 2.50, \] essentially unchanged, as expected when mortality is far slower than disease progression.
The herd-immunity threshold is $1 - 1/2.5 = 0.6$, so vaccinating $60\%$ of the population would halt sustained transmission.

## Simulation

We integrate the closed SEIR ODEs from a nearly susceptible population with a small infectious seed and plot the epidemic curve.

### R

```r
library(deSolve)

seir <- function(t, y, p) {
  with(as.list(c(y, p)), {
    N  <- S + E + I + R
    dS <- -beta * S * I / N
    dE <-  beta * S * I / N - sigma * E
    dI <-  sigma * E - gamma * I
    dR <-  gamma * I
    list(c(dS, dE, dI, dR))
  })
}

p  <- c(beta = 0.5, sigma = 1/3, gamma = 0.2)   # R0 = beta/gamma = 2.5
y0 <- c(S = 999999, E = 0, I = 1, R = 0)
t  <- seq(0, 200, by = 1)
out <- ode(y = y0, times = t, func = seir, parms = p)

matplot(out[, "time"], out[, c("S", "E", "I", "R")], type = "l",
        xlab = "day", ylab = "count", lty = 1)
max(out[, "I"])   # peak infectious ~ 1.3e5 around day ~ 70
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

def seir(t, y, beta, sigma, gamma):
    S, E, I, R = y
    N = S + E + I + R
    return [-beta*S*I/N,
             beta*S*I/N - sigma*E,
             sigma*E - gamma*I,
             gamma*I]

beta, sigma, gamma = 0.5, 1/3, 0.2   # R0 = 2.5
y0 = [999999, 0, 1, 0]
sol = solve_ivp(seir, [0, 200], y0, args=(beta, sigma, gamma),
                t_eval=np.arange(0, 201), rtol=1e-8)

peak_I = sol.y[2].max()
print(round(peak_I))            # ~ 132000
print(sol.t[sol.y[2].argmax()]) # peak day ~ 70
```

### Julia

```julia
using DifferentialEquations

function seir!(du, u, p, t)
    S, E, I, R = u
    beta, sigma, gamma = p
    N = S + E + I + R
    du[1] = -beta*S*I/N
    du[2] =  beta*S*I/N - sigma*E
    du[3] =  sigma*E - gamma*I
    du[4] =  gamma*I
end

u0 = [999999.0, 0.0, 1.0, 0.0]
p  = (0.5, 1/3, 0.2)            # R0 = 2.5
prob = ODEProblem(seir!, u0, (0.0, 200.0), p)
sol  = solve(prob, Tsit5(), saveat = 1.0)

maximum(getindex.(sol.u, 3))   # peak infectious ~ 1.32e5
```

## Why it matters

The SEIR model and its relatives are the workhorses of applied epidemiology, from pandemic forecasting to vaccination planning.
By separating latent from infectious time they correctly predict the *timing* of an epidemic — its growth rate and peak — which matters enormously for hospital surge planning even though the latent stage leaves $R_0$ untouched in a closed population.
Adding vital dynamics, waning immunity, and vaccination turns the same skeleton into models of endemic disease, recurrent epidemics, and the coverage targets that guide immunization programs.

## Related

- [The SIR Model](sir.md)
- [The Next-Generation Matrix and R₀](next-generation-matrix.md)
- [Equilibria and Linear Stability](equilibria-and-stability.md)
- [Vector-Borne Disease Models](vector-borne.md)
- [Stochastic Epidemics and the Gillespie Algorithm](stochastic-epidemics.md)
- [Quantitative Methods](../math.md)
