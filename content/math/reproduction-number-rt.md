---
title: "The Effective Reproduction Number and Forecasting"
---

# The Effective Reproduction Number and Forecasting

During an outbreak the single most watched number is whether transmission is still growing, and that question is answered by the effective reproduction number.
It turns a messy stream of daily case counts into a running verdict on the epidemic's direction, and it is the quantity behind most real-time forecasts and policy dashboards.

![An epidemic's incidence (top) and its estimated effective reproduction number R_t (bottom), which crosses 1 as the epidemic peaks.](../assets/figures/rt-epidemic.svg)

## From $R_0$ to $R_t$

The basic reproduction number $R_0$ is the average number of secondary cases one infectious person generates in a fully susceptible population.
It is a fixed property of a pathogen and setting, defined only at the very start of an epidemic (see the [SIR model](sir.md) and the [next-generation matrix](next-generation-matrix.md)).
The **effective reproduction number** $R_t$ is the same idea measured in real time: the average number of people each current case actually infects, given how much susceptibility remains and what interventions are in place.
Because susceptibility depletes and behavior changes, $R_t$ moves over time even though $R_0$ does not.

## Reading $R_t$

The rule is simple and is the whole reason the quantity is tracked.
$R_t > 1$ means each generation of cases is larger than the last, so the epidemic is growing.
$R_t < 1$ means each generation is smaller, so the epidemic is shrinking.
$R_t = 1$ is the tipping point where incidence is momentarily flat, which is exactly when the epidemic curve reaches its peak.
In the figure, $R_t$ crosses $1$ at the same day the incidence curve turns over.

## The renewal equation

The link between $R_t$ and case counts is the **renewal equation**, which says today's new infections are a scaled sum of past infections weighted by how infectious those cases are now:

\[
I_t = R_t \sum_{s\ge 1} I_{t-s}\, w_s .
\]

Here $I_t$ is incidence on day $t$ and $w_s$ is the **generation-interval distribution**—the probability that transmission happens $s$ days after a case was infected.
The sum $\sum_s I_{t-s} w_s$ is the current "force of infection" contributed by everyone infected earlier, so $R_t$ is simply the factor that turns that force into new cases.
This is closely related to the theory of [branching processes](branching-processes.md), where each case independently seeds a random number of offspring.

## Estimating $R_t$ from incidence

Rearranging the renewal equation gives a direct estimator: divide observed incidence by the expected transmission potential,

\[
\hat{R}_t = \frac{I_t}{\sum_{s\ge 1} I_{t-s}\, w_s}.
\]

In practice we cannot observe the generation interval directly, so the serial interval (the gap between symptom onset in an infector and infectee) is used as a proxy for $w_s$.
The widely used EpiEstim approach places a prior on $R_t$ and models incidence as [Poisson](poisson-distribution.md) counts, then does [Bayesian inference](bayesian-inference.md) over a short sliding window so the estimate can track a changing $R_t$ while smoothing out daily noise.

## Growth rate and $R_t$

There is a tight relationship between $R_t$ and the exponential growth rate $r$ of the epidemic curve, defined by $I_t \propto e^{rt}$ in the growth phase.
If the generation interval has mean $T_g$, then to a first approximation $R_t \approx 1 + r\,T_g$, and more precisely $R_t = 1/M(-r)$ where $M$ is the moment-generating function of the generation-interval distribution.
The intuition is that the same growth rate implies a larger $R_t$ when generations are longer, because more transmission has to be packed into each slower cycle.

## Nowcasting and forecasting

Recent case counts are always incomplete: infections from the last few days have not yet been reported, so the tail of the curve is artificially low, a problem called right-truncation.
**Nowcasting** corrects for these reporting delays, reconstructing what recent incidence will look like once late reports arrive, which prevents a spurious apparent drop in $R_t$ at the present day.
Once the recent curve is trustworthy, **short-term forecasting** projects incidence forward by assuming $R_t$ stays roughly constant and iterating the renewal equation ahead a week or two.
Because the estimate rests on noisy, delayed data, forecasts are reported with uncertainty bands rather than single lines.

## In code

### R

```r
w <- c(0.05, 0.15, 0.25, 0.25, 0.15, 0.10, 0.05); w <- w / sum(w)
T <- 60
Rt_true <- 0.7 + 1.6 * exp(-(0:(T-1)) / 30)
I <- numeric(T); I[1] <- 10
for (t in 2:T) {
  s <- 1:min(t - 1, length(w))
  I[t] <- Rt_true[t] * sum(I[t - s] * w[s])
}
cat(which.max(I), "\n")   # peak day (1-indexed)
```

### Python

```python
import numpy as np
rng = np.random.default_rng(3)

# discretized generation interval, mean ~5 days
w = np.array([0.05, 0.15, 0.25, 0.25, 0.15, 0.10, 0.05]); w = w / w.sum()

T = 60
Rt_true = 0.7 + 1.6 * np.exp(-np.arange(T) / 30)   # starts >1, declines through 1
I = np.zeros(T); I[0] = 10.0
for t in range(1, T):                               # renewal equation
    lam = sum(I[t-k] * w[k-1] for k in range(1, min(t, len(w)) + 1))
    I[t] = Rt_true[t] * lam

# back out a simple R_t estimate: I_t / sum_s I_{t-s} w_s
Rt = np.full(T, np.nan)
for t in range(1, T):
    lam = sum(I[t-k] * w[k-1] for k in range(1, min(t, len(w)) + 1))
    Rt[t] = I[t] / lam

print("peak day", int(np.argmax(I)))     # peak day 48
for t in (5, 20, 40):
    print(t, round(float(Rt[t]), 2), round(float(I[t]), 1))
# 5 2.05 8.1
# 20 1.52 73.3
# 40 1.12 247.1
```

<!-- python-output:auto -->
```text
peak day 48
5 2.05 8.1
20 1.52 73.3
40 1.12 247.1
```
<!-- /python-output:auto -->

### Julia

```julia
w = [0.05, 0.15, 0.25, 0.25, 0.15, 0.10, 0.05]; w ./= sum(w)
T = 60
Rt_true = 0.7 .+ 1.6 .* exp.(-(0:T-1) ./ 30)
I = zeros(T); I[1] = 10.0
for t in 2:T
    s = 1:min(t - 1, length(w))
    I[t] = Rt_true[t] * sum(I[t .- s] .* w[s])
end
println(argmax(I))   # peak day
```

## Why it matters

$R_t$ is the real-time speedometer of an epidemic: it tells public health teams whether current measures are enough, and it does so days before the peak is obvious in the raw counts.
The renewal equation that defines it also powers nowcasts and short-term forecasts, making it the shared foundation for both situational awareness and prediction during an outbreak.

## Related

- [Compartmental models (SIR)](sir.md)
- [SEIR models](seir-models.md)
- [Next-generation matrix](next-generation-matrix.md)
- [Branching processes](branching-processes.md)
- [Stochastic epidemics](stochastic-epidemics.md)
- [Bayesian inference](bayesian-inference.md)
- [Proper Scoring Rules](proper-scoring-rules.md)
- [The Euler–Lotka Equation and the r–R₀ Relationship](../epidemiology/euler-lotka.md) — the renewal-equation link between the growth rate $r$ and $R$ through the generation interval
- [The Speed and Strength of Epidemic Control](../epidemiology/epidemic-control.md) — why interventions must act on both $R_t$ and the generation interval to be effective
- [Quantitative Methods](../math.md)
