---
title: "Density-Dependent and Frequency-Dependent Transmission"
description: "How the contact rate scales with host density sets whether an epidemic has a critical density threshold, and why directly transmitted, sexually transmitted, and vector-borne diseases behave differently."
---

# Density-Dependent and Frequency-Dependent Transmission

The rate at which new infections appear is a product of how many infectious individuals there are and how often a susceptible meets one.
That second piece — the contact rate — is where two classic assumptions part ways: does an individual meet more others as the population gets denser, or does it keep a roughly fixed number of contacts no matter how crowded things get?
The answer decides whether a pathogen faces a critical host density below which it cannot spread, and it changes what control does.

![Left: the per-individual contact rate rises with density under density-dependent transmission but stays flat under frequency-dependent transmission. Right: as a result density-dependent R0 grows with host density and crosses one at a threshold N_T, while frequency-dependent R0 is constant.](../assets/figures/transmission-modes.svg)

## One transmission term, two contact rules

Write new infections per unit time as a per-capita contact rate $C(N)$, a per-contact transmission probability $\beta$, and the chance a contact is with an infectious individual, $I/N$: $$\text{new infections} = \beta\,C(N)\,S\,\frac{I}{N}.$$ Everything hinges on how the contact rate $C(N)$ depends on the total host density $N$.

**Density-dependent transmission** assumes contacts scale with density, $C(N)=\kappa N$.
Twice as many hosts in the same area means twice as many encounters per individual.
Substituting collapses the term to the **mass-action** form $$\frac{dI}{dt}=\beta\kappa\,S I - \gamma I,$$ where the transmission constant is often just written $\beta' = \beta\kappa$.
This is the assumption baked into the classic [SIR model](sir.md) when it is written with $\beta S I$.

**Frequency-dependent transmission** (also called *standard incidence*) assumes the contact rate is fixed, $C(N)=\kappa$, independent of density.
Each individual makes about the same number of contacts whether the population is sparse or dense.
The term becomes $$\frac{dI}{dt}=\beta\kappa\,\frac{S I}{N} - \gamma I,$$ which is the $\beta S I / N$ form.

The two models look almost identical — they differ only by a factor of $N$ — but that factor changes the biology completely.

## The critical difference: a density threshold

Consider a pathogen invading a fully susceptible population, so $S\approx N$.
It spreads when $dI/dt>0$, i.e. when the [basic reproduction number](next-generation-matrix.md) $R_0>1$.

Under **density dependence**, seeding one infection into $S=N$ gives $dI/dt = (\beta\kappa N - \gamma)I$, so $$R_0 = \frac{\beta\kappa N}{\gamma}.$$ This scales with density.
Setting $R_0=1$ gives a **critical host density** $$N_T = \frac{\gamma}{\beta\kappa},$$ below which the pathogen cannot invade no matter how it is introduced.
Thinning the host population below $N_T$ eradicates the disease — the logic behind culling and behind the local fadeout of measles in small communities before vaccination.

Under **frequency dependence**, the $N$ cancels: $$R_0 = \frac{\beta\kappa}{\gamma},$$ independent of population size.
There is **no density threshold**.
A sexually transmitted infection can persist in a small, sparse population just as well as a large one, because partners are acquired at a rate set by behavior, not by crowding.

## Which assumption fits which disease

The right choice is an empirical question about how contact scales, not a mathematical preference.

- **Density-dependent** fits many directly transmitted diseases where crowding raises encounter rates: airborne and fecal-oral infections in wildlife and livestock, phocine distemper in seals, many plant pathogens.
- **Frequency-dependent** fits sexually transmitted infections (partner acquisition is behavioral), vector-borne diseases (the [biting rate](vector-borne.md) is set by the vector, not host density), and social-contact diseases in populations that regulate group size.

Real systems often sit between the two, and a common compromise is the power law $C(N)=\kappa N^{q}$ with $0\le q\le 1$: $q=1$ recovers density dependence, $q=0$ recovers frequency dependence.
Fitting $q$ to contact or incidence data is a standard way to let the data decide ([McCallum, Barlow & Hone 2001](https://doi.org/10.1016/S0169-5347(01)02144-9)).

## A worked example

Take a recovery rate $\gamma=0.1\ \text{day}^{-1}$ (a 10-day infectious period) and compare two population sizes, $N=100$ and $N=1000$.

For a **density-dependent** pathogen with $\beta\kappa=0.002\ \text{day}^{-1}$ per individual, the threshold is $N_T=\gamma/(\beta\kappa)=0.1/0.002=50$ hosts.
So $R_0=\beta\kappa N/\gamma$ is $2$ at $N=100$ and $20$ at $N=1000$ — the same pathogen barely spreads in the small population and explodes in the large one.

For a **frequency-dependent** pathogen with $\beta\kappa=0.3\ \text{day}^{-1}$, $R_0=0.3/0.1=3$ in *both* populations.
Halving or doubling the host density does nothing to invasion.

## In code

We compute $R_0$ under both assumptions at two densities to see the density dependence appear and disappear.

### R

```r
gamma <- 0.1

# density-dependent: R0 scales with N, threshold at N_T
bk_dd <- 0.002
R0_dd <- function(N) bk_dd * N / gamma
N_T <- gamma / bk_dd                 # critical host density = 50

# frequency-dependent: R0 independent of N
bk_fd <- 0.3
R0_fd <- function(N) bk_fd / gamma

sapply(c(100, 1000), R0_dd)          # 2 and 20
sapply(c(100, 1000), R0_fd)          # 3 and 3
N_T                                  # 50
```

### Python

```python
gamma = 0.1
bk_dd, bk_fd = 0.002, 0.3

R0_dd = lambda N: bk_dd * N / gamma          # scales with density
R0_fd = lambda N: bk_fd / gamma              # flat in density
N_T = gamma / bk_dd                          # critical host density

print("density-dependent R0:", [round(R0_dd(N), 2) for N in (100, 1000)])
print("frequency-dependent R0:", [round(R0_fd(N), 2) for N in (100, 1000)])
print("critical host density N_T:", N_T)
```

<!-- python-output:auto -->
```text
density-dependent R0: [2.0, 20.0]
frequency-dependent R0: [3.0, 3.0]
critical host density N_T: 50.0
```
<!-- /python-output:auto -->

### Julia

```julia
gamma = 0.1
bk_dd, bk_fd = 0.002, 0.3

R0_dd(N) = bk_dd * N / gamma      # scales with density
R0_fd(N) = bk_fd / gamma          # flat in density
N_T = gamma / bk_dd               # critical host density = 50

R0_dd.((100, 1000))               # (2.0, 20.0)
R0_fd.((100, 1000))               # (3.0, 3.0)
```

## Why it matters

The transmission term is the single most consequential modeling choice in an epidemic model, and it is easy to make by accident: writing $\beta S I$ versus $\beta S I / N$ commits you to a whole theory of how contact works.
Get it wrong and the model can predict a density threshold that does not exist, or miss one that does — which in turn misprices interventions like culling, vaccination, and social distancing.
The same distinction propagates into $R_0$ calculations via the [next-generation matrix](next-generation-matrix.md), into the [vector-borne](vector-borne.md) models where frequency dependence is the norm, and into the [evolution of virulence](evolution-of-virulence.md), where how transmission scales with host density shapes the selective pressure on the pathogen.

## Related

- [Compartmental Models (SIR)](sir.md) — where the $\beta S I / N$ term comes from
- [The Next-Generation Matrix and R₀](next-generation-matrix.md)
- [Vector-Borne Disease Models](vector-borne.md) — frequency-dependent transmission via biting
- [SEIR and Compartmental Extensions](seir-models.md)
- [Exponential and Logistic Growth](logistic-growth.md) — density dependence in population growth
- [Adaptive Dynamics and the Evolution of Virulence](evolution-of-virulence.md)
- [Quantitative Methods](../math.md)
