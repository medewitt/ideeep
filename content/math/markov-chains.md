---
title: "Markov Chains"
---

# Markov Chains

A Markov chain is a stochastic process that hops between states, where the probability of the next state depends only on the current state and not on the path that led there.
This "memoryless" assumption is simple enough to analyze with linear algebra yet rich enough to model gene fixation, epidemic compartments, and the sampling engines behind modern statistics.

![Left: the transition diagram for the two-state weather chain, with its four one-step probabilities and stationary distribution $\pi=(4/7,\,3/7)$. Right: two long simulations started from opposite states both have their running frequency of Sunny converge to $\pi_1=4/7\approx0.571$, so the chain forgets where it began.](../assets/figures/markov-chains.svg "fig:markov")

## States, transitions, and the Markov property

Let the process take values in a finite set of states $\{1, 2, \dots, k\}$ and let $X_n$ be the state at step $n$.
The defining assumption is the Markov property, \[ \Pr(X_{n+1} = j \mid X_n = i, X_{n-1}, \dots, X_0) = \Pr(X_{n+1} = j \mid X_n = i), \] so the past is irrelevant once the present is known.
A time-homogeneous chain packs these one-step [probabilities](probability-basics.md) into a transition matrix $P$ with entries \[ P_{ij} = \Pr(X_{n+1} = j \mid X_n = i). \] Each row is a probability distribution over destinations, so every row sums to $1$ and all entries are non-negative — $P$ is a stochastic matrix.

## Evolving the distribution

Represent the state of belief as a row vector $\pi_0$ giving the probability of starting in each state.
One step forward is a vector–[matrix product](matrix-operations.md): the distribution after one step is $\pi_0 P$, and by induction the distribution after $n$ steps is \[ \pi_n = \pi_0 P^n. \] The entry $(P^n)_{ij}$ is the probability of being in state $j$ exactly $n$ steps after starting in state $i$.

## Stationary distribution

A stationary (or invariant) distribution is a probability row vector $\pi$ that is unchanged by one more step: \[ \pi = \pi P, \qquad \sum_i \pi_i = 1. \] The equation $\pi = \pi P$ says $\pi$ is a left [eigenvector](eigenvalues-and-eigenvectors.md) of $P$ with eigenvalue $1$; every stochastic matrix has such an eigenvalue, so a stationary distribution always exists.
If the chain is irreducible (every state reachable from every other) and aperiodic, the stationary distribution is unique and the chain converges to it from any starting point: $\pi_n \to \pi$ as $n \to \infty$, regardless of $\pi_0$.

## Absorbing chains and hitting probabilities

Not every chain mixes toward a stationary distribution.
A state $i$ is absorbing if $P_{ii} = 1$: once entered, the chain never leaves.
The [Wright–Fisher model of genetic drift](genetic-drift.md) is exactly such a chain — the count of a neutral allele in a finite population performs a random walk with absorbing boundaries at $0$ (loss) and $2N$ (fixation), so every population eventually fixes or loses the allele.
For absorbing chains the interesting quantities are absorption probabilities (the chance of ending in each absorbing state) and expected hitting times, both obtained by solving linear systems built from the transient part of $P$.

## Worked example

Consider a two-state weather chain with states Sunny ($1$) and Rainy ($2$) and transition matrix \[ P = \begin{bmatrix} 0.7 & 0.3 \\ 0.4 & 0.6 \end{bmatrix}. \] To find the stationary distribution $\pi = (\pi_1, \pi_2)$ we solve $\pi = \pi P$ with $\pi_1 + \pi_2 = 1$.
Writing out the first component, \[ \pi_1 = 0.7\,\pi_1 + 0.4\,\pi_2 \;\Longrightarrow\; 0.3\,\pi_1 = 0.4\,\pi_2 \;\Longrightarrow\; \pi_2 = \tfrac{3}{4}\pi_1. \] Imposing normalization, $\pi_1 + \tfrac34\pi_1 = 1$, so $\pi_1 = \tfrac{4}{7}$ and $\pi_2 = \tfrac{3}{7}$: \[ \pi = \left(\tfrac{4}{7},\ \tfrac{3}{7}\right) \approx (0.5714,\ 0.4286). \] In the long run the chain is Sunny about $57\%$ of days regardless of today's weather ([@fig:markov]).

## Simulation

Simulate a long trajectory and confirm the empirical frequency of each state converges to $\pi$.

### R

```r
set.seed(42)
P <- matrix(c(0.7, 0.3,
              0.4, 0.6), nrow = 2, byrow = TRUE)

n <- 100000
x <- integer(n); x[1] <- 1
for (t in 2:n) x[t] <- sample(1:2, 1, prob = P[x[t - 1], ])

table(x) / n            # ~ 0.571, 0.429

# stationary vector as left eigenvector with eigenvalue 1
ev <- eigen(t(P))$vectors[, 1]
Re(ev / sum(ev))        # ~ 0.5714, 0.4286
```

### Python

```python
import numpy as np
rng = np.random.default_rng(42)

P = np.array([[0.7, 0.3],
              [0.4, 0.6]])

n = 100_000
x = np.empty(n, dtype=int); x[0] = 0
for t in range(1, n):
    x[t] = rng.choice(2, p=P[x[t - 1]])

print(np.bincount(x) / n)          # ~ [0.571, 0.429]

# stationary vector: left eigenvector for eigenvalue 1
vals, vecs = np.linalg.eig(P.T)
pi = np.real(vecs[:, np.argmin(abs(vals - 1))])
print(pi / pi.sum())               # ~ [0.5714, 0.4286]
```

<!-- python-output:auto -->
```text
[0.57124 0.42876]
[0.57142857 0.42857143]
```
<!-- /python-output:auto -->

### Julia

```julia
using LinearAlgebra, Random, Statistics
Random.seed!(42)

P = [0.7 0.3;
     0.4 0.6]

n = 100_000
x = Vector{Int}(undef, n); x[1] = 1
for t in 2:n
    r = rand()
    x[t] = r < P[x[t-1], 1] ? 1 : 2
end

[count(==(s), x) / n for s in 1:2]     # ~ [0.571, 0.429]

# stationary vector: left eigenvector for eigenvalue 1
F = eigen(collect(P'))
pi = real.(F.vectors[:, argmin(abs.(F.values .- 1))])
pi ./ sum(pi)                          # ~ [0.5714, 0.4286]
```

## Why it matters

Markov chains are one of the most reusable modelling tools in quantitative biology and statistics.
The same $\pi = \pi P$ machinery gives the long-run behaviour of a weather model, the fixation probabilities of a drifting allele, and the equilibrium of a compartmental epidemic; run in reverse, constructing a chain whose stationary distribution is a target posterior is exactly the idea behind [Markov chain Monte Carlo](mcmc.md).

## Related

- [Eigenvalues and Eigenvectors](eigenvalues-and-eigenvectors.md)
- [Matrix Operations](matrix-operations.md)
- [Markov Chain Monte Carlo](mcmc.md)
- [Genetic Drift and the Wright–Fisher Model](genetic-drift.md)
- [Probability Basics](probability-basics.md)
- [Quantitative Methods](../math.md)
