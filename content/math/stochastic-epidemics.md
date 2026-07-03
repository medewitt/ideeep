---
title: "Stochastic Epidemics and the Gillespie Algorithm"
---

# Stochastic Epidemics and the Gillespie Algorithm

Deterministic ODE models describe the average behavior of very large populations, but real outbreaks begin with a handful of cases where chance rules.
Even when $R_0>1$ an introduction can fizzle out entirely, and to capture that we model the epidemic as a random process rather than a smooth flow.

## Why chance matters

The [SIR model](sir.md) written as differential equations predicts that whenever $R_0>1$ the infectious class grows and an epidemic occurs.
That is only true on average and in the limit of large numbers.
Early in an outbreak there might be just one or two infectious individuals, and each recovery or transmission is a discrete random event.
By bad luck the first few cases can recover before infecting anyone, and the outbreak dies out even though conditions favored growth.
This randomness arising from the discreteness of individuals and events is called **demographic stochasticity**, and it is invisible to the deterministic model.

## The epidemic as a Markov jump process

We treat the state $(S, I)$ (with $R = N - S - I$ determined) as a continuous-time Markov chain.
From any state only two kinds of events can occur, each with its own rate:

- **Infection** ($S \to S-1$, $I \to I+1$) at rate $\displaystyle \beta \frac{S I}{N}$
- **Recovery** ($I \to I-1$) at rate $\gamma I$

Between events nothing happens; the state jumps at random instants.
Because the process is memoryless, the time to the next event of a given type is [exponentially distributed](exponential-distribution.md), and the total number of events in a window is governed by the [Poisson distribution](poisson-distribution.md).

## The Gillespie algorithm

The Gillespie stochastic simulation algorithm (SSA), also called the direct method, generates *exact* sample trajectories of this jump process — no time-discretization error.
It rests on two facts about competing exponential clocks.

First, if the total event rate is $R_{\text{tot}} = \sum_i r_i$, the waiting time $\tau$ until the *next* event (whichever it is) is exponential with rate $R_{\text{tot}}$:

\[
\tau \sim \text{Exponential}(R_{\text{tot}}), \qquad \tau = -\frac{\ln u_1}{R_{\text{tot}}},
\]

where $u_1$ is uniform on $(0,1)$.
Second, the event that actually fires is chosen with probability proportional to its own rate, $P(\text{event }i) = r_i / R_{\text{tot}}$.

The loop is:

1. Compute all event rates $r_i$ from the current state and their sum $R_{\text{tot}}$.
2. Draw the waiting time $\tau = -\ln(u_1)/R_{\text{tot}}$ and advance time $t \leftarrow t + \tau$.
3. Draw $u_2$ and pick the event whose cumulative rate first exceeds $u_2 R_{\text{tot}}$.
4. Update the state according to that event, and repeat until no events are possible ($R_{\text{tot}} = 0$).

For the SIR model the process stops when $I = 0$: the outbreak is over.

## Minor and major outbreaks

Run the SSA many times from a single infectious seed and the outcomes split into two clumps.
Some trajectories die out almost immediately after a handful of cases — **minor outbreaks** — while others take off and infect a large fraction of the population — **major outbreaks**.
The gap between them is the signature of stochasticity: the deterministic model sees only the average.

While the susceptible pool is still essentially full, each infection behaves like an independent birth-and-death event, so the early phase is well approximated by a [branching process](branching-processes.md) with mean offspring $R_0$.
That approximation gives the probability an introduction fails to establish.
For the stochastic SIR started from one case, the extinction (minor-outbreak) probability is

\[
P(\text{minor outbreak}) \approx \frac{1}{R_0} \quad (R_0 > 1),
\]

so with $R_0 = 2$ roughly half of introductions die out by chance despite favorable conditions.
Conditional on takeoff, the **final-size distribution** — the total number ever infected — concentrates near the deterministic prediction, giving the characteristic bimodal picture of small versus large outbreaks.

## Worked example

Consider a stochastic SIR with population $N = 1000$, transmission rate $\beta = 0.4\ \text{day}^{-1}$, and recovery rate $\gamma = 0.2\ \text{day}^{-1}$, so $R_0 = \beta/\gamma = 2$.
Suppose the current state is $S = 990$, $I = 5$.
The two event rates are

\[
r_{\text{inf}} = \beta \frac{S I}{N} = 0.4 \cdot \frac{990 \cdot 5}{1000} = 1.98\ \text{day}^{-1},
\qquad
r_{\text{rec}} = \gamma I = 0.2 \cdot 5 = 1.0\ \text{day}^{-1}.
\]

The total rate is $R_{\text{tot}} = 2.98\ \text{day}^{-1}$, so the expected time to the next event is $1/2.98 \approx 0.336$ days.
The next event is an infection with probability $1.98/2.98 \approx 0.66$ and a recovery with probability $1.0/2.98 \approx 0.34$.
Because $R_0 = 2$, roughly $1/R_0 = 50\%$ of outbreaks seeded by a single case will go extinct before becoming major — a fraction the deterministic model cannot express.

## Simulation

We implement the Gillespie SSA from scratch (no ODE solver) and run several trajectories, seeding the RNG for reproducibility.

### R

```r
set.seed(42)

gillespie_sir <- function(N = 1000, I0 = 5, beta = 0.4, gamma = 0.2, tmax = 200) {
  S <- N - I0; I <- I0; t <- 0
  ts <- t; Is <- I
  while (I > 0 && t < tmax) {
    r_inf <- beta * S * I / N
    r_rec <- gamma * I
    Rtot  <- r_inf + r_rec
    if (Rtot == 0) break
    t <- t - log(runif(1)) / Rtot                 # exponential waiting time
    if (runif(1) < r_inf / Rtot) { S <- S - 1; I <- I + 1 }  # infection
    else                         { I <- I - 1 }              # recovery
    ts <- c(ts, t); Is <- c(Is, I)
  }
  list(t = ts, I = Is, final_size = N - S)
}

runs <- replicate(5, gillespie_sir()$final_size)
runs   # mix of minor (~single digits) and major (~800) outbreaks; R0 = 2
```

### Python

```python
import numpy as np
rng = np.random.default_rng(42)

def gillespie_sir(N=1000, I0=5, beta=0.4, gamma=0.2, tmax=200.0):
    S, I, t = N - I0, I0, 0.0
    ts, Is = [t], [I]
    while I > 0 and t < tmax:
        r_inf = beta * S * I / N
        r_rec = gamma * I
        Rtot = r_inf + r_rec
        if Rtot == 0:
            break
        t += -np.log(rng.random()) / Rtot            # exponential waiting time
        if rng.random() < r_inf / Rtot:              # infection
            S, I = S - 1, I + 1
        else:                                        # recovery
            I -= 1
        ts.append(t); Is.append(I)
    return np.array(ts), np.array(Is), N - S

sizes = [gillespie_sir()[2] for _ in range(5)]
print(sizes)   # bimodal: some minor (~few), some major (~800); R0 = 2
```

<!-- python-output:auto -->
```text
[816, 866, 777, 796, 787]
```
<!-- /python-output:auto -->

### Julia

```julia
using Random
Random.seed!(42)

function gillespie_sir(; N=1000, I0=5, beta=0.4, gamma=0.2, tmax=200.0)
    S, I, t = N - I0, I0, 0.0
    ts, Is = [t], [I]
    while I > 0 && t < tmax
        r_inf = beta * S * I / N
        r_rec = gamma * I
        Rtot  = r_inf + r_rec
        Rtot == 0 && break
        t += -log(rand()) / Rtot                 # exponential waiting time
        if rand() < r_inf / Rtot
            S -= 1; I += 1                        # infection
        else
            I -= 1                               # recovery
        end
        push!(ts, t); push!(Is, I)
    end
    (t = ts, I = Is, final_size = N - S)
end

sizes = [gillespie_sir().final_size for _ in 1:5]
println(sizes)   # mix of minor and major outbreaks; R0 = 2
```

## Why it matters

Stochastic epidemic models answer questions the deterministic ones cannot: the probability an introduction sparks an outbreak, the risk of fade-out in a small community, and the full spread of possible final sizes rather than a single number.
The Gillespie algorithm makes these accessible with a handful of lines of code and no approximation, and the same SSA drives models across chemical kinetics, population genetics, and systems biology.
Understanding when to reach for a stochastic model — small numbers, early phase, extinction risk — versus a deterministic one is a core judgment in infectious-disease modeling.

## Related

- [The SIR Model](sir.md)
- [Branching Processes](branching-processes.md)
- [Exponential Distribution](exponential-distribution.md)
- [Poisson Distribution](poisson-distribution.md)
- [SEIR and Compartmental Extensions](seir-models.md)
- [The Next-Generation Matrix and R₀](next-generation-matrix.md)
- [Quantitative Methods](../math.md)
