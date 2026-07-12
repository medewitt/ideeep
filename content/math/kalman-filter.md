---
title: "The Kalman Filter"
description: "The Kalman filter for linear-Gaussian state-space models — the predict/update recursion, the Kalman gain, and the RTS smoother — with worked epidemiological examples: recovering time-varying transmission, and fusing high-frequency wastewater with slower case reports."
---

# The Kalman Filter

The Kalman filter is the exact, closed-form solution to a recurring problem: track a hidden state that drifts over time when all you see is a noisy, indirect measurement of it.
It is a two-line recursion — **predict** where the state is heading, then **correct** that guess with the new data — that is optimal whenever the dynamics are linear and the noise is Gaussian.
For infectious-disease work it is the natural engine for smoothing noisy surveillance signals, estimating a time-varying growth rate or reproduction number, and **fusing multiple data streams** that arrive at different rates, all with honest uncertainty and near-zero compute.

![Left: the Kalman filter tracking a noisy random-walk signal, its 95% band containing the true state. Right: the Kalman gain and posterior standard deviation converge to a steady state within a few steps, as the recursion forgets its prior.](../assets/figures/kalman-filter.svg)

It is also the linear-Gaussian anchor of a whole family of filters.
When the model is nonlinear or non-Gaussian — as mechanistic epidemic models usually are — the exact recursion no longer holds, and the [particle filter](state-space-particle-filter.md) and the [POMP inference toolkit](partially-observed-markov-processes.md) take over.
The Kalman filter is where that story starts.

## The linear-Gaussian state-space model

The filter assumes a **linear-Gaussian [state-space model](state-space-particle-filter.md)**: a hidden state vector $x_t$ that evolves linearly with Gaussian shocks, observed through a linear map with Gaussian noise,

\[
x_t = A\,x_{t-1} + w_t, \qquad w_t \sim \mathcal{N}(0, Q),
\label{eq:kf-process}
\]

\[
y_t = H\,x_t + v_t, \qquad v_t \sim \mathcal{N}(0, R).
\label{eq:kf-obs}
\]

Here $A$ is the transition matrix, $H$ maps the state to the measurement, and $Q$ and $R$ are the process- and observation-noise covariances.
Because everything is linear and Gaussian, the belief about the state stays Gaussian forever, so the filter only ever has to track a **mean $\hat{x}_t$ and covariance $P_t$** — no integrals, no sampling.

## The predict–update recursion

Each step has two halves.
First **predict**: push the previous estimate through the dynamics [@eq:kf-process], which moves the mean and *inflates* the covariance by the process noise,

\[
\hat{x}_{t\mid t-1} = A\,\hat{x}_{t-1}, \qquad P_{t\mid t-1} = A\,P_{t-1}\,A^\top + Q.
\label{eq:kf-predict}
\]

Then **update**: fold in the new observation, weighting prediction against data by the **Kalman gain** $K_t$,

\[
K_t = P_{t\mid t-1} H^\top \left( H\,P_{t\mid t-1} H^\top + R \right)^{-1},
\label{eq:kf-gain}
\]

\[
\hat{x}_t = \hat{x}_{t\mid t-1} + K_t\big( y_t - H\,\hat{x}_{t\mid t-1} \big), \qquad
P_t = (I - K_t H)\,P_{t\mid t-1}.
\label{eq:kf-update}
\]

The term $y_t - H\hat{x}_{t\mid t-1}$ is the **innovation** — how much the observation surprised us — and the gain [@eq:kf-gain] decides how much of that surprise to believe.
The gain is a precision-weighted compromise: when the measurement is clean ($R$ small) it pulls the estimate hard toward the data; when the measurement is noisy it barely moves.
For a stationary model the gain and covariance settle to a **steady state** within a handful of steps (the right panel above), so the filter quickly "forgets" its starting guess — which is why the initial prior rarely matters.

## A worked example

Take a scalar local-level model: the state is a slowly wandering quantity (log-incidence, a biomarker level) with process SD $0.3$ (so $Q = 0.09$), observed with noise SD $1.0$ (so $R = 1$).
Suppose the filter predicts $\hat{x}_{t\mid t-1} = 5.0$ with variance $P_{t\mid t-1} = 0.35$, and the new observation is $y_t = 6.0$.
The gain is $K_t = 0.35 / (0.35 + 1) = 0.26$, so the update nudges the estimate only about a quarter of the way to the data: $\hat{x}_t = 5.0 + 0.26 \times (6.0 - 5.0) = 5.26$, with variance $(1 - 0.26)\times 0.35 = 0.26$.
Iterating, the gain converges to $\approx 0.26$ and the posterior SD to $\approx 0.51$ — the filtered signal is **half as noisy** as the raw observations, which is the smoothing the filter buys you.

## In code

The R version uses the [`dlm`](https://cran.r-project.org/package=dlm) package (with `KFAS` and `MARSS` as alternatives), which provides the filter, the smoother, missing-data handling, and the likelihood.
The Python and Julia versions implement the predict–update recursion by hand so the two-line loop is visible.

### R

```r
library(dlm)
set.seed(1)
n <- 60
x_true <- cumsum(rnorm(n, 0, 0.3)) + 5
y <- x_true + rnorm(n, 0, 1)

# local-level model: dV = observation variance, dW = process variance
mod  <- dlmModPoly(order = 1, dV = 1.0, dW = 0.09)
filt <- dlmFilter(y, mod)      # Kalman filter
smoo <- dlmSmooth(filt)        # RTS smoother (uses all the data)

c(filter_rmse = sqrt(mean((dropFirst(filt$m) - x_true)^2)),
  smooth_rmse = sqrt(mean((dropFirst(smoo$s) - x_true)^2)))
```

### Python

```python
import numpy as np

rng = np.random.default_rng(0)
n = 60
x_true = np.cumsum(rng.normal(0, 0.3, n)) + 5.0     # latent random walk
y = x_true + rng.normal(0, 1.0, n)                  # noisy observations

q, r = 0.09, 1.0                                    # process / obs variance
xhat, P = y[0], 1.0
xf = np.zeros(n)
for t in range(n):
    xp, Pp = xhat, P + q                            # predict
    K = Pp / (Pp + r)                               # Kalman gain
    xhat = xp + K * (y[t] - xp)                     # update
    P = (1 - K) * Pp
    xf[t] = xhat

print(f"steady-state gain     = {K:.3f}")
print(f"filter RMSE vs truth  = {np.sqrt(np.mean((xf - x_true) ** 2)):.3f}")
print(f"raw obs RMSE vs truth = {np.sqrt(np.mean((y - x_true) ** 2)):.3f}")
```

<!-- python-output:auto -->
```text
steady-state gain     = 0.258
filter RMSE vs truth  = 0.626
raw obs RMSE vs truth = 1.013
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics

Random.seed!(1)
n = 60
x_true = cumsum(randn(n) .* 0.3) .+ 5
y = x_true .+ randn(n)

q, r = 0.09, 1.0
xhat, P = y[1], 1.0
xf = zeros(n)
for t in 1:n
    xp, Pp = xhat, P + q               # predict
    K = Pp / (Pp + r)                  # Kalman gain
    xhat = xp + K * (y[t] - xp)        # update
    P = (1 - K) * Pp
    xf[t] = xhat
end
sqrt(mean((xf .- x_true).^2))          # filtered RMSE, well below the obs noise
```

## The smoother

The filter uses only data up to time $t$, which is what you want in real time but wastes information when you are looking back.
The **Rauch–Tung–Striebel (RTS) smoother** makes a second, backward pass that conditions each state on the *entire* series, sharpening every estimate and narrowing every band — especially at turning points, where a filter always lags.
Use the **filter** for nowcasting and forecasting, the **smoother** for retrospective reconstruction (`dlmSmooth` above does exactly this).

## Example: recovering time-varying transmission

Transmission is never constant — interventions, behavior, and seasonality all move it — so a central task is estimating a **time-varying growth rate or reproduction number** from a case series.
The Kalman filter handles this with a **local-linear-trend** model: let the log of incidence have both a level and a *slope*, and make the slope itself a random walk.
The slope is exactly the epidemic **growth rate $r_t$**, and it maps to the reproduction number through the [generation-interval](../epidemiology/epidemiological-intervals.md) relation $R_t = 1 / \sum_s w_s e^{-r_t s}$ (the discrete-time [renewal-equation](renewal-equation.md) form of the Wallinga–Lipsitch conversion).

![Left: reported cases and the Kalman-filtered growth rate, which turns negative as the epidemic is brought under control. Right: the implied time-varying reproduction number tracks the true step changes from 1.5 to 0.75 to 1.2, with a filter lag at each turn.](../assets/figures/kalman-time-varying-rt.svg)

This is a genuinely *linear-Gaussian* model on the log scale, so the ordinary Kalman filter — no approximations — recovers $R_t$ and its uncertainty.

```python
import numpy as np

rng = np.random.default_rng(8)
T = 50
w = np.array([0.25, 0.35, 0.25, 0.15])          # generation-interval weights
L = len(w)
t = np.arange(T)
R_true = np.where(t < 16, 1.5, np.where(t < 30, 0.75, 1.2))

# renewal-equation incidence, observed at 50% reporting
I = np.zeros(T)
I[:L] = [30, 40, 55, 70]
for k in range(L, T):
    I[k] = rng.poisson(R_true[k] * np.sum(w * I[k - L:k][::-1]))
cases = rng.poisson(0.5 * I)
y = np.log(np.maximum(cases, 1.0))

# local-linear-trend Kalman: state = [level, slope = growth rate r_t]
A = np.array([[1., 1.], [0., 1.]])
H = np.array([1., 0.])
Q = np.diag([1e-3, 8e-3])
Rm = 0.15
x = np.array([y[L], 0.0])
P = np.eye(2) * 0.5
r_hat = np.zeros(T)
for k in range(T):
    x = A @ x
    P = A @ P @ A.T + Q                          # predict
    K = P @ H / (H @ P @ H + Rm)                 # gain
    x = x + K * (y[k] - H @ x)                   # update
    P = (np.eye(2) - np.outer(K, H)) @ P
    r_hat[k] = x[1]

# growth rate -> R_t via the discretized renewal relation
R_est = np.array([1.0 / np.sum(w * np.exp(-r * np.arange(1, L + 1))) for r in r_hat])
print("week  R_true  R_est")
for k in (8, 15, 20, 29, 36, 46):
    print(f"{k + 1:4d}   {R_true[k]:.2f}    {R_est[k]:.2f}")
print(f"RMSE(R_t) = {np.sqrt(np.mean((R_est[L + 2:] - R_true[L + 2:]) ** 2)):.3f}")
```

<!-- python-output:auto -->
```text
week  R_true  R_est
   9   1.50    1.42
  16   1.50    1.54
  21   0.75    0.72
  30   0.75    0.81
  37   1.20    1.22
  47   1.20    1.27
RMSE(R_t) = 0.123
```
<!-- /python-output:auto -->

In R the same model is two lines with `dlm` — a second-order polynomial model whose second state component is the slope:

```r
library(dlm)
# local linear trend on log-cases; component 2 of the state is the growth rate
mod <- dlmModPoly(order = 2, dV = 0.15, dW = c(1e-3, 8e-3))
sm  <- dlmSmooth(log(pmax(cases, 1)), mod)
r_t <- dropFirst(sm$s[, 2])                       # smoothed growth rate
R_t <- 1 / sapply(r_t, function(r) sum(w * exp(-r * seq_along(w))))
```

### The mechanistic route: the ensemble Kalman filter

The model above is *phenomenological* — it never mentions $S$, $I$, or $\beta$.
To estimate a time-varying transmission rate **inside a mechanistic SIR**, you make $\log\beta_t$ a random-walk state appended to $(S, I)$ and filter the augmented system.
That dynamic is nonlinear (incidence $\propto \beta S I$), so the plain Kalman filter no longer applies.
The **extended Kalman filter (EKF)** linearizes the dynamics with a Jacobian, but on epidemic models it is notoriously fragile and prone to divergence.
The **ensemble Kalman filter (EnKF)** is the robust workhorse: it represents the state by an ensemble, pushes each member through the *exact* nonlinear simulator, and computes the Kalman update from the ensemble's sample covariance — no Jacobian required.

```r
# ensemble Kalman filter over an augmented state (S, I, log beta) — sketch
ens <- init_ensemble(m = 300)                     # draw S, I, log beta
for (t in seq_along(reports)) {
  ens$logbeta <- ens$logbeta + rnorm(300, 0, sigma)   # random walk on log beta
  ens <- sir_step(ens)                                # push through the simulator
  yhat <- rho * ens$new_infections                    # predicted observation
  K    <- cov(cbind(ens$S, ens$I, ens$logbeta), yhat) / (var(yhat) + R_obs)
  ens  <- ens + K %o% (reports[t] + rnorm(300, 0, sqrt(R_obs)) - yhat)  # update
}
```

This augmented-state EnKF is the method behind operational influenza forecasting ([Shaman & Karspeck 2012](https://doi.org/10.1073/pnas.1208772109)).
When even a Gaussian ensemble is too crude — strongly nonlinear dynamics, discrete counts, multimodal beliefs — the fully general replacement is the [particle filter](state-space-particle-filter.md), and the [`pomp` toolkit](partially-observed-markov-processes.md) fits the same time-varying-$\beta$ model without any Gaussian assumption.

## Example: fusing wastewater and case reports

Modern surveillance mixes streams that report at **different rates and with different noise**: wastewater signal can arrive daily but is very noisy, while confirmed cases arrive weekly and are cleaner but lag.
A Kalman filter fuses them effortlessly, because the update step [@eq:kf-update] simply runs **once per available observation** — when a stream is silent, you skip its update, and the filter coasts on the prediction.
Both streams are treated as noisy linear reads of one shared latent log-incidence $m_t$, each with its own scaling constant and variance.

![Left: two surveillance streams on their own scales — noisy daily wastewater and sparse weekly case reports. Right: the Kalman filter fuses them into one latent-incidence estimate that denoises the wastewater and is anchored by the weekly cases, far closer to the truth than either stream alone.](../assets/figures/kalman-nowcast-fusion.svg)

```python
import numpy as np

rng = np.random.default_rng(2)
D = 84
m0 = (np.cumsum(rng.normal(0, 0.06, D)) + np.log(800)
      + 0.7 * np.sin(2 * np.pi * np.arange(D) / 45))
latent = np.exp(m0)                                    # true daily incidence
ww = 0.002 * latent * np.exp(rng.normal(0, 0.45, D))   # daily wastewater (noisy)
cases = np.full(D, np.nan)
for d in range(0, D, 7):                               # cases reported weekly only
    cases[d] = rng.poisson(0.4 * latent[d])

q, r1, r2 = 0.06 ** 2, 0.45 ** 2, 0.12 ** 2            # process / two obs variances
c1, c2 = np.log(0.002), np.log(0.40)                   # stream scaling constants


def run(use_cases):
    m, P = np.log(800), 1.0
    est = np.zeros(D)
    for d in range(D):
        P += q                                         # predict (random walk)
        K = P / (P + r1)                               # update with wastewater (daily)
        m += K * (np.log(ww[d]) - (c1 + m))
        P = (1 - K) * P
        if use_cases and not np.isnan(cases[d]) and cases[d] > 0:
            K = P / (P + r2)                           # update with cases (weekly)
            m += K * (np.log(cases[d]) - (c2 + m))
            P = (1 - K) * P
        est[d] = np.exp(m)
    return est


rmse = lambda e: np.sqrt(np.mean((e - latent) ** 2))
print(f"raw wastewater RMSE  = {rmse(ww / 0.002):6.1f}")
print(f"KF, wastewater only  = {rmse(run(False)):6.1f}")
print(f"KF, fused with cases = {rmse(run(True)):6.1f}")
```

<!-- python-output:auto -->
```text
raw wastewater RMSE  =  540.7
KF, wastewater only  =  373.9
KF, fused with cases =  278.8
```
<!-- /python-output:auto -->

The fused estimate is much closer to the truth than either the raw wastewater or the wastewater-only filter — the frequent stream supplies the shape and the sparse stream anchors the level.
In R, `dlm` (or `KFAS`) does this natively: stack the two series as columns, mark the missing case-days `NA`, and the filter skips them automatically.

```r
library(dlm)
z1 <- log(ww) - log(0.002)                 # wastewater, de-scaled to the level
z2 <- log(cases) - log(0.40)               # weekly cases; NA on non-report days
Y  <- cbind(z1, z2)

# one shared random-walk level read by both streams, with their own variances
mod <- dlm(FF = matrix(1, 2, 1), V = diag(c(0.45^2, 0.12^2)),
           GG = 1, W = 0.06^2, m0 = log(800), C0 = 1)
fused <- exp(dropFirst(dlmFilter(Y, mod)$m))   # NA case-days are skipped
```

## Other epidemiological uses

The same machinery recurs across surveillance and modeling:

- **Nowcasting and backfill.** Reporting delays mean recent counts are incomplete; a structural time-series Kalman model with a day-of-week component estimates the true recent level and projects the fill-in — see [Nowcasting](../epidemiology/nowcasting.md).
- **Excess-mortality baselines.** A seasonal local-level model gives the expected deaths and a prediction interval; the gap to observed deaths is the [excess](../epidemiology/excess-mortality.md).
- **Within-host viral load.** Noisy qPCR / Ct trajectories over time are smoothed into a clean [within-host](within-host-dynamics.md) load curve, with the slope estimating growth or clearance rate.
- **Multi-signal surveillance.** The fusion pattern above extends to any number of streams — ILI, hospitalizations, syndromic, wastewater — each a linear read of a shared latent burden, weighted by its reliability ([surveillance systems](../epidemiology/surveillance-systems.md)).
- **Data assimilation for forecasting.** Cycling an EnKF between mechanistic simulation and observation is the backbone of operational [epidemic forecasting](../epidemiology/epidemic-forecasting.md).

## The wider filtering family

The Kalman filter is the exact solution at the linear-Gaussian corner; everything else is a way to cope when a model leaves it.

| Filter | Handles | Cost |
|--------|---------|------|
| Kalman | linear, Gaussian | trivial, exact |
| Extended Kalman (EKF) | mild nonlinearity via Jacobian | cheap, can diverge |
| Unscented Kalman (UKF) | stronger nonlinearity, no Jacobian | cheap, still Gaussian |
| Ensemble Kalman (EnKF) | nonlinear, high-dimensional | moderate, Gaussian update |
| [Particle filter](state-space-particle-filter.md) | arbitrary nonlinear / non-Gaussian | expensive, general |

The first four keep the Gaussian bookkeeping and differ only in how they push it through nonlinearity; the particle filter drops the Gaussian assumption entirely and *samples* the belief instead.
For mechanistic transmission models — nonlinear, with discrete counts and no closed-form likelihood — that last step is usually necessary, which is where the [POMP inference toolkit](partially-observed-markov-processes.md) picks up.

## Why it matters

The Kalman filter is the cheapest honest way to turn a noisy, partial signal into a state estimate with calibrated uncertainty, and an enormous amount of routine epidemiology is exactly that problem: denoising a case series, tracking a growth rate, reconstructing incidence behind reporting delays, combining data streams that disagree.
Its predict–update logic — carry a belief forward, then correct it by the data in proportion to their relative precision — is also the conceptual template for every filter that follows, from the ensemble Kalman filters used in flu forecasting to the particle filters behind mechanistic model fitting.
Learn it here in its exact, linear-Gaussian form, and the nonlinear generalizations are just the same idea working harder.

## Related

- [State-Space Models and Particle Filtering](state-space-particle-filter.md) — the nonlinear, non-Gaussian generalization of this page
- [POMP Models and Plug-and-Play Inference](partially-observed-markov-processes.md) — fitting mechanistic models when the Kalman assumptions fail
- [The Effective Reproduction Number and Forecasting](reproduction-number-rt.md) — a prime target of the time-varying-transmission filter
- [The Renewal Equation](renewal-equation.md) — the growth-rate-to-$R_t$ conversion used above
- [Random Walks and Brownian Motion](random-walk-brownian-motion.md) — the process model at the heart of the local-level filter
- [Gaussian Processes](gaussian-processes.md) — the other Gaussian workhorse; a state-space view of GPs yields Kalman-speed inference
- [Nowcasting](../epidemiology/nowcasting.md) · [Excess Mortality](../epidemiology/excess-mortality.md) — applications of structural-model filtering
- [Quantitative Methods](../math.md)
