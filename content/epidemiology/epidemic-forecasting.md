---
title: "Epidemic Forecasting"
description: "Short-term forecasting of epidemic incidence by exponential-growth and renewal-equation projection, why forecasts need uncertainty fans, and how they are scored."
---

# Epidemic Forecasting

Forecasting an epidemic means answering a narrow, urgent question: how many cases next week?
A short horizon is where the data still constrain the answer, and the honest output is not a single line but a fan of plausible trajectories.
The simplest methods extrapolate the recent trend, but every one of them is only as good as its treatment of uncertainty and only as trustworthy as its record against later data.

![An observed incidence curve with a short-term forecast projected forward as a widening uncertainty fan rather than a single line.](../assets/figures/epidemic-forecasting.svg)

## Two simple forecasts

The most direct forecast fits **exponential growth** to recent incidence.
On the log scale case counts are roughly linear during the growth phase, so a straight-line fit to $\log I(t)$ gives a growth rate $r$, and projecting the line ahead gives a point forecast $I(t + h) = I(t)\, e^{r h}$.
This works for a few days and then fails, because it ignores the susceptible depletion and behavior change that eventually bend the curve down.

A more structured forecast iterates the [renewal equation](../math/renewal-equation.md) forward under an assumed reproduction number:

\[
I(t + 1) = R_t \sum_{s \ge 1} I(t + 1 - s)\, w(s).
\]

Holding $R_t$ at its recently estimated value and stepping ahead projects incidence while respecting the generation-interval delay, which keeps the near-term shape realistic even as growth slows.
Both methods need a clean recent curve to start from, which is why a [nowcast](nowcasting.md) usually comes first.

## A forecast is a fan, not a line

A point forecast without an interval is close to useless, because the whole value of a forecast is telling decision-makers how wrong it might be.
Uncertainty enters from several directions: the growth rate or $R_t$ is estimated from noisy counts, incidence itself is a random process, and reporting is incomplete at the present.
A sensible forecast propagates these into a **predictive distribution** and reports its quantiles, so the projection widens into a fan whose spread grows with the horizon.
A model that reports a tight interval and is then routinely wrong is worse than one that admits it does not know.

## Short-term forecast versus long-term projection

Horizon changes the nature of the exercise.
A **short-term forecast**, days to a couple of weeks out, is statistically reliable because the recent trend and the generation interval pin down the near future.
A **long-term projection**, months out, depends on things no data can yet constrain, such as future policy, seasonality, and behavior, so it is a **scenario** conditional on stated assumptions rather than a forecast.
Presenting a scenario as a forecast is a common and damaging error; the two answer different questions and deserve different labels.

## Evaluating forecasts

Forecasts are judged after the fact against what actually happened, using **proper scoring rules** that reward calibrated, sharp predictive distributions and cannot be gamed by hedging.
The **logarithmic score** evaluates the predictive density at the observed count, and the **continuous ranked probability score** (CRPS) generalizes absolute error to a full distribution, penalizing both bias and overconfident intervals.
Because a proper score is optimized in expectation by reporting your true predictive distribution, it removes any incentive to shade a forecast toward what looks safe.
The theory and the mechanics are on the [proper scoring rules](../math/proper-scoring-rules.md) page.

## A worked example

Take the first two weeks of an outbreak growing at roughly $r = 0.16$ per day.
Fit a straight line to $\log(\text{count})$ against day; the slope estimates $r$ and implies a doubling time of $\log 2 / r \approx 4.3$ days.
Project four days past the last observation by extending the fitted line, and attach a prediction interval from the residual scatter of the fit, widening it with the horizon.
When those four days are later observed, score each forecast, for instance with the CRPS, and average over the days to summarize performance; comparing that average against a naive baseline shows whether the model added anything.

## In code

### R

```r
set.seed(1834)
day <- 0:13
r_true <- 0.18
y <- exp(log(15) + r_true * day + rnorm(length(day), 0, 0.15))

fit <- lm(log(y) ~ day)                        # log-linear growth fit
future <- data.frame(day = 14:17)
pi <- predict(fit, future, interval = "prediction", level = 0.95)

data.frame(day = future$day,
           point = round(exp(pi[, "fit"])),
           lower = round(exp(pi[, "lwr"])),
           upper = round(exp(pi[, "upr"])))
```

### Python

```python
import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(1834)

# Early exponential growth with observation noise on the log scale.
day = np.arange(14)
r_true = 0.18
y = np.exp(np.log(15) + r_true * day + rng.normal(0, 0.15, day.size))

# Log-linear (exponential-growth) fit.
X = sm.add_constant(day)
model = sm.OLS(np.log(y), X).fit()
print(f"fitted r = {model.params[1]:.3f} /day (true {r_true})")
print(f"doubling time = {np.log(2) / model.params[1]:.1f} days")

# Forecast the next four days with 95% prediction intervals.
future = np.arange(14, 18)
sf = model.get_prediction(sm.add_constant(future, has_constant="add"))
sf = sf.summary_frame(alpha=0.05)
point = np.exp(sf["mean"].to_numpy())
lower = np.exp(sf["obs_ci_lower"].to_numpy())
upper = np.exp(sf["obs_ci_upper"].to_numpy())

print("day  point  lower  upper")
for d, p_, lo, hi in zip(future, point, lower, upper):
    print(f"{d:3d}  {p_:5.0f}  {lo:5.0f}  {hi:5.0f}")
```

<!-- python-output:auto -->
```text
fitted r = 0.187 /day (true 0.18)
doubling time = 3.7 days
day  point  lower  upper
 14    200    144    279
 15    241    172    339
 16    291    205    413
 17    351    245    503
```
<!-- /python-output:auto -->

The fitted growth rate recovers the truth, and each forecast day carries a prediction interval that widens with the horizon; scoring those intervals against the eventual counts is how competing models are compared.

### Julia

```julia
using GLM, DataFrames, Random
Random.seed!(1834)

day = 0:13
r_true = 0.18
y = exp.(log(15) .+ r_true .* day .+ 0.15 .* randn(length(day)))

df = DataFrame(day = collect(day), logy = log.(y))
fit = lm(@formula(logy ~ day), df)
r_hat = coef(fit)[2]                            # fitted growth rate
future = DataFrame(day = 14:17)
exp.(predict(fit, future))                      # point forecasts
```

## Why it matters

Public health teams act on the near future, and a calibrated short-term forecast tells them whether hospitals are about to fill or an outbreak is already easing, days before the raw counts make it obvious.
Keeping the horizon short, reporting a fan instead of a line, and scoring every forecast against what happened is what separates a useful projection from a confident guess.
The same renewal machinery that defines $R_t$ drives these forecasts, which is why nowcasting, $R_t$ estimation, and forecasting are best treated as one pipeline rather than three separate tools.

## Related

- [The Effective Reproduction Number and Forecasting](../math/reproduction-number-rt.md)
- [Proper Scoring Rules](../math/proper-scoring-rules.md)
- [Branching Processes](../math/branching-processes.md)
- [The Renewal Equation](../math/renewal-equation.md)
- [Nowcasting and Reporting Delays](nowcasting.md)
- [Epidemiology](../epidemiology.md)
