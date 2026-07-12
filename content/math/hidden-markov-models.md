---
title: "Hidden Markov Models"
description: "Hidden Markov models — a discrete latent state evolving as a Markov chain, observed only through noisy emissions — with the forward, Viterbi, and Baum-Welch algorithms, worked on a latent low/high-risk regime driving STI reinfection."
---

# Hidden Markov Models

Some of the most useful hidden states are not numbers but **regimes**: a person is in a high-risk or a low-risk period, an epidemic is growing or declining, a stretch of genome is coding or non-coding, an animal is foraging or resting.
A **hidden Markov model (HMM)** is the tool for exactly this — a discrete latent state that jumps between a few categories as a [Markov chain](markov-chains.md), which we never observe directly but only through a noisy, state-dependent **emission**.
It is the discrete-state sibling of the [Kalman filter](kalman-filter.md) and the [particle filter](state-space-particle-filter.md): the same predict-then-correct logic, but the belief is a small vector of category probabilities instead of a Gaussian or a particle cloud, which makes everything exact and cheap.

Consider a sexually transmitted infection with reinfection.
An individual's underlying **risk regime** drifts over time — a high-risk period (a new partnership, a partner with other partners) raises the monthly chance of acquiring or reacquiring infection; a low-risk period lowers it.
We do not see the regime; we see a longitudinal string of **test results**.
An HMM reconstructs the hidden risk trajectory from those tests, and estimates how sticky each regime is and how differently they generate infections.

![Top: one person's monthly test results, with positive tests clustering inside the true (shaded) high-risk periods. Bottom: the HMM posterior probability of being high-risk and the Viterbi most-likely regime path, both recovering the shaded episodes from the tests alone.](../assets/figures/hidden-markov-model.svg)

## The model

An HMM has three pieces.
A hidden state $z_t \in \{1, \dots, K\}$ follows a Markov chain with a $K\times K$ **transition matrix** $A$, where $A_{ij} = \Pr(z_t = j \mid z_{t-1} = i)$, started from an initial distribution $\pi$.
Each state emits an observation through its own **emission distribution** $b_j(y_t) = \Pr(y_t \mid z_t = j)$ — here a Bernoulli, "test positive with probability $p_j$", with $p_{\text{high}} \gg p_{\text{low}}$.
The Markov chain is on the *hidden* state, not the data: the observations are conditionally independent given the states, and all the memory lives in $z_t$.

The likelihood of a whole series sums over every possible hidden path,

\[
\Pr(y_{1:T}) = \sum_{z_{1:T}} \pi_{z_1} b_{z_1}(y_1) \prod_{t=2}^{T} A_{z_{t-1} z_t}\, b_{z_t}(y_t),
\label{eq:hmm-lik}
\]

which has $K^T$ terms — astronomically many — yet the special Markov structure collapses it to a linear-time recursion.

## Three questions, three algorithms

Every HMM task is one of three classic problems ([Rabiner 1989](https://doi.org/10.1109/5.18626)).

**Likelihood — the forward algorithm.** Define $\alpha_t(j) = \Pr(y_{1:t}, z_t = j)$, the joint probability of the data so far and being in state $j$ now.
It obeys a one-step recursion that carries the sum in [@eq:hmm-lik] forward in linear time,

\[
\alpha_t(j) = b_j(y_t) \sum_{i=1}^{K} \alpha_{t-1}(i)\, A_{ij},
\label{eq:hmm-forward}
\]

and $\Pr(y_{1:T}) = \sum_j \alpha_T(j)$.
This is the exact analogue of the Kalman filter's predict ($\sum_i \alpha_{t-1}(i) A_{ij}$) and update ($\times\, b_j(y_t)$) steps.

**Decoding — Viterbi and forward–backward.** To recover the hidden regimes there are two answers.
The **Viterbi algorithm** replaces the sum in [@eq:hmm-forward] with a *max*, tracing the single **most likely path** $\hat{z}_{1:T}$ through the states,

\[
\delta_t(j) = b_j(y_t)\, \max_i\, \delta_{t-1}(i)\, A_{ij},
\label{eq:hmm-viterbi}
\]

with back-pointers to reconstruct the path.
The **forward–backward algorithm** instead adds a backward pass $\beta_t$ and returns the smoothed **posterior** $\gamma_t(j) = \Pr(z_t = j \mid y_{1:T})$ at every step — the soft, per-time probability of each regime (the blue curve in the figure), as opposed to Viterbi's single hard path (the dark step).

**Learning — Baum–Welch.** When $A$, the emission parameters, and $\pi$ are unknown, **Baum–Welch** — the [EM algorithm](maximum-likelihood.md) for HMMs — estimates them from the observations alone.
It alternates a forward–backward pass (the E-step, computing expected state and transition counts $\gamma_t$ and $\xi_t$) with a re-estimation of the parameters from those expected counts (the M-step), climbing the likelihood to a local maximum.
Pooling many individuals' series sharpens the estimates enormously, which is why cohort data are ideal.

## A worked example

We simulate a cohort of 80 people, each tested monthly for five years, with a sticky low/high-risk latent regime (high-risk months are positive with probability $0.55$, low-risk with $0.03$).
From the **test results alone** — never the true regime — Baum–Welch recovers the emission and transition parameters, and Viterbi decodes each person's hidden risk trajectory.

## In code

The R version uses [`depmixS4`](https://cran.r-project.org/package=depmixS4) (a standard package for latent-regime models; `HMM` and `hmmTMB` are alternatives).
The Python and Julia versions implement the forward–backward, Baum–Welch, and Viterbi recursions by hand to expose the machinery.

### R

```r
library(depmixS4)
# `tests`: long format, one row per person-month, `positive` in {0, 1}
mod <- depmix(positive ~ 1, data = tests, nstates = 2,
              family = binomial(), ntimes = rep(60, 80))   # 80 people x 60 months
set.seed(1)
fit <- fit(mod)              # Baum-Welch (EM)
summary(fit)                 # emission probabilities + transition matrix

post <- posterior(fit)       # Viterbi path (post$state) + smoothed P(state | data)
```

### Python

```python
import numpy as np

rng = np.random.default_rng(2)
A = np.array([[0.95, 0.05], [0.15, 0.85]])       # true low/high-risk transitions
p_inf = np.array([0.03, 0.55])                    # test-positive prob by regime
pi = np.array([0.85, 0.15])
Npat, T = 80, 60

def simulate():
    z = np.zeros(T, int); z[0] = rng.random() > pi[0]
    for t in range(1, T):
        z[t] = rng.random() > A[z[t - 1], 0]
    return z, (rng.random(T) < p_inf[z]).astype(int)

Z, X = map(np.array, zip(*[simulate() for _ in range(Npat)]))

def emit(p, xt):
    return np.where(xt == 1, p, 1 - p)           # Bernoulli emission

def fwd_bwd(x, A, p, pi):
    al = np.zeros((T, 2)); be = np.zeros((T, 2)); c = np.zeros(T)
    al[0] = pi * emit(p, x[0]); c[0] = al[0].sum(); al[0] /= c[0]
    for t in range(1, T):                        # forward
        al[t] = (al[t - 1] @ A) * emit(p, x[t]); c[t] = al[t].sum(); al[t] /= c[t]
    be[-1] = 1
    for t in range(T - 2, -1, -1):               # backward
        be[t] = A @ (emit(p, x[t + 1]) * be[t + 1]) / c[t + 1]
    g = al * be; g /= g.sum(1, keepdims=True)     # smoothed posterior
    return g, al, be

# ---- Baum-Welch (EM), pooled over the whole cohort ----
Ah = np.array([[0.9, 0.1], [0.3, 0.7]]); ph = np.array([0.05, 0.40]); pih = np.array([0.8, 0.2])
for _ in range(60):
    xit = np.zeros((2, 2)); g0 = np.zeros(2); ne = np.zeros(2); de = np.zeros(2)
    for x in X:
        g, al, be = fwd_bwd(x, Ah, ph, pih)
        for t in range(T - 1):                   # expected transition counts
            m = (al[t][:, None] * Ah) * (emit(ph, x[t + 1]) * be[t + 1])[None, :]
            xit += m / m.sum()
        g0 += g[0]; ne += (g * x[:, None]).sum(0); de += g.sum(0)
    Ah = xit / xit.sum(1, keepdims=True); ph = ne / de; pih = g0 / Npat

def viterbi(x, A, p, pi):                         # most-likely regime path
    lA = np.log(A); d = np.log(pi) + np.log(emit(p, x[0])); bp = np.zeros((T, 2), int)
    for t in range(1, T):
        mm = d[:, None] + lA; bp[t] = mm.argmax(0); d = mm.max(0) + np.log(emit(p, x[t]))
    path = np.zeros(T, int); path[-1] = d.argmax()
    for t in range(T - 2, -1, -1):
        path[t] = bp[t + 1, path[t + 1]]
    return path

acc = np.mean([(viterbi(X[i], Ah, ph, pih) == Z[i]).mean() for i in range(Npat)])
print(f"emission P(pos)  true {p_inf}  est {ph.round(3)}")
print(f"stay probs       true {np.diag(A).round(2)}  est {np.diag(Ah).round(2)}")
print(f"Viterbi decoding accuracy = {acc:.2f}")
```

<!-- python-output:auto -->
```text
emission P(pos)  true [0.03 0.55]  est [0.036 0.559]
stay probs       true [0.95 0.85]  est [0.95 0.85]
Viterbi decoding accuracy = 0.91
```
<!-- /python-output:auto -->

### Julia

```julia
using LinearAlgebra

emit(p, xt) = xt == 1 ? p : 1 .- p

# forward algorithm: log-likelihood of one series under (A, p, pi)
function forward(x, A, p, pi)
    a = pi .* [emit(p[1], x[1]), emit(p[2], x[1])]
    ll = log(sum(a)); a ./= sum(a)
    for t in 2:length(x)
        a = (A' * a) .* [emit(p[1], x[t]), emit(p[2], x[t])]
        ll += log(sum(a)); a ./= sum(a)
    end
    ll
end

# Viterbi: most-likely hidden regime path (log space)
function viterbi(x, A, p, pi)
    T = length(x); lA = log.(A)
    d = log.(pi) .+ log.([emit(p[1], x[1]), emit(p[2], x[1])]); bp = zeros(Int, T, 2)
    for t in 2:T
        m = d .+ lA
        bp[t, :] = [argmax(m[:, j]) for j in 1:2]
        d = [maximum(m[:, j]) for j in 1:2] .+ log.([emit(p[1], x[t]), emit(p[2], x[t])])
    end
    path = zeros(Int, T); path[T] = argmax(d)
    for t in T-1:-1:1; path[t] = bp[t+1, path[t+1]]; end
    path
end
```

## Filtering, smoothing, or the single best path

The three decoders answer different questions, and the choice matters.
The **filtered** posterior $\Pr(z_t \mid y_{1:t})$ (the forward pass alone) is the real-time belief — use it to flag someone as *currently* likely high-risk.
The **smoothed** posterior $\gamma_t = \Pr(z_t \mid y_{1:T})$ (forward–backward) uses the whole record and is what you want for retrospective reconstruction, exactly as the [RTS smoother](kalman-filter.md) improves on the Kalman filter.
**Viterbi** returns one globally consistent path — preferable when the *sequence* of regimes must be coherent (a decoded genome segmentation, a clean set of risk episodes) rather than a soft per-month probability.

## Connections and extensions

An HMM is precisely a [state-space model](state-space-particle-filter.md) with a **discrete** latent state, so it sits in the same family as the filters on the neighboring pages: swap the Gaussian state of the [Kalman filter](kalman-filter.md) for a categorical one and the integrals become sums.
When the discrete states are too coarse — when the hidden quantity is really continuous — the [Kalman](kalman-filter.md) and [particle](state-space-particle-filter.md) filters take over; when the process is a mechanistic simulator, the [POMP toolkit](partially-observed-markov-processes.md) does.

The basic HMM makes two assumptions worth stretching for epidemiology:

- **Transitions ignore the data.** In the reinfection story, an infection itself might *raise* the chance of staying high-risk (behavioral or biological feedback).
  A **non-homogeneous** or **input-driven** HMM lets $A$ depend on covariates or past outcomes, capturing exactly that "reinfection begets risk" dependence.
- **Dwell times are geometric.** A plain HMM implies each regime lasts a geometric number of steps; a **hidden semi-Markov model** replaces that with an explicit duration distribution when regimes have a characteristic length.
- **Emissions are memoryless.** An **autoregressive HMM** lets each observation depend on recent ones, for signals with short-term structure within a regime.

## Other uses

The same three algorithms recur across biology and surveillance:

- **Genomics.** Segmenting a genome into CpG islands, isochores, or coding/non-coding regions; gene finding; profile HMMs for sequence alignment; and base-calling in sequencers are all Viterbi decodings of a hidden annotation ([genomic surveillance](../epidemiology/genomic-surveillance.md)).
- **Epidemic phase.** Classifying a case series into latent growth, plateau, and decline regimes, a discrete companion to the continuous [growth-rate filter](kalman-filter.md).
- **Behavior and physiology.** Animal-movement states (foraging vs transiting) from tracking data, sleep staging from EEG, and ion-channel open/closed gating are canonical two- or three-state HMMs.
- **Care cascades.** Latent engagement states (in care, disengaged, transferred) behind observed clinic visits, for HIV and TB program monitoring.

## Why it matters

Hidden Markov models turn a noisy stream of yes/no or categorical observations into a reconstructed history of *regimes* — who was high-risk and when, which stretch of genome codes for what, whether an epidemic is in a growth or decline phase — together with calibrated uncertainty and estimates of how the hidden system switches and emits.
They do it exactly and in linear time, and they generalize cleanly: the forward recursion is the Kalman/particle predict–update in discrete clothing, and relaxing the geometric-dwell, data-independent-transition, and memoryless-emission assumptions opens onto semi-Markov, input-driven, and autoregressive models without leaving the framework.
For any question that is really "which hidden category was the system in, given what we saw," the HMM is the first tool to reach for.

## Related

- [The Kalman Filter](kalman-filter.md) — the continuous-state sibling; the forward recursion is its predict/update in discrete form
- [State-Space Models and Particle Filtering](state-space-particle-filter.md) — the general nonlinear, non-Gaussian filter; an HMM is its discrete-state case
- [POMP Models and Plug-and-Play Inference](partially-observed-markov-processes.md) — when the hidden process is a mechanistic simulator
- [Markov Chains](markov-chains.md) — the transition dynamics of the hidden state
- [Maximum Likelihood Estimation](maximum-likelihood.md) — the target Baum–Welch (EM) climbs
- [The Effective Reproduction Number and Forecasting](reproduction-number-rt.md) — a continuous view of the epidemic-phase question HMMs pose discretely
- [Genomic Surveillance](../epidemiology/genomic-surveillance.md) — sequence segmentation and annotation by HMM
- [Quantitative Methods](../math.md)
