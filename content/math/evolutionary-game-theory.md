---
title: "Evolutionary Game Theory"
---

# Evolutionary Game Theory

When an individual's fitness depends on what everyone else is doing, evolution becomes a game.
Instead of climbing a fixed fitness landscape, strategies compete against each other, and the "best" move depends on which moves are currently common.

![Replicator dynamics of the Hawk–Dove game converge to the mixed ESS from any starting frequency.](../assets/figures/evolutionary-game-theory.svg)

## Payoffs and strategies

A game is specified by a **payoff matrix** that gives the reward to each strategy when it meets each other strategy.
Write $A_{ij}$ for the payoff to a player using strategy $i$ against an opponent using strategy $j$.
The canonical biological example is the **Hawk–Dove game**, in which two animals contest a resource of value $V$, and escalated fights cost $C$.

Hawks always escalate; Doves display but retreat if the opponent escalates.
Two Hawks fight, split the value, and share the injury cost, for an expected payoff $(V-C)/2$.
A Hawk meeting a Dove takes the whole resource, $V$; the Dove gets nothing.
Two Doves share peacefully, each getting $V/2$.

\[
A = \begin{bmatrix} (V-C)/2 & V \\ 0 & V/2 \end{bmatrix},
\qquad \text{rows and columns ordered } (\text{Hawk}, \text{Dove}).
\]

## Evolutionarily stable strategies

An **evolutionarily stable strategy (ESS)**, introduced by Maynard Smith, is a strategy that, once adopted by (almost) the whole population, cannot be invaded by any rare mutant.
Formally, strategy $s$ is an ESS if for every alternative $s'$ either its self-payoff is strictly larger, $A(s,s) > A(s',s)$, or the payoffs tie against $s$ and $s$ does better against the mutant, $A(s,s) = A(s',s)$ and $A(s,s') > A(s',s')$.
The first condition says $s$ is a best reply to itself (a Nash equilibrium); the second breaks ties in favor of the resident.

An ESS is the game-theoretic version of an uninvadable phenotype, and it links directly to the optimum concepts of [optimization](optimization.md): it is a fitness peak defined relative to the current population rather than in isolation.

## The replicator equation

To see how strategy frequencies actually change, let $x_i$ be the frequency of strategy $i$, with $\sum_i x_i = 1$.
Its expected payoff is $f_i(\mathbf{x}) = \sum_j A_{ij} x_j$, and the population mean payoff is $\bar f(\mathbf{x}) = \sum_j x_j f_j(\mathbf{x})$.
The **replicator equation** says a strategy grows in proportion to how much it beats the average:

\[
\dot{x}_i = x_i\big(f_i(\mathbf{x}) - \bar f(\mathbf{x})\big).
\]

Strategies that earn more than the mean increase in frequency; those below the mean decline; and the simplex $\sum_i x_i = 1$ is preserved because $\sum_i \dot x_i = \bar f - \bar f = 0$.

### ESS and fixed points

The fixed points of the replicator dynamics are exactly the states where every surviving strategy earns the mean payoff, $f_i = \bar f$ for all $i$ with $x_i > 0$.
This connects the two viewpoints: **an ESS is an asymptotically stable fixed point of the replicator dynamics**, an equilibrium that neighbouring frequency mixtures flow back toward.
Checking that stability is the same linear-stability calculation used for any dynamical system in [equilibria and stability](equilibria-and-stability.md); like the coupled feedbacks of [predator–prey](predator-prey.md) models, the game can also produce cycles or coexistence rather than a single winner.

## Worked example: the Hawk–Dove mixed ESS

Assume war is expensive, $C > V$, so neither pure strategy is stable: a population of all Doves is invaded by Hawks (who take $V$ from every Dove), while a population of all Hawks is invaded by Doves (who avoid the ruinous $(V-C)/2$).
Look instead for a **mixed ESS**: a fraction $\hat p$ of Hawks at which Hawk and Dove earn equal payoffs.

The expected payoffs, given a Hawk frequency $p$, are

\[
f_H = p\,\frac{V-C}{2} + (1-p)\,V, \qquad
f_D = p\cdot 0 + (1-p)\,\frac{V}{2}.
\]

Setting $f_H = f_D$ and simplifying, the $V$ and $pV$ terms cancel to leave $-pC + V = 0$, so

\[
\hat p = \frac{V}{C}.
\]

The population settles where the fraction of Hawks equals the value-to-cost ratio.
Cheap resources or costly fights (small $V/C$) yield a mostly peaceful population; valuable resources with mild costs (large $V/C$) yield mostly aggression.
For $V = 2$ and $C = 3$, $\hat p = 2/3$: two-thirds Hawks is the uninvadable mix.

## In code

We integrate the replicator dynamics for the Hawk–Dove game with $V = 2$, $C = 3$ and confirm convergence to $\hat p = V/C = 2/3$.

### R

```r
library(deSolve)

A <- matrix(c(-0.5, 2,      # Hawk-Dove payoffs, V = 2, C = 3
               0.0, 1),
            nrow = 2, byrow = TRUE)

repl <- function(t, x, p) {
  f    <- as.vector(A %*% x)   # payoff to each strategy
  fbar <- sum(x * f)           # mean payoff
  list(x * (f - fbar))
}

out <- ode(c(H = 0.9, D = 0.1), seq(0, 50, 0.1), repl, parms = NULL)
tail(out, 1)                   # H -> 0.6667 = V/C, D -> 0.3333
```

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp

A = np.array([[-0.5, 2.0],     # Hawk-Dove payoffs, V = 2, C = 3
              [ 0.0, 1.0]])

def repl(t, x):
    f = A @ x
    return x * (f - x @ f)     # x_i (f_i - mean payoff)

sol = solve_ivp(repl, (0, 50), [0.9, 0.1], t_eval=[50])
print(sol.y[:, -1])            # -> [0.667, 0.333], Hawk freq = V/C = 2/3
```

<!-- python-output:auto -->
```text
[0.66673614 0.33326386]
```
<!-- /python-output:auto -->

### Julia

```julia
A = [-0.5 2.0;                 # Hawk-Dove payoffs, V = 2, C = 3
      0.0 1.0]

x = [0.9, 0.1]; dt = 0.01
for _ in 1:5000
    f = A * x
    global x += dt .* (x .* (f .- x'f))   # x'f is the mean payoff
end
println(x)                     # -> [0.667, 0.333], Hawk freq = V/C = 2/3
```

## Why it matters

Evolutionary game theory reframes natural selection for the common situation where fitness is frequency-dependent: mating systems, foraging and contest behaviour, sex ratios, and microbial public goods.
It explains why populations often settle at mixtures rather than a single optimal type, and it supplies the machinery — payoff matrices, the ESS criterion, and the replicator equation — used to analyse [the evolution of cooperation](evolution-of-cooperation.md) and [the evolution of virulence](evolution-of-virulence.md).

## Related

- [The Evolution of Cooperation](evolution-of-cooperation.md)
- [Adaptive Dynamics and the Evolution of Virulence](evolution-of-virulence.md)
- [Equilibria and Stability](equilibria-and-stability.md)
- [Lotka–Volterra Predator–Prey Dynamics](predator-prey.md)
- [Optimization](optimization.md)
- [Quantitative Methods](../math.md)
