---
title: "Branching Processes"
---

# Branching Processes

A branching process models a population in which each individual independently produces a random number of offspring drawn from a fixed offspring distribution.
The classic version is the Galton–Watson process, and it answers a sharp question: starting from a single ancestor, does the lineage die out or grow without bound?

## The Galton–Watson process

Label the generations $0, 1, 2, \dots$, starting with one individual in generation $0$.
Each individual, [independently](probability-basics.md), leaves a random number of offspring $X$ with probability mass function $p_k = P(X=k)$.
Let $Z_n$ be the population size in generation $n$, so $Z_0 = 1$ and each individual in generation $n$ founds the next generation.

The offspring distribution has a mean, the [expected](expected-value.md) number of children per individual, $$m = \mathbb{E}[X] = \sum_{k\ge 0} k\,p_k.$$ This single number controls the qualitative fate of the process.

## Expected growth

Because individuals reproduce independently, expectations multiply across generations.
Conditioning on the previous generation gives $\mathbb{E}[Z_{n}\mid Z_{n-1}] = m\,Z_{n-1}$, and taking expectations again yields $$\mathbb{E}[Z_n] = m^{\,n}.$$ The expected population size grows or shrinks geometrically at rate $m$.

In the epidemic reading, one individual is one infection and its "offspring" are the people it infects, so $m$ is exactly the basic reproduction number $R_0$.
The mean chain then grows like $R_0^{\,n}$, the same quantity that the [next-generation matrix](next-generation-matrix.md) computes for structured populations and that drives the early exponential phase of an [SIR](sir.md) outbreak.

## The probability generating function

The natural bookkeeping tool for offspring counts is the probability generating function (PGF) $$G(s) = \mathbb{E}[s^{X}] = \sum_{k\ge 0} p_k s^{k}, \qquad 0\le s\le 1.$$ It packages the whole offspring distribution into one function, much as the [moment generating function](moment-generating-functions.md) does for continuous variables.
Its derivative at $s=1$ recovers the mean, $G'(1) = m$, and composing $G$ with itself tracks successive generations.

## Extinction

Let $q$ be the probability of ultimate extinction — that the lineage eventually reaches size $0$.
Extinction of the whole process happens exactly when each of the first generation's sub-lineages goes extinct, and those are independent copies of the original.
This self-similarity gives the fixed-point equation $$q = G(q).$$ The extinction probability is the smallest solution of $s = G(s)$ in the interval $[0,1]$.

Classifying by the mean $m$:

- **Subcritical** ($m<1$): the only fixed point up to $1$ forces $q=1$; extinction is certain.
- **Critical** ($m=1$): still $q=1$; the process dies out with probability one (though it can drift large first).
- **Supercritical** ($m>1$): there is a fixed point $q<1$, so the process survives with positive probability $1-q$.

The gap between the critical case and genuine growth is why small populations can vanish by chance even when conditions favor increase — the same stochastic fragility seen in [genetic drift](genetic-drift.md).

## Outbreaks: will an introduction take off?

Branching processes describe the early, stochastic phase of an outbreak, when the susceptible pool is still effectively unlimited.
A single imported case starts one lineage of infections; either it fizzles out or it seeds a major outbreak.

A common and tractable choice is a Poisson offspring distribution with mean $R_0$ (see the [Poisson distribution](poisson-distribution.md)), whose PGF is $G(s) = e^{R_0(s-1)}$.
The extinction probability solves $$s = e^{R_0(s-1)},$$ and the probability of a major outbreak is $1-q$.
When $R_0 \le 1$ every introduction eventually dies out; only $R_0>1$ gives a genuine chance of takeoff.

## Worked example

Take a Poisson offspring distribution with $R_0 = 2$, so we solve $$s = e^{2(s-1)}.$$ One root is $s=1$, but we want the smallest root in $[0,1]$.
Iterating $s_{k+1} = e^{2(s_k-1)}$ from $s_0 = 0$ gives $s_1 = e^{-2}\approx 0.135$, then $0.176$, $0.194$, $0.200$, converging to $$q \approx 0.203.$$ So the probability of extinction from a single introduction is about $0.203$, and the probability of a major outbreak is $$1-q \approx 0.797.$$ Even with $R_0=2$, roughly one in five introductions fizzles out purely by chance.

## In code

### R

```r
# Extinction probability by fixed-point iteration: s = G(s)
G <- function(s, R0 = 2) exp(R0 * (s - 1))   # Poisson offspring PGF
q <- 0
for (i in 1:100) q <- G(q)
q            # ~ 0.2032
1 - q        # ~ 0.7968  (major-outbreak probability)

# Simulate branching trees and estimate extinction empirically
set.seed(1)
sim_extinct <- function(R0 = 2, gens = 40) {
  z <- 1
  for (g in 1:gens) {
    z <- sum(rpois(z, R0))   # each individual has Poisson(R0) offspring
    if (z == 0) return(TRUE) # extinct
  }
  FALSE                      # still alive -> treat as survival
}
mean(replicate(10000, sim_extinct()))  # ~ 0.20, matches q
```

### Python

```python
import numpy as np

def G(s, R0=2.0):        # Poisson offspring PGF
    return np.exp(R0 * (s - 1))

q = 0.0
for _ in range(100):
    q = G(q)
print(q, 1 - q)          # ~ 0.2032  0.7968

rng = np.random.default_rng(1)
def sim_extinct(R0=2.0, gens=40):
    z = 1
    for _ in range(gens):
        z = rng.poisson(R0, size=z).sum()  # offspring of current generation
        if z == 0:
            return True
    return False
print(np.mean([sim_extinct() for _ in range(10000)]))  # ~ 0.20
```

### Julia

```julia
using Distributions, Statistics, Random

G(s; R0=2.0) = exp(R0 * (s - 1))     # Poisson offspring PGF
q = 0.0
for _ in 1:100
    q = G(q)
end
println((q, 1 - q))                  # ~ (0.2032, 0.7968)

Random.seed!(1)
function sim_extinct(; R0=2.0, gens=40)
    z = 1
    for _ in 1:gens
        z = sum(rand(Poisson(R0), z))
        z == 0 && return true
    end
    false
end
println(mean(sim_extinct() for _ in 1:10000))  # ~ 0.20
```

## Why it matters

Branching processes turn a vague worry — "could this spread?" — into a precise probability, separating the deterministic message of $R_0$ from the luck of small numbers.
They explain why an outbreak with $R_0>1$ can still fail to establish, why small populations wink out despite favorable growth, and how genealogies and family names go extinct.
The same machinery underlies nuclear chain reactions, PCR amplification, surname survival, and the founding dynamics of new mutations.

## Related

- [Probability Basics](probability-basics.md)
- [Expected Value](expected-value.md)
- [Poisson Distribution](poisson-distribution.md)
- [Moment Generating Functions](moment-generating-functions.md)
- [Next-Generation Matrix](next-generation-matrix.md)
- [The SIR Model](sir.md)
- [Stochastic Epidemics and the Gillespie Algorithm](stochastic-epidemics.md)
- [Genetic Drift](genetic-drift.md)
- [Quantitative Methods](../math.md)
