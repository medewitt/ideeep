---
title: "Compartmental Models in Biology"
---

# Compartmental Models

Compartmental models have many shapes and sizes.
They divide a population into distinct **compartments** — groups defined by their status with respect to a disease — and describe how individuals move between them over time.
Despite their simplicity, compartmental models are one of the most powerful tools in infectious disease ecology and epidemiology.

## The SIR model

The classic example is the **SIR model**, which divides a population into three compartments:

- **S** — *Susceptible*: individuals who can become infected
- **I** — *Infectious*: individuals who are infected and can transmit
- **R** — *Recovered* (or removed): individuals who are no longer susceptible or infectious

Individuals flow from $S \to I \to R$.
The dynamics are governed by a system of ordinary differential equations:

\[
\begin{aligned}
\frac{dS}{dt} &= -\beta \frac{S I}{N} \\
\frac{dI}{dt} &= \beta \frac{S I}{N} - \gamma I \\
\frac{dR}{dt} &= \gamma I
\end{aligned}
\]

where $\beta$ is the transmission rate, $\gamma$ is the recovery rate, and $N = S + I + R$ is the total population size.

## The basic reproduction number

A key quantity derived from the model is the **basic reproduction number**, $R_0$ — the average number of secondary infections produced by a single infectious individual in a fully susceptible population.
For the SIR model,

\[
R_0 = \frac{\beta}{\gamma}
\]

When $R_0 > 1$, an outbreak can grow; when $R_0 < 1$, it dies out.

## Extensions

The SIR framework extends naturally to capture more biological detail:

- **SEIR** — adds an *Exposed* (latent) compartment for diseases with an incubation period
- **SIS** — allows individuals to return to the susceptible class (no lasting immunity)
- **SIRS** — adds waning immunity, returning recovered individuals to susceptible
- **Vital dynamics** — births and deaths for longer time horizons
- **Vector, spatial, and stochastic** variants for more realistic systems

## Analyzing model behavior

To understand a model's long-term behavior, we identify its equilibria and study their stability.
This is done by linearizing the system and examining the [Jacobian matrix](jacobians.md), which shows how the SIR model can be analyzed at the disease-free equilibrium.

## Related

- [Jacobians](jacobians.md) — stability analysis for the SIR model
- [The Next-Generation Matrix and R₀](next-generation-matrix.md)
- [Equilibria and Linear Stability](equilibria-and-stability.md)
- [Exponential and Logistic Growth](logistic-growth.md)
- [Bifurcations](bifurcations.md) — the $R_0=1$ threshold
- [Pharmacokinetics: Compartment Models](pharmacokinetics.md) — the same compartment framework applied to drugs
- [Mathematical Biology (BIO 301)](../bio301-math-bio.md) — the course where these models are developed in depth
