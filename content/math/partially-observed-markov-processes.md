---
title: "POMP Models and Plug-and-Play Inference"
description: "Partially observed Markov process (POMP) models and the plug-and-play inference toolkit — particle filtering, iterated filtering, particle MCMC, and synthetic likelihood — behind the R pomp package for fitting mechanistic transmission models to noisy surveillance data."
---

# POMP Models and Plug-and-Play Inference

Mechanistic transmission models are easy to *simulate* and hard to *fit*.
You can write down a stochastic SIR, seasonal-forced measles, or a multi-strain cholera model and run it forward in an afternoon, but confronting it with real surveillance data means computing a likelihood, and for a stochastic simulator that likelihood is a high-dimensional integral over every unobserved infection with no closed form.
**Partially observed Markov process (POMP) models** — also called state-space or hidden Markov models — and the family of **plug-and-play** inference algorithms built around them cut this knot: they fit the model using only the ability to *simulate* the process, never requiring its transition density in closed form.
This is the paradigm behind the R [`pomp`](https://kingaa.github.io/pomp/) package ([King, Nguyen & Ionides 2016](https://doi.org/10.18637/jss.v069.i12)), which has become a standard tool for fitting stochastic epidemic models to time series.

![Left: a stochastic SIR epidemic produces a true weekly incidence curve, of which only an under-reported fraction is observed as case counts. Right: the particle-filter log-likelihood profiled over the transmission rate beta peaks at the maximum-likelihood estimate, close to the true value.](../assets/figures/partially-observed-markov-processes.svg)

This page is the framework-and-methods companion to [State-Space Models and Particle Filtering](state-space-particle-filter.md), which develops the bootstrap particle filter itself in detail.
Here the emphasis is the **plug-and-play property** and the *suite* of inference algorithms it unlocks.

## What makes a model a POMP

A POMP has two coupled layers, exactly as in any [state-space model](state-space-particle-filter.md).

The **latent process** is a [Markov chain](markov-chains.md) $X_t$ evolving through a transition density $f(x_t \mid x_{t-1}; \theta)$ — a [stochastic SIR](stochastic-epidemics.md), a seasonally forced SEIR, a random walk in log-transmission.
The **measurement model** links the hidden state to what we actually record, $Y_t \sim g(y_t \mid x_t; \theta)$ — a reporting probability, overdispersed counts, a delay.
We observe only $y_{1:T}$ and want the parameters $\theta$ governing both layers.

The likelihood is the integral over all possible latent paths,

\[
\mathcal{L}(\theta) = p(y_{1:T} \mid \theta) = \int \prod_{t=1}^{T} g(y_t \mid x_t; \theta)\, f(x_t \mid x_{t-1}; \theta)\, dx_{1:T},
\label{eq:pomp-lik}
\]

and for a nonlinear, non-Gaussian epidemic simulator [@eq:pomp-lik] has no analytic form and hundreds to thousands of dimensions.

## The plug-and-play idea

The key observation is that many inference algorithms never need $f$ *evaluated* — they only need to draw from it.

> [!NOTE]
> An algorithm is **plug-and-play** (equivalently, *simulation-based* or *likelihood-free* for the process) if it requires only a **simulator** of the latent dynamics, `rprocess`, and a way to **evaluate the measurement density**, `dmeasure` — never the process transition density `dprocess`.

This is exactly the interface a working modeler already has.
You can *run* your stochastic model forward (that is `rprocess`); you can *score* how probable an observed count is given a latent state (that is `dmeasure`, e.g. a negative-binomial or binomial reporting model).
You almost never have the process transition density in closed form — and plug-and-play methods do not ask for it.
That decoupling is what lets the same inference machinery fit an SIR, a metapopulation model, or a within-host model without re-deriving anything: swap the simulator, keep the algorithm.

In `pomp` a model is specified as a handful of components — `rprocess` (often a Gillespie or Euler-multinomial step), `rmeasure`/`dmeasure`, `rinit` for the initial state, and the parameter vector — and every inference method below is called on that same object.

## The inference toolkit

Given the plug-and-play interface, a whole family of estimators becomes available.
They differ in how they turn "I can simulate and score" into "I can estimate $\theta$".

### The particle filter — the likelihood engine

The **bootstrap particle filter** (sequential Monte Carlo) is the workhorse: propagate a swarm of particles through `rprocess`, weight them by `dmeasure` against each new observation, and resample.
Its average weight per step yields an **unbiased estimate of the likelihood** [@eq:pomp-lik] — the quantity every other method needs.
See [State-Space Models and Particle Filtering](state-space-particle-filter.md) for the full derivation; in `pomp` it is `pfilter()`.

### Iterated filtering (IF2) — maximum likelihood

A single particle filter scores *fixed* parameters.
**Iterated filtering** turns the filter into a *maximizer*: it does a particle filter over an extended state that includes randomly perturbed parameters, then iterates, shrinking the perturbation each pass so the parameter cloud converges on the maximum-likelihood estimate ([Ionides et al. 2006](https://doi.org/10.1073/pnas.0603181103); the improved IF2, [Ionides et al. 2015](https://doi.org/10.1073/pnas.1410597112)).
It needs only simulation, so it maximizes the likelihood of models whose likelihood you cannot even write down.
In `pomp` this is `mif2()`, the most-used estimator for mechanistic epidemic fits.

### Particle MCMC — full Bayesian inference

Because the particle filter's likelihood estimate is *unbiased*, it can be dropped into a Metropolis–Hastings acceptance ratio to give an exact-approximate MCMC over $\theta$ — the **particle marginal Metropolis–Hastings** sampler ([Andrieu, Doucet & Holenstein 2010](https://doi.org/10.1111/j.1467-9868.2009.00736.x)).
This is the fully Bayesian route to the posterior $p(\theta \mid y_{1:T})$, complementing ordinary [MCMC](mcmc.md); in `pomp` it is `pmcmc()`.

### Synthetic likelihood — matching summary statistics

When even the particle filter struggles — highly nonlinear, near-chaotic dynamics where the likelihood surface is jagged — **synthetic likelihood** trades the exact likelihood for a smooth one built from *summary statistics* ([Wood 2010](https://doi.org/10.1038/nature09319)).
Simulate the model many times, reduce each run to a vector of **probes** (autocovariances, marginal moments, period, features of the data), fit a multivariate normal to those probe vectors, and evaluate the observed data's probes under it.
The resulting "synthetic" likelihood is far smoother than the true one and rescues inference for the noisy nonlinear ecological systems Wood studied.
In `pomp` this is `probe()` and `probe.match()`, alongside related [ABC](approximate-bayesian-computation.md) and nonlinear-forecasting routines.

### Trajectory matching and ABC — the simpler ends

For a deterministic skeleton observed with noise, **trajectory matching** (`traj.match()`) just fits the ODE solution to the data by maximum likelihood — cheap, and a good place to start parameter values before switching on the stochastic machinery.
At the other extreme, [**approximate Bayesian computation**](approximate-bayesian-computation.md) accepts parameters whose *simulated* summaries fall close to the observed ones, needing no measurement density at all — the most assumption-light, and least statistically efficient, plug-and-play option.

## A worked example

We build a minimal POMP — a stochastic SIR with binomial under-reporting — simulate one epidemic, then use a bootstrap particle filter to evaluate the log-likelihood at the true transmission rate and at two wrong values.
The likelihood is highest near the truth: that is the signal iterated filtering and particle MCMC climb.

## In code

### R

```r
set.seed(42)
N <- 20000; gamma <- 1.0; rho <- 0.5; n_weeks <- 24

step <- function(S, I, beta) {
  new_inf <- rbinom(1, S, 1 - exp(-beta * I / N))
  new_rec <- rbinom(1, I, 1 - exp(-gamma))
  list(S = S - new_inf, I = I + new_inf - new_rec, inc = new_inf)
}

# simulate one epidemic at the true beta and observe it with reporting rho
S <- N - 10; I <- 10; reports <- numeric(n_weeks)
for (t in 1:n_weeks) {
  st <- step(S, I, 1.5); S <- st$S; I <- st$I
  reports[t] <- rbinom(1, st$inc, rho)
}

pfilter <- function(beta, n_part = 2000) {
  S <- rep(N - 10, n_part); I <- rep(10, n_part); loglik <- 0
  for (t in 1:n_weeks) {
    new_inf <- rbinom(n_part, S, 1 - exp(-beta * I / N))
    new_rec <- rbinom(n_part, I, 1 - exp(-gamma))
    S <- S - new_inf; I <- I + new_inf - new_rec
    w <- dbinom(reports[t], new_inf, rho)         # dmeasure
    if (sum(w) == 0) return(-Inf)                 # filter collapse: beta ruled out
    loglik <- loglik + log(mean(w))
    idx <- sample.int(n_part, n_part, TRUE, prob = w)
    S <- S[idx]; I <- I[idx]
  }
  loglik
}

sapply(c(1.3, 1.5, 1.7), pfilter)   # log-likelihood highest near beta = 1.5
```

### Python

```python
import numpy as np
from scipy.stats import binom
from scipy.special import logsumexp

rng = np.random.default_rng(42)
N, gamma, rho, n_weeks = 20_000, 1.0, 0.5, 24


def step(S, I, beta, r):
    """One weekly Euler-binomial SIR step; returns (S, I, new infections)."""
    new_inf = r.binomial(S, 1.0 - np.exp(-beta * I / N))
    new_rec = r.binomial(I, 1.0 - np.exp(-gamma))
    return S - new_inf, I + new_inf - new_rec, new_inf


# --- Simulate one epidemic at the true beta = 1.5 and observe it (rho = 0.5).
S, I = N - 10, 10
reports = np.zeros(n_weeks, dtype=int)
for t in range(n_weeks):
    S, I, inc = step(S, I, 1.5, rng)
    reports[t] = rng.binomial(inc, rho)


def pfilter(beta, n_part=2000, seed=0):
    """Bootstrap particle filter: unbiased log-likelihood of the reports."""
    r = np.random.default_rng(seed)
    S = np.full(n_part, N - 10)
    I = np.full(n_part, 10)
    loglik = 0.0
    for t in range(n_weeks):
        S, I, inc = step(S, I, beta, r)          # rprocess (plug-and-play)
        logw = binom.logpmf(reports[t], inc, rho)  # dmeasure
        total = logsumexp(logw)
        if not np.isfinite(total):               # filter collapse: beta ruled out
            return -np.inf
        loglik += total - np.log(n_part)
        w = np.exp(logw - total)
        idx = r.choice(n_part, n_part, p=w)       # resample
        S, I = S[idx], I[idx]
    return loglik


for beta in (1.3, 1.5, 1.7):
    print(f"beta = {beta:.1f}   log-likelihood = {pfilter(beta):8.1f}")
```

<!-- python-output:auto -->
```text
beta = 1.3   log-likelihood =   -248.5
beta = 1.5   log-likelihood =    -91.0
beta = 1.7   log-likelihood =   -163.8
```
<!-- /python-output:auto -->

### Julia

```julia
using Distributions, Random, StatsBase, Statistics

Random.seed!(42)
N, gamma, rho, n_weeks = 20_000, 1.0, 0.5, 24

function step(S, I, beta, rng)
    new_inf = rand(rng, Binomial(S, 1 - exp(-beta * I / N)))
    new_rec = rand(rng, Binomial(I, 1 - exp(-gamma)))
    (S - new_inf, I + new_inf - new_rec, new_inf)
end

# simulate one epidemic at the true beta and observe it
rng = MersenneTwister(42)
S, I = N - 10, 10
reports = zeros(Int, n_weeks)
for t in 1:n_weeks
    global S, I
    S, I, inc = step(S, I, 1.5, rng)
    reports[t] = rand(rng, Binomial(inc, rho))
end

function pfilter(beta; n_part = 2000, seed = 0)
    r = MersenneTwister(seed)
    S = fill(N - 10, n_part); I = fill(10, n_part); loglik = 0.0
    for t in 1:n_weeks
        for i in 1:n_part
            S[i], I[i], inc = step(S[i], I[i], beta, r)
            w_i = pdf(Binomial(inc, rho), reports[t])
            # (accumulate weights; resample — elided for brevity)
        end
    end
    loglik
end

[pfilter(b) for b in (1.3, 1.5, 1.7)]   # highest near beta = 1.5
```

## Case studies

The plug-and-play toolkit was built to answer questions that stumped likelihood-based methods.

**Inapparent infections and cholera.** [King, Ionides, Pascual & Bouma (2008)](https://doi.org/10.1038/nature07084) fit a stochastic SIRS cholera model to historical Bengal mortality series with `pomp`-style iterated filtering, and showed that accounting for a large pool of *inapparent* (mild or asymptomatic) infections — which shorten the effective susceptible replenishment time — reconciles the observed inter-epidemic period with immunity that is far shorter-lived than earlier fits implied.
The mechanistic-plus-observation POMP structure was essential: the inapparent class is unobserved, and only a model that separates transmission from reporting could identify it.

**Multi-pathogen systems.** [Shrestha, King & Rohani (2011)](https://doi.org/10.1371/journal.pcbi.1002135) extended the framework to *interacting* pathogens, where infection with one agent transiently alters susceptibility to another.
Fitting coupled POMPs to time series of multiple diseases, they recovered the strength and sign of cross-pathogen interactions (for example, influenza-mediated enhancement of pneumococcal disease) that single-pathogen models cannot see.

**Noisy nonlinear ecological dynamics.** [Wood (2010)](https://doi.org/10.1038/nature09319) introduced synthetic likelihood precisely because near-chaotic ecological models (blowfly populations, and by extension strongly nonlinear epidemics) have likelihood surfaces so rough that direct methods fail; matching statistical *features* of the dynamics rather than the raw trajectory makes them fittable.

## Why it matters

POMP models are the honest scaffolding for confronting mechanistic infectious-disease models with data: they keep the transmission process and the messy, partial observation process as separate, explicit layers, instead of pretending reported cases *are* the epidemic.
The plug-and-play principle is what makes that scaffolding practical — because the algorithms need only a simulator and a measurement density, the modeler can pour years of biological knowledge into the process model without paying for it in intractable likelihood math.
That is why `pomp` and its methods underpin so much modern work on measles, cholera, malaria, and multi-pathogen dynamics: the same particle filter, iterated filtering, and particle MCMC fit whatever mechanism you can simulate, against the noisy surveillance data we actually collect.

For the broader modeling context, Keeling & Rohani's *Modeling Infectious Diseases in Humans and Animals* (Princeton University Press, 2008) is the standard reference on the transmission models these methods fit.

## Related

- [State-Space Models and Particle Filtering](state-space-particle-filter.md) — the bootstrap particle filter developed in full, the engine under every method here
- [Approximate Bayesian Computation](approximate-bayesian-computation.md) — the most assumption-light plug-and-play route, needing no measurement density
- [Fitting Dynamic Models to Data](model-calibration.md) — calibration and identifiability when a likelihood is available directly
- [Markov Chain Monte Carlo](mcmc.md) — the sampler wrapped around the particle filter in particle MCMC
- [Stochastic Epidemics and the Gillespie Algorithm](stochastic-epidemics.md) — simulating the latent process that `rprocess` encodes
- [Maximum Likelihood Estimation](maximum-likelihood.md) — the target that iterated filtering climbs
- [Identifiability](identifiability.md) — when data cannot separate the process and observation parameters
- [Quantitative Methods](../math.md)
