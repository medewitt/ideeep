---
title: "Random Walks and Brownian Motion"
description: "The simple random walk and its diffusive scaling limit, Brownian motion — displacement grows like the square root of time, with applications to dispersal, genetic drift, and trait evolution."
---

# Random Walks and Brownian Motion

A drunkard staggering left or right, a pollen grain jittering in water, and a neutral allele drifting in a finite population all trace out the same kind of path: a sequence of small, independent, unpredictable steps.
The **random walk** is the simplest stochastic process, and when you zoom out — many tiny steps over a long time — it converges to **Brownian motion**, the continuous process at the heart of diffusion, genetic drift, and continuous-time trait evolution.
Its signature is a rule you will meet again and again: typical displacement grows not like time but like the *square root* of time.

![Six sample paths of standard Brownian motion spreading away from the origin, bounded on average by the $\pm\sqrt{t}$ envelope.](../assets/figures/random-walk-brownian-motion.svg)

## The simple random walk

Start at the origin and take independent steps $X_1, X_2, \dots$, each $+1$ or $-1$ with probability $\tfrac{1}{2}$.
Your position after $n$ steps is the partial sum \[ S_n = \sum_{i=1}^{n} X_i. \] Each step is a [random variable](random-variables.md) with $\mathbb{E}[X_i] = 0$ and $\operatorname{Var}(X_i) = 1$.
Because the steps are independent and have mean zero, the walk has no preferred direction: \[ \mathbb{E}[S_n] = 0, \qquad \operatorname{Var}(S_n) = \sum_{i=1}^{n} \operatorname{Var}(X_i) = n. \] The expectation being zero is the easy part; the variance adding up is the important part.
Variances of independent quantities sum, so the spread of $S_n$ is $\operatorname{SD}(S_n) = \sqrt{n}$.

This is the fundamental fact.
After $n$ steps the walker is *not* typically near step $n$ away — it is typically about $\sqrt{n}$ away.
To wander twice as far you must wait four times as long.
This slow, square-root spreading is what "diffusive" means, and it separates random motion from directed motion, where displacement would grow linearly in time.

## From random walk to Brownian motion

The $\sqrt{n}$ scaling tells us exactly how to zoom out.
Rescale the walk in time by a factor $N$ and in space by $\sqrt{N}$, and look at \[ W_N(t) = \frac{S_{\lfloor N t \rfloor}}{\sqrt{N}}. \] As $N \to \infty$ this rescaled walk converges to a limiting process $W(t)$ called **Brownian motion** (or the **Wiener process**).
The [central limit theorem](central-limit-theorem.md) supplies the reason: $S_{\lfloor Nt\rfloor}$ is a sum of about $Nt$ independent steps, so once divided by $\sqrt{N}$ it is approximately [normal](normal-distribution.md) with mean $0$ and variance $t$.
Any step distribution with finite variance gives the *same* limit — the microscopic details of a single step wash out, leaving a universal Gaussian process.
This is why Brownian motion appears whenever many small independent perturbations accumulate.

### Defining properties

Standard Brownian motion $W(t)$ is characterized by four properties.

- **Starts at zero:** $W(0) = 0$.
- **Independent increments:** for non-overlapping time intervals, the displacements are independent, so the future is conditionally independent of the past given the present — a continuous cousin of the [Markov](markov-chains.md) property.
- **Gaussian increments:** for $s < t$, \[ W(t) - W(s) \sim \mathcal{N}\!\big(0,\ t - s\big), \] so the variance of an increment equals the elapsed time and $\operatorname{Var}(W(t)) = t$.
- **Continuous paths:** $t \mapsto W(t)$ is continuous, yet **nowhere differentiable** — the path has no well-defined velocity at any instant, because over a tiny interval $\Delta t$ the step size is of order $\sqrt{\Delta t}$, so the difference quotient $\Delta W / \Delta t \sim 1/\sqrt{\Delta t}$ blows up.

The path is therefore continuous but infinitely wiggly, a fractal that looks statistically the same at every magnification.

### Drift and scaling

Real processes rarely have unit variance and zero trend, so we add two parameters.
A **drift** $\mu$ imposes a directional tendency and a **volatility** (or diffusion) scale $\sigma$ stretches the fluctuations: \[ W_D(t) = \mu\, t + \sigma\, W(t). \] Then $\mathbb{E}[W_D(t)] = \mu t$ grows linearly while $\operatorname{Var}(W_D(t)) = \sigma^2 t$ still grows linearly in time, so $W_D(t) \sim \mathcal{N}(\mu t,\ \sigma^2 t)$.
Drift dominates at long times (it scales like $t$) while diffusion dominates at short times (it scales like $\sqrt{t}$), and the crossover between "the trend" and "the noise" happens near $t \approx \sigma^2 / \mu^2$.

### Connection to the diffusion equation

Brownian motion is the probabilistic face of the [heat (diffusion) equation](spatial-diffusion.md).
Let $p(x, t)$ be the density of $W_D(t)$ started at the origin; it is the Gaussian \[ p(x, t) = \frac{1}{\sqrt{2\pi \sigma^2 t}} \exp\!\left(-\frac{(x - \mu t)^2}{2 \sigma^2 t}\right), \] and with no drift ($\mu = 0$) this density solves \[ \frac{\partial p}{\partial t} = D\, \frac{\partial^2 p}{\partial x^2}, \qquad D = \tfrac{1}{2}\sigma^2. \] The variance $\operatorname{Var}(W(t)) = \sigma^2 t = 2Dt$ growing linearly in time is the probabilistic statement of Fick's law: a spreading Gaussian is both an ensemble of Brownian particles and a solution of the diffusion equation.
The same $D$ that scales a single particle's wandering sets the rate at which a whole population's density flattens out.

## Mean-reverting and multiplicative relatives

Two variants appear constantly in biology and finance.
**Geometric Brownian motion** models a quantity that varies multiplicatively rather than additively — its logarithm is Brownian motion with drift, $\log Y(t) = \log Y(0) + \mu t + \sigma W(t)$, so $Y(t)$ stays positive and its relative changes, not its absolute changes, are Gaussian; it is the standard model for exponentially growing populations or asset prices under noise.
The **Ornstein–Uhlenbeck process** adds a restoring pull toward a mean $\theta$, following $dY = -\alpha\,(Y - \theta)\,dt + \sigma\, dW$, so instead of wandering off forever the process is **mean-reverting**: excursions decay at rate $\alpha$ and the variance saturates at $\sigma^2 / (2\alpha)$ rather than growing without bound.
Ornstein–Uhlenbeck is the natural model for a trait held near an adaptive optimum by [selection](gaussian-processes.md), and it is the mean-reverting counterpart to Brownian motion's unbounded drift.

## A worked example

A tagged fish disperses along a river as Brownian motion with no drift and diffusion scale $\sigma = 3\ \text{km}\,\text{day}^{-1/2}$, so its position at time $t$ days is $W_D(t) \sim \mathcal{N}(0,\ \sigma^2 t)$.
After $t = 16$ days the position has standard deviation \[ \operatorname{SD}(W_D(16)) = \sigma \sqrt{t} = 3 \sqrt{16} = 12\ \text{km}. \] A central 95% interval for its displacement is therefore $\pm 1.96 \times 12 \approx \pm 23.5\ \text{km}$, so it is about 95% likely to be found within roughly 24 km of the release point despite there being no average movement at all.
Note the square-root law in action: to double the typical dispersal distance to 24 km, the fish must swim for $t = 64$ days, four times as long.
The chance it has drifted more than 30 km downstream is $P(W_D(16) > 30) = P\!\big(Z > 30/12\big) = P(Z > 2.5) \approx 0.006$.

## In code

### R

```r
set.seed(7)
reps <- 2e5
for (n in c(10, 100, 1000)) {
  steps <- matrix(sample(c(-1, 1), reps * n, replace = TRUE), nrow = reps)
  Sn <- rowSums(steps)
  cat(sprintf("n=%4d  E[S_n]=%+.3f  Var[S_n]=%7.1f  (theory %d)\n",
              n, mean(Sn), var(Sn), n))
}
```

### Python

```python
import numpy as np
rng = np.random.default_rng(7)

reps = 200_000
for n in (10, 100, 1000):
    steps = rng.choice([-1, 1], size=(reps, n))      # simple +/-1 random walk
    Sn = steps.sum(axis=1)
    print(f"n={n:>4}  E[S_n]={Sn.mean():+.3f}  Var[S_n]={Sn.var():7.1f}  (theory {n})")

# Diffusive scaling: S_n / sqrt(n) is approximately standard normal at t = 1.
W1 = rng.normal(0.0, 1.0, size=reps)                 # standard BM at time t = 1
print(f"P(-1.96 < W(1) < 1.96) = {np.mean(np.abs(W1) < 1.96):.3f}  (theory 0.950)")
```

<!-- python-output:auto -->
```text
n=  10  E[S_n]=+0.005  Var[S_n]=   10.0  (theory 10)
n= 100  E[S_n]=-0.012  Var[S_n]=  100.1  (theory 100)
n=1000  E[S_n]=-0.036  Var[S_n]= 1000.3  (theory 1000)
P(-1.96 < W(1) < 1.96) = 0.950  (theory 0.950)
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics
Random.seed!(7)

reps = 200_000
for n in (10, 100, 1000)
    Sn = [sum(rand((-1, 1), n)) for _ in 1:reps]
    println("n=$n  E[S_n]=", round(mean(Sn), digits=3),
            "  Var[S_n]=", round(var(Sn), digits=1), "  (theory $n)")
end
```

## Why it matters

Brownian motion is the default null model for aimless movement, and departures from it are how we detect *directed* processes.
In movement ecology, animal dispersal is often modeled as diffusion, so a home range spreads like $\sqrt{t}$ and the diffusion coefficient $D$ converts tracking data into a colonization or [spatial-spread](spatial-diffusion.md) rate.
In population genetics, [genetic drift](genetic-drift.md) turns allele frequencies into a random walk whose variance accumulates over generations, and the diffusion approximation — treating frequency as a bounded Brownian-type process — underlies the classical theory of fixation and heterozygosity loss.
In macroevolution, quantitative traits are modeled as Brownian motion along the branches of a phylogeny, so that the expected squared difference between two species grows in proportion to the time since their common ancestor, and an Ornstein–Uhlenbeck version captures stabilizing selection toward an optimum.
The same mathematics that describes a pollen grain jittering under molecular bombardment thus describes a lineage's trait wandering through deep time.

## Related

- [The Central Limit Theorem](central-limit-theorem.md)
- [Normal Distribution](normal-distribution.md)
- [Random Variables](random-variables.md)
- [Markov Chains](markov-chains.md)
- [Reaction–Diffusion and Spatial Spread](spatial-diffusion.md)
- [Gaussian Processes](gaussian-processes.md)
- [Genetic Drift](genetic-drift.md)
- [Quantitative Methods](../math.md)
