---
title: "Proper Scoring Rules"
---

# Proper Scoring Rules

A forecast that says "70% chance of an outbreak" should be judged by how well its *probabilities* match what actually happens, not by a single right/wrong call as reality is basically one draw from a random process.
A **proper scoring rule** is a way of scoring probabilistic forecasts that a forecaster minimizes only by reporting their honest beliefs — so it rewards calibration and cannot be gamed.

![Both the Brier score and the logarithmic score are minimized when the reported probability equals the true probability, so honest forecasting is optimal.](../assets/figures/scoring-rules.svg)

## What makes a score "proper"

A scoring rule assigns a penalty $S(q, y)$ to a probabilistic forecast $q$ once the outcome $y$ is observed (we use the convention that **lower is better**).
It is **proper** if a forecaster who truly believes the probability is $p$ cannot lower their *expected* penalty by reporting anything other than $p$:

\[
p \in \arg\min_{q}\ \mathbb{E}_{y\sim p}\big[S(q, y)\big].
\]

It is **strictly proper** if that best report is unique — honesty is not just allowed but is the single optimum.
Improper scores (for example, plain accuracy or a linear score) can reward overconfident or hedged forecasts, which is exactly what you do not want.

## The Brier score

For a probability $q$ of a binary event with outcome $y \in \{0, 1\}$, the **Brier score** is the squared error

\[
\text{Brier} = (q - y)^2 .
\]

Its expected value when the true probability is $p$ is $p(1-q)^2 + (1-p)q^2$, a parabola minimized at $q = p$ — so it is strictly proper.
For a categorical forecast it generalizes to $\sum_i (q_i - y_i)^2$.

## The logarithmic score

The **logarithmic score** penalizes the log of the probability you assigned to what actually happened:

\[
\text{logscore} = -\log q \ \text{ if the event occurs}, \qquad -\log(1-q) \ \text{ if it does not}.
\]

It is strictly proper, connects directly to the [log-likelihood](maximum-likelihood.md) and [Bayesian](bayesian-inference.md) model evidence, and punishes confident mistakes severely — assigning probability $0$ to something that then happens gives an infinite penalty.

## Continuous forecasts: CRPS

For a forecast that is a whole predictive distribution $F$ of a real quantity (say, next week's case count), the **continuous ranked probability score** generalizes the Brier score:

\[
\text{CRPS}(F, y) = \int_{-\infty}^{\infty} \big(F(x) - \mathbf{1}\{x \ge y\}\big)^2 \, dx .
\]

It is proper, reduces to absolute error for a point forecast, and is reported in the same units as the data.
The **weighted interval score (WIS)** used by collaborative epidemic forecast hubs (such as the U.S.
COVID-19 and FluSight hubs) is a quantile-based approximation to the CRPS.

## Calibration and sharpness

Gneiting's guiding principle is to **maximize sharpness subject to calibration**: prefer confident (sharp) forecasts, but only as confident as the data justify (calibrated).
Proper scores reward exactly this balance, which is why they, rather than accuracy, are the standard for comparing probabilistic and epidemic forecasts.

## In code

Compute the scores for a set of forecasts, and confirm propriety by checking that the expected penalty is minimized at the true probability.

### Python

```python
import numpy as np

def brier(q, y):     return (q - y) ** 2
def logscore(q, y):  return -(y * np.log(q) + (1 - y) * np.log(1 - q))

# Three forecasts vs. their realized 0/1 outcomes
q = np.array([0.9, 0.6, 0.2]);  y = np.array([1, 1, 0])
print("mean Brier   =", round(brier(q, y).mean(), 3))     # 0.07
print("mean logscore=", round(logscore(q, y).mean(), 3))  # 0.28

# Propriety: with true p = 0.7, expected Brier is lowest when you report 0.7
p = 0.7
grid = np.linspace(0.01, 0.99, 99)
exp_brier = p * (1 - grid) ** 2 + (1 - p) * grid ** 2
print("expected Brier minimized at q =", round(grid[exp_brier.argmin()], 2))  # 0.70
```

<!-- python-output:auto -->
```text
mean Brier   = 0.07
mean logscore= 0.28
expected Brier minimized at q = 0.7
```
<!-- /python-output:auto -->

### R

```r
brier    <- function(q, y) (q - y)^2
logscore <- function(q, y) -(y * log(q) + (1 - y) * log(1 - q))
q <- c(0.9, 0.6, 0.2); y <- c(1, 1, 0)
mean(brier(q, y))      # 0.07
mean(logscore(q, y))   # 0.28
# (scoringRules and scoringutils implement Brier, log score, CRPS, and WIS)
```

### Julia

```julia
brier(q, y)    = (q - y)^2
logscore(q, y) = -(y * log(q) + (1 - y) * log(1 - q))
q = [0.9, 0.6, 0.2]; y = [1, 1, 0]
using Statistics
mean(brier.(q, y))      # 0.07
mean(logscore.(q, y))   # 0.28
```

## Why it matters

Proper scoring rules are the honest yardstick for probabilistic prediction: they let you compare epidemic forecasts, diagnostic models, and Bayesian posteriors on a footing that rewards well-calibrated uncertainty instead of lucky point guesses.
They turn "was the forecast good?" into a number you can average, rank, and optimize.

## Related

- [The Effective Reproduction Number and Forecasting](reproduction-number-rt.md)
- [Bayesian Inference](bayesian-inference.md)
- [Diagnostic Testing and Screening](diagnostic-testing.md)
- [Maximum Likelihood](maximum-likelihood.md)
- [Hypothesis Testing](hypothesis-testing.md)
- [Quantitative Methods](../math.md)
